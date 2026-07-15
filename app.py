from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        year = int(request.form['year'])
        q1 = float(request.form['q1'])
        q2 = float(request.form['q2'])
        q3 = float(request.form['q3'])
        q4 = float(request.form['q4'])

        # Пока просто выведем их в консоль, чтобы проверить
        print(f"Год: {year}")
        print(f"Q1: {q1}, Q2: {q2}, Q3: {q3}, Q4: {q4}")

        # Здесь дальше будет вызов функции расчёта и генерации PDF
        return f"Данные получены! Год: {year}, доходы: {q1}, {q2}, {q3}, {q4}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)