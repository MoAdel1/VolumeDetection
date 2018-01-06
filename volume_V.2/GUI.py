## [imports section]
# GUI modules
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *
# system call module
import os


## [code functions]
def process_image():
    if(poly.index("end")==0 or split.index("end")==0 or ref.index("end")==0 or image_path.get()==""):
        showinfo("Error!", "empty field exist")
        poly.delete(0,END)
        split.delete(0,END)
        ref.delete(0,END)
        image_path.set("")
    else:
        try:
            image_directory = str(image_path.get())
            poly_order = int(poly.get())
            split_order = int(split.get())
            ref_per = float(ref.get())
            split_flag = str(view_split.get())
            half_flag = str(view_half.get())
            system_call = "python main.py -i "+image_directory+" -l "+str(ref_per)+" -s "+str(split_order)+" -p "+str(poly_order)+" -v "+split_flag+" -c "+half_flag
            os.system(system_call)
            poly.delete(0,END)
            split.delete(0,END)
            ref.delete(0,END)
            image_path.set("")
        except ValueError:
            showinfo("Error!", "Wrong entry type in one of the fields")
######
def browse_image():
    path = askopenfilename(filetypes=(("JPEG images","*.jpg"),("PNG images","*.png"),("All files","*.*")))
    if(path):
        image_path.set(path)

## [GUI main loop]
root = Tk()
root.resizable(width=False, height=False)
w = 460 # width for the Tk root
h = 300 # height for the Tk root
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
# set window title
root.title("Estimator")
# path entry
image_path = StringVar()
image_path.set("")
path_label = Label(text="choose path to image:",font=("Helvetica",12))
path_label.place(x=0,y=0,width=165,height=25)
path = Button(root,text="browse",font=("Helvetica",12),command=browse_image)
path.place(x=0,y=26,width=160,height=25)
# reference object perimeter
ref_label = Label(text="reference perimeter:",font=("Helvetica",12))
ref_label.place(x=0,y=76,width=150,height=25)
ref = Entry(root,font=("Helvetica",12))   
ref.place(x=0,y=101,width=160,height=25)
# number of splits
split_label = Label(text="number of splits:",font=("Helvetica",12))
split_label.place(x=0,y=152,width=125,height=25)
split = Entry(root,font=("Helvetica",12))   
split.place(x=0,y=177,width=160,height=25)
# polynomial order
poly_label = Label(text="polynomial order:",font=("Helvetica",12))
poly_label.place(x=0,y=228,width=130,height=25)
poly = Entry(root,font=("Helvetica",12))   
poly.place(x=0,y=253,width=160,height=25)
# Process Image
process = Button(root,text="Process Image",font=("Helvetica",12),command=process_image)
process.place(x=300,y=135,width=160,height=25)
# view options
view_half = IntVar()
view_half_button = Checkbutton(root,text="view curve fitting",variable=view_half,font=("Helvetica",12))
view_half_button.place(x=287,y=160,width=160,height=25)
view_split = IntVar()
view_split_button = Checkbutton(root,text="view split regions",variable=view_split,font=("Helvetica",12))
view_split_button.place(x=290,y=185,width=160,height=25)


root.mainloop()

