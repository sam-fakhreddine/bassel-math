import random
import string

#import jsonify
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_folder='static')
# a dictionary to store the sessions
sessions = {}

@app.route("/")
def index():
    return render_template("index.html")


def safe_eval(problem):
    num1, operation, num2 = problem.split()
    num1, num2 = int(num1), int(num2)
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2
    else:
        return "Invalid operation"


def generate_problem(intake):
    #print(intake)
    grade = random.randint(1, 3)
    grade_parameters = {
        1: {"max_number": 99, "operations": ["+", "-"]},
        2: {"max_number": 999, "operations": ["+", "-", "*"]},
        3: {"max_number": 999, "operations": ["+", "-", "*", "/"]},
    }

    if grade not in grade_parameters:
        return "Invalid grade"

    params = grade_parameters[grade]
    num1 = random.randint(1, params["max_number"])
    num2 = random.randint(1, num1)  # Ensures num2 is always smaller than or equal to num1
    operation = random.choice(params["operations"])

    if operation == "/":
        # Find a divisor that divides num1 evenly
        divisors = [divisor for divisor in range(1, num1 + 1) if num1 % divisor == 0]
        num2 = random.choice(divisors)
    problem = f"{num1} {operation} {num2}"
    print(problem)
    return problem

@app.route("/start", methods=["GET"])
def start_session():
    session_id = ''.join(random.choices(string.hexdigits, k=6))
    problems = []

    for _ in range(12):
        grade = random.randint(1, 6)
        problem = generate_problem(grade)
        problems.append(problem)

    sessions[session_id] = {"problems": problems, "answers": [], "score": 0, "grade": grade}
    
    # return a JSON response
    return jsonify({"problems": problems, "session_id": session_id})




@app.route("/submit", methods=["POST"])
@app.route("/submit", methods=["POST"])
def submit_answers():
    data = request.json
    
    if data is None or "session_id" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    session_id = data.get("session_id")
    answers = data.get("answers", [])

    if session_id is None or not isinstance(answers, list):
        return jsonify({"error": "Invalid request data"}), 400

    if session_id not in sessions:
        return jsonify({"error": "Invalid session ID"}), 400

    session = sessions[session_id]
    grade = session["grade"]
    problems = session["problems"]
    correct_answers = []

    if len(answers) != len(problems):
        return jsonify({"error": "Invalid number of answers"}), 400

    for i, (problem, answer) in enumerate(zip(problems, answers)):
        if safe_eval(problem) == answer:  # replace calculate_answer with safe_eval
            session["score"] += 1
            correct_answers.append(i + 1)

    del sessions[session_id]
    return jsonify({"score": session["score"], "correct_answers": correct_answers}), 200



if __name__ == "__main__":
    app.run(debug=True)
