from flask import Flask, render_template, request
from tax_calculator import calculate_tax_by_quarters

app = Flask(__name__)

@app.template_filter('rub')
def format_rub(value):
    """Форматирует число с пробелами между разрядами: 1000000 -> 1 000 000"""
    return f"{value:,.2f}".replace(",", " ")

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        year = int(request.form['year'])
        tax_system = request.form['tax_system']
        tax_rate = float(request.form['tax_rate'])
        q1 = float(request.form['q1'].replace(' ', ''))
        q2 = float(request.form['q2'].replace(' ', ''))
        q3 = float(request.form['q3'].replace(' ', ''))
        q4 = float(request.form['q4'].replace(' ', ''))

        result = calculate_tax_by_quarters(q1, q2, q3, q4, tax_rate, year)

        return render_template('result.html', result=result, tax_system=tax_system)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)