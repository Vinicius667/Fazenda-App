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
frame_editar_pesagens = Frame(root,bg="black")


frames = (frame_machos_dados,frame_machos_pesagens,frame_editar_pesagens,frame_menu)
for frame in frames:
    frame.grid(row=0,column=0,sticky="nsew")

frame_menu.tkraise()




b_gado_macho_dados = Button(frame_menu,text="Dados",padx=30,pady=30,command=lambda:gotoframe(frame_machos_dados))
b_gado_macho_dados.place(relx=0.5, rely=0.3, anchor=CENTER)
b_gado_femea = Button(frame_menu,text="Pesagens",padx=30,pady=30,command=lambda:gotoframe(frame_machos_pesagens))
b_gado_femea.place(relx=0.5, rely=0.5, anchor=CENTER)
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


macho = Animal(lf_todos_animais,frame_machos_pesagens,animais_data_peso)

macho.tree_info.generate_tree(
    ("Animal", "Peso", "Ultima pesagem", "Pesagens", "Engorda"),
    (50, 50, 100, 100, 80))

macho.tree_info.fill_tree()



def tree_info_handler(e,animal):
    was_selected = what_was_selected_tree(e)
    regiao = was_selected[0]
    if regiao == 'heading':
        coluna = was_selected[1]
        coluna = int(coluna[1:])-1
        animal.tree_info.sort_by_heading(coluna)
    elif regiao == "cell":
        cells = was_selected[1]
        tree_info_selected(cells,animal)

def tree_info_selected(cells_selected,animal):
    print(f"The animal selected was {cells_selected}")




macho.tree_info.tree.bind("<Double-1>",lambda e : tree_info_handler(e,macho))
macho.tree_info.tree.place(relwidth=1,relheight=0.9,rely=0.1)


#########################  frame_machos_pesagens






macho.tree_dummy.generate_tree(
    ("Animal","Peso"),
    (50,50)
    )



macho.tree_dummy.tree.place(relwidth=0.2,relheight=0.9,relx=0.0,rely=0.0)

b_selecionar_data = Button(frame_machos_pesagens,text="Selecionar data")
b_selecionar_data.place(relx=0.5,rely=0.35,anchor=CENTER)



e_animal = Entry(frame_machos_pesagens)
e_animal.place(relwidth=0.05,relx=0.45,rely=0.5,anchor=CENTER)

e_peso = Entry(frame_machos_pesagens)
e_peso.place(relwidth=0.05,relx=0.55,rely=0.5,anchor=CENTER)

l_animal = Label(frame_machos_pesagens,text="Animal",bg="grey")
l_peso = Label(frame_machos_pesagens,text="Peso",bg="grey")

l_animal.place(relx=0.45,rely=0.45,anchor=CENTER)
l_peso.place(relx=0.55,rely=0.45,anchor=CENTER)



#l_info_pesagem = Label(frame_machos_pesagens,text="",bg="grey")

macho.tree_dummy.l_info_pesagem.place(relx=0.5,rely=0.7,anchor=CENTER)





b_inserir_pesagem = Button(frame_machos_pesagens,text="Inserir pesagem",command=lambda : inserir_pesagem(macho))
b_inserir_pesagem.place(relx=0.5,rely=0.6,anchor=CENTER)


data = datetime(2022,10,4)
def inserir_pesagem(animal):
    result = animal.inserir_pesagem(data)
    print(result)




def tree_dummy_handler(e,animal:Animal,tipo:str):
    try:
        animal = int(e_animal.get())
        peso = int(e_peso.get())
        e_peso.delete(0,END)
        e_animal.delete(0,END)
        insertion_ok = macho.tree_dummy.insert_one(animal,peso)
        print(insertion_ok)
    except ValueError:
        pass
    if tipo == "animal":
        e_peso.focus()
    elif tipo == "peso":
        e_animal.focus()




def tree_dummy_handler_delete(e,animal):
    was_selected = what_was_selected_tree(e)
    if was_selected[0] == "cell":
        cells= was_selected[1]
        animal.tree_dummy.delete_list_cells(cells)


e_animal.bind("<Return>",lambda e :tree_dummy_handler(e,macho,"animal"))
e_peso.bind("<Return>",lambda e :tree_dummy_handler(e,macho,"peso"))
macho.tree_dummy.tree.bind("<Delete>",lambda e :tree_dummy_handler_delete(e,macho))



cal = Calendar(frame_machos_pesagens,firstweekday="sunday")
cal.place(relx=0.5,rely=0.15,anchor=CENTER)




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