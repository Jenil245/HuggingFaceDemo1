from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"error : {e}")