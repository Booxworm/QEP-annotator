import tkinter as tk
from tkinter.constants import E
import preprocessing
import annotate
from functools import partial

from PIL import ImageTk, Image

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dbms = preprocessing.DBMS()
        self.qepAnnotator = annotate.QEPAnnotator()
        self.qepGraph = preprocessing.QepGraph()

        self.title('Group 40 QEP Annotator')
        self.geometry("1200x800")
        self['background'] = '#62c2da'

        self.loginWindow()

    def loginWindow(self):

        title = tk.Label(self, text='Login')
        title.pack(pady=50)
        title['background'] = '#62c2da'
        title.config(font=('Helvetica bold', 20, "bold"))

        topFrame = tk.Frame(self)
        topFrame.pack(pady=20)
        topFrame['background'] = '#62c2da'

        bottomFrame = tk.Frame(self)
        bottomFrame.pack()
        bottomFrame['background'] = '#62c2da'

        # database label and text entry box
        databaseLabel = tk.Label(topFrame, text='Database')
        databaseLabel.grid(row=0, column=0)
        databaseLabel.config(font=('Helvetica bold', 14, "bold"))
        databaseLabel['background'] = '#62c2da'
        database = tk.StringVar(value='TPC-H')
        databaseEntry = tk.Entry(topFrame, textvariable=database)
        databaseEntry.grid(row=0, column=1, padx=20)
        databaseEntry.config(font=('Helvetica bold', 14))

        # user label and text entry box
        userLabel = tk.Label(topFrame, text='User')
        userLabel.grid(row=1, column=0)
        userLabel.config(font=('Helvetica bold', 14, "bold"))
        userLabel['background'] = '#62c2da'
        user = tk.StringVar(value='postgres')
        userEntry = tk.Entry(topFrame, textvariable=user)
        userEntry.grid(row=1, column=1, padx=20)
        userEntry.config(font=('Helvetica bold', 14))

        # password label and password entry box
        passwordLabel = tk.Label(topFrame,text='Password')
        passwordLabel.grid(row=2, column=0)
        passwordLabel.config(font=('Helvetica bold', 14, "bold"))
        passwordLabel['background'] = '#62c2da'
        password = tk.StringVar()
        passwordEntry = tk.Entry(topFrame, textvariable=password, show='*')
        passwordEntry.grid(row=2, column=1, padx=20)
        passwordEntry.config(font=('Helvetica bold', 14))

        # host label and text entry box
        hostLabel = tk.Label(topFrame, text='Host')
        hostLabel.grid(row=3, column=0)
        hostLabel.config(font=('Helvetica bold', 14, "bold"))
        hostLabel['background'] = '#62c2da'
        host = tk.StringVar(value='localhost')
        hostEntry = tk.Entry(topFrame, textvariable=host)
        hostEntry.grid(row=3, column=1, padx=20)
        hostEntry.config(font=('Helvetica bold', 14))

        # port label and text entry box
        portLabel = tk.Label(topFrame, text='Port')
        portLabel.grid(row=4, column=0)
        portLabel.config(font=('Helvetica bold', 14, "bold"))
        portLabel['background'] = '#62c2da'
        port = tk.StringVar(value='5432')
        portEntry = tk.Entry(topFrame, textvariable=port)
        portEntry.grid(row=4, column=1, padx=20)
        portEntry.config(font=('Helvetica bold', 14))

        validateLogin = partial(self.validateLogin, database, user, password, host, port)

        #login button
        loginButton = tk.Button(bottomFrame, text='Login', command=validateLogin, foreground = 'white', background='#063970', height = 2, width = 20)
        loginButton.grid(row=0, column=0)
        loginButton.config(font=('Calibri', 14, "bold"))
        self.errorMsg = tk.Label(bottomFrame, text='Failed to connect to database', fg='#f00')
        self.errorMsg.grid(row=1, column=0)
        self.errorMsg.config(font=('Helvetica bold', 14, "bold"))
        self.errorMsg['background'] = '#62c2da'
        self.errorMsg.grid_forget()

    def mainWindow(self):
        topFrame = tk.Frame(self)
        topFrame.pack()
        topFrame['background'] = '#62c2da'

        bottomFrame = tk.Frame(self)
        bottomFrame.pack()
        bottomFrame['background'] = '#62c2da'

        ##############################
        # Frame for Application Name #
        ##############################

        # Frame widget for application name
        nameFrame = tk.Frame(master=topFrame)
        nameFrame.pack(side=tk.TOP)
        nameFrame['background'] = '#62c2da'

        # Label widget for application name
        nameLabel = tk.Label(master=nameFrame, text = 'Group 40 QEP Annotator')
        nameLabel.config(font=('Helvetica bold', 20, "bold"))
        nameLabel.pack()
        nameLabel['background'] = '#62c2da'


        ############################
        # Frame for entering query #
        ############################

        # Frame widget for query
        queryFrame = tk.Frame(master=topFrame)
        queryFrame.pack(side=tk.LEFT)
        queryFrame['background'] = '#62c2da'

        # Text widget to enter query
        self.queryText = tk.Text(master=queryFrame, width=40, height=10, borderwidth=4, relief="solid")
        self.queryText.pack(padx=20, pady=5)
        self.queryText.config(font=('Helvetica bold', 14))


        # Label widget for query
        queryLabel = tk.Label(master=queryFrame, text='Query')
        queryLabel.pack()
        queryLabel['background'] = '#62c2da'
        queryLabel.config(font=('Helvetica bold', 14, "bold"))

        # #####################
        # # Frame for buttons #
        # #####################

        # # Frame widget for buttons
        # buttonFrame = tk.Frame(master=topFrame)
        # buttonFrame.pack(side=tk.LEFT)
        # buttonFrame['background'] = '#62c2da'
    

        # # Button widget to submit query
        # submitQueryButton = tk.Button(master=buttonFrame, text='Input Query', command=self.processQuery, foreground = 'white', height = 2, width = 20)
        # submitQueryButton.pack(pady=5)
        # submitQueryButton['background'] = '#063970'
        # submitQueryButton.config(font=('Calibri', 14, "bold"))

        # # Button widget to clear query
        # clearQueryButton = tk.Button(master=buttonFrame, text='Clear', command=self.clearQuery, foreground = 'white', height = 2, width = 20)
        # clearQueryButton.pack(pady=5)
        # clearQueryButton['background'] = '#063970'
        # clearQueryButton.config(font=('Calibri', 14, "bold"))

        ###################################
        # Frame for displaying annotation #
        ###################################

        annotationFrame = tk.Frame(master=topFrame)
        annotationFrame.pack(side=tk.LEFT)
        annotationFrame['background'] = '#62c2da'

        # Text widget to enter query
        self.annotationText = tk.Text(master=annotationFrame, state=tk.DISABLED, width=60, height=10, borderwidth=4, relief="solid")
        self.annotationText.pack(padx=20, pady=5)
        self.annotationText.config(font=('Helvetica bold', 14))

        annotationLabel = tk.Label(master=annotationFrame, text='Annotation')
        annotationLabel.pack()
        annotationLabel['background'] = '#62c2da'
        annotationLabel.config(font=('Helvetica bold', 14, "bold"))

        #############################
        # Frame for Database Schema #
        #############################
        schemaFrame = tk.Frame(master=bottomFrame)
        schemaFrame.pack(side=tk.LEFT)
        schemaFrame['background'] = '#62c2da'


        # Button widget to submit query
        submitQueryButton = tk.Button(master=schemaFrame, text='Submit Query', command=self.processQuery, foreground = 'white', height = 2, width = 20)
        submitQueryButton.pack(pady=5)
        submitQueryButton['background'] = '#063970'
        submitQueryButton.config(font=('Calibri', 14, "bold"))

        # Button widget to clear query
        clearQueryButton = tk.Button(master=schemaFrame, text='Clear', command=self.clearQuery, foreground = 'white', height = 2, width = 20)
        clearQueryButton.pack(pady=5)
        clearQueryButton['background'] = '#063970'
        clearQueryButton.config(font=('Calibri', 14, "bold"))

        # Button widget to open database schema window
        schemaButton = tk.Button(master=schemaFrame, text='Database Schema', command=self.goToSchema, foreground = 'white', height = 2, width = 20)
        schemaButton.pack(pady=5)
        schemaButton['background'] = '#063970'
        schemaButton.config(font=('Calibri', 14, "bold"))

        #############################
        # Frame for displaying tree #
        #############################

        treeFrame = tk.Frame(master=bottomFrame)
        treeFrame.pack(side=tk.LEFT)
        treeFrame['background'] = '#62c2da'

        treeLabel = tk.Label(master=treeFrame, text='Physical Query Plan')
        treeLabel.pack(side=tk.BOTTOM)
        treeLabel['background'] = '#62c2da'
        treeLabel.config(font=('Helvetica bold', 14, "bold"))

        self.treeCanvas = tk.Canvas(treeFrame, width=700, height=500, borderwidth=4, relief="solid", highlightthickness=0)  
        self.treeCanvas.pack(pady=5, padx=15)

        self.img = ImageTk.PhotoImage(Image.open("images/blank.png"))  
        self.treeCanvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Invisible frame for alignment
        invisibleFrame = tk.Frame(master=bottomFrame)
        invisibleFrame.pack(side=tk.LEFT)
        invisibleFrame['background'] = '#62c2da'

        # Invisible label to align treeFrame to center
        invisibleLabel = tk.Label(master=invisibleFrame, text='', foreground = 'white', height = 2, width = 20)
        invisibleLabel.pack(padx=30)
        invisibleLabel['background'] = '#62c2da'
    
    def schemaWindow(self):

        ###################
        # Frame for title #
        ###################

        # Frame widget for title
        nameFrame = tk.Frame(self)
        nameFrame.pack(side=tk.TOP)
        nameFrame['background'] = '#62c2da'

        # Label widget for title
        nameLabel = tk.Label(master=nameFrame, text = 'Database Schema')
        nameLabel.config(font=('Helvetica bold', 20, "bold"))
        nameLabel.pack()
        nameLabel['background'] = '#62c2da'

        topFrame = tk.Frame(self)
        topFrame.pack(side=tk.TOP, pady=20)
        topFrame['background'] = '#62c2da'

        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=tk.LEFT, anchor=tk.W)
        bottomFrame['background'] = '#62c2da'

        #############################
        # Frame for database schema #
        #############################
        schemaFrame = tk.Frame(master=topFrame)
        schemaFrame.pack(side=tk.LEFT)
        schemaFrame['background'] = '#62c2da'
        schemaFrame.pack()

        tables = self.dbms.getTables()

        tableFrame = tk.Frame(schemaFrame)
        tableFrame.grid(row=0, column=0)
        tableFrame['background'] = '#62c2da'
        
        columnFrame = tk.Frame(schemaFrame, highlightthickness=1, highlightcolor='black')
        columnFrame.grid(row=0, column=1, padx=10)

        columnText = tk.Text(columnFrame, state=tk.DISABLED, width=50, height=28, borderwidth=4, relief="solid")
        columnText.pack()
        columnText['background'] = '#62c2da'
        columnText.config(font=('Helvetica bold', 14, "bold"))

        for i in range(len(tables)):
            buttonFunc = partial(self.displaySchema, columnText, tables[i])
            button = tk.Button(tableFrame, text=tables[i], command=buttonFunc, foreground = 'white', height = 2, width = 20)
            button.grid(row=i, column=0, pady=5)
            button['background'] = '#063970'
            button.config(font=('Helvetica bold', 14, "bold"))

        ####################
        # Frame for button #
        ####################
        schemaFrame = tk.Frame(master=bottomFrame)
        schemaFrame.pack(side=tk.LEFT, anchor='s')
        schemaFrame['background'] = '#62c2da'

        # Button widget to open main window
        schemaButton = tk.Button(master=schemaFrame, text='Back', command=self.goToMain, foreground = 'white', height = 2, width = 20)
        schemaButton.pack(padx=10)
        schemaButton['background'] = '#063970'
        schemaButton.config(font=('Calibri', 14, "bold"))

    def validateLogin(self, database, user, password, host, port):
        connected = self.dbms.connect(
            database=database.get(),
            user=user.get(),
            password=password.get(),
            host=host.get(), 
            port=port.get()
        )

        if connected:
            self.goToMain()
        else:
            self.errorMsg.grid()

    def processQuery(self):
        # Get query
        error =  None
        try:
            query = ' '.join((self.queryText.get(1.0, tk.END)).split('\n'))
            result = self.dbms.explainQuery(query)
        except Exception as e:
            error = e
            print(e)

        if error:
            self.annotationText.configure(state=tk.NORMAL, fg='red')
            self.annotationText.delete(1.0, tk.END)
            self.annotationText.insert(tk.END, error)
            self.annotationText.configure(state=tk.DISABLED)
        else:
            # Update annotation
            self.qepAnnotator = annotate.QEPAnnotator()
            annotation = self.qepAnnotator.computeOutputString(result)

            self.annotationText.configure(state=tk.NORMAL, fg='black')
            self.annotationText.delete(1.0, tk.END)
            self.annotationText.insert(tk.END, annotation)
            self.annotationText.configure(state=tk.DISABLED)

            # Update tree
            self.qepGraph.createQepGraph(result)
            self.img = ImageTk.PhotoImage(Image.open("images/qep.png"))  
            self.treeCanvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def clearQuery(self):
        self.queryText.delete(1.0, tk.END)

        self.annotationText.configure(state=tk.NORMAL)
        self.annotationText.delete(1.0, tk.END)
        self.annotationText.configure(state=tk.DISABLED)
        
        self.img = ImageTk.PhotoImage(Image.open("images/blank.png"))  
        self.treeCanvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def goToMain(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.mainWindow()

    def goToSchema(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        self.schemaWindow()
    
    def displaySchema(self, textWidget, table):
        columns = self.dbms.getColumns(table)
        stringColumns = '\n'.join(columns)

        textWidget.configure(state=tk.NORMAL)
        textWidget.delete(1.0, tk.END)
        textWidget.insert(tk.END, stringColumns)
        textWidget.configure(state=tk.DISABLED)
