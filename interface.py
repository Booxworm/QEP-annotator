import tkinter as tk

from PIL import ImageTk, Image

class App(tk.Tk):
    def __init__(self, dbms, qepAnnotator, qepGraph):
        super().__init__()
        
        self.dbms = dbms
        self.qepAnnotator = qepAnnotator
        self.qepGraph = qepGraph
        self.createWindow()
        
    def createWindow(self):
        topFrame = tk.Frame(self)
        topFrame.pack()

        bottomFrame = tk.Frame(self)
        bottomFrame.pack()

        ############################
        # Frame for entering query #
        ############################

        # Frame widget for query
        queryFrame = tk.Frame(master=topFrame)
        queryFrame.pack(side=tk.LEFT)

        # Text widget to enter query
        self.queryText = tk.Text(master=queryFrame, width=40, height=10)
        self.queryText.pack()

        # Label widget for query
        queryLabel = tk.Label(master=queryFrame, text='QUERY')
        queryLabel.pack()

        #####################
        # Frame for buttons #
        #####################

        # Frame widget for buttons
        buttonFrame = tk.Frame(master=topFrame)
        buttonFrame.pack(side=tk.LEFT)

        # Button widget to submit query
        submitQueryButton = tk.Button(master=buttonFrame, text='Submit', command=self.processQuery)
        submitQueryButton.pack()

        # Button widget to clear query
        clearQueryButton = tk.Button(master=buttonFrame, text='Clear text', command=self.clearQuery)
        clearQueryButton.pack()

        ###################################
        # Frame for displaying annotation #
        ###################################

        annotationFrame = tk.Frame(master=topFrame)
        annotationFrame.pack(side=tk.LEFT)

        # Text widget to enter query
        self.annotationText = tk.Text(master=annotationFrame, state=tk.DISABLED, width=40, height=10)
        self.annotationText.pack()

        annotationLabel = tk.Label(master=annotationFrame, text='ANNOTATION')
        annotationLabel.pack()


        #############################
        # Frame for displaying tree #
        #############################

        treeFrame = tk.Frame(master=bottomFrame)
        treeFrame.pack(side=tk.LEFT)

        treeLabel = tk.Label(master=treeFrame, text='TREE')
        treeLabel.pack()

        self.treeCanvas = tk.Canvas(treeFrame, width=700, height=500)  
        self.treeCanvas.pack()

        self.img = ImageTk.PhotoImage(Image.open("images/blank.png"))  
        self.treeCanvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    
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