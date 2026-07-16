INSURANCE_CONTRIBUTIONS = {
    2024: 49500,
    2025: 53658,
    2026: 57390,
}

ADDITIONAL_CONTRIBUTION_RATE = 0.01       # 1%
ADDITIONAL_CONTRIBUTION_THRESHOLD = 300000  # порог дохода
VAT_INCOME_THRESHOLD = 20_000_000  # порог для обязанности платить НДС с 2026 года


def calculate_tax_by_quarters(q1: float, q2: float, q3: float, q4: float,
                               tax_rate: float, year: int,
                               has_employees: bool = False) -> dict:
    incomes = [q1, q2, q3, q4]
    insurance_total = INSURANCE_CONTRIBUTIONS.get(year, 0)

    cumulative_income = 0
    cumulative_paid = 0
    quarters = []

    for i, income in enumerate(incomes, start=1):
        cumulative_income += income
        base_tax_cumulative = cumulative_income * tax_rate / 100

        # Доп. взнос 1% с дохода свыше порога, нарастающим итогом
        additional_contribution_cumulative = max(
            cumulative_income - ADDITIONAL_CONTRIBUTION_THRESHOLD, 0
        ) * ADDITIONAL_CONTRIBUTION_RATE

        # Общий пул для вычета: фикс. взносы + доп. взнос 1%
        total_deduction_pool = insurance_total + additional_contribution_cumulative

        if has_employees:
            max_deduction = base_tax_cumulative * 0.5
            deduction_cumulative = min(total_deduction_pool, max_deduction)
        else:
            deduction_cumulative = min(total_deduction_pool, base_tax_cumulative)

        tax_after_deduction = base_tax_cumulative - deduction_cumulative
        tax_to_pay_this_quarter = max(tax_after_deduction - cumulative_paid, 0)
        cumulative_paid += tax_to_pay_this_quarter

        quarters.append({
            "quarter": i,
            "income_quarter": round(income, 2),
            "cumulative_income": round(cumulative_income, 2),
            "base_tax_cumulative": round(base_tax_cumulative, 2),
            "additional_contribution_cumulative": round(additional_contribution_cumulative, 2),
            "deduction_cumulative": round(deduction_cumulative, 2),
            "tax_to_pay_this_quarter": round(tax_to_pay_this_quarter, 2),
        })

    return {
        "quarters": quarters,
        "total_income": round(cumulative_income, 2),
        "insurance_contribution": insurance_total,
        "additional_contribution_total": quarters[-1]["additional_contribution_cumulative"],
        "total_tax_for_year": round(cumulative_paid, 2),
        "has_employees": has_employees,
        "exceeds_vat_threshold": cumulative_income > VAT_INCOME_THRESHOLD,
    }