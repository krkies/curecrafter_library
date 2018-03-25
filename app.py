from Network import Network
from GenMol import GenMol

threshold = 50
gridSize = 0.1
originX = 0
originY = 0
originZ = 0


from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]


@app.route('/incomes')
def get_incomes():
  return "jsonify(incomes)"


@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204

if __name__ == "__main__":
    print("RUN")
    app.run(debug=True, use_reloader=True)
