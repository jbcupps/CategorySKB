from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def intro():
    return send_from_directory('', 'index.html')

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/modeler')
def modeler():
    return render_template('modeler.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True)