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

    def generate_tree(self, columns, width):
        self.tree["columns"] = columns
        self.tree.column("#0", width=0, stretch=NO)
        for col, wid in zip(columns, width):
            self.tree.column(col, width=wid, minwidth=wid, anchor=CENTER)
        self.tree.heading("#0", text="")
        for col, wid in zip(columns, width):
            self.tree.heading(col, text=col, anchor=CENTER)

    def delete_all_tree(self):
        self.tree.delete(*self.tree.get_children())


class TreeEdit(MyTree):
    def __init__(self,frame,animal_):
        super().__init__(frame)
        self.animal_ = animal_
        self.l_info_pesagem = Label(frame, text="", bg="grey")
        self.generate_tree(("Animal","Peso (kg)"),(50,80))
        self.data = False
        self.l_data_inserida = Label(frame,text="",bg="grey")
        self.stringvar = StringVar(frame)
        self.stringvar.set("Selecione uma data")
        self.optionmenu = OptionMenu(frame, self.stringvar, *["Selecione uma data"])
        self.update_option_menu()

    def update_option_menu(self):
        self.optionmenu['menu'].delete(0, 'end')
        for datetime in self.animal_.all_datas:
            data = datetime.strftime("%d/%m/%Y")
            self.optionmenu['menu'].add_command(label=data,command=lambda value=data: self.stringvar.set(value))



    def delete_cells(self):
        pass






class TreeDummy(MyTree):
    """Controla as treeinfos e a lista das treeinfos"""

    def __init__(self, frame):
        super().__init__(frame)
        self.lista = []
        self.l_info_pesagem = Label(frame, text="", bg="grey")
        self.generate_tree(("Animal","Peso (kg)"),(50,50))
        self.sum_tree = ttk.Treeview(frame)
        self.generate_sum_tree(("Quantidade","Peso total"),(50,50))
        self.data = False
        self.l_data_inserida = Label(frame,text="",bg="grey")
        self.e_animal = Entry(frame)
        self.e_peso = Entry(frame)
        self.l_animal = Label(frame, text="Animal", bg="grey")
        self.l_peso = Label(frame, text="Peso", bg="grey")
        self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
        self.pack_on_frame()

        
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

    def generate_sum_tree(self, columns, width):
        self.sum_tree["columns"] = columns
        self.sum_tree.column("#0", width=0, stretch=NO)
        for col, wid in zip(columns, width):
            self.sum_tree.column(col, width=wid, minwidth=wid, anchor=CENTER)
        self.sum_tree.heading("#0", text="")
        for col, wid in zip(columns, width):
            self.sum_tree.heading(col, text=col, anchor=CENTER)

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
        super().__init__(frame)
        self.animal_ = animal_
        #self.animais_data_peso = animais_data_peso
        self.lista = []
        self.generate_tree_info()
        self.tree_info_col_sort = 0
        self.tree_info_reverse_sort = False
        self.generate_tree(
            ("Animal", "Peso (kg)", "Ultima pesagem", "Pesagens", "Engorda"),
            (50, 50, 100, 100, 80))
        self.fill_tree()


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
        self.tree_dummy = TreeDummy(frame_tree_dummy)
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


if __name__ == "__main__":
    animais_data_peso = pickle.load(open("animais_data_peso.pkl", "rb"))
    animais_data_peso = {200: animais_data_peso[200], 216: animais_data_peso[216]}
    animais_tree_info = []
    animais_tree_info = excel_handler.generate_tree_info(animais_data_peso, animais_tree_info)


    root = Tk()
    create_screen(root)
    frame = Frame(root,bg="pink")
    frame.grid(row=0, column=0, sticky="nsew")

    macho = Animal(frame,frame,animais_tree_info)


    macho.tree_info.generate_tree(
        ("Animal", "Peso (kg)", "Ultima pesagem", "Pesagens", "Engorda"),
        (50, 50, 100, 100, 80))

    macho.tree_info.fill_tree()
    macho.tree_info.tree.pack()
    macho.tree_info.sort_by_heading(2)

    root.mainloop()


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



def tree_dummy_handler(e,animal,tipo,e_animal,e_peso):
    try:
        entrada_animal = e_animal.get()
        entrada_peso = e_peso.get()
        value_animal = int(entrada_animal)
        valie_peso = float(entrada_peso)
        e_peso.delete(0,END)
        e_animal.delete(0,END)
        insertion_ok = animal.tree_dummy.insert_one(value_animal,valie_peso)
    except ValueError:
        if entrada_animal != "" and entrada_peso != "":
            animal.tree_dummy.update_info("Animal e peso devem ser números.")
    if tipo == "animal":
        e_peso.focus()
    elif tipo == "peso":
        e_animal.focus()


def tree_dummy_handler_delete(e,animal):
    was_selected = what_was_selected_tree(e)
    if was_selected[0] == "cell":
        cells= was_selected[1]
        animal.tree_dummy.delete_list_cells(cells)


def update_pesagens_frame(e,animal):
    animal.tree_dummy.update_info("")
    animal.tree_dummy.update_sum_tree()

