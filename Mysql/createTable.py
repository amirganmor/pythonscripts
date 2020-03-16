import psycopg2
db="dwh"
hos="redshift-small-hdd.cwn3tgmpcufx.us-east-1.redshift.amazonaws.com"
por="5439"
us="amir"
pas="Amirganmor_1"


con=psycopg2.connect(dbname= db, host=hos, port= por, user= us, password= pas)
curs = con.cursor()
#query = "select * from marketing.costs_by_looker"
#query = "select * from marketing.finance_manually_cost"
query = "create table  marketing.finance_manually_cost(date date, cost_type varchar(100), cost varchar(100) );"
curs.execute(query)
con.commit()
#results = curs.fetchall()
#print(results)
