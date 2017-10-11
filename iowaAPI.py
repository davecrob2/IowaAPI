from flask import Flask, request, g, jsonify
import sqlite3


app=Flask(__name__)


def connection():
	conn=sqlite3.connect('IowaVoters.db')
	return(conn)

def get_connection():
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db=connection()
	return(g.sqlite_db)

@app.teardown_appcontext
def close_db(error):
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()


@app.route('/get_voters_where')
def get_info():
	c=get_connection()
	curs=c.cursor()

	arguments=request.args

@app.route('/testing')
def get_args():
	
	arguments=request.args
	c=get_connection()
	curs=c.cursor()

	results=dict()
	datalist=list()
	fetchnum=0

	if arguments.get('limit'):
		fetchnum=int(arguments.get('limit'))

	
	for i in range(fetchnum):
		#If the county is specified, this will return the county
		if arguments.get('county'):
			curs.execute("SELECT County FROM Monthly_Voter_Totals where County=?",(arguments['county'],))
			results['county']=curs.fetchone()[0]
		
		#This is an if statement to catch improperly formatted months and convert properly formatted months to SQL readable month format
		if len(arguments.get('month')) == 2:
			monthformat=arguments.get('month')+"%"
		else:
			monthformat="0"+arguments.get('month')+"%"
		
		#If a month is specfied, this will return the date
		if arguments.get('month'):
			curs.execute("SELECT Date FROM Monthly_Voter_Totals where Date Like ? AND County=?",(monthformat,arguments['county'],))
			results['month']=curs.fetchone()[0]

		#If a party is specified, this will return the total number of voters in each party selected and the total number of active voters
		party=arguments.get('party')
		if party == 'democrat':
			curs.execute('SELECT SUM("DemocratActive")+SUM("DemocratInactive") FROM Monthly_Voter_Totals WHERE county=?',(arguments['county'],))
			results['Democrats']=str(curs.fetchone()[0])
			curs.execute('SELECT DemocratActive FROM Monthly_Voter_Totals WHERE county=?',(arguments['county'],))
			results['Democrats-Active']=str(curs.fetchone()[0])
		elif party == 'republican':
			curs.execute('SELECT SUM("RepublicanActive")+SUM("RepublicanInactive") FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Republican']=str(curs.fetchone()[0])
			curs.execute('SELECT RepublicanActive FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Republicans-Active']=str(curs.fetchone()[0])
		elif party == 'Libertarian':
			curs.execute('SELECT SUM("LibertarianActive")+SUM("LibertarianInactive") FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Libertarian']=str(curs.fetchone()[0])
			curs.execute('SELECT LibertarianActive FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Libertarian-Active']=str(curs.fetchone()[0])
		elif party == 'Other':
			curs.execute('SELECT SUM("OtherActive")+SUM("OtherInactive") FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Other']=str(curs.fetchone()[0])
			curs.execute('SELECT OtherActive FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['Other-Active']=str(curs.fetchone()[0])
		elif party == 'No Party':
			curs.execute('SELECT SUM("NoPartyActive")+SUM("NoPartyInactive") FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['No Party']=str(curs.fetchone()[0])
			curs.execute('SELECT NoPartyActive FROM Monthly_Voter_Totals WHERE County=?',(arguments['county'],))
			results['No Party-Active']=str(curs.fetchone()[0])
		datalist.append(results)
	return(jsonify(results))