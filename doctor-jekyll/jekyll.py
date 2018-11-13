from subprocess import check_output
from flask import Flask, flash, redirect, render_template, request, session, abort

jekyll = Flask(__name__)


def get_memory():
    mem = check_output(["free", "-m"])
    return mem


@jekyll.route("/system_info")
def system_info():
    return "Data"


@jekyll.route("/")
@jekyll.route("/index")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    jekyll.run(debug=True)
