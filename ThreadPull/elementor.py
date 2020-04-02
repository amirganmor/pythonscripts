import datetime
from subprocess import call
import gzip
import shutil
import sys
import multiprocessing
import time
import smtplib

def send_email(user, password, recipient, subject, body):
    gmail_user = user
    gmail_pwd = password
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()


def SerialRun(DB , table, awsPath) :
    homePath="/home/ubuntu/jsonFromSql/cron/"
    tmp = homePath +  table + DB +"_tmp.txt"
    RunTable = str(table.split("--")[0])
    if DB == "website_db" :
        tableFile ="website_db." + RunTable
        command2 = "ssh carmitelementor@104.248.94.171 -p 51865 -t  'mysql -u carmit_read -p'KG02=C[vjdaLskcnjhs1c\!rtv6' -h 35.246.223.158 --default-character-set=utf8 -e \"select *  from "  + tableFile  + "  \"'  > " + tmp
    elif  DB == "statslmn_stats" :
        tableFile ="statslmn_stats." + RunTable
        command2 = "ssh yakir@207.154.219.93 -p 51865 -t 'mysql -u sara -p'KvnaOL0}]dfPFGLP\!@95' -h 127.0.0.1  --default-character-set=utf8 -e \"select *  from "  + tableFile +  "\" '  > " + tmp
    elif DB == "stream_db" :
        tableFile ="stream_db." + RunTable
        command2 = "ssh carmitelementor@104.248.94.171 -p 51865 -t  'mysql -u sara_read -p'LMbJo#pWieRvAzc,BVv'  -h 35.198.129.2 --default-character-set=utf8 -e \"select *  from "  + tableFile  + "  \"'  > " + tmp
    call(command2, shell=True)
    fileName =str(table) + DB + ".json"
    outFileName = homePath +  fileName
    zippedOut = homePath  + str(table) + DB + ".json.gz"
    s3OutName=str(table) + ".json.gz"
    s3OutFile=homePath + s3OutName
    f1 = open(tmp , "r" )
    headers = f1.readline().split("\t")
    headers[-1] = str(headers[-1]).replace("\n" , "")

    with open (outFileName, 'a', encoding="utf8") as f:
        for aline in f1 :
            values = aline.split("\t")
            if values[0][0:2] == "\\n" :
                 continue
            values[-1] = str(values[-1]).replace("\n" , "")
            #print(values)
            tmpJson = "{\n"
            try:
                for x in range(len(headers)-1):
                    tmpJson = tmpJson + "\t\"" + str(headers[x]) + "\": \"" + str(values[x]).replace("  " , "").replace("\"" ,  "\'").replace("\." , "\\.")  + "\",\n"
                tmpJson = tmpJson + "\t\"" + str(headers[x+1]) + "\": \"" + str(values[x+1]).replace("  " , "").replace("\"" ,  "\'").replace("\." , "\\.")  + "\"\n"
                tmpJson = tmpJson + "}\n"
                f.write(tmpJson)
            except:
                #f.write("An exception occurred\n" + str(aline) + "\n" + str(len(values)) + "\n"   + str(len(headers)) + "\n")
                #print("An exception occurred\n" + str(aline) + "\n" + str(len(values)) + "\n"   + str(len(headers)) + "\n" )
                userMail="amir@elementor.com"
                pwdMail="theicea13"
                recipientSara="sarah@elementor.com"
                recipientAmir="amir@elementor.com"
                subjectMail="problem with Sql to Json Run, Table : " + table  + " DB : " + DB
                bodyMail="An exception occurred\n line :      " + str(aline) + "\n num of Values:   " + str(len(values)) + "\n num of headers : "   + str(len(headers)) + "\n"
                send_email(userMail, pwdMail, recipientAmir, subjectMail, bodyMail)
                send_email(userMail, pwdMail, recipientSara, subjectMail, bodyMail)
                exit()
    f1.close()
    f.close()
    with open(outFileName, 'rb') as f_in:
        with gzip.open( outFileName + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("end")


def parallelJob(DB ,table , filters , awsPath , startLine , EndLine , jobNum ) :
    homePath="/home/ubuntu/jsonFromSql/cron/"
    tmpFile =  homePath + "tmpJob_" +  str(table) + DB + str(jobNum) + ".txt"
    outFileName = homePath +  str(table) + DB + "_"  + str(jobNum) + ".json"
    utfComv =  " " + tmpFile
    RunTable = str(table.split("--")[0])
    if DB == "website_db" :
        utfComv =  " " + tmpFile
        sql = "select " + str(filters) + "  from website_db."  + RunTable + "  LIMIT " + str(startLine) + ", " +  str(EndLine)
        ssh = "ssh carmitelementor@104.248.94.171 -p 51865 -t "
        command2 = ssh + "'mysql -u carmit_read -p'KG02=C[vjdaLskcnjhs1c\!rtv6'  -h 35.246.223.158  --default-character-set=utf8 -e \" " +  sql  + "\" ' > " + utfComv
    elif  DB == "statslmn_stats" :
        sql = "select "  + str(filters) + "  from statslmn_stats."  + RunTable + " LIMIT " + str(startLine) + ", " +  str(EndLine)
        ssh = "ssh yakir@207.154.219.93 -p 51865 -t"
        command2 = ssh + " 'mysql -u sara -p'KvnaOL0}]dfPFGLP\!@95' -h 127.0.0.1  --default-character-set=utf8 -e \""  +  sql +  "\" ' > " + utfComv
    elif  DB == "stream_db" :
        sql = "select "  + str(filters) + "  from stream_db."  + RunTable + " LIMIT " + str(startLine) + ", " +  str(EndLine)
        ssh = "ssh carmitelementor@104.248.94.171 -p 51865 -t "
        command2 = ssh + " 'mysql -u sara_read -p'LMbJo#pWieRvAzc,BVv'  -h 35.198.129.2 --default-character-set=utf8 -e \""  +  sql +  "\" ' > " + utfComv
    call(command2, shell=True)
    f1 = open(tmpFile , "r" )
    headers = f1.readline().split("\t")
    headers[-1] = str(headers[-1]).replace("\n" , "")
    with open (outFileName, 'a', encoding="utf8") as f:
        for aline in f1 :
            values = aline.split("\t")
            if values[0][0:2] == "\\n" :
                 continue
            values[-1] = str(values[-1]).replace("\n" , "")
            #print(values)
            tmpJson = "{\n"
            try:
                for x in range(len(headers)-1):
                    tmpJson = tmpJson + "\t\"" + str(headers[x]) + "\": \"" + str(values[x]).replace("  " , "").replace("\"" ,  "\'").replace("\." , "\\.")  + "\",\n"
                tmpJson = tmpJson + "\t\"" + str(headers[x+1]) + "\": \"" + str(values[x+1]).replace("  " , "").replace("\"" ,  "\'").replace("\." , "\\.")  + "\"\n"
                tmpJson = tmpJson + "}\n"
                f.write(tmpJson)
            except:
                if DB == "stream_db" and  table == "lmntr_stream_meta" and len(values) == 3 and len(headers) == 4 :
                    tmpJson = tmpJson + "\t\"" + str(headers[x+1]) + "\": \"" + "library" + "\"\n"
                    tmpJson = tmpJson + "}\n"
                    f.write(tmpJson)
                    continue
                #f.write("An exception occurred\n" + str(aline) + "\n" + str(len(values)) + "\n"   + str(len(headers)) + "\n")
                #print("An exception occurred\n" + str(aline) + "\n" + str(len(values)) + "\n"   + str(len(headers)) + "\n" )
                userMail="amir@elementor.com"
                pwdMail="theicea13"
                recipientSara="sarah@elementor.com"
                recipientAmir="amir@elementor.com"
                subjectMail="problem with Sql to Json Run, Table : " + table + "file number: " + jobNum  + " DB : " + DB
                bodyMail="An exception occurred\n line :      " + str(aline) + "\n num of Values:   " + str(len(values)) + "\n num of headers : "   + str(len(headers)) + "\n"
                send_email(userMail, pwdMail, recipientAmir, subjectMail, bodyMail)
                send_email(userMail, pwdMail, recipientSara, subjectMail, bodyMail)
                exit()
    f1.close()
    f.close()
    call( "rm -rf  " +  tmpFile  , shell=True)
    with open(outFileName, 'rb') as f_in:
        with gzip.open( outFileName + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    call( "rm -rf  " +  outFileName  , shell=True)
    if awsPath == "none" :
        aaaa=1
    else :
        call( "rm -rf  " +  outFileName + "  " + tmpFile  , shell=True)
        outName = table + "_" + jobNum +".json.gz"
        outFile =  outFileName + '.gz'
        aa3= datetime.datetime.now().replace(second=0, microsecond=0)
        bb3= str(aa3).split(" ")
        date11 = bb3[0] + "_" +bb3[1]
        aa = " aws s3 cp " + outFile + "  " +  awsPath + outName + "_"  + date11 + "    --region us-east-1  "
        call( aa, shell=True)
        call( "rm -rf  " +   outFileName + '.gz'  , shell=True)
    print("end process : " + jobNum )



def fetchLast15DStreamId() :
    homePath="/home/ubuntu/jsonFromSql/cron/"
    tmpFile =  homePath + "SteamDBLast15DaysUserId.txt"
    sql = "select min(id) from stream_db.lmntr_stream where created>=date_add(current_date,INTERVAL -15 DAY)"
    ssh = "ssh carmitelementor@104.248.94.171 -p 51865 -t "
    command2 = ssh + " 'mysql -u sara_read -p'LMbJo#pWieRvAzc,BVv'  -h 35.198.129.2 --default-character-set=utf8 -e \""  +  sql +  "\" ' > " + tmpFile
    call(command2, shell=True)
    f1 = open(tmpFile, "r")
    f1.readline()
    res1 = str(f1.readline())
    f1.close()
    sql2 = "select meta_id from stream_db.lmntr_stream_meta  where record_id = " + str(res1) + " limit 1;"
    command2 = ssh + " 'mysql -u sara_read -p'LMbJo#pWieRvAzc,BVv'  -h 35.198.129.2 --default-character-set=utf8 -e \""  +  sql2 +  "\" ' > " + tmpFile
    call(command2, shell=True)
    f1 = open(tmpFile, "r")
    f1.readline()
    res = str(f1.readline())
    f1.close()
    return res




DB=str(sys.argv[1])
table=str(sys.argv[2])
if __name__ == '__main__':
    aa3= datetime.datetime.now().replace(second=0, microsecond=0)
    bb3= str(aa3).split(" ")
    date11 = bb3[0] + "_" +bb3[1]
    ditcPaths = {}
    homePath="/home/ubuntu/jsonFromSql/cron/"
    call("rm -rf " + homePath + table  + DB + "*.json " + homePath + table + DB + "*json.gz "   + homePath + "tmpJob_" + table + DB +  "*.txt "  + homePath +  table + DB + "_tmp.txt " , shell=True)
    if (len(table.split("--manually"))) == 2 :
        table = table.split("--manually")[0]
        f3 = open("/home/ubuntu/jsonFromSql/pathsManually" , "r")
    else :
        f3 = open("/home/ubuntu/jsonFromSql/paths" , "r")
    for line in f3 :
        val= line.split()
        ditcPaths[val[0]] = val[1]
    f3.close()
    awsPath = ditcPaths[str(table) + "," +  str(DB)]
    #parallel more then 4 process :
    parallelDictJumps =  {"stats_sites" : [0, 1780000 , 3560000 , 5340000 , 7120000 , 8300000]  }
    parallelDictRange =  {"stats_sites" : [1780000, 1780000 , 1780000 , 1780000 , 1180000 , 19660000]  }
    parallelDict =  [ "lmntr_2_edd_license_activations--stream,website_db" , "lmntr_usermeta,website_db"  , "lmntr_2_edd_license_activations,website_db" , "lmntr_users,website_db"  , "affiliate_wp_visits,website_db" , "lmntr_stream,website_db" , "lmntr_stream_meta,website_db", "lmntr_stream,stream_db" ]
    pool = multiprocessing.Pool(8)
    if table in parallelDictJumps :
        filters = "id , url , scheme , domain , domain1 , path , is_elementor_home , created , updated , uninstall_date , status , api_status , pro  , \
              elementor_version , pro_version , first_payment_id  , lang , theme_id , theme_slug , ip , theme_version , is_localhost  , is_multisite  , \
              is_tracked , scan_time , scan_start_time  "
        for it in range (0, (len(parallelDictJumps[table]))  ) :
            iterNum = int(it)+1
            jump= (parallelDictJumps[table][it])
            rangeOf= (parallelDictRange[table][it])
            pool.apply_async( parallelJob , [ DB , table , filters , awsPath , str(jump) , str(rangeOf) , str(iterNum) ] )
        pool.close()
        pool.join()
    elif  table == "lmntr_stream_meta" and DB == "stream_db" :
        filters ="*"
        #call("rm -rf " + homePath + "SteamDBLast15DaysUserId.txt" )
        IdStart= int(fetchLast15DStreamId()) - 37
        f2 = open(homePath + "TablesLinesCount/lmntr_stream_metastream_db_Lines.txt" , "r" )
        TotLines = int(f2.readline()) - IdStart
        jump = round(TotLines / 8)
        #x=8
        #pool.apply_async(parallelJob , [ DB , table , filters , awsPath , str(x*jump) , str(jump) , str(x+1) ] )
        for x in range(0, 8):
            if x == 7 :
                pool.apply_async(parallelJob , [ DB , table , filters , awsPath , str(x*jump + IdStart ) , str(10 * jump) , str(x+1) ] )
            else :
                pool.apply_async(parallelJob , [ DB , table , filters , awsPath , str(x*jump + IdStart ) , str(jump) , str(x+1) ] )
        pool.close()
        pool.join()
    #parallel run 4 cores
    elif str(table) + "," +  str(DB) in parallelDict :
        if table == "lmntr_usermeta" :
            filters = " umeta_id,user_id,meta_key,SUBSTRING(meta_value, 1, 80) as meta_value "
        else :
            filters = "*"
        RunTable = str(table.split("--")[0])
        f2 = open(homePath + "TablesLinesCount/" + RunTable + DB + "_Lines.txt" , "r" )
        TotLines = int(f2.readline())
        jump = round(TotLines / 4)
        for x in range(0, 3):
            pool.apply_async( parallelJob , [ DB , table , filters , "none" , str(x*jump) , str(jump) , str(x+1) ] )
        pool.apply_async( parallelJob , [ DB , table , filters , "none" , str(3*jump) , str(10*jump) , str(4) ] )
        pool.close()
        pool.join()
        outNamePre = homePath+  table + DB + ".json.gz"
        call( "cat /home/ubuntu/jsonFromSql/cron/" + table + DB + "*.json.gz > " + outNamePre  , shell=True)
        aa = " aws s3 cp " + outNamePre + "  " + awsPath + table +  "_"  + date11 + ".json.gz    --region us-east-1  "
        call( aa, shell=True)
    #serial run
    else:
        SerialRun( DB ,  table , awsPath )
        aa = " aws s3 cp /home/ubuntu/jsonFromSql/cron/" + table + DB + ".json.gz "  + awsPath + table  + "_"  + date11 + ".json.gz    --region us-east-1  "
        call( aa, shell=True)
    call("rm -rf " + homePath + table  + DB + "*.json " + homePath + table + DB + "*json.gz "   + homePath + "tmpJob_" + table + DB +  "*.txt "  + homePath +  table + DB + "_tmp.txt " , shell=True)
    print("end")
