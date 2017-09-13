import MySQLdb
# setting the library as a variable called plt
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="blackhole",  # your password
                     db="Black_Hole_Data")        # name of the database

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor(MySQLdb.cursors.DictCursor)

BHiord = 101863521

#this is our mysql query
#cur.execute("""select distinct BHiord FROM Black_Hole_Accretion_Disk""")
cur.execute("""SELECT Time, Final_BH_Mass  FROM Black_Hole_Accretion_Disk WHERE BHiord='%s'"""% BHiord)


#It is going to fetch the executed mysql query into rows.
#Hence assigning it to row
rows = cur.fetchall()
Time = []
Mass = []
timeUnitCF = 38759428183.8
MassUnitCF = 1.84793e16


for row in rows:
    row['Time'] = format(row['Time'], '.8f')
    row['Final_BH_Mass'] = format(row['Final_BH_Mass'], '.17')

rows = sorted(rows,key=lambda x: x['Time'])

print 'Time 			Mass'
for row in rows:
	if((float(row['Time']) != 0.00647407)):
	    print "%s,	%s" % (row["Time"], row["Final_BH_Mass"])
	    Time.append(float(row['Time']) * timeUnitCF)
	    if (row["Final_BH_Mass"] > 0):
	    	Mass.append((float(row["Final_BH_Mass"]) * MassUnitCF)/1000000.0)

del rows[:] 

# print str(MinTime) + ' ' + str(MaxTime)

#ax.fill(Time, Mass, zorder=10)
plt.plot(Time, Mass, linewidth=2)
plt.tick_params(axis='both', labelsize = 14)
# setting the title of the graph
plt.title("Mass vs Time (BlackHole id = %s)" % BHiord, fontsize=14)
plt.xlabel("Time(In Million Years)")
plt.ylabel("Mass (Solar Mass) Msol")
plt.savefig('blackhole_%s_plot.png' % BHiord, bbox_inches='tight')

print 'there are ' + str(len(Time)) + ' rows'
#closing the function
cur.close()