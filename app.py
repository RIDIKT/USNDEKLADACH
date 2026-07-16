from flask import Flask, render_template, request
from tax_calculator import calculate_tax_by_quarters

app = Flask(__name__)

@app.template_filter('rub')
def format_rub(value):
    return f"{value:,.2f}".replace(",", " ")

def parse_money(raw_value, field_name):
    try:
        cleaned = raw_value.replace(' ', '').replace(',', '.')
        num = float(cleaned)
    except (ValueError, AttributeError):
        raise ValueError(f'Поле "{field_name}" должно быть числом')
    if num < 0:
        raise ValueError(f'Поле "{field_name}" не может быть отрицательным')
    return num

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        errors = []

        year = None
        try:
            year = int(request.form['year'])
            if year < 2000 or year > 2100:
                errors.append("Введите корректный год")
        except (ValueError, KeyError):
            errors.append("Год должен быть числом")

        tax_system = request.form.get('tax_system', '')
        if not tax_system:
            errors.append("Выберите систему налогообложения")

        tax_rate = None
        try:
            tax_rate = float(request.form['tax_rate'])
            if tax_rate < 0 or tax_rate > 100:
                errors.append("Ставка налога должна быть от 0 до 100%")
        except (ValueError, KeyError):
            errors.append("Ставка налога должна быть числом")

        quarter_labels = {'q1': 'Доход за 1 квартал', 'q2': 'Доход за 2 квартал',
                           'q3': 'Доход за 3 квартал', 'q4': 'Доход за 4 квартал'}
        quarters_input = {}
        for field, label in quarter_labels.items():
            try:
                quarters_input[field] = parse_money(request.form.get(field, ''), label)
            except ValueError as e:
                errors.append(str(e))

        if errors:
            return render_template('index.html', errors=errors)

        result = calculate_tax_by_quarters(
            quarters_input['q1'], quarters_input['q2'],
            quarters_input['q3'], quarters_input['q4'],
            tax_rate, year
        )
        return render_template('result.html', result=result, tax_system=tax_system)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)