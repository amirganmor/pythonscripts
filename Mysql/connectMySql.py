import mysql.connector

table1='lmntr_2_edd_activity_log_temp'
mydb = mysql.connector.connect (
    host = "localhost",
    user ="root",
    passwd="theicea13",
    port="3306",
)
#print(mydb)

curs = mydb.cursor()
#query = "show tables" 
query = "SELECT * FROM sakila.actor"
curs.execute(query)
results = curs.fetchall()
print(results)
