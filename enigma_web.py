from flask import Flask, render_template, request, redirect, url_for, session, Response
from enigma import Enigma
import os



app = Flask(__name__)
app.secret_key = os.urandom(24)


ACCESS_PASSCODE = 'Conquer31606'
enigma_machine = Enigma()



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('passcode') == ACCESS_PASSCODE:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Passcode.'
    return render_template('login.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    output = ''
    input_text = ''
    
    if request.method == 'POST':
        if 'reset' in request.form:
            global enigma_machine
            enigma_machine = Enigma()
            return redirect(url_for('index'))

        input_text = request.form.get('message', '')
        enigma_machine.set_message(input_text)
        output = ''.join(enigma_machine.process_message())

    return render_template('index.html', output=output, input_text=input_text)


@app.route("/wav")
def streamwav():
    def generate():
        with open("signals/song.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)