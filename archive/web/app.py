from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    numbers = random.sample(range(1, 51), 20)
    magic_numbers = []

    if request.method == 'POST':
        magic_numbers = list(filter(
            lambda x: x % 2 == 0 or x % 3 == 0 or x**2 < 100,
            numbers
        ))

    return render_template('index.html', numbers=numbers, magic_numbers=magic_numbers)

if __name__ == '__main__':
    app.run(debug=True)