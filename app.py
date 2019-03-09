from flask import Flask, request
import data_passer, json, time
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
trips = {
    'data': None
}

#

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/trainpoll/<line>', methods=['GET', 'POST'])
def poll(line):
    
    
    line = 'SPRP'
    if request.method != "GET":
        return 'Wrong req'
    else:
        print('trips server data: ' +str(trips['data']))
        print('current time: ' +str(time.time()))
        if (trips['data'] == None) or ((time.time() - trips.get('data')[0])  > 60):
            print('data updated!')
            trips['data'] = data_passer.get_train_data(['SPRP'])
        
        output = {
            'data': trips['data']
        }

        print(output)
        print(json.dumps(output))
        return json.dumps(output)
