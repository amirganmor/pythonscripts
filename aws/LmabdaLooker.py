import json
import psycopg2


def lambda_handler(event, context):
    db="dwh"
    hos="redshift-small-hdd.cwn3tgmpcufx.us-east-1.redshift.amazonaws.com"
    por="5439"
    us="amir"
    pas="Amirganmor_1"
    con=psycopg2.connect(dbname= db, host=hos, port= por, user= us, password= pas)
    curs = con.cursor()
    
    dontSkip = 1
    typeOf = str(event['data']['typeName'])
    if typeOf == "Cost" :
        newCost = event['form_params']['NewValue']
        date = event['data']['DateVal']
        costType = event['data']['cost_type']
        query = "DELETE FROM marketing.costs_by_looker WHERE cost_type = '" + costType + "' AND  date LIKE '" + date +"%';"
        query1 = "INSERT INTO marketing.costs_by_looker (date,cost_type,cost) VALUES  ('" + date + "-01','"+ costType +"','" +  newCost + "');"
    elif  typeOf == "Insert" :
        month = event['form_params']['month']
        costType = event['form_params']['cost_type']
        newCost = event['form_params']['NewValue']
        query = "DELETE FROM marketing.costs_by_looker WHERE cost_type = '" + costType + "' AND  date LIKE '" + month +"%';"
        query1 = "INSERT INTO marketing.costs_by_looker (date,cost_type,cost) VALUES  ('" + month + "-01','"+ costType +"','" +  newCost + "');"    
    elif typeOf == "Date" :
        date = event['data']['DateVal']
        costType = event['data']['cost_type']
        month = event['form_params']['month']
        query = "DELETE FROM  marketing.costs_by_looker WHERE   cost_type  = '" + costType + "' AND date LIKE '" + month +"%'"
        query1 = "UPDATE marketing.costs_by_looker  SET date = '" +  month + "-01' WHERE cost_type = '" + costType + "' AND date = '" + date  + "-01'" 
    elif typeOf == "Delete" :
        dontSkip = 0
        costType = event['data']['cost_type']
        date = event['data']['DateVal']
        query = "DELETE FROM  marketing.costs_by_looker WHERE   cost_type  = '" + costType + "' AND date LIKE '" + date +"%'"
    
    
    curs.execute(query)
    con.commit()
    if dontSkip ==1 :
        curs.execute(query1)
        con.commit()
    con.close()    

    return {
        "statusCode": 200,
        "body": json.dumps('{"looker": {"success": true,"refresh_query": true}}' )
    }
