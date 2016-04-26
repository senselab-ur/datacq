from flask import Flask
from flask import render_template
from flask import Response
from flask import stream_with_context
from flask import request
import csv

app = Flask(__name__)

@app.route('/')
def IndexPage():
    return render_template('index.html')

@app.route('/data.csv')
def FetchData():
    def readCSV():
        data = open('data.csv','r')
        reader = csv.reader(data)
        for row in reader:
            yield ';'.join(row) + '\n'
    return Response(readCSV(), mimetype="text/csv")

@app.route('/stream')
def stream():
    def readCSV():
        data = open('data.csv','r')
        reader = csv.reader(data)
        for row in reader:
            yield ';'.join(row) + '\n'
    return Response(stream_with_context(readCSV()))

@app.route('/test')
def Test():
    return render_template('readfile.html')

if __name__ == '__main__':
    app.run(host="localhost", port=3000, threaded=True, debug=True)
