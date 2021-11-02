from typing import final
import preprocessing
from collections import defaultdict, deque

class QEPAnnotator:

    def __init__(self):
        self.qepHashMap = {}
        self.qepRes = []
        self.outputString = ""

    def getOutputString(self):
        return self.outputString
    
    def setOutputString(self, _string):
        self.outputString = _string
    
    def getHashMap(self):
        return self.qepHashMap
    
    def getQepRes(self):
        return self.qepRes

    def getHashMapLength(self):
        count = 0
        for key in self.qepHashMap.keys():
            count += 1
        return count

    #Parsing the QEP data
    def qepTraversal(self, qep, qepQueue):
        level = 1
        qepQueue.append((qep, level))

        while qepQueue:
            temp = qepQueue.popleft()
            self.qepRes.append((temp[0]["Node Type"], level))
            
            if temp[1] in self.qepHashMap:
                self.qepHashMap[temp[1]].append(temp[0])
            else:
                self.qepHashMap[temp[1]] = [temp[0]]

            if "Plans" in temp[0]:
                level += 1
                for eachPlans in temp[0]["Plans"]:
                    qepQueue.append((eachPlans, level))


# Traversal is done. Now to parse the JSON

class Parser:

    '''
    Hash Join Parser
    '''
    def hash_join_parser(self, qep):
        outputString = "This node will perform a hash join on relation " 

        planOne = qep["Plans"][0]
        planTwo = qep["Plans"][1]


        if planOne["Node Type"] == "Hash":
            tempString = planOne["Plans"][0]["Relation Name"]
            outputString += tempString
        else:
            tempString = planOne["Relation Name"]
            outputString += tempString
        
        if planTwo["Node Type"] == "Hash":
            tempString = " and relation " + planTwo["Plans"][0]["Relation Name"] + ". "
            outputString += tempString
        else:
            tempString = " and relation " + planTwo["Relation Name"] + ". "
            outputString += tempString


        if "Hash Cond" in qep:
            tempString = "This join will be under the condition of " + qep["Hash Cond"] + " to get the final result."
            outputString += tempString

        return outputString

    '''
    Sequential Scan Parser
    '''
    def seq_scan_parser(self, qep):
        outputString = "This node will perform a sequential scan on relation "

        if "Relation Name" in qep:
            tempString = qep["Relation Name"] + ". "
            outputString += tempString

        if "Alias" in qep:
            tempString = "The alias of this relation is known as " + qep["Alias"] + ". "
            outputString += tempString

        if "Filter" in qep:
            tempString = "The sequential scan will be bounded by the condition " + qep["Filter"] + ". "
            outputString += tempString        
        
        return outputString


    '''
    Hash Parser
    '''
    def hash_parser(self, qep):
        outputString = "This node will perform utilization of hash memory with rows from the relation " + qep["Plans"][0]["Relation Name"] + ". "

        return outputString

    '''

    '''

    


# Test

if __name__ == "__main__":
    dbms = preprocessing.DBMS()

    pw = input('Please enter password for postgres: ')
    connected = dbms.connect(password=pw)
    while not connected:
        pw = input('Please enter password again: ')
        connected = dbms.connect(password=pw)

    #Get the query input
    query = dbms.getQuery()

    #Explain the query in the form of JSON format
    qep = dbms.explainQuery(query)
    print("This is the qep")
    print(qep)


    #Creating queue and result to return order
    qepQueue = deque()
    qepAnnotator = QEPAnnotator()

    qepAnnotator.qepTraversal(qep["Plan"], qepQueue)
    print(qepAnnotator.getQepRes())
    print("This is the hashMap")

    print(qepAnnotator.getHashMap())
    print("###########################")

    #Testing Parser

    parser = Parser()
    final_output = ""
    steps = 1
    hashMap = qepAnnotator.getHashMap()
    for i in reversed(range(qepAnnotator.getHashMapLength())):
        length = i+1
        for j in range(len(hashMap[length])):
            if hashMap[length][j]["Node Type"] == "Seq Scan":
                final_output += "Step " + str(steps) + ": " +  parser.seq_scan_parser(hashMap[length][j]) + "\n"
            if hashMap[length][j]["Node Type"] == "Hash":
                final_output += "Step " + str(steps) + ": " +  parser.hash_parser(hashMap[length][j]) + "\n"
            if hashMap[length][j]["Node Type"] == "Hash Join":
                final_output += "Step " + str(steps) + ": " +  parser.hash_join_parser(hashMap[length][j]) + "\n"
            steps+= 1


    #Set output string for qep Annotator

    qepAnnotator.setOutputString(final_output)

    print(qepAnnotator.getOutputString())

'''
select *
from customer C,
orders O
where C.c_custkey =
O.o_custkey;
'''
