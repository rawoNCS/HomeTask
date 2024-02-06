from flask import Flask, request

app = Flask(__name__)
last_msg = {"result": ''}


@app.route('/')
def index():
    return "It's alive!"


@app.route('/reverse/', methods=['GET'])
def reverse():
    if request.method == 'GET':
        input_string = request.args.get("in")
        output_string = reverse_sentence(input_string)
        return {"result": output_string}


@app.route('/restore/', methods=['GET'])
def restore():
    if request.method == 'GET':
        return {
            "result": last_msg["result"]
        }


def reverse_sentence(sentence=''):
    words = sentence.split(' ')
    reversed_sentence = ' '.join(reversed(words))
    last_msg["result"] = reversed_sentence
    return reversed_sentence


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
