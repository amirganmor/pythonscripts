import mysql.connector


mydb = mysql.connector.connect (
    database='website_db' , 
    host = "35.246.223.158",
    user ="data_team",
    passwd="eV5*mQV(tB",
    port="3306",
)
#print(mydb)

curs = mydb.cursor()
#query = "show tables" 
query = "SELECT * FROM website_db.affiliate_wp_affiliatemeta"
curs.execute(query)
results = curs.fetchall()
print(results)
