from flask import Flask, render_template, request, redirect, abort, flash, url_for, json, Markup, session
import urllib
import json
import datetime
import numpy as np
from bokeh.plotting import figure,show
from bokeh.io import output_file,output_server
import os


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def main():
	return redirect('/index')

@app.route('/index')
def index():
	return render_template('index.html')
  
@app.route('/index', methods=['POST'])
def search():
	error = None  
  
	uh=urllib.urlopen('https://www.quandl.com/api/v3/datasets/WIKI/'+request.form['ticker']+'.json')
	qc=uh.read()
	js=json.loads(str(qc))
	data=js["dataset"]["data"]
    
	t=int(request.form['cars'])
	stk=request.form['ticker']
	table={1:'Open',2:'High',3:'Low',4:'Close',5:'Volume',6:'Ex-Dividend',7:'Split Ratio',8:'Adj. Open',9:'Adj. High',10:'Adj. Low',11:'Adj. Close',12:'Adj. Volume'}
	item=table[t]	
	tit=item+' of '+stk+' (Data from Quandle WIKI)'

	date=[]
	acp=[]
	
	for i in data:
		a1=datetime.datetime.strptime(i[0], '%Y-%m-%d')    
		date.append(datetime.date(a1.year,a1.month,a1.day))
		acp.append(i[t])

		np_acp=np.array(acp)

	output_file("./templates/output.html")
	p=figure(x_axis_type="datetime",title=tit,x_axis_label = "Date",y_axis_label = item)
	r=p.line(date,acp)
	show(p)
	
	#files = os.listdir(os.curdir)
	#return json.dumps({'error':files})
	#flash(request.form['ticker']+' '+request.form['cars'])
	return render_template('output.html')

#@app.errorhandler(500)
#def internal_error(exception):
	#return json.dumps({'err':exception})

if __name__ == '__main__':
	app.debug = True
	app.run(debug=True)