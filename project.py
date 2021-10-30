from psycopg2 import connect
import interface
import preprocessing

qepGraph = preprocessing.QepGraph()
dbms = preprocessing.DBMS()

pw = input('Please enter password for postgres: ')
connected = dbms.connect(password=pw)
while not connected:
    pw = input('Please enter password again: ')
    connected = dbms.connect(password=pw)

app = interface.App(dbms, qepGraph)
app.mainloop()

# import preprocessing

# qepGraph = preprocessing.QepGraph()

# pw = input("Please enter password for postgres: ")
# dbms = preprocessing.DBMS(pw)

# query = dbms.getQuery()

# # for row in dbms.executeQuery(query):
# #     print(row)

# qep = dbms.explainQuery(query)

# qepGraph.createQepGraph(qep)


# print("Operation done successfully")