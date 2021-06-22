import sqlite3

def create_connection(db_file):

	try:
		conn = sqlite3.connect(db_file)
		return conn
	except sqlite3.Error as e:
		print(f"create_connection Error: {e}")

def sql_query(conn, sql, id=None, rtn=None):

	try:
		c = conn.cursor()
		if id:
			c.execute(sql, (id,))
		else:
			c.execute(sql)
	except sqlite3.Error as e:
		print(f"sql_query Error: {e}")
	else:
		conn.commit()

		if rtn:
			if(rtn == "lastrowid"):
				return c.lastrowid
			if(rtn == "fetchall"):
				return c.fetchall()
			if(rtn == "fetchone"):
				return c.fetchone()
	finally:
		conn.close()

def sql_initialize(conn, schema):
    
    with open(schema, 'r') as sql_file:
        sql_script = sql_file.read()
    
    try:
        c = conn.cursor()
        c.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        print(f"sql_initialize: {e}")
    finally:
        conn.close()

sql = "webform.db"

db = create_connection(sql)

sql = "SELECT * from regions"

regions = sql_query(db, sql, rtn="fetchall")

for region in regions:
    print(region)