from bottle import run, get, post, view, request, redirect
import requests, bottle, json, threading, time, sys


peers = sys.argv[2:]
messages = []

@get('/')
@view('index')
def index():
    return {'messages': messages}
    

@get('/new')
@view('new')
def new():
	return

@post('/sendMessage')
def newMessage():
    user = request.forms.get('user')
    msg = request.forms.get('message')
    messages.append([user, msg])
    redirect('/')

@get('/peers')
def index():
    return json.dumps(peers)

@get('/messages')
def index():
    return json.dumps(messages)

def client():
    time.sleep(5)
    while True:
	time.sleep(1)
        np = []
        nm = []
        for p in peers:
            r = requests.get(p + '/peers')
            np = np + json.loads(r.text)

            m = requests.get(p + '/messages')
            nms = json.loads(m.text)
	    for msg in nms:
       		if msg not in messages:
			messages.append(msg)
	
        peers[:] = list(set(np + peers))

        print(peers)
        print(messages)

t = threading.Thread(target=client)
t.start()


run(host='localhost', port=int(sys.argv[1]))
