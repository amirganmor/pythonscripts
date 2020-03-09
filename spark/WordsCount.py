from pyspark import SparkContext , SparkConf
conf = SparkConf().setAppName("wordCount").setMaster("local[3]")
sc = SparkContext( conf = conf)
lines = sc.textFile("c1.txt")
words = lines.flatMap(lambda line: line.split(" "))
wordsCount = words.countByValue()
for word ,count in wordsCount.items() :
    print ("{} : {}".format(word,count)) 
