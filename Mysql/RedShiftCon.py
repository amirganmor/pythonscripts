import psycopg2
db="dwh"
hos="redshift-small-hdd.cwn3tgmpcufx.us-east-1.redshift.amazonaws.com"
por="5439"
us="amir"
pas="Amirganmor_1"


con=psycopg2.connect(dbname= db, host=hos, port= por, user= us, password= pas)
curs = con.cursor()
query = "select * from marketing.costs_by_looker"
curs.execute(query)
results = curs.fetchall()
print(results)
