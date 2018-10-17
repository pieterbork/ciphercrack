from flask import Flask, render_template, request
from .core import crack

app = Flask(__name__)

@app.route('/')
def index():
    cipher = request.args.get('ciphertext')
    if cipher:
        try:
            result = crack(cipher)
            return render_template('index.html', plaintext=result)
        except:
            result = "Sorry, there was an issue trying to crack this ciphertext."
            return render_template('index.html', error=result)
    return render_template('index.html', greeting='Paste some ciphertext in that box!')
