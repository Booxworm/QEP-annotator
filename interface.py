import tkinter as tk
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
        self.loginWindow()
        self['background'] = '#62c2da'

    def loginWindow(self):
        #window
        # tkWindow = tk.Tk()  
        self.geometry('400x150')
        self.title('Tkinter Login Form')

        topFrame = tk.Frame(self)
        topFrame.pack()
        bottomFrame = tk.Frame(self)
        bottomFrame.pack()

        # database label and text entry box
        databaseLabel = tk.Label(topFrame, text='Database').grid(row=0, column=0)
        database = tk.StringVar(value='TPC-H')
        databaseEntry = tk.Entry(topFrame, textvariable=database).grid(row=0, column=1)  

        # user label and text entry box
        userLabel = tk.Label(topFrame, text='User').grid(row=1, column=0)
        user = tk.StringVar(value='postgres')
        userEntry = tk.Entry(topFrame, textvariable=user).grid(row=1, column=1)  

        # password label and password entry box
        passwordLabel = tk.Label(topFrame,text='Password').grid(row=2, column=0)  
        password = tk.StringVar()
        passwordEntry = tk.Entry(topFrame, textvariable=password, show='*').grid(row=2, column=1)  

        # host label and text entry box
        hostLabel = tk.Label(topFrame, text='Host').grid(row=3, column=0)
        host = tk.StringVar(value='localhost')
        hostEntry = tk.Entry(topFrame, textvariable=host).grid(row=3, column=1)  

        # port label and text entry box
        portLabel = tk.Label(topFrame, text='Port').grid(row=4, column=0)
        port = tk.StringVar(value='5432')
        portEntry = tk.Entry(topFrame, textvariable=port).grid(row=4, column=1)  

        validateLogin = partial(self.validateLogin, database, user, password, host, port)

        #login button
        loginButton = tk.Button(bottomFrame, text='Login', command=validateLogin).grid(row=0, column=0)
        self.errorMsg = tk.Label(bottomFrame, text='Failed to connect to database', fg='#f00')
        self.errorMsg.grid(row=1, column=0)
        self.errorMsg.grid_forget()

    def validateLogin(self, database, user, password, host, port):
        connected = self.dbms.connect(
            database=database.get(),
            user=user.get(),
            password=password.get(),
            host=host.get(), 
            port=port.get()
        )

        if connected:
            # self.errorMsg.grid_forget()
            for widgets in self.winfo_children():
                widgets.destroy()
            self.createWindow()
        else:
            self.errorMsg.grid()

    def createWindow(self):
        self.geometry("1200x800")
        topFrame = tk.Frame(self)
        topFrame.pack()
        topFrame['background'] = '#62c2da'

        bottomFrame = tk.Frame(self)
        bottomFrame.pack()
        bottomFrame['background'] = '#62c2da'

        ############################
        # Frame for Application Name #
        ############################

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

        # Label widget for query
        queryLabel = tk.Label(master=queryFrame, text='Query')
        queryLabel.pack()
        queryLabel['background'] = '#62c2da'
        queryLabel.config(font=('Helvetica bold', 14, "bold"))

        #####################
        # Frame for buttons #
        #####################

        # Frame widget for buttons
        buttonFrame = tk.Frame(master=topFrame)
        buttonFrame.pack(side=tk.LEFT)
        buttonFrame['background'] = '#62c2da'
    

        # Button widget to submit query
        submitQueryButton = tk.Button(master=buttonFrame, text='Input Query', command=self.processQuery, foreground = 'white', height = 2, width = 20)
        submitQueryButton.pack(pady=5)
        submitQueryButton['background'] = '#063970'
        submitQueryButton.config(font=('Calibri', 14, "bold"))

        # Button widget to clear query
        clearQueryButton = tk.Button(master=buttonFrame, text='Clear', command=self.clearQuery, foreground = 'white', height = 2, width = 20)
        clearQueryButton.pack(pady=5)
        clearQueryButton['background'] = '#063970'
        clearQueryButton.config(font=('Calibri', 14, "bold"))

        ###################################
        # Frame for displaying annotation #
        ###################################

        annotationFrame = tk.Frame(master=topFrame)
        annotationFrame.pack(side=tk.LEFT)
        annotationFrame['background'] = '#62c2da'

        # Text widget to enter query
        self.annotationText = tk.Text(master=annotationFrame, state=tk.DISABLED, width=40, height=10, borderwidth=4, relief="solid")
        self.annotationText.pack(padx=20, pady=5)

        annotationLabel = tk.Label(master=annotationFrame, text='Annotation')
        annotationLabel.pack()
        annotationLabel['background'] = '#62c2da'
        annotationLabel.config(font=('Helvetica bold', 14, "bold"))

        # Frame for Database Schema #
        ##############################
        schemaFrame = tk.Frame(master=bottomFrame)
        schemaFrame.pack(side=tk.LEFT, anchor='s')
        schemaFrame['background'] = '#62c2da'

        # Button widget to open database schema window
        schemaButton = tk.Button(master=schemaFrame, text='Database Schema', foreground = 'white', height = 2, width = 20)
        schemaButton.pack(pady=33)
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
        self.treeCanvas.pack(pady=5, padx=30)

        self.img = ImageTk.PhotoImage(Image.open("images/blank.png"))  
        self.treeCanvas.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Invisible frame for alignment #
        ##############################
        invisibleFrame = tk.Frame(master=bottomFrame)
        invisibleFrame.pack(side=tk.LEFT)
        invisibleFrame['background'] = '#62c2da'

        # Invisible label to align treeFrame to center
        invisibleLabel = tk.Label(master=invisibleFrame, text='', foreground = 'white', height = 2, width = 20)
        invisibleLabel.pack(padx=30)
        invisibleLabel['background'] = '#62c2da'


    
    def processQuery(self):
        # Get query
        query = ' '.join((self.queryText.get(1.0, tk.END)).split('\n'))
        result = self.dbms.explainQuery(query)

        # Update annotation
        annotation = self.qepAnnotator.computeOutputString(result)

        self.annotationText.configure(state=tk.NORMAL)
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

# class QueryFrame(tk.Frame):
#     def __init__(self, container):
#         super().__init__(container)

#         # Label widget for query
#         self.label = tk.Label(self, text='QUERY')
#         self.label.pack()

#         # Text widget to enter query
#         self.text = tk.Text(self, height=10, width=30)
#         self.text.pack()

#         # Button widget to submit query
#         self.button = tk.Button(self, text='Submit')
#         self.button.pack()

# class AnnotationFrame(tk.Frame):
#     def __init__(self, container):
#         super().__init__(container)

#         # Label widget for annotation
#         label = tk.Label(self, text='ANNOTATION')
#         label.pack()

#         # Text widget to enter query
#         text = tk.Text(self, state='disabled', height=10, width=30)
#         text.pack()

# class TreeFrame(tk.Frame):
#     def __init__(self, container):
#         super().__init__(container)

#         # Label widget for tree
#         label = tk.Label(self, text='TREE')
#         label.pack()

#         # Canvas widget for image
#         canvas = tk.Canvas(self, width=700, height=500)  
#         canvas.pack()

#         # Image of QEP tree
#         self.img = ImageTk.PhotoImage(Image.open('images/blank.png'))  
#         canvas.create_image(0, 0, anchor=tk.NW, image=self.img)