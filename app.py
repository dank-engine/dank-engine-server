from flask import Flask, request
import data_passer, json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/trainpoll/<line>', methods=['GET', 'POST'])
def poll(line):
    if request.method != "GET":
        return 'Wrong req'
    else:
        output = json.dumps(data_passer.get_train_data([]))
        print(output)
        return output
