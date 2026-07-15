# tax_calculator.py

# Фиксированные страховые взносы по годам (нужно проверять актуальные цифры на год расчёта)
INSURANCE_CONTRIBUTIONS = {
    2024: 49500,
    2025: 53658,
    2026: 57390,
}

def calculate_tax(total_income: float, tax_rate: float, year: int) -> dict:
    """
    Считает налог УСН (Доходы) с учётом уменьшения на страховые взносы.
    """
    # Базовый налог до вычетов
    base_tax = total_income * tax_rate / 100

    # Страховые взносы за нужный год (если года нет в словаре - берём 0 и предупреждаем)
    insurance = INSURANCE_CONTRIBUTIONS.get(year, 0)

    # Налог к оплате не может уйти в минус
    tax_to_pay = max(base_tax - insurance, 0)

    return {
        "total_income": total_income,
        "tax_rate": tax_rate,
        "base_tax": round(base_tax, 2),
        "insurance_contribution": insurance,
        "tax_to_pay": round(tax_to_pay, 2),
    }