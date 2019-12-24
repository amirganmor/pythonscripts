import MySQLdb
db = MySQLdb.connect(host = "35.246.223.158",    # your host, usually localhost
                     user ="data_team",         # your username
                     passwd="eV5*mQV(tB",  # your password
                     db="website_db")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM website_db.affiliate_wp_affiliatemeta")

# print all the first cell of all the rows
res =  cur.fetchall()
print(res)
#for row in cur.fetchall():
#    print (row[0])

db.close()
