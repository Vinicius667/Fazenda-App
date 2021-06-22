from tkinter import *
#from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
import excel_handler
from gado_func import *
from tkcalendar import *



all_animais = pickle.load(open("all_animais.pkl","rb"))
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

frame_machos_pesagens = Frame(root,bg="grey")
frame_menu = Frame(root,bg="red")
frame_machos_dados = Frame(root,bg="green")
frame_editar_pesagens = Frame(root,bg="blue")


frames = (frame_machos_dados,frame_machos_pesagens,frame_editar_pesagens,frame_menu)
for frame in frames:
    frame.grid(row=0,column=0,sticky="nsew")

frame_menu.tkraise()


b_gado_macho_dados = Button(frame_menu,text="Dados",padx=30,pady=30,command=lambda:gotoframe(frame_machos_dados))
b_gado_macho_dados.place(relx=0.5, rely=0.3, anchor=CENTER)
b_pesagens = Button(frame_menu,text="Pesagens",padx=30,pady=30,command=lambda:gotoframe(frame_machos_pesagens))
b_pesagens.place(relx=0.5, rely=0.5, anchor=CENTER)
b_editar_pesagens = Button(frame_menu,text="Editar pesagens",padx=30,pady=30,command=lambda:gotoframe(frame_editar_pesagens))
b_editar_pesagens.place(relx=0.5, rely=0.7, anchor=CENTER)



#########################  frame_machos_dados

macho = Animal(frame_machos_dados,frame_machos_pesagens,frame_editar_pesagens,animais_data_peso,all_datas)



for frame in frames:
    if frame != frame_menu:
        b_voltar_menu = Button(frame,text="Voltar ao menu",command=lambda:gotoframe(frame_menu))
        b_voltar_menu.place(relx=1,rely=0,anchor=NE)




#########################  frame_machos_pesagens


macho.tree_info.tree.bind("<Button-1>",lambda e : tree_info_handler(e,macho))



b_pesagens.bind('<Button-1>', lambda e: macho.tree_dummy.update_pesagens_frame(e))

















root.mainloop()


