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
animais_data_peso = {200:animais_data_peso[200],216:animais_data_peso[216]}


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
b_trabalhadores = Button(frame_menu,text="Editar pesagens",padx=30,pady=30,command=lambda:gotoframe(frame_editar_pesagens))
b_trabalhadores.place(relx=0.5, rely=0.7, anchor=CENTER)



#########################  frame_machos_dados
lf_pesquisa_animal = LabelFrame(frame_machos_dados,text="Pesquisar animal")
lf_pesquisa_animal.place(relwidth=0.4,relheight=0.1)

e_pesquisa_animal = Entry(lf_pesquisa_animal,text="Animal a ser pesquisado (Ex: 71)",width=15,font=60)
e_pesquisa_animal.grid(row=0,column=1,padx=20,pady=20)
b_pesquisa_animal = Button(lf_pesquisa_animal,text="Pesquisar")
b_pesquisa_animal.grid(row=0,column=2,padx=20,pady=20)



lf_todos_animais=LabelFrame(frame_machos_dados,text="Todos animais",bg="pink")
lf_todos_animais.place(relwidth=0.4,relheight=0.9,rely=0.1)




lf_animal_info = LabelFrame(frame_machos_dados,text="Informações do animal",bg="red")
lf_animal_info.place(relwidth=0.6,relheight=1,relx=0.4)

for frame in frames:
    if frame != frame_menu:
        b_voltar_menu = Button(frame,text="Voltar ao menu",command=lambda:gotoframe(frame_menu))
        b_voltar_menu.place(relx=1,rely=0,anchor=NE)




#########################  frame_machos_pesagens

macho = Animal(lf_todos_animais,frame_machos_pesagens,frame_editar_pesagens,animais_data_peso,all_datas)
macho.tree_dummy.tree.place(relwidth=0.2,relheight=0.9,relx=0.0,rely=0.0)
macho.tree_dummy.sum_tree.place(relwidth=0.2,relheight=0.1,relx=0.0,rely=0.9)
macho.tree_dummy.l_info_pesagem.place(relx=0.5,rely=0.7,anchor=CENTER)

macho.tree_info.tree.bind("<Button-1>",lambda e : tree_info_handler(e,macho))
macho.tree_info.tree.place(relwidth=1,relheight=0.9,rely=0.1)

e_animal = Entry(frame_machos_pesagens)
e_animal.place(relwidth=0.05,relx=0.45,rely=0.6,anchor=CENTER)

e_peso = Entry(frame_machos_pesagens)
e_peso.place(relwidth=0.05,relx=0.55,rely=0.6,anchor=CENTER)

l_animal = Label(frame_machos_pesagens,text="Animal",bg="grey")
l_peso = Label(frame_machos_pesagens,text="Peso",bg="grey")


cal = Calendar(frame_machos_pesagens,firstweekday="sunday",showweeknumbers=False,locale="pt_BR")
cal.place(relx=0.5,rely=0.15,anchor=CENTER)

l_animal.place(relx=0.45,rely=0.55,anchor=CENTER)
l_peso.place(relx=0.55,rely=0.55,anchor=CENTER)


#l_data_inserida = Label(frame_machos_pesagens,text="",bg="grey")
macho.tree_dummy.l_data_inserida.place(relx=0.5,rely=0.4,anchor=CENTER)

def cal2date(cal):
    dia,mes,ano = [int(el) for el in cal.get_date().split("/")]
    data = datetime(ano,mes,dia)
    return  data

def data_selecionada_dummy(cal,animal):
    data = cal2date(cal)
    animal.tree_dummy.data = data
    animal.tree_dummy.l_data_inserida.config(text=data.strftime("%d/%m/%y"))


b_selecionar_data_dummy = Button(frame_machos_pesagens,text="Seleciona data",command= lambda : data_selecionada_dummy(cal,macho))
b_selecionar_data_dummy.place(relx=0.5,rely=0.35,anchor=CENTER)



b_inserir_pesagem = Button(frame_machos_pesagens,text="Inserir pesagem",command=lambda : inserir_pesagem(macho))
b_inserir_pesagem.place(relx=0.5,rely=0.65,anchor=CENTER)

e_animal.bind("<Return>",lambda e :tree_dummy_handler(e,macho,"animal",e_animal,e_peso))
e_peso.bind("<Return>",lambda e :tree_dummy_handler(e,macho,"peso",e_animal,e_peso))
macho.tree_dummy.tree.bind("<Delete>",lambda e :tree_dummy_handler_delete(e,macho))


b_pesagens.bind('<Button-1>',lambda e : update_pesagens_frame(e,macho))


#########################  frame_editar_pesagens
cal2 = Calendar(frame_editar_pesagens,firstweekday="sunday",showweeknumbers=False,locale="pt_BR")
macho.tree_edit.tree.pack()

b_selecionar_data_edit = Button(frame_editar_pesagens,text="Seleciona data",command= lambda : data_selecionada_edit(cal2,macho))
b_selecionar_data_edit.pack()




cal2.pack()
macho.tree_edit.l_data_inserida.pack()
macho.tree_edit.optionmenu.pack()

def data_selecionada_edit(cal2,animal):
    data = cal2date(cal2)
    animal.tree_edit.data = data
    animal.tree_edit.l_data_inserida.config(text=data.strftime("%d/%m/%y"))




root.mainloop()






'''

def f_pesquisa_animal():
    animal_pesquisado = e_pesquisa_animal.get()
    l_animal_pesquisado = Label(text=animal_pesquisado).pack()
    e_pesquisa_animal.delete(0, END)
b_pesquisa_animal = Button(root,text="Pesquisar",command=f_pesquisa_animal).pack()

my_img = ImageTk.PhotoImage(Image.open("sky.jpg"))
lab = Label(image=my_img).pack()

'''