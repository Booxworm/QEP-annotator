from collections import deque

class QEPAnnotator:

    def __init__(self):
        self.qepHashMap = {}
        self.qepRes = []
    
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

    #Computing output string from query

    def computeOutputString(self, qep):
        #Getting queue and instantiating QEP annotator
        qepQueue = deque()
        
        self.qepTraversal(qep["Plan"], qepQueue)

        #Instantiating Parser class
        parser = Parser()
        final_output = ""
        steps = 1
        hashMap = self.getHashMap()
        for i in reversed(range(self.getHashMapLength())):
            length = i+1
            for j in range(len(hashMap[length])):
                if hashMap[length][j]["Node Type"] == "Seq Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.seq_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Hash":
                    final_output += "Step " + str(steps) + ": " +  parser.hash_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Hash Join":
                    final_output += "Step " + str(steps) + ": " +  parser.hash_join_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Aggregate":
                    final_output += "Step " + str(steps) + ": " +  parser.aggregate_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "CTE Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.cte_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Function Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.function_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Unrecognize":
                    final_output += "Step " + str(steps) + ": " +  parser.generic_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Group":
                    final_output += "Step " + str(steps) + ": " +  parser.group_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Index Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.index_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Index Only Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.index_only_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Limit":
                    final_output += "Step " + str(steps) + ": " +  parser.limit_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Materialize":
                    final_output += "Step " + str(steps) + ": " +  parser.materialize_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Merge Join":
                    final_output += "Step " + str(steps) + ": " +  parser.merge_join_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Nested Loop":
                    final_output += "Step " + str(steps) + ": " +  parser.nested_loop_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Sort":
                    final_output += "Step " + str(steps) + ": " +  parser.sort_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Subquery Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.subquery_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Unique":
                    final_output += "Step " + str(steps) + ": " +  parser.unique_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Values Scan":
                    final_output += "Step " + str(steps) + ": " +  parser.values_scan_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "SetOp":
                    final_output += "Step " + str(steps) + ": " +  parser.setop_parser(hashMap[length][j]) + "\n"
                elif hashMap[length][j]["Node Type"] == "Append":
                    final_output += "Step " + str(steps) + ": " +  parser.append_parser(hashMap[length][j]) + "\n"
                else:
                    final_output += "Step " + str(steps) + ": " + "The output will be based on its node type " + str(hashMap[length][j]["Node Type"]) + "." + "\n"
                steps+= 1

        

        return final_output

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
    Append Parser
    '''

    def append_parser(self, qep):
        outputString = "This node will perform the combination of its child nodes  "

        if "Plans" in qep:
            for child in qep["Plans"]:
                outputString += child["Node Type"] + ", "

            outputString = outputString[:-2]

        outputString += " into one result set"

        return outputString

    '''
    SetOp Parser
    '''
    def setop_parser(self, qep):
        outputString = "This node will perform SetOp Parsing. It finds the "

        cmd_name = str(qep["Command"])

        if cmd_name == "Except" or cmd_name == "Except All":
            outputString += "differences"
        
        else:
            outputString += "similarities"

        outputString += " between the two previously scanned tables using the " + qep["Node Type"] + " operation."

        return outputString

    '''
    Aggregate Parser
    '''
    def aggregate_parser(self, qep):
        outputString = ""

        if qep["Strategy"]  == "Sorted":
            outputString = "This node performs an aggregate based on sorting. "
            if "Group Key" in qep:
                tempString = "The result is grouped by "
                for groupKey in qep["Group Key"]:
                    tempString += groupKey + ", "
            
                tempString = tempString[:-2] + ". "

            outputString += tempString

            if "Filter" in qep:
                outputString += "It will be bounded by the condition " + qep["Filter"] + ". "
            
            return outputString


        if qep["Strategy"] == "Hashed":
            outputString = "This node performs an aggregate based on hashing. "
            
            if len(qep["Group Key"]) == 1:
                tempString = "It will hash all the rows based on the key "
                tempString += qep["Group Key"][0] + ". "
                
                outputString += tempString

            else:
                tempString = "It hashes all the rows based on the keys "
                for key in qep["Group Key"]:
                    tempString += key + ", "
                
                tempString += "and finally returns the desired row after manipulation. "
            
                outputString += tempString

                return outputString
        
        if qep["Strategy"] == "Plain":
            outputString = "The result will be aggregated based on a " + qep["Node Type"] + " function. "


            return outputString

    '''
    CTE Scan Parser
    '''

    def cte_scan_parser(self, qep):
        outputString = "This node will perform a CTE scan through the table "

        outputString += str(qep["CTE Name"]) + " which will be stored in memory."

        if "Index Cond" in qep:
            outputString += "This scan will be applied with the condition(s) "+ qep["Index Cond"] + ". "

        if "Filter" in qep:
            outputString += "The results will finally be filtered by " + qep["Filter"] + ". "
        
        return outputString


    '''
    Function Scan Parser
    '''

    def function_scan_parser(self, qep):
        outputString = "This node will perform a function scan by running the function " + qep["Function Name"] + " and returns the records that were created by it. "
        return outputString


    '''
    Generic Parser
    '''

    def generic_parser(self, qep):
        outputString = "The node type here is " + qep["Node Type"] + ". "
        outputString = "This node will perform a function with its children nodes. "
        tempString = ""
        if "Plans" in qep:
            tempString = "It will make use of its children nodes "
            for child in qep["Plans"]:
                tempString += child["Node Type"]

        if len(tempString) <1:
            return outputString
        else:
            outputString += tempString + ". "


    '''
    Group Parser
    '''

    def group_parser(self, qep):
        outputString = "This node will perform a grouping based on "
        tempString = ""
        if len(qep["Group Key"]) == 1:
            tempString = "the  key" + qep["Group Key"][0] + "."
        
        else:
            tempString = "the keys "
            for key in qep["Group Key"][:-1]:
                tempString += key + ", "
            
            tempString = tempString[:-2] + "."

        outputString += tempString

        return outputString


    '''
    Index Scan Parser
    '''

    def index_scan_parser(self, qep):
        outputString = "This node performs an index scan. "
        
        tempString = "It performs the index scan by using an index table " + qep["Index Name"] + ". "
        if "Index Cond" in qep:
            tempString += "The scan will be applied with the condition " + qep["Index Cond"] + ". "
    
        tempString += "It opens up the relation " + qep["Relation Name"] + "and fetches rows pointed to the index matched in the scan. "
    
        if "Filter" in qep:
            tempString += "The result of this scan will then be filtered by " + qep["Filter"] + ". "
        
        outputString += tempString

        return outputString

    
    '''
    Index Only Scan Parser
    '''
    def index_only_scan_parser(self, qep):
        outputString = "This node performs an index only scan. "
        tempString = ""
        if "Index Cond" in qep:
            tempString += "The scan will be applied with the condition " + qep["Index Cond"] + ". "
        
        outputString += tempString + "It will then return the matches found in index table as the result"

        if "Filter" in qep:
            outputString += "The result will then be filtered by " + qep["Filter"] + ". "

        return outputString



    '''
    Limit Parser
    '''
    def limit_parser(self, qep):
        outputString = "This node will perform a limit scan on the relation " + qep['Relation Name'] + ". "
        outputString += "However, instead of scanning the entire table, it only does so with a limit of " + str(qep["Plan Rows"]) + "entries. "

        return outputString



    '''
    Materialize Parser (think again)
    '''
    def materialize_parser(self, qep):
        outputString = "This node is performs materialization. This will "

    '''
    Merge Join Parser
    '''
    def merge_join_parser(self, qep):

        outputString = "This node will perform a merge join."
        

        if "Plans" in qep:
            tempString = "The children of this nodes that will be considered in merge join are the relation"
            for child in qep["Plans"]:
                if "Relation Name" in child:
                    tempString += child["Relation Name"] + ", "
            
            tempString = tempString[:-2]

            outputString += tempString

        if "Merge Cond" in qep:
            outputString +=  "The result will be bounded by the condition " + qep["Merge Cond"] + ". "
        
        if "Join Type" == 'Semi':
            outputString += "However, when projecting results, only the rows fro mthe left relation are returned"
        
        return outputString
    


    '''
    Nested Loop Parser
    '''

    def nested_loop_parser(self, qep):
        outputString = "This node performs a nested loop scan on the relations "

        planOne = qep["Plans"][0]
        planTwo =  qep["Plans"][1]

        outputString += planOne["Relation Name"] + "and "

        outputString += planTwo["Relation Name"] + ". "

        outputString += "The join result between both scan results are then returned as new rows."

        return outputString


    '''
    SetOp Parser
    '''

    def setOp_parser(self, qep):
        return 

    '''
    Sort Parser 
    ''' 

    def sort_parser(self, qep):
        
        outputString = "This node performs sorting by using attribute "
        if "DESC" in qep["Sort Key"]:
            outputString += qep["Sort Key"] + "in descending order."
        elif "INC" in qep["Sort Key"]:
            outputString += qep["Sort Key"] + "in ascending order."
        else:
            outputString += qep["Sort Key"] + "."

        return outputString

    '''
    Subquery Scan Parser
    '''

    def subquery_scan_parser(self, qep):
        outputString = "This node performs a subquery scan of relation " + qep["Plans"][0]["Relation Name"] + ". "

        return outputString


    '''
    Unique Parser
    '''
    def unique_parser(self, qep):
        outputString = "This node will extract the unique values from the table based on attribute" + qep["Plans"][0]["Sort Key"] + ". "
        return outputString


    '''
    Values Scan Parser
    '''

    def values_scan_parser(self, qep):
        outputString = "This node will scan through the given values from the query "

        return outputString
# Test

if __name__ == "__main__":

    qepAnnotator = QEPAnnotator()
    print(qepAnnotator.computeOutputString())
    

'''
select *
from customer C,
orders O
where C.c_custkey =
O.o_custkey;



max
select max(p_retailprice)
from part
'''
