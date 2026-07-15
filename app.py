from flask import Flask, render_template, request
from tax_calculator import calculate_tax

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = int(request.form['year'])
        tax_system = request.form['tax_system']
        tax_rate = float(request.form['tax_rate'])
        q1 = float(request.form['q1'])
        q2 = float(request.form['q2'])
        q3 = float(request.form['q3'])
        q4 = float(request.form['q4'])

        total_income = q1 + q2 + q3 + q4

        result = calculate_tax(total_income, tax_rate, year)

        return render_template('result.html', result=result, tax_system=tax_system)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)