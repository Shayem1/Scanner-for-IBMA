from tkinter import *
import customtkinter
import time
import sys
import datetime
import xlsxwriter
import os
from openpyxl import Workbook
from openpyxl import load_workbook
# importing packages


# function to save data
def save_data():
    save_data_manual()
    # Set up the next save to occur after 5 minutes
    GUI.after(15000, save_data)

def save_data_manual():
    global workbook, worksheet, wb, sheet
    name = str(day_of_week)+" "+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+".xlsx"

    try:
        workbook.close()
        if os.path.exists(name):
            os.remove(name)
            workbook = xlsxwriter.Workbook(name)
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 1, "Id")
            worksheet.set_column("A:G", 20)
            workbook.close()
            row = 2
            wb = load_workbook(name, data_only=True)
            sheet = wb.active

            for i in button_list:
                id = i.cget("text")
                sheet.cell(row,1).value = str(row)
                sheet.cell(row,2).value = str(id)
                row += 1

            wb.template = False
            wb.save(name)
    except:
        print("stawp touching my files :(")
    


# function to remove invalid ID's
def remove_red():
    global red_list, button_list
    # Iterate over a copy of red_list to avoid modifying it while iterating
    for i in red_list:
        i.destroy()
        if i in button_list:
            button_list.remove(i)
        red_list.remove(i)
    if len(red_list) > 0:
        remove_red()
    selected_student.configure(text="Selected Student:\nNo one selected")
    del_selected_ID.configure(state=DISABLED)


# function to remove certain ID
def selected_id(id):
    global button_list, red_list
    id.destroy()
    if id in button_list:
        button_list.remove(id)
    if id in red_list:
        red_list.remove(id)
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
    try:
        if len(string) == 8 and int(string[0,3])>= 2016 and int(string[0,3]) <= 2099:
            list1 = [True,"#13005e", "White"]
    except: pass

    if len(string) == 9 and "IBM" in string:
        list1 = [True, "#0f39d4", "Black"]
    
    else:
        list1 = [False, "red", "Black"]

    return list1

# scanner main entry
def ID_entered(event):
    global IDlist, StudID, button_list, id, index, wb, sheet, red_list
    # student ID is sent to be validated
    id = input_id.get()
    validation = data_validation(id)

    #adds ID's
    color = validation[1]
    Tcolor = validation[2]
    StudID = customtkinter.CTkButton(master=IDframe, text=id, font=("arial",35), fg_color=color, text_color=Tcolor, corner_radius=10)
    StudID.pack(pady=10)
    
    #makes the scroll wheel to the bottom/new entries
    GUI.update_idletasks()
    canvas.yview_moveto(1)

    # stores ID's in a list
    IDlist.append(id)
    button_list.append(StudID)
    StudID.configure(command=lambda button = StudID: selection(button))
    
    
    sheet.cell(index,1).value = str(index)
    sheet.cell(index,2).value = str(id)
    wb.save(name)
    
    if validation[0] == False:
        red_list.append(StudID)

    index += 1

    # resets the entry field
    input_id.delete(0, END)
    time_update_manual()

def time_update_manual():
    T = time.localtime()
    minute = T[4]
    if len(str(minute)) == 1:
        minute = "0"+str(minute)
    today = "Today is:\n\n"+str(day_of_week)+" "+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+"  "+str(T[3])+":"+str(minute)
    time_text.configure(text=today)

def time_update():
    T = time.localtime()
    minute = T[4]
    if len(str(minute)) == 1:
        minute = "0"+str(minute)
    today = "Today is:\n\n"+str(day_of_week)+" "+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+"  "+str(T[3])+":"+str(minute)
    time_text.configure(text=today)
    GUI.after(10000, time_update)
    

# initialising the GUI
GUI = customtkinter.CTk()
GUI.geometry("1200x800")
GUI.maxsize(width=1200, height=800)
GUI.minsize(width=1200, height=800)
GUI.title("Student ID Scanner")
GUI.grid_rowconfigure(1, weight=1, uniform="equal")
GUI.grid_columnconfigure(2, weight=1, uniform="equal")
customtkinter.set_appearance_mode("dark")

IDlist = [] #temp variable
index = 2
button_list = []
red_list = []

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

#save data setup
name = str(day_of_week)+" "+str(T[2])+"-"+str(T[1])+"-"+str(T[0])+".xlsx"

#prevents overwriting data after a crash
if os.path.exists(name):
    GUI.destroy()
    quit()

workbook = xlsxwriter.Workbook(name)

worksheet = workbook.add_worksheet()

worksheet.write(0, 1, "Id")
worksheet.set_column("A:G", 20)
workbook.close()

row = 2
wb = load_workbook(name, data_only=True)
sheet = wb.active

time_update()
save_data()

# text setup
studentid_text = customtkinter.CTkLabel(master= GUI, text="   Student ID   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
studentid_text.grid(pady=15, row=0, column = 0)

OPTIONS_text = customtkinter.CTkLabel(master= GUI, text="   OPTIONS   ", font=("arial",45), fg_color="#41229c", corner_radius=10)
OPTIONS_text.grid(pady=15, row=0, column = 1, columnspan = 4)

manual_text = customtkinter.CTkLabel(master= option_frame, text="Manual Entry", font=("arial",40), fg_color="#41229c", corner_radius=10)
manual_text.place(relx = 0.05, rely =0.35)

del_red = customtkinter.CTkButton(master= option_frame, text="Delete All Red", font=("arial",40), fg_color="#f50a0e", corner_radius=15, height=60)
del_red.configure( command= lambda: remove_red())
del_red.place(relx = 0.5, rely =0.85)

del_selected_ID = customtkinter.CTkButton(master= option_frame, text="Delete \n selected ID", state=DISABLED,font=("arial",40), fg_color="#f50a0e", corner_radius=10)
del_selected_ID.place(relx = 0.07, rely =0.55)

selected_student = customtkinter.CTkLabel(master=option_frame, text="Selected Student:\nNo one selected", font=("arial",35))
selected_student.place(relx = 0.52, rely = 0.56)

save_button = customtkinter.CTkButton(master= option_frame, text="SAVE", state=NORMAL,font=("arial",40), fg_color="#30cf0c", corner_radius=10)
save_button.place(relx = 0.13, rely =0.86)
save_button.configure(command = lambda: save_data_manual())

#set up entry box
input_id = customtkinter.CTkEntry(master=option_frame, placeholder_text = "Write ID here", font=("arial",35), width=300, height= 45)
input_id.place(relx = 0.5, rely = 0.35)

# pressing enter will accept the entry
input_id.bind("<Return>", ID_entered)

#binds the curser to the entry field
input_id.focus_force()

GUI.mainloop()