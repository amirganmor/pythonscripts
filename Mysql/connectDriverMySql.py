import jaydebeapi
import jpype
import asyncio
import json
import os


#equerement - Java 8 
#install /mysql-connector-java-8.0.17
#install visual stidio 2019 (for visual studio 2014)
#downgrade 


convertStrings=False

def fetch_db_Win1( db):
    table1='lmntr_2_edd_activity_log_temp'
    table2='lmntr_8_posts'
    conn = jaydebeapi.connect("com.mysql.jdbc.Driver",
                              "jdbc:mysql://35.246.223.158:3306"
                              "/{}?zeroDateTimeBehavior=convertToNull".format(db),
                              {'user': "data_team",
                               'password': "eV5*mQV(tB"
                               },                              
                              'C:/Program Files (x86)/MySQL/Connector J 8.0/mysql-connector-java-8.0.17.jar'
                              )
    curs = conn.cursor()
    #query = "show tables" 
    query = "select  count(*)  from {}  ".format(table1)
    curs.execute(query)
    results = curs.fetchall()
    print(results)
'''
    curs2 = conn.cursor()
    query2 = "SELECT * FROM website_db.affiliate_wp_affiliatemeta"
    curs2.execute(query2)
    results2 = curs2.fetchall()
    print(results2)
'''
#main
if __name__ == '__main__':
    print('start')
    fetch_db_Win1('website_db')
    print('end')
