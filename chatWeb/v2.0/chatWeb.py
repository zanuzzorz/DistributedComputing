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

def client_peers():
	time.sleep(5)
	while True:
		np = []
		for p in peers:
			r = requests.get(p + '/peers')
			np = np + json.loads(r.text)
		peers[:] = list(set(np + peers))
		print(peers)
		time.sleep(1)


def client_messages():
	time.sleep(5)
	while True:
		nm = []
		for p in peers:
			m = requests.get(p + '/messages')
			nms = json.loads(m.text)
			for msg in nms:
					if msg not in messages:
						messages.append(msg)
	
		time.sleep(1)

t = threading.Thread(target=client_peers)
t.start()

t2 = threading.Thread(target=client_messages)
t2.start()


run(host='localhost', port=int(sys.argv[1]))
