from bottle import run, get, post, view, request, redirect
import requests, bottle, json, threading, time, sys


peers = sys.argv[2:]
porta = int(sys.argv[1])

messages = []
port_clock = {}

tempo = 0

#tempo = [0] * (len(peers) + 1)
# def inc_tempo():
# 	tempo[0] += 1
# 	return tempo[:]

def inc_tempo():
	global tempo
	tempo += 1

def add_port_clock(p, c):
	return port_clock.update(dict({p:c}))


@get('/')
@view('index')
def index():
	return {'messages': messages, 'clock': str(tempo)}


@get('/new')
@view('new')
def new():
	return

@post('/sendMessage')
def newMessage():
	user = request.forms.get('user')
	msg = request.forms.get('message')

	clock = 0
	if [user, msg, port_clock] not in messages:
		clock = tempo + 1
		add_port_clock(str(porta),clock)
		messages.append([user, msg, str(port_clock) ])
		inc_tempo()
	redirect('/')


@get('/peers')
def index():
	return json.dumps(peers)


@get('/messages')
def index():
	return json.dumps(messages)


@get('/clock')
def index():
	return json.dumps(tempo)


@get('/port')
def index():
	return json.dumps(porta)



def sync_clock():
	time.sleep(5)
	while True:
		nt = []
		global tempo
		for p in peers:
			t = requests.get(p + '/clock')
			nt = json.loads(t.text)
			port = requests.get(p + '/port')
			nport = json.loads(port.text)
			if nt >= tempo:
				add_port_clock(str(nport),nt)
				tempo = nt

		print(tempo)
		print(messages)
		time.sleep(1)


def sync_peers():
	time.sleep(5)
	while True:
		np = []
		cont = 0
		for p in peers:
			r = requests.get(p + '/peers')
			np = np + json.loads(r.text)
		peers[:] = list(set(np + peers))
		print(peers)
		time.sleep(1)


def sync_messages():
	time.sleep(5)
	while True:
		for p in peers:
			m = requests.get(p + '/messages')
			for msg in json.loads(m.text):
				if msg not in messages and msg != []: 
					if (msg[0] not in messages and msg[1] not in messages):
						messages.append(msg)
		print(messages)
		time.sleep(1)

t1 = threading.Thread(target=sync_clock)
t1.start()

t2 = threading.Thread(target=sync_peers)
t2.start()

t3 = threading.Thread(target=sync_messages)
t3.start()


run(host='localhost', port= porta)
