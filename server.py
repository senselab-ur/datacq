from flask import Flask
from flask import render_template
from flask import Response
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

if __name__ == '__main__':
    app.run(host="localhost", port=3000, threaded=True, debug=True)
