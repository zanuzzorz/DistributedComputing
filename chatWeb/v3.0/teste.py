from bottle import run, get, post, view, request, redirect
import requests, bottle, json, threading, time, sys


peers = sys.argv[2:]
porta = int(sys.argv[1])

messages = []

tempo = [0] * (len(peers) + 1)
clock = []

def inc_tempo():
	tempo[0] += 1
	return tempo[:]



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
	#inc_tempo()
	clock = inc_tempo()
	messages.append([user, msg, dict({porta:clock})])
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


def sync_clock():
	time.sleep(5)
	while True:
		nt = []
		cont = 0
		for p in peers:

			t = requests.get(p + '/clock')
			nt = nt + json.loads(t.text)
			print("NTTTT")
			print(nt)
			if cont > 0:
				tempo[cont] = nt[0]
				# if messages and len(messages) > 1:
				# 	del messages[cont]
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
		for p in peers:
			m = requests.get(p + '/messages')
			nms = json.loads(m.text)
			for msg in nms:
					x = json.dumps(messages)			
					load = json.loads(x)	
					#and (msg[0] not in messages and msg[1] not in messages):
					if msg not in messages and msg not in load: 
						# puts(msg[0])
						# puts(msg[1])
						# puts(messages)
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
