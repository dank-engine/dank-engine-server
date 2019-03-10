from flask import Flask, request, session
from flask_session import Session
import data_passer, json, time
app = Flask(__name__)

#Sessions, but unused as of yet
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

#temporary storage
trips = {
    'data': None,
}

#Hello World sanity check
@app.route('/')
def hello_world():
    return 'Hello, World!'

#actual program
#route takes variable of what lines to retriev
@app.route('/trainpoll/<line>', methods=['GET', 'POST'])
def poll(line):
    
    
    lines = line.split(',')
    for line in lines:
        if line not in data_passer.lines:
            return 'Invalid Lines'

    if request.method != "GET":
        return 'Wrong req'
    else:
        print('trips server data: ' +str(trips['data']))
        print('current time: ' +str(time.time()))
        if (trips['data'] == None) or ((time.time() - trips.get('data')[0])  > 60):
            print('data updated!')
            trips['data'] = data_passer.get_train_data(lines)
        
        output = {
            'data': trips['data']
        }

        print(output)
        print(json.dumps(output))
        return json.dumps(output)
