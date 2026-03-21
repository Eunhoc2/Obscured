from flask import Flask



app = Flask(__name__)

@app.route('/')
def index():
    return 'Hi Mom!'



if __name__ == '__main__':
    app.run(debug = True)