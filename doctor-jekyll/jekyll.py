import json
from subprocess import check_output
from flask import Flask, flash, redirect, render_template, request, session, abort

jekyll = Flask(__name__)


def normalize_to_list(command):
    # Treating output for string usage
    word = ""
    c_list = []
    for c in command:
        if c != " ":
            word += c
        elif c == " " and len(word) > 1:
            c_list.append(word)
            word = ""
    return c_list


def get_memory():
    # Calling command to get memory usage
    mem = check_output(["free", "-m"]).decode("utf-8")
    mem_list = normalize_to_list(mem)

    # The last one needs special attention
    available = mem_list[11].split("\n")

    # Creating a dict to easily convert to json
    mem_dict = {
        "total": int(mem_list[6]),
        "used": int(mem_list[7]),
        "free": int(mem_list[8]),
        "shared": int(mem_list[9]),
        "buff_cache": int(mem_list[10]),
        "available": int(available[0])
    }

    return mem_dict


def get_swap():
    # Calling command to get swap usage
    swa = check_output(["free", "-m"]).decode("utf-8")
    swa_list = normalize_to_list(swa)

    print(swa_list)

    # Creating a dict to easily convert to json
    swa_dict = {
        "total_swap": int(swa_list[12]),
        "used_swap": int(swa_list[13]),
        "free_swap": (int(swa_list[12]) - int(swa_list[13]))
    }

    return swa_dict



@jekyll.route("/system_info")
def system_info():
    info = get_memory()
    info.update(get_swap())
    return json.dumps(info)


@jekyll.route("/")
@jekyll.route("/index")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    jekyll.run(debug=True)
