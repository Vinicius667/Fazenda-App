from tkinter import *
#from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
import excel_handler
from gado_func import *
from tkcalendar import *
from tkinter import messagebox
from ttkthemes import ThemedTk,THEMES




all_datas = pickle.load(open("all_datas.pkl","rb"))
animais_info = pickle.load(open("animais_info.pkl","rb"))

#root = Tk()
root = ThemedTk()
root.set_theme("elegance")
root.title("Controle Fazenda")
root.iconbitmap("cow.ico")
root.state("zoomed")

screen_width = root.winfo_width()
screen_height = root.winfo_height()

root.minsize(screen_width//2,screen_height)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)



macho = Animal(root,animais_info,all_datas)




root.mainloop()


