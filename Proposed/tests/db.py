	from flask import Flask, jsonify

	import mysql.connector

	app = Flask(__name__)

	con = mysql.connector.connect(
		host = 'localhost',
		user = 'dbbd_admin',
		password = 'admin@1234',
		database = 'dbbd'
	)

	@app.route('/gettables', methods=['GET','POST'])
	
	def get_tables():
		cursor = con.cursor()
		
		cursor.execute('SHOW TABLES;')
		
		tables = cursor.fetchall() # Fetches all results returned
		
		cursor.close()
		
		con.close() # Closing Connection
		
		table_names = [table[0] for table in tables]
		
		return jsonify({'tables':table_names}), 200
		
	if __name__ == '__main__':
		print("Connecting to DB")
		app.run(debug=True)
	  