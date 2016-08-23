from bottle import run, get, post, view, request, redirect

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
    messages.append((user, msg))
    redirect('/')


run(host='localhost', port=8080)