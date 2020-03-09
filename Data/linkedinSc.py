import psycopg2
import os, random, sys, time
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs
import random
import time

def sleepFunc() :
    a=random.randint(0, 15)
    print("sleep for " +  str(a) + " secs " )
    time.sleep(a)

def sleepFuncMin() :
    a=random.randint(1 , 3)
    a1 = int(a)*60
    print("sleep for " +  str(a1) + " secs " )
    time.sleep(a1)

def Query(LIMIT , OFFSET) :
    db="dwh"
    hos="redshift-elementor-prod.cwn3tgmpcufx.us-east-1.redshift.amazonaws.com"
    por="5439"
    us="awsuser"
    pas="Awsuser1234"
    con=psycopg2.connect(dbname= db, host=hos, port= por, user= us, password= pas)
    curs = con.cursor()
    query = "SELECT \
    	lmntr_2_edd_activity_log_agg.email  AS \"lmntr_2_edd_activity_log_agg.customer_email\", \
    	lmntr_2_edd_activity_log_agg.country_state  AS \"lmntr_2_edd_activity_log_agg.country_state\", \
    	lmntr_2_edd_activity_log_agg.country_name  AS \"lmntr_2_edd_activity_log_agg.country_name\", \
    	lmntr_2_edd_activity_log_agg.ip  AS \"lmntr_2_edd_activity_log_agg.ip\", \
    	lmntr_2_edd_activity_log_agg.name  AS \"lmntr_2_edd_activity_log_agg.customer_name\", \
    	lmntr_2_edd_activity_log_agg.customer_id  AS \"lmntr_2_edd_activity_log_agg.customer_id\", \
    	lmntr_2_edd_activity_log_agg.subscription_activity  AS \"lmntr_2_edd_activity_log_agg.subscription_activity\", \
        lmntr_2_edd_activity_log_agg.plan_id  AS \"lmntr_2_edd_activity_log_agg.plan_id\" \
    FROM stats.lmntr_2_edd_activity_log_agg  AS lmntr_2_edd_activity_log_agg \
    WHERE  (1 = 1) and (subscription_activity = 'active')  \
    GROUP BY 1,2,3,4,5,6,7,8 \
    ORDER BY 1  \
    LIMIT " + str(LIMIT) + " offset  "  + str(OFFSET)
    curs.execute(query)
    results = curs.fetchall()
    return results

def LinkedinCheck(results ,username , password ) :
    #connect
    linkedinBasePath="https://www.linkedin.com"
    browser = webdriver.Chrome("C:\\Users\\amir\\Desktop\\pyLib\\chromedriver.exe")
    browser.get('https://www.linkedin.com/uas/login')
    #file = open('C:\\Users\\amir\\Desktop\\pyLib\\t2\\config.txt')
    #lines = file.readlines()
    #username = lines[0]
    #password = lines[1]
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    try:
        elementID.submit()
    except:
        #submit no need
        amir=1
    UsersSet = set()
    d = {}
    with open("dict.txt") as f:
        for line in f :
            (key, val) = line.split(",")
            d[key] = val
    f1 = open("OutReports/1res.txt", "a" ,  encoding='utf-8')
    f2 = open("OutReports/0res.txt", "a" , encoding='utf-8')
    f3=  open("OutReports/2MuchRes.txt", "a" , encoding='utf-8')
    f4=  open("OutReports/8res.txt", "a" , encoding='utf-8')
    ii=0
    for resT in results :
        print("iteration num : " +  str(ii))
        ii=ii+1
        Name1= str(resT[4])
        FirstN=Name1.split(" ")[0]
        LastN=Name1.split(" ")[-1]
        full_Name = str(resT[4]).replace(" " , "%20")
        if full_Name in UsersSet :
            continue
        UsersSet.add(full_Name)
        visitingProfileID = '/search/results/all/?keywords=' + full_Name + '&origin=GLOBAL_SEARCH_HEADER'
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        browser.get(fullLink)
        sleepFunc()
        src = browser.page_source
        soup = BeautifulSoup(src ,'lxml'  )
        res = soup.findAll('h3', {'class': 'search-results__total pt4 pb0 t-14 t-black--light t-normal pl5 clear-both'})
        if len(res) == 0 :
            out1 =  str(resT[0]) + "\n"
            f2.write(out1) 
            continue
        a1=str(res[0].contents[0])
        resNo = str(a1).replace("  ","").replace("\n" , "") 
        if resNo == "No results found.":
            out1 =  str(resT[0]) + "\n"
            f2.write(out1) 
            continue              
        MatchNum=int(a1.replace("  " , "").split(" ")[1].replace("," , ""))
        if ( MatchNum ==1  ) :
            titels = soup.findAll('p', {'class': 'subline-level-1 t-14 t-black t-normal search-result__truncate'})
            if len(titels) == 0 :
                out1 =  str(resT[0]) + "\n"
                f2.write(out1) 
                continue
            TitString=str(titels[0].contents).replace("  ","").replace("\\n" , "").replace("[" , "").replace("]" ,"").replace("'" , "")
            names = soup.findAll('span', {'class': 'name actor-name'})
            if len(names) == 0 :
                out1 =  str(resT[0]) + "\n"
                f2.write(out1) 
                continue
            namString = str(names[0].contents).replace("  ","").replace("\\n" , "").replace("[" , "").replace("]" ,"").replace("'" , "")
            places = soup.findAll('p', {'class': 'subline-level-2 t-12 t-black--light t-normal search-result__truncate'})
            plaString = str(places[0].contents).replace("  ","").replace("\\n" , "").replace("[" , "").replace("]" ,"").replace("'" , "")

            links = soup.findAll('a', {'class': 'search-result__result-link ember-view'})
            linString = str((links[0]).get('href')).replace("[" , "").replace("]" ,"").replace("'" , "")
            out1 = str(resT[0]) + " , " + linkedinBasePath + linString + " , " + TitString  + "\n"
            f1.write(out1) 
        else :
            country=str(resT[2]).replace("," , " ")           
            if country == "United States" :
                City = str(resT[1]).replace("," , " ")
                if City in d :
                    country = City
            if country in d :
                FiltSearch = d[country]
                #visitingProfileID = FiltSearch + full_Name + '&origin=GLOBAL_SEARCH_HEADER'
                visitingProfileID=FiltSearch + full_Name + '&firstName=' + FirstN + '&lastName=' + LastN + '&origin=GLOBAL_SEARCH_HEADER'
                fullLink = 'https://www.linkedin.com' + visitingProfileID 
                browser.get(fullLink)
                sleepFunc()
            src = browser.page_source
            soup = BeautifulSoup(src ,'lxml'  )
            res1 = soup.findAll('h3', {'class': 'search-results__total pt4 pb0 t-14 t-black--light t-normal pl5 clear-both'})
            if len(res1) == 0 or resNo == "No results found.":
                out0 =  str(resT[0]) + "\n"
                f2.write(out0) 
                continue
            a2=str(res[0].contents[0])
            resNo = str(a2).replace("  ","").replace("\n" , "")
            if resNo == "No results found.":
                out0 =  str(resT[0]) + "\n"
                f2.write(out0) 
                continue            
            MatchNum1=int(a2.replace("  " , "").split(" ")[1].replace("," , ""))
            if ( MatchNum1 > 10 ) :
                outM =  str(resT[0]) + ", " + str(MatchNum1) + " Matches \n"
                f3.write(outM) 
                continue
            names = soup.findAll('span', {'class': 'name actor-name'})
            i=-1
            L=-1
            titels = soup.findAll('p', {'class': 'subline-level-1 t-14 t-black t-normal search-result__truncate'})
            links = soup.findAll('a', {'class': 'search-result__result-link ember-view'})
            places = soup.findAll('p', {'class': 'subline-level-2 t-12 t-black--light t-normal search-result__truncate'})
            out1 = str(resT[0]) + " \n"
            f4.write(out1) 
            for na in  names :
                i=i+1
                L=L+1
                namString = str(na.contents).replace("  ","").replace("\\n" , "")
                TitString=str(titels[i].contents).replace("  ","").replace("\\n" , "")
                TitString2=TitString.replace("[" , "").replace("]" ,"").replace("'" , "")
                TitString1 =TitString2.replace("</span>", "").replace(", <span dir=\"ltr\">" , "")
                while "ivm-image-view-model ember-view" not in str(links[L]) :
                    L = L+1
                linString1 = str((links[L]).get('href')).replace("[" , "").replace("]" ,"").replace("'" , "")
                #print(linString1)
                out1 =linkedinBasePath + linString1 + " , " + TitString1  + "\n"
                f4.write(out1) 
            if len(names) == 1 :
                out1 = str(resT[0]) + " , " + linkedinBasePath + linString1 + " , " + TitString1  + "\n"
                f1.write(out1) 


if __name__ == '__main__':
    f2 = open("OutReports/RunRes.txt", "w" ,  encoding='utf-8')
    f2.write("Fail All")
    f2.close()
    fileLines = open("C:\\Users\\amir\\Desktop\\pyLib\\t2\\accounts.txt" , "r")
    for aline in fileLines:
        val = aline.split(",")
        username = val[0]
        password = val[1]
        for itr in range(0,3):
            f1 = open("OutReports/counter.txt", "r" ,  encoding='utf-8')
            counter =f1.readlines()
            f1.close()
            LIMIT = 100
            OFFSET = int(counter[0]) 
            results = Query(LIMIT , OFFSET)
            f = open("Us1.txt", "w" ,  encoding='utf-8')
            for res in results :
                print (res)
                f.write(str(res).replace("'" , "") + "\n")
            f.close()
            #exit()
            LinkedinCheck(results , username , password)
            f1 = open("OutReports/counter.txt", "w" ,  encoding='utf-8')
            NewCounter = int(counter[0]) + LIMIT
            f1.write(str(NewCounter))
            f1.close()
            sleepFuncMin()
        f2 = open("OutReports/RunRes.txt", "w" ,  encoding='utf-8')
        f2.write("Pass")
        f2.close()

        
