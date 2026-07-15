# tax_calculator.py

INSURANCE_CONTRIBUTIONS = {
    2024: 49500,
    2025: 53658,
    2026: 57390,
}

def calculate_tax_by_quarters(q1: float, q2: float, q3: float, q4: float,
                               tax_rate: float, year: int,
                               has_employees: bool = False) -> dict:
    """
    Считает налог УСН (Доходы) по кварталам нарастающим итогом,
    с вычетом страховых взносов.
    """
    incomes = [q1, q2, q3, q4]
    insurance_total = INSURANCE_CONTRIBUTIONS.get(year, 0)

    cumulative_income = 0
    cumulative_paid = 0  # сколько уже "начислено к оплате" за предыдущие кварталы
    quarters = []

    for i, income in enumerate(incomes, start=1):
        cumulative_income += income
        base_tax_cumulative = cumulative_income * tax_rate / 100

        if has_employees:
            max_deduction = base_tax_cumulative * 0.5
            deduction_cumulative = min(insurance_total, max_deduction)
        else:
            deduction_cumulative = min(insurance_total, base_tax_cumulative)

        tax_after_deduction = base_tax_cumulative - deduction_cumulative

        # Сколько нужно доплатить именно в этом квартале
        tax_to_pay_this_quarter = tax_after_deduction - cumulative_paid
        tax_to_pay_this_quarter = max(tax_to_pay_this_quarter, 0)

        cumulative_paid += tax_to_pay_this_quarter

        quarters.append({
            "quarter": i,
            "income_quarter": round(income, 2),
            "cumulative_income": round(cumulative_income, 2),
            "base_tax_cumulative": round(base_tax_cumulative, 2),
            "deduction_cumulative": round(deduction_cumulative, 2),
            "tax_to_pay_this_quarter": round(tax_to_pay_this_quarter, 2),
        })

    return {
        "quarters": quarters,
        "total_income": round(cumulative_income, 2),
        "insurance_contribution": insurance_total,
        "total_tax_for_year": round(cumulative_paid, 2),
        "has_employees": has_employees,
    }