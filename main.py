import json
from prettytable import PrettyTable
from flask import Flask, request, jsonify, render_template

LOGS_PASSWORD = "90457ghoaHJLVBSJFdfnb79q35y4terv24875gq0rnvb"
app = Flask(__name__)


def generate_secret_code(nickname, score, date):
    result = 89756
    for letter in nickname:
        result += ord(letter)
    result += score
    minute = date.split(" ")[1].split(":")[1]
    result = result * int(minute)

    return result

def read_log_file():
    try:
        with open("scores_log.json", "r") as file:
            existing_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_log = []

    return existing_log


def append_json_to_file(score):
    existing_log = read_log_file()
    existing_log.append(score)

    with open("scores_log.json", "w") as file:
        json.dump(existing_log, file, indent=2)


@app.route("/")
def home():
    existing_log = read_log_file()
    existing_log = sorted(existing_log, key=lambda x: x["score"], reverse=True)
    existing_log = [{"no": i + 1, "score": entry["score"], "nick": entry["nick"]} for i, entry in enumerate(existing_log)]

    return render_template("top-10.html", logs=existing_log)


@app.route("/get-top-10", methods=['GET'])
def get_top_10():
    existing_log = read_log_file()
    existing_log = sorted(existing_log, key=lambda x: x["score"], reverse=True)
    existing_log = [f"{i + 1};{entry['score']};{entry['nick']}"
                    for i, entry in enumerate(existing_log) if i < 10]
    print(existing_log)
    return existing_log


@app.route("/upload", methods=['POST'])
def upload():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    nickname = data.get("nick")
    score = data.get("score")
    date = data.get("date")
    system_user_name = data.get("user")
    host_name = data.get("host")
    os_name = data.get("os")
    code = data.get("code")

    if not nickname or not isinstance(score, int):
        return jsonify({"error": "Incorrect data"}), 400

    if not generate_secret_code(nickname, score, date) == code:
        return jsonify({"error": "Not authorized upload"})

    append_json_to_file(data)
    print(data)
    return jsonify({"status": "OK"}), 200


@app.route("/show-logs", methods=['POST'])
def show_logs():
    secret = request.form.get("secret")
    if secret != "90457ghoaHJLVBSJFdfnb79q35y4terv24875gq0rnvb":
        return "Unauthorized", 401

    existing_log = read_log_file()
    existing_log = sorted(existing_log, key=lambda x: x["date"], reverse=True)

    return render_template("logs.html", logs=existing_log)


def main():
    pass


main()


if __name__ == '__main__':
    app.run(debug=False)

