from tkinter import *
import customtkinter
import time
import sys
from PIL import Image, ImageTk
# importing packagees

# makes the entry box the focus
def focus():
    input_id.focus_force()

# function to remove invalid ID's
def remove_red():
    for i in red_list:
        i.destroy()

# function to remove certain ID
def selected_id(id):
    button_list.remove(button_list.index[id])

# function to select ID
def selection(id):
    
    selected_student.configure(text="Selected Student:\n"+str(id))
    """if first_run == True:
        first_run = False
        del_selected_ID.configure(command = selected_id(StudID))"""
    pass

# scanner setup
def data_validation(string):
    if len(string) == 8 and "20" in string:
        list1 = [True,"#13005e", "White"]

    elif len(string) == 9 and "IBM" in string:
        list1 = [True, "#0f39d4", "Black"]
    
    else:
        list1 = [False, "red", "Black"]

    return list1

# scanner main entry
def ID_entered(event):
    global IDlist, StudID
    # student ID is sent to be validated
    validation = data_validation(input_id.get())

    index =+ 1

    #adds ID's
    color = validation[1]
    Tcolor = validation[2]
    StudID = customtkinter.CTkButton(master=IDframe, text=input_id.get(), font=("arial",35), fg_color=color, text_color=Tcolor, corner_radius=10, command=selection(index))
    StudID.pack(pady=10)

    #makes the scroll wheel to the bottom/new entries
    GUI.update_idletasks()
    canvas.yview_moveto(1)

    # stores ID's in a list
    IDlist.append(input_id.get())
    button_list.append(StudID)

    if validation[0] == False:
        red_list.append(StudID)

    # resets the entry field
    input_id.delete(0, END)

    time_update()

def time_update():
    T = time.localtime()
    today = "Today is: "+str(T[2])+"/"+str(T[1])+"/"+str(T[0])+"  "+str(T[3])+":"+str(T[4])
    time_text.configure(text=today)
    GUI.after(10000, time_update)

# initialising the GUI
GUI = customtkinter.CTk()
GUI.geometry("1200x800")
GUI.maxsize(width=1200, height=800)
GUI.minsize(width=1200, height=800)
GUI. title("Student ID Scanner")
GUI.grid_rowconfigure(1, weight=1, uniform="equal")
GUI.grid_columnconfigure(2, weight=1, uniform="equal")
customtkinter.set_appearance_mode("dark")

# initialising student ID output frame
IDframe = customtkinter.CTkScrollableFrame(master= GUI, width= 300, corner_radius=30)
IDframe.grid(padx = 50, row=1, column = 0,  sticky="nsew", pady=20)
canvas = IDframe._parent_canvas

option_frame = customtkinter.CTkFrame(master=GUI, width=670, height= 600, corner_radius=20)
option_frame.grid(padx = 25, row=1, column = 1,  sticky="nsew", pady=20)

# time setup
T = time.localtime()
if T[3] == 12 or T[3] < 7:
    p = "pm"
else: p="am"
today = "Today is: "+str(T[2])+"/"+str(T[1])+"/"+str(T[0])+"  "+str(T[3])+":"+str(T[4])+" "+str(p)
time_text = customtkinter.CTkLabel(master= option_frame, text=today, font=("arial",40))
time_text.place(relx = 0.12, rely = 0.07)
time_update()

# text setup
studentid_text = customtkinter.CTkLabel(master= GUI, text="   Student ID   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
studentid_text.grid(pady=15, row=0, column = 0)

OPTIONS_text = customtkinter.CTkLabel(master= GUI, text="   OPTIONS   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
OPTIONS_text.grid(pady=15, row=0, column = 1, columnspan = 4)

manual_text = customtkinter.CTkLabel(master= option_frame, text="Manual Entry", font=("arial",40), fg_color="#41229c", corner_radius=10)
manual_text.place(relx = 0.05, rely =0.2)

del_red = customtkinter.CTkButton(master= option_frame, text="Delete All Red", font=("arial",40), fg_color="#f50a0e", corner_radius=15, height=60, command=remove_red)
del_red.place(relx = 0.3, rely =0.85)

del_selected_ID = customtkinter.CTkButton(master= option_frame, text="Delete \n selected ID", state=DISABLED,font=("arial",40), fg_color="#f50a0e", corner_radius=10)
del_selected_ID.place(relx = 0.07, rely =0.35)

selected_student = customtkinter.CTkLabel(master=option_frame, text="Selected Student:\nNo one selected", font=("arial",35))
selected_student.place(relx = 0.52, rely = 0.36)

global button_list, IDlist, red_list
IDlist = [] #temp variable
button_list = []
red_list = []
first_run = True
index = 0

#set up entry box
input_id = customtkinter.CTkEntry(master=option_frame, placeholder_text = "Write ID here", font=("arial",35), width=300, height= 45)
input_id.place(relx = 0.5, rely = 0.2)

# pressing enter will accept the entry
input_id.bind("<Return>", ID_entered)

#binds the curser to the entry field
input_id.focus_force()
GUI.bind("key", focus())



GUI.mainloop()