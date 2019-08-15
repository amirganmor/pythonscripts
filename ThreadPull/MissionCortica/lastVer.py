import threading
import time
import logging
import glob
import shutil
import os
import sys


#global vars
numOfThreads=3
lock = threading.Lock() 
goodLibs=True


#Tread Pool class 
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)

#help func for thread pool class to check intersections
def f(s, pool,A,B,C,X):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        #time.sleep(0.5)
        CheckSim(A,B,C,X)
        pool.makeInactive(name)

#help func for thread pool class to check each file validity
def f2(s, pool,File):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        #time.sleep(0.5)
        VerifyDirsNnums2(File)
        pool.makeInactive(name)


#check similarities func
def CheckSim(A,B,C,X):  
  eqAmount = int(X)
  f1 = open(A, "r")
  a=f1.read().split(",")
  lenA=len(a) 
  if lenA < X:
    return
  for ff in glob.glob(B + "*.csv") :
    f2 = open(ff, "r")
    b=f2.read().split(",")
    lenB=len(b)
    if lenB < X:
        continue
    indexA=0
    indexB=0
    MatchCount =0
    while indexA  < lenA  and indexB   < lenB : 
        if int(a[indexA]) == int(b[indexB]) :
            MatchCount = MatchCount + 1
            indexA= indexA + 1
            indexB= indexB+ 1
        elif int(a[indexA]) > int(b[indexB]) :
            indexB= indexB+ 1
        else :
            indexA= indexA+ 1   
    if MatchCount >= eqAmount : 
        #print(ff)
        shutil.copy(ff, C)
        thread_scores(ff ,MatchCount )
        break
    
      
#check inputs dirs and Min Amount num are valid + earse ild content
def VerifyDirsNnums(A , B , C , X ):  
    goodLib=True
    if not os.path.exists(A):
        print ("-E- input Lib A :" + A + "\nis not exists , exit from program")
        return False
    if not os.path.exists(B):
        print ("-E- input Lib A :" + B + "\nis not exists , exit from program")
        return  False
    if not os.path.exists(C):
        print ("-E- input Lib A :" + C + "\nis not exists , exit from program")
        return False
    #remove old content in C
    files1 = glob.glob(C + "*")
    for fff in files1:
        os.remove(fff)
    #check  minimal amount of equal numbers
    try:
        valX = int(X)
    except ValueError:
        print("-E- input minimal amount of equal numbers x : " + str(X)  +"\nis not an Integer. It's a string , exit from program")
        return  False
    return goodLib

#check for each csv file in A and B dirs Validity (one int seperate in commas , in Ascending order )
def VerifyDirsNnums2( file ): 
        global goodLibs
        f1 = open(file, "r")
        lastNum=0
        for num in f1.read().split(",") :
            try:
                valNum = int(num)
            except ValueError:
                goodLibs=False
                msg = "-E- input  : " + str(num)  + "at file : " + str(file) + "\nis not an Integer ,please fix.. exit from program"
                Lib_ErrMsg(msg)
                break
            if valNum < lastNum :
                goodLibs=False
                msg ="-E- At file  : " + file  + " Numbers are not sorted! " + "\n please fix.. exit from program"
                Lib_ErrMsg(msg)
                break
            lastNum=valNum
        return goodLibs

#the "heart" of the program handles, in multi-threading, the loading, “similarity” testing and copying of files 
def MainFunc(A,B,C,X):
    CheckInParams = VerifyDirsNnums(A,B,C,X )
    if not (CheckInParams): 
        print("Error In Input dirs or Min Num , please fix , look at the errior messages!")
        sys.exit(0)
    pool = ThreadPool()
    s = threading.Semaphore(numOfThreads)
    threads = []
    i=0
    arr = [A , B]
    for dir in arr :
        for ff in glob.glob(dir + "*.csv") :
            t = threading.Thread(target=f2, name='thread_'+str(i), args=(s, pool,ff))
            i=i+1       
            threads.append(t)  
            t.start()
    for x in threads:
        x.join()
    if not (goodLibs): 
        print("Error In Input dirs or Min Num , please fix , look at the errior messages!")
        sys.exit(0)
    print("input dir , min num , and its content are valid start main program")
    scoresFie = C + "\\" +"scores.txt"
    global fFin
    fFin = open(scoresFie, 'w')
    pool = ThreadPool()
    s = threading.Semaphore(numOfThreads)
    i=0
    threads = []
    for ff in glob.glob(A + "*.csv") :
        t = threading.Thread(target=f, name='thread_'+str(i), args=(s, pool,ff,B,C,X))
        i=i+1       
        threads.append(t)  
        t.start()

    for x in threads:
        x.join()
    print ("All  threads are finished")
    fFin.close()   


#help func for scores.txt (use of locks)
def thread_scores(file , intersections):
    phrase = str(file) + "   " +str(intersections)
    lock.acquire()
    fFin.write(phrase + "\n")
    lock.release()
#help func Err messages (use of locks)
def Lib_ErrMsg(msg):
    lock.acquire()
    print (msg)
    lock.release()




#main
if __name__ == '__main__':
    #set the libs and minimal amount of equal numbers -A,B,C,X
    A="C:\\try\\t1\\"
    B="C:\\try\\t2\\"
    C="C:\\try\\t3\\"
    X=5
    #run
    MainFunc(A,B,C,X)

    
    
    
