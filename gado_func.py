from tkinter import *
# from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
import excel_handler
from tkcalendar import *


def gotoframe(frame):
    frame.tkraise()



def what_was_selected_tree(e):
    tree = e.widget
    regiao = tree.identify_region(e.x, e.y)
    if regiao == 'heading':
        coluna = tree.identify_column(e.x)
        return ['heading', coluna]
    elif regiao == "cell":
        cells = [int(cell) for cell in tree.selection()]
        return ['cell', cells]



def create_screen(root):
    root.state("zoomed")

    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    root.minsize(screen_width // 2, screen_height)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)




class MyTree():
    """Funções comuns para todas as trees"""
    def __init__(self, frame):
        self.tree = ttk.Treeview(frame)
    
    @staticmethod
    def generate_tree(tree,columns, width):
        tree["columns"] = columns
        tree.column("#0", width=0, stretch=NO)
        for col, wid in zip(columns, width):
            tree.column(col, width=wid, minwidth=wid, anchor=CENTER)
        tree.heading("#0", text="")
        for col, wid in zip(columns, width):
            tree.heading(col, text=col, anchor=CENTER)

    def delete_all_tree(self):
        self.tree.delete(*self.tree.get_children())

    @staticmethod
    def cal2date(cal):
        dia, mes, ano = [int(el) for el in cal.get_date().split("/")]
        data = datetime(ano, mes, dia)
        return data


class TreeEdit(MyTree):
    def __init__(self,frame,animal_):
        super().__init__(frame)
        self.animal_ = animal_
        self.l_info_pesagem = Label(frame, text="", bg="grey")
        self.generate_tree(self.tree,("Animal","Peso (kg)"),(50,80))
        self.data = False
        self.l_data_inserida = Label(frame,text="",bg="grey")
        self.stringvar = StringVar(frame)
        self.stringvar.set("Selecione uma data")
        self.optionmenu = OptionMenu(frame, self.stringvar, *["Selecione uma data"])
        self.update_option_menu()
        self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
        self.b_selecionar_data_edit = Button(frame,text="Seleciona data",command= lambda : self.data_selecionada_edit())
        self.pack_on_frame()
        self.dummy_lista = []

    def data_selecionada_edit(self):
        self.data = self.cal2date(self.cal)
        self.l_data_inserida.config(text=self.data.strftime("%d/%m/%y"))
        
    def pack_on_frame(self):
        self.l_data_inserida.pack()
        self.optionmenu.pack()
        self.tree.pack()
        self.b_selecionar_data_edit.pack()
        self.cal.pack()
        self.stringvar.trace("w",self.update_tree)
        self.tree.bind("<Delete>", lambda e: self.tree_dummy_handler_delete(e))

    def tree_dummy_handler_delete(self,e):
        was_selected = what_was_selected_tree(e)
        if was_selected[0] == "cell":
            cells = was_selected[1]
            self.delete_list_cells(cells)

    def update_option_menu(self):
        self.optionmenu['menu'].delete(0, 'end')
        for date in self.animal_.all_datas:
            data = date.strftime("%d/%m/%Y")
            self.optionmenu['menu'].add_command(label=data,command=lambda value=data: self.stringvar.set(value))


    def update_tree(self,*args):
        d,m,a= [int(el) for el in self.stringvar.get().split("/")]
        data = datetime(a,m,d)
        for animal,data_peso_ in self.animal_.animais_data_peso.items():
            for i, data_peso in enumerate(data_peso_):
                if data == data_peso[0]:
                    self.dummy_lista.append([animal,data_peso[1],i])
        self.fill_tree()

    def fill_tree(self):
        self.delete_all_tree()
        i = 0
        for animal,peso,index in self.dummy_lista:
            self.tree.insert(parent="", index=END, iid=i, values=[animal,peso])
            i+=1

    def delete_cells(self):
        pass






class TreeDummy(MyTree):
    """Controla as treeinfos e a lista das treeinfos"""

    def __init__(self, frame,animal_):
        super().__init__(frame)
        self.animal_ = animal_
        self.lista = []
        self.l_info_pesagem = Label(frame, text="", bg="grey")
        self.generate_tree(self.tree,("Animal","Peso (kg)"),(50,50))
        self.sum_tree = ttk.Treeview(frame)
        self.generate_tree(self.sum_tree,("Quantidade","Peso total"),(50,50))
        self.data = False
        self.l_data_inserida = Label(frame,text="",bg="grey")
        self.e_animal = Entry(frame)
        self.e_peso = Entry(frame)
        self.l_animal = Label(frame, text="Animal", bg="grey")
        self.l_peso = Label(frame, text="Peso", bg="grey")
        self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
        self.b_pesagens = Button(frame,text="Pesagens",padx=30,pady=30,command=lambda:gotoframe(frame))
        self.b_selecionar_data_dummy = Button(frame,text="Seleciona data",command=  self.data_selecionada_dummy)
        self.b_inserir_pesagem = Button(frame,text="Inserir pesagem",command=self.animal_.inserir_pesagem)
        self.pack_on_frame()

    def data_selecionada_dummy(self):
        data = self.cal2date(self.cal)
        self.data = data
        self.l_data_inserida.config(text=data.strftime("%d/%m/%y"))


    def pack_on_frame(self):
        self.tree.place(relwidth=0.2, relheight=0.9, relx=0.0, rely=0.0)
        self.sum_tree.place(relwidth=0.2, relheight=0.1, relx=0.0, rely=0.9)
        self.l_info_pesagem.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.e_animal.place(relwidth=0.05, relx=0.45, rely=0.6, anchor=CENTER)
        self.e_peso.place(relwidth=0.05, relx=0.55, rely=0.6, anchor=CENTER)
        self.cal.place(relx=0.5, rely=0.15, anchor=CENTER)
        self.l_animal.place(relx=0.45, rely=0.55, anchor=CENTER)
        self.l_peso.place(relx=0.55, rely=0.55, anchor=CENTER)
        self.l_data_inserida.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.b_selecionar_data_dummy.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.b_inserir_pesagem.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.e_animal.bind("<Return>", lambda e: self.tree_dummy_handler(e, "animal"))
        self.e_peso.bind("<Return>", lambda e: self.tree_dummy_handler(e, "peso",))
        self.tree.bind("<Delete>", lambda e: self.tree_dummy_handler_delete(e))

    def tree_dummy_handler_delete(self,e):
        was_selected = what_was_selected_tree(e)
        if was_selected[0] == "cell":
            cells = was_selected[1]
            self.delete_list_cells(cells)

    def tree_dummy_handler(self, e, tipo):
        try:
            entrada_animal = self.e_animal.get()
            entrada_peso = self.e_peso.get()
            value_animal = int(entrada_animal)
            valie_peso = float(entrada_peso)
            self.e_peso.delete(0, END)
            self.e_animal.delete(0, END)
            insertion_ok = self.insert_one(value_animal, valie_peso)
        except ValueError:
            if entrada_animal != "" and entrada_peso != "":
                self.update_info("Animal e peso devem ser números.")
        if tipo == "animal":
            self.e_peso.focus()
        elif tipo == "peso":
            self.e_animal.focus()


            
    def update_pesagens_frame(self,e):
        self.update_info("")
        self.update_sum_tree()



    def fill_tree(self):
        if len(self.tree.get_children()) > 0:
            self.tree.delete_all_tree()
        for i, item in enumerate(self.lista):
            self.tree.insert(parent="", index=END, iid=i, values=item)

    def delete_list_cells(self, cells):
        self.delete_all_tree()
        for i in sorted(cells, reverse=True):
            self.lista.pop(i)
        self.fill_tree()

    def insert_one(self,animal,peso):
        if animal in [animal[0] for animal in self.lista]:
            self.update_info(f"Animal {animal} já foi adicionado!")
            return [False,animal]
        self.delete_all_tree()
        self.lista.append([animal,peso])
        self.fill_tree()
        self.update_info()
        self.update_sum_tree()
        return True


    def update_info(self,texto=""):
        self.l_info_pesagem.config(text=texto)

    def update_sum_tree(self):
        soma = 0
        for animal,peso in self.lista:
            soma += peso
        self.sum_tree.delete(*self.sum_tree.get_children())
        self.sum_tree.insert(parent="", index=END, iid=0, values=[len(self.lista),soma])





class TreeInfo(MyTree):
    def __init__(self, frame,animal_):
        self.lf_todos_animais = LabelFrame(frame, text="Todos animais", bg="pink")
        self.frame = frame
        super().__init__(self.lf_todos_animais)
        self.animal_ = animal_
        self.lista = []
        self.generate_tree_info()
        self.tree_info_col_sort = 0
        self.tree_info_reverse_sort = False
        self.generate_tree(self.tree,
            ("Animal", "Peso (kg)", "Ultima pesagem", "Pesagens", "Engorda"),
            (50, 50, 100, 100, 80))
        self.fill_tree()
        self.lf_pesquisa_animal = LabelFrame(frame, text="Pesquisar animal")
        self.e_pesquisa_animal = Entry(self.lf_pesquisa_animal, text="Animal a ser pesquisado (Ex: 71)", width=15, font=60)
        self.b_pesquisa_animal = Button(self.lf_pesquisa_animal, text="Pesquisar")
        self.lf_animal_info = LabelFrame(frame, text="Informações do animal", bg="red")
        self.pack_on_frame()
        
    def pack_on_frame(self):
        self.lf_animal_info.place(relwidth=0.6, relheight=1, relx=0.4)
        self.lf_pesquisa_animal.place(relwidth=0.4, relheight=0.1)
        self.lf_todos_animais.place(relwidth=0.4, relheight=0.9, rely=0.1)
        self.e_pesquisa_animal.grid(row=0, column=1, padx=20, pady=20)
        self.b_pesquisa_animal.grid(row=0, column=2, padx=20, pady=20)
        self.tree.place(relwidth=1, relheight=0.9, rely=0.1)
    @property
    def animais_data_peso(self):
        return self.animal_.animais_data_peso

    def fill_tree(self):
        self.delete_all_tree()
        for i, animal in enumerate(self.lista):
            if animal[2] == datetime(1900, 1, 1, 0, 0):
                data = "Sem pesagem"
            else:
                data = animal[2].strftime("%d/%m/%Y")
            vals = [animal[0], animal[1], data, animal[3], animal[4]]
            self.tree.insert(parent="", index=END, iid=i, values=vals)

    def sort_by_heading(self,col):
        if self.tree_info_col_sort == col:
            self.tree_info_reverse_sort = not self.tree_info_reverse_sort
        else:
            self.tree_info_reverse_sort = True
        self.tree_info_col_sort = col
        self.delete_all_tree()
        self.lista= sorted(self.lista, key=lambda x: x[col], reverse=self.tree_info_reverse_sort)
        self.fill_tree()

    def generate_tree_info(self):
        try:
            self.delete_all_tree()
            self.lista = []
        except AttributeError:
            pass
        for animal in self.animal_.animais_data_peso:
            self.lista.append([animal, 0, datetime(1900, 1, 1, 0, 0), 0, "Não"])

        self.lista.sort()

        for i, animal in enumerate(self.lista):
            animal[3] = len(self.animais_data_peso[animal[0]])

        for i, animal in enumerate(self.lista):
            try:
                animal[1] = self.animais_data_peso[animal[0]][0][1]
                animal[2] = self.animais_data_peso[animal[0]][0][0]
            except IndexError:
                pass



class Animal:
    def __init__(self,frame_tree_info,frame_tree_dummy,frame_tree_edit,animais_data_peso,all_datas):
        self.frame_tree_info= frame_tree_info
        self.frame_tree_dummy = frame_tree_dummy
        self.animais_data_peso = animais_data_peso
        self.tree_info = TreeInfo(frame_tree_info,self)
        self.tree_dummy = TreeDummy(frame_tree_dummy,self)
        self.all_datas = all_datas
        self.tree_edit = TreeEdit(frame_tree_edit,self)


    def inserir_pesagem(self):
        was_conflict = False
        conflitos = []
        for animal, peso in self.tree_dummy.lista:
            if animal in self.tree_info.animais_data_peso.keys():
                for data_saved, peso_saved in self.tree_info.animais_data_peso[animal]:
                    if data_saved == self.tree_dummy.data:
                        if peso != peso_saved:
                            was_conflict = True
                            conflitos.append([animal, peso_saved])
            else:
                self.tree_info.animais_data_peso[animal] = []

        if not was_conflict:
            if isinstance(self.tree_dummy.data,bool):
                self.tree_dummy.update_info(f"É necessário escolher uma data para a pesagem.")
                return [True]
            for animal, peso in self.tree_dummy.lista:
                self.tree_info.animais_data_peso[animal].append((self.tree_dummy.data, peso))
                self.tree_info.animais_data_peso[animal] = sorted(self.tree_info.animais_data_peso[animal], reverse=True)
                print(animal)
            self.tree_dummy.update_info(f"Animais inseridos na base de dados: {len(self.tree_dummy.lista)} ")
            self.tree_info.generate_tree_info()
            self.tree_info.fill_tree()
            self.tree_dummy.delete_all_tree()
            self.tree_dummy.lista = []
            self.tree_dummy.update_sum_tree()
            self.tree_dummy.data = False
            self.tree_dummy.l_data_inserida.config(text="")
            if not (self.tree_dummy.data in self.all_datas):
                self.all_datas.append(self.tree_dummy.data)
        else:
            self.tree_dummy.update_info(f"Em {self.tree_dummy.data.strftime('%d/%m/%Y')} houve conflitos {conflitos}")

        return [was_conflict, conflitos]




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


def inserir_pesagem(animal):
    insertion_ok = animal.inserir_pesagem()[0]










