import psycopg2
import os, random, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import codecs
import random
import time
import pandas as pd

def sleepFunc() :
    a=random.randint(2, 6)
    print("sleep for " +  str(a) + " secs " )
    time.sleep(a)

def sleepFuncMin() :
    a=random.randint(1 , 3)
    a1 = int(a)*60
    print("sleep for " +  str(a1) + " secs " )
    time.sleep(a1)


def FaceCheck(SearchList) :
    #connect
    linkedinBasePath="https://www.facebook.com/groups/Elementors/members/"
    browser = webdriver.Chrome("C:\\Users\\amir\\Desktop\\pyLib\\chromedriver.exe")
    browser.get(linkedinBasePath)
    elementID = browser.find_element_by_id('email')
    username = "artur.pythonov"
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('pass')
    password = "elementor178"
    elementID.send_keys(password)
    try :
        elementID.submit()
    except:
        #submit no need
        amir=1
    ele = browser.find_elements_by_class_name("_58al")
    f1 = open(SearchList, "r" ,  encoding='utf-8')
    f2 = open("results/FaceMatches1.txt", "w" ,  encoding='utf-8')
    f3 =  open("results/FaceNoMatches1.txt", "w" ,  encoding='utf-8')
    for row in f1 :
        if row == "\n" :
            continue
        name = row.split(',')[1].replace("\"" ,"" )
        print (name)
        ele[0].send_keys(name)
        sleepFunc()
        src = browser.page_source
        soup = BeautifulSoup(src ,'lxml'  )
        NoRes= soup.findAll('div', {'class': '_327d'})
        if (len(NoRes) > 0 ) :
            #print(NoRes[0].contents[0])
            mm=10
            f3.write(row) 
        else :
            #s= soup.findAll('span', {'class': '_1oqv _50f8'})
            #numOfRes=str(s[2]).replace("<span class=\"_1oqv _50f8\">" , "").replace("</span>" , "").replace("\u200f" , "")
            #print(numOfRes)
            cc= soup.findAll('ul', {'class': 'uiList clearfix _5bbv _4kg _4ks'})
            #print(cc[0].contents[0].text)
            text = str(cc[0].contents[0].text)
            textFiltered = filterTxt(text)
            f2.write(name.replace("\n" , "").ljust(50) + textFiltered.ljust(50) + "\n")
        ele[0].send_keys(Keys.LEFT_CONTROL + "a")
        ele[0].send_keys(Keys.DELETE)

def filterTxt(text) : 
    tmp=text.split("month ago")
    if len(tmp) >1:
	    return tmp[1]   
    tmp11=str(tmp[0]).split("months ago")
    if len(tmp11) >1 :
	    return tmp11[1]
    tmp1=str(tmp11[0]).split("year ago")
    if len(tmp1) >1 :
	    return tmp1[1]
    tmp2=str(tmp1[0]).split("years ago")
    if len(tmp2) >1 :
	    return tmp2[1]    
    tmp3=str(tmp2[0]).split("2017")
    if len(tmp3) >1 :
	    return tmp3[1]   
    tmp4=str(tmp3[0]).split("2018")
    if len(tmp4) >1 :
	    return tmp4[1]
    tmp5=str(tmp4[0]).split("2016")
    if len(tmp5) >1 :
	    return tmp5[1]
    return "NA"

if __name__ == '__main__':
	SearchList="list1.csv"
	FaceCheck(SearchList)

        
