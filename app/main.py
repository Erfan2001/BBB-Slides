from flask import Flask, render_template, request, send_file, redirect
from app.calculation import calculate
from pathlib import Path
from shutil import rmtree
import os
app = Flask(__name__)


# @app.route('/')
# def main():
#     return render_template('index.html')


# @app.route('/action', methods=["POST", "GET"])
# def action():
#     if request.method == "POST":
#         length = calculate(request.form.get('action1'))
#         return send_file('./sample.zip',as_attachment=True)
#         os.remove("./sample.zip")
#     else:
#         return "<h1>Salama</h1>"

@app.route('/slide')
def action():
    response = calculate(f"{request.args.get('url')}")
    return {"data": response}


@app.route('/download/<x>')
def getter(x):
    print(x)
    # print(request.args.get("url"))
    return send_file('../data/%s.zip' % str(x), as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>You could not find me yet :)))</h1><br/><h2><a href="https://www.linkedin.com/in/erfan-nourbakhsh-221540197/">You can contact me</a></h2>'
