from tax_calculator import calculate_tax_by_quarters, round_rub


def test_round_rub_half_up():
    assert round_rub(2.5) == 3
    assert round_rub(2.4) == 2
    assert round_rub(0.49) == 0


def test_deduction_reduces_tax_to_zero_when_insurance_covers_it():
    result = calculate_tax_by_quarters(1_000_000, 0, 0, 0, 6, 2025)

    q1 = result["quarters"][0]
    assert q1["base_tax_cumulative"] == 60000
    assert q1["deduction_cumulative"] == 60000
    assert q1["tax_to_pay_this_quarter"] == 0
    assert result["total_tax_for_year"] == 0


def test_employees_cap_deduction_at_half_of_tax():
    result = calculate_tax_by_quarters(1_000_000, 0, 0, 0, 6, 2025, has_employees=True)

    q1 = result["quarters"][0]
    assert q1["deduction_cumulative"] == 30000
    assert q1["tax_to_pay_this_quarter"] == 30000
    assert result["total_tax_for_year"] == 30000


def test_additional_one_percent_contribution_above_threshold():
    result = calculate_tax_by_quarters(1_000_000, 0, 0, 0, 6, 2025)

    assert result["quarters"][0]["additional_contribution_cumulative"] == 7000
    assert result["additional_contribution_total"] == 7000


def test_no_additional_contribution_below_threshold():
    result = calculate_tax_by_quarters(100_000, 0, 0, 0, 6, 2025)

    assert result["quarters"][0]["additional_contribution_cumulative"] == 0


def test_unknown_year_has_no_insurance_deduction():
    result = calculate_tax_by_quarters(100_000, 0, 0, 0, 6, 1999)

    assert result["insurance_contribution"] == 0
    q1 = result["quarters"][0]
    assert q1["deduction_cumulative"] == 0
    assert q1["tax_to_pay_this_quarter"] == 6000


def test_exceeds_vat_threshold_flag():
    above = calculate_tax_by_quarters(6_000_000, 6_000_000, 6_000_000, 6_000_000, 6, 2025)
    below = calculate_tax_by_quarters(1_000_000, 1_000_000, 1_000_000, 1_000_000, 6, 2025)

    assert above["exceeds_vat_threshold"] is True
    assert below["exceeds_vat_threshold"] is False


def test_quarterly_payments_progress_cumulatively():
    result = calculate_tax_by_quarters(250_000, 300_000, 280_000, 320_000, 6, 2025)

    payments = [q["tax_to_pay_this_quarter"] for q in result["quarters"]]
    incomes = [q["cumulative_income"] for q in result["quarters"]]

    assert incomes == [250_000, 550_000, 830_000, 1_150_000]
    assert sum(payments) - sum(q["tax_to_decrease_this_quarter"] for q in result["quarters"]) == result["total_tax_for_year"]
