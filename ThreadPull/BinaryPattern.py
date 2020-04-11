import re
import base64
import multiprocessing
import time
import os
import shutil
import sys

#global vars :
threashold = 4
numOfProcesses = int(multiprocessing.cpu_count())

#help func to "shape" the json file
def truncate_utf8_chars(filename, count, ignore_newlines=True):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1

#sigle search  - input 1 file path , 2 exprssion to serach in the file which repeat itself abobe threashold
#output is list which each element contains number of repeatation and there place in the file
def singleSearch (InFile , expression ) :
    #stage1 - replace a with " "
    returnList = []
    with open(InFile, "rb") as imageFile:
         f = base64.b16encode(imageFile.read())
    d= str(f).replace(expression , " ")
    #stage2 - 2 lists , one of words one of " "
    tokens = re.findall('\s+', d)
    words=d.split()
    total = 0
    #stage3 - loop throgh those 2 lists and report
    for i in range(0, len(tokens)) :
        total += len(words[i]) 
        if len(tokens[i]) >= threashold :
            #print(len(tokens[i]))
            returnList.append(str(total -1 ) + " " + str(len(tokens[i])) )
            #print("place : " + str(total -1 ))
        total += len(tokens[i]) 
    return returnList

#procces run , inputs - 1.dictionary to run , 2- process number , 3 - path to file
#for each process - write info file- which later will be merge with the other processes files
def Jobfunc(dict1 , jobnum , InFile ) :
    outfile = "RunResults/tmpfile_" + str(jobnum) + ".txt"
    f2 = open(outfile, "w" ,  encoding='utf-8')
    for key, value in dict1.items():
        tmpList = singleSearch(InFile ,key  )
        for out in tmpList :
            out1=out.split()
            line = "\t {'range': (" + str(out1[0]) + ", " + str(int(out1[0]) + int(out1[1])) + ") , \'size\': " + str(int(out1[1])) + ", \'repeating_Hex\': " + str(key) + "}"
            f2.write(line + ",\n")
    f2.close()

#Main function - 3input parmeters : 1.file path 2 dictionary of hexadecimal strings/regExp 3.dictionary of Extra arguments
#merge the two dictionaries and spread the run into difrrents processes , 
#merge all results into ajson output file
def MainFunc (InFile , InDict , ExtraArgs) :
    #merge the two dictiionaries
    mergedDict = InDict.copy()   
    mergedDict.update(ExtraArgs)
    #calcilate the number of searches per core/process
    jump = len(mergedDict) / numOfProcesses
    carriage =  len(mergedDict) % numOfProcesses
    pool = multiprocessing.Pool()
    count = 0
    for x in range(0, numOfProcesses):
        if carriage > 0 :
            R=1
            carriage-=1
        else :
            R=0
        tot = round(R+jump)
        if tot < 1 :
            break
        #need to split the dict
        d= dict(list(mergedDict.items())[count:count+tot])
        pool.apply_async(Jobfunc , [ d, x , InFile  ])
        count = count + tot
    pool.close()
    pool.join()
    filenames = os.listdir("RunResults")
    with open('RunResults/OutFile.json', 'w') as outfile:
        outfile.write("{results: [\n ")
        for fname in filenames:
            fname1 = "RunResults/" + fname
            with open(fname1) as infile:
                outfile.write(infile.read())
    truncate_utf8_chars('RunResults/OutFile.json', 1)
    with open('RunResults/OutFile.json', 'a') as outfile:
        outfile.write("\n]}")

#main  delete privious run outputs , set parameters for current run and call to the main functions with the 
# 3input parmeters : 1.file path 2 dictionary of hexadecimal strings/regExp 3.dictionary of Extra arguments
# ant the end prints the total runtime 
if __name__ == '__main__':
    start_time = time.time()
    #remove last run results
    try :
        shutil.rmtree("RunResults", ignore_errors=False, onerror=None )
    except OSError as ex:
        doNothing=1
    try :
        os.mkdir("RunResults")
    except OSError as ex:
        doNothing=1
    
    #set the input parameters
    inFile = "C:\\Users\\amir\\Desktop\\pyLib\\a.img"
    inDict={"0" : "zero" ,  "1" :"one" ,"2" : "two" , "3" : "three" , "4" : "four" , "5" : "five" , "6" : "six" , "7" : "seven" , "8" : "eight" , "9" : "nine"}
    ExtraArgs= {"A" : "ten" , "B" : "eleven" , "C" : "twelve" , "D" : "fourten" , "E" : "fifteen" , "F" : "sixteen"}
    #call main fun
    MainFunc (inFile , inDict , ExtraArgs)
    print("total runtime : --- %s seconds ---" % (time.time() - start_time))
  


