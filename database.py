#!/usr/bin/python
import MySQLdb
<<<<<<< HEAD

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="dantes",  # your password
                     db="Black_Hole_Data")        # name of the database
=======
import DatabasConfig as DB

db = MySQLdb.connect(host       = "localhost",            # your host, usually localhost
                     user       = "root",                 # your username 
                     passwd     = "dantes",             # your password
                     db         = "Black_Hole_Data")        # name of the database
>>>>>>> 638fab862459a35bf12541ccbd5f224f03bac923

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

#cur.execute("SELECT * FROM Black_Hole_Data")

def send_query_to_db(Query, ID):
	try:
<<<<<<< HEAD
		query1 = 'INSERT IGNORE INTO Black_Hole_Accretion_Disk (Uid) VALUES (%s)' % ID
=======
		query1 = 'INSERT IGNORE INTO Orbits (Uid) VALUES (%s)' % ID
>>>>>>> 638fab862459a35bf12541ccbd5f224f03bac923
		#
		cur.execute(query1)
		# Use all the SQL you like
		
		cur.execute(Query)
		print query1
		print Query
		print ID
		db.commit()
	except:
		# Rollback in case there is any error
		print 'error query not executed correctly'
		db.rollback()
	# print all the first cell of all the rows

<<<<<<< HEAD
propertyFields = [    'BHiord'           ,\
					  'Gasiord'          ,\
					  'Time'             ,\
					  'Initial_Gas_Mass' ,\
					  'Initial_BH_Mass'  ,\
					  'Final_Gas_Mass'   ,\
					  'Final_BH_Mass'    ,\
					  'Gasmass'          ,\
					  'dMacc'            ,\
					  'DMask'            ,\
					  'dx'               ,\
					  'dy'               ,\
					  'dz'               ,\
					  'dvx'              ,\
					  'dvy'              ,\
					  'dvz'              ,\
					  'u'                ,\
					  'bhsoft'           ,\
					  'tcooloff'         ,\
					  'afac'             ,\
					  'rho'              ,\
					  'temp'             ,\
					  'metals'           ,\
					  'h2frac'           ,\
					  'tcool']
num_lines = 0
dataFile = 'mediumfile.log'
=======
propertyFields = DB.get_all_fields()
print propertyFields


num_lines = 0
dataFile = 'OrbitMediumLog'
>>>>>>> 638fab862459a35bf12541ccbd5f224f03bac923
Uid = 1


num_lines = 0
total_data = 0

with open(dataFile, 'r') as f:
    for line in f:
        data_in_file = line.split()

        query = ''
        set_statements = []
        final_set_statements = ''
<<<<<<< HEAD
        query_update_statement = "UPDATE IGNORE Black_Hole_Accretion_Disk \nSET %s \nWHERE  Uid = %s"
=======
        query_update_statement = "UPDATE IGNORE Orbits \nSET %s \nWHERE  Uid = %s"
>>>>>>> 638fab862459a35bf12541ccbd5f224f03bac923
    	
    	i = 0
    	for data in data_in_file:
    		set_statements.append('%s = %s' % (propertyFields[i], data))

    		#set_statements += ('SET    ' + propertyFields[i] +  ' = ' + data_in_file[i] + '\n ')
    		i += 1
    	final_set_statements = ", \n".join(set_statements)

    	# print string_test
    	query = query_update_statement % (final_set_statements, Uid)
    	print query
		# print query
    	send_query_to_db(query, Uid)
    	print "\n"
    	Uid += 1
        num_lines += 1
        total_data += len(data_in_file)

print 'total of lines = %d' % num_lines
print 'total of data = %d' % total_data

cur.close()
db.close()
