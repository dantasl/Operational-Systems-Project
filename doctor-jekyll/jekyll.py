import json
from subprocess import check_output, Popen, PIPE, STDOUT
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
    c_list.append(word)  # Last word can enter simply like this
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


@jekyll.route("/pgfaults")
def get_pg_fault():
    cmd = "ps -eo min_flt,maj_flt,pid | less"
    pg_fault = check_output(cmd, shell=True).decode("utf-8")  # Calling command to get page faults
    items = pg_fault.split("\n")
    items_list_big = [item.split(" ") for item in items]

    items_list = []
    for item_list in items_list_big:
        local_list = []
        for item in item_list:
            if len(item) > 0:
                local_list.append(item)
        items_list.append(local_list)

    items_list_dict = []
    for item in items_list[1:]:
        if len(item) == 3:
            item_dict = {
                "page_minor": item[0],
                "page_major": item[1],
                "pid": item[2]
            }
            if item_dict["page_minor"] != '0' and item_dict["page_major"] != '0':
                items_list_dict.append(item_dict)

    return json.dumps(items_list_dict)


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
