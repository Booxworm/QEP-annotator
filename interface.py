import tkinter as tk
from PIL import ImageTk, Image  

window = tk.Tk()

############################
# Frame for entering query #
############################

# Frame widget for query
frame_query = tk.Frame(master=window)
frame_query.pack(side=tk.LEFT)

# Label widget for query
label_query = tk.Label(master=frame_query, text='QUERY')
label_query.pack()

# Text widget to enter query
text_query = tk.Text(master=frame_query)
text_query.pack()

# Button widget to submit query
button_query = tk.Button(master=frame_query, text='Submit')
button_query.pack()

###################################
# Frame for displaying annotation #
###################################

frame_annotation = tk.Frame(master=window)
frame_annotation.pack(side=tk.LEFT)

label_annotation = tk.Label(master=frame_annotation, text='ANNOTATION')
label_annotation.pack()


#############################
# Frame for displaying tree #
#############################

frame_tree = tk.Frame(master=window)
frame_tree.pack(side=tk.LEFT)

label_tree = tk.Label(master=frame_tree, text='TREE')
label_tree.pack()

canvas = tk.Canvas(frame_tree, width=700, height=500)  
canvas.pack()

img = ImageTk.PhotoImage(Image.open("images/qep.png"))  
canvas.create_image(0, 0, anchor=tk.NW, image=img)


window.mainloop()
