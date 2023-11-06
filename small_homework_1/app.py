from flask import Flask
from api import get_all_tests_average_marks, get_all_failed_students

app = Flask(__name__)

@app.route('/')
def home():
    html = "<ul>"
    html += "<li><a href='/tests'>Tests</a></li>"
    html += "<li><a href='/failed'>Failed</a></li>"
    html += "</ul>"

    return html

@app.route('/tests')
def tests():
    tests_average_marks = get_all_tests_average_marks()

    html = "<table>"
    html += "<tr>"
    html += "<th>Test Name</th>"
    html += "<th>Average Mark</th>"
    html += "</tr>"
    for test_name, average_mark in tests_average_marks.items():
        html += "<tr>"
        html += f"<td>{test_name}</td>"
        html += f"<td>{average_mark}</td>"
        html += "</tr>"
    html += "</table>"

    return html

@app.route('/failed')
def failed():
    failed_students = get_all_failed_students()

    html = "<ul>"
    for student_name in failed_students:
        html += f"<li>{student_name}</li>"
    html += "</ul>"

    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')