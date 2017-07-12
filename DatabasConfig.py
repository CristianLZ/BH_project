import numpy as np
import MySQLdb

DB_file_config = np.load('saved_database_info.npy').item()

host   = DB_file_config['host']           # your host, usually localhost
user   = DB_file_config['user']           # your username 
passwd = DB_file_config['passwd']         # your password
db     = DB_file_config['db']             # name of the database

database = MySQLdb.connect(host="localhost",            # your host, usually localhost
                     user="root",                 # your username 
                     passwd="dantes",             # your password
                     db="Black_Hole_Data")        # name of the database

# database = MySQLdb.connect(host, user, passwd, db)
cur = database.cursor()

def get_BH_list_ID():
	cur = database.cursor(MySQLdb.cursors.DictCursor)

	cur.execute("""select distinct BHiord FROM Black_Hole_Accretion_Disk""")
	all_BH_ids = cur.fetchall()

	return all_BH_ids

def get_DB_tables_List():
	cur.execute("SHOW TABLES")
	tables = cur.fetchall()
	
	return tables

def get_axis_by_id(BHiord, field_x_axis, field_y_axis):
	cur = database.cursor(MySQLdb.cursors.DictCursor)
	cur.execute("""SELECT %s, %s  FROM Black_Hole_Accretion_Disk WHERE BHiord='%s'""" % (field_x_axis, field_y_axis , BHiord)) 
	rows = cur.fetchall()

	return rows

def get_all_fields():
	cur.execute("""SELECT column_name from information_schema.columns where table_name='Black_Hole_Accretion_Disk'""")
	all_rows = cur.fetchall()
	x = []
	for item in all_rows:
		x.extend(item)
	return x