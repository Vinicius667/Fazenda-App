from tkinter import *
#from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
import excel_handler
from gado_func import *
from tkcalendar import *



#all_animais = pickle.load(open("all_animais.pkl","rb"))
all_datas = pickle.load(open("all_datas.pkl","rb"))
animais_data_peso = pickle.load(open("animais_data_peso.pkl","rb"))
#animais_data_peso = {200:animais_data_peso[200],216:animais_data_peso[216]}

root = Tk()
root.title("Controle Fazenda")
root.iconbitmap("cow.ico")
root.state("zoomed")

screen_width = root.winfo_width()
screen_height = root.winfo_height()

root.minsize(screen_width//2,screen_height)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)


macho = Animal(root,animais_data_peso,all_datas)




root.mainloop()


