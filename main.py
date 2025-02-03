from tkinter import *
import customtkinter
import time
import sys
from PIL import Image, ImageTk
import datetime
import xlsxwriter
from openpyxl import Workbook
from openpyxl import load_workbook
# importing packages


# function to save data
def save_data():

    for value in IDlist:
        sheet.cell(row,1).value = str(row)
        sheet.cell(row,2).value = str(value)
        row += 1
        wb.template = False
        wb.save(name)
    

# function to remove invalid ID's
def remove_red():
    for i in red_list:
        i.destroy()
    selected_student.configure(text="Selected Student:\nNo one selected")
    del_selected_ID.configure(state=DISABLED)

# function to remove certain ID
def selected_id(id):
    id.destroy()
    del_selected_ID.configure(state=DISABLED)
    selected_student.configure(text="Selected Student:\nNo one selected")
    GUI.update_idletasks()


# function to select ID
def selection(id):
    selected_student.configure(text="Selected Student:\n"+str(id.cget("text")))
    del_selected_ID.configure(state=NORMAL)
    del_selected_ID.configure(command=lambda: selected_id(id))
    GUI.update_idletasks()

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
    global IDlist, StudID, index, button_list
    # student ID is sent to be validated
    validation = data_validation(input_id.get())

    #adds ID's
    color = validation[1]
    Tcolor = validation[2]
    StudID = customtkinter.CTkButton(master=IDframe, text=input_id.get(), font=("arial",35), fg_color=color, text_color=Tcolor, corner_radius=10)
    StudID.pack(pady=10)
    
    index = index + 1
    #makes the scroll wheel to the bottom/new entries
    GUI.update_idletasks()
    canvas.yview_moveto(1)

    # stores ID's in a list
    IDlist.append(input_id.get())
    button_list.append(StudID)
    StudID.configure(command=lambda button = StudID: selection(button))


    if validation[0] == False:
        red_list.append(StudID)

    # resets the entry field
    input_id.delete(0, END)

    time_update()

def time_update():
    T = time.localtime()
    minute = T[4]
    if len(str(minute)) == 1:
        minute = "0"+str(minute)
    today = "Today is:\n\n"+str(day_of_week)+" "+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+"  "+str(T[3])+":"+str(minute)
    time_text.configure(text=today)
    GUI.after(10000, time_update)
    save_data()


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
current_date = datetime.datetime.now()
day_of_week = current_date.strftime('%A')
T = time.localtime()
minute = T[4]
if str(minute) == 1:
    minute = "0"+str(minute)
today = "Today is: "+str(day_of_week)+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+"  "+str(T[3])+":"+str(minute)
time_text = customtkinter.CTkLabel(master= option_frame, text=today, font=("arial",40))
time_text.place(relx = 0.2, rely = 0.05)
time_update()

#save files setup
name = str(day_of_week)+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+".xlsx"
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet()
worksheet.write(0, 1, "Id")
worksheet.set_column("A:G", 20)
row = 2
workbook.close()
wb = load_workbook(name, data_only=True)
sheet = wb.active

# text setup
studentid_text = customtkinter.CTkLabel(master= GUI, text="   Student ID   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
studentid_text.grid(pady=15, row=0, column = 0)

OPTIONS_text = customtkinter.CTkLabel(master= GUI, text="   OPTIONS   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
OPTIONS_text.grid(pady=15, row=0, column = 1, columnspan = 4)

manual_text = customtkinter.CTkLabel(master= option_frame, text="Manual Entry", font=("arial",40), fg_color="#41229c", corner_radius=10)
manual_text.place(relx = 0.05, rely =0.35)

del_red = customtkinter.CTkButton(master= option_frame, text="Delete All Red", font=("arial",40), fg_color="#f50a0e", corner_radius=15, height=60, command=remove_red)
del_red.place(relx = 0.3, rely =0.85)

del_selected_ID = customtkinter.CTkButton(master= option_frame, text="Delete \n selected ID", state=DISABLED,font=("arial",40), fg_color="#f50a0e", corner_radius=10)
del_selected_ID.place(relx = 0.07, rely =0.55)

selected_student = customtkinter.CTkLabel(master=option_frame, text="Selected Student:\nNo one selected", font=("arial",35))
selected_student.place(relx = 0.52, rely = 0.56)

global index
IDlist = [] #temp variable
button_list = []
red_list = []
first_run = True
index = -1

#set up entry box
input_id = customtkinter.CTkEntry(master=option_frame, placeholder_text = "Write ID here", font=("arial",35), width=300, height= 45)
input_id.place(relx = 0.5, rely = 0.35)

# pressing enter will accept the entry
input_id.bind("<Return>", ID_entered)

#binds the curser to the entry field
input_id.focus_force()




GUI.mainloop()