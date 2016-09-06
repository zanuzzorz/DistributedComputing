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
	return {'messages': messages}


@get('/new')
@view('new')
def new():
	return

@post('/sendMessage')
def newMessage():
	user = request.forms.get('user')
	msg = request.forms.get('message')

	clock = tempo + 1
	if [user, msg] not in messages:
		add_port_clock(porta,clock)
		messages.append([user, msg, port_clock])
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
		cont = 0
		for p in peers:

			t = requests.get(p + '/clock')
			nt = json.loads(t.text)
			port = requests.get(p + '/port')
			nport = json.loads(port.text)
			if cont > 0:
				if messages:
					add_port_clock(nport,nt)
					# del messages[cont]

			cont += 1
		print(tempo)
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
		nm = []
		aux = ''
		for p in peers:
			m = requests.get(p + '/messages')
			nms = json.loads(m.text)
			for msg in nms:
					x = json.dumps(messages)
					load = json.loads(x)	
					if msg not in messages and msg not in load: 
						if (msg[0] not in messages and msg[1] not in messages):
							nm = msg
							if messages:
								aux = json.dumps(msg)
								#nm = str(aux)[1:-1]#.replace('{','').replace('}', '')
								nm = json.loads(aux)
								#del messages[-1]
								messages[-1] = nm
							else:
								messages.append(nm)
		print(messages)
		time.sleep(1)

t1 = threading.Thread(target=sync_clock)
t1.start()

t2 = threading.Thread(target=sync_peers)
t2.start()

t3 = threading.Thread(target=sync_messages)
t3.start()


run(host='localhost', port= porta)
