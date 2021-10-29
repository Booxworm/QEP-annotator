import preprocessing

qepGraph = preprocessing.QepGraph()

pw = input("Please enter password for postgres: ")
dbms = preprocessing.DBMS(pw)

query = dbms.getQuery()

# for row in dbms.executeQuery(query):
#     print(row)

qep = dbms.explainQuery(query)

qepGraph.createQepGraph(qep)


print("Operation done successfully")