import MySQLdb
# setting the library as a variable called plt
import matplotlib.pyplot as plt
import numpy as np

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="blackhole",  # your password
                     db="Black_Hole_Data")        # name of the database

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor(MySQLdb.cursors.DictCursor)


#this is our mysql query
#cur.execute("""select distinct BHiord FROM Black_Hole_Accretion_Disk""")
cur.execute("""SELECT Time, Final_BH_Mass  FROM Black_Hole_Accretion_Disk WHERE BHiord='101863510'""")


#It is going to fetch the executed mysql query into rows.
#Hence assigning it to row
rows = cur.fetchall()
Time = []
Mass = []

for row in rows:
    # print "%s, %s" % (row["Time"], row["Final_BH_Mass"])
    Time.append(row["Time"])
    Mass.append(row["Final_BH_Mass"])

fig, ax = plt.subplots()

MaxTime = max(Time)
MinTime = min(Time)

x = np.linspace(0, 1, 500)
y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

# print str(MinTime) + ' ' + str(MaxTime)

#ax.fill(Time, Mass, zorder=10)
plt.plot(Time, Mass, linewidth=2)
plt.tick_params(axis='both', labelsize = 14)
# setting the title of the graph
plt.title("Mass vs Time (BlackHole id = 101863510)", fontsize=14)
plt.xlabel("Time")
plt.ylabel("Mass")
plt.savefig('blackhole_1_plot.png', bbox_inches='tight')

print 'there are ' + str(len(rows)) + ' rows'
#closing the function
cur.close()