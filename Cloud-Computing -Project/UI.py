from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for
import sys
import time
from work_delegation import divide_work

app = Flask(__name__, static_folder='static')

def stringFormat(s):
	return str(s)[3:-2];

@app.route('/airfoil', methods=['POST', 'GET'])
def start_page():
	if request.method == 'GET':
		return render_template("startPage.html");
	if request.method == 'POST':
		data = request.form;
		NACA = stringFormat(data.getlist('NACA'));
		maxA = stringFormat(data.getlist('maxA'));
		minA = stringFormat(data.getlist('minA'));
		nrA = stringFormat(data.getlist('nrA'));
		t = stringFormat(data.getlist('t'));
		vi = stringFormat(data.getlist('vi'));
		samp = stringFormat(data.getlist('samp'));
		speed = stringFormat(data.getlist('speed'));
		nrN = stringFormat(data.getlist('nrN'));
		nrR = stringFormat(data.getlist('nrR'));
		#time.sleep(5)
		#divide_work(int, int, int, int, int, str, int, float, float, float)
		filename = divide_work(int(minA), int(maxA), int(nrA), int(nrN), int(nrR), NACA, int(samp), float(vi), float(speed), float(t))
		return send_from_directory('/home/ubuntu/results/', filename);
		#return send_from_directory('./', 'result.txt');

@app.route('/result', methods=['POST','GET'])
def result():
	if request.method == 'GET':
		return "GET"
	if request.method == 'POST':
		print(request.form);
		#return send_from_directory('./', request.form);
	return send_from_directory('./', 'result.txt');


if __name__ == '__main__':
	app.run(host='::',debug=True)
