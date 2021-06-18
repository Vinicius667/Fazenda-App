from tkinter import *
# from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
import excel_handler


def gotoframe(frame):
    frame.tkraise()


def generate_tree(tree, columns, width):
    tree["columns"] = columns
    tree.column("#0", width=0, stretch=NO)
    for col, wid in zip(columns, width):
        tree.column(col, width=wid, minwidth=wid, anchor=CENTER)
    tree.heading("#0", text="")
    for col, wid in zip(columns, width):
        tree.heading(col, text=col, anchor=CENTER)


def what_was_selected_tree(e):
    tree = e.widget
    regiao = tree.identify_region(e.x, e.y)
    if regiao == 'heading':
        coluna = tree.identify_column(e.x)
        return ['heading', coluna]
    elif regiao == "cell":
        cells = [int(cell) for cell in tree.selection()]
        return ['cell', cells]


def delete_all_tree(tree):
    tree.delete(*tree.get_children())


# apenas para tree que sao preenchicas com listas sem aninhamento eg: tree_dummy_pesos
'''
def fill_tree(tree, lista):
    if len(tree.get_children()) > 0:
        delete_all_tree(tree)
    for i, item in enumerate(lista):
        tree.insert(parent="", index=END, iid=i, values=item)


def delete_cells_tree(tree, cells):
    tree.delete(cells)


def delete_list_cells_and_fill_tree(tree, cells, lista):
    for i in sorted(cells, reverse=True):
        lista.pop(i)
    fill_tree(tree, lista)

'''

######### tree_info







# [(animal,peso)] => {animal:[[data,peso]]}
def dummy_to_data_peso(dummy_animal_peso, animais_data_peso, data):
    was_conflict = False
    conflitos = []
    for animal, peso in dummy_animal_peso:
        if animal in animais_data_peso.keys():
            for data_saved, peso_saved in animais_data_peso[animal]:
                if data_saved == data:
                    if peso != peso_saved:
                        was_conflict = True
                        conflitos.append([animal, peso_saved])
        else:
            animais_data_peso[animal] = []

    if not was_conflict:
        for animal, peso in dummy_animal_peso:
            animais_data_peso[animal].append((data, peso))
            animais_data_peso[animal] = sorted(animais_data_peso[animal], reverse=True)
            print(animal)
            print(animais_data_peso[animal])

    return [was_conflict, conflitos]


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


class TreeDummy(MyTree):
    """Controla as treeinfos e a lista das treeinfos"""

    def __init__(self, frame):
        self.lista = []
        super().__init__(frame)

    def fill_tree(self):
        if len(self.tree.get_children()) > 0:
            delete_all_tree(self.tree)
        for i, item in enumerate(self.lista):
            self.tree.insert(parent="", index=END, iid=i, values=item)

    def delete_list_cells(self, cells):
        self.delete_all_tree()
        for i in sorted(cells, reverse=True):
            self.lista.pop(i)
        self.fill_tree()

    def insert_one(self,animal,peso):
        self.delete_all_tree()
        self.lista.append([animal,peso])
        self.fill_tree()


class TreeInfo(MyTree):
    def __init__(self, frame,animais_data_peso):
        super().__init__(frame)
        self.animais_data_peso = animais_data_peso
        self.lista = []
        self.generate_tree_info()
        self.tree_info_col_sort = 0
        self.tree_info_reverse_sort = False


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
            self.tree_info_reverse_sort = False
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
        for animal in self.animais_data_peso:
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
    def __init__(self,frame_ti,frame_td,animais_data_peso):
        self.frame_ti= frame_ti
        self.tree_info = TreeInfo(frame_ti,animais_data_peso)
        self.tree_dummy = TreeDummy(frame_td)



    def inserir_pesagem(self,data):
        was_conflict = False
        conflitos = []
        for animal, peso in self.tree_dummy.lista:
            if animal in self.tree_info.animais_data_peso.keys():
                for data_saved, peso_saved in self.tree_info.animais_data_peso[animal]:
                    if data_saved == data:
                        if peso != peso_saved:
                            was_conflict = True
                            conflitos.append([animal, peso_saved])
            else:
                self.tree_info.animais_data_peso[animal] = []

        if not was_conflict:
            for animal, peso in self.tree_dummy.lista:
                self.tree_info.animais_data_peso[animal].append((data, peso))
                self.tree_info.animais_data_peso[animal] = sorted(self.tree_info.animais_data_peso[animal], reverse=True)
                print(animal)
        self.tree_info.generate_tree_info()
        self.tree_info.fill_tree()
        self.tree_dummy.delete_all_tree()
        self.tree_dummy.lista = []
        print(len(self.tree_info.lista))
        print(len(self.tree_info.lista))
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
        ("Animal", "Peso", "Ultima pesagem", "Pesagens", "Engorda"),
        (50, 50, 100, 100, 80))

    macho.tree_info.fill_tree()
    macho.tree_info.tree.pack()
    macho.tree_info.sort_by_heading(2)

    root.mainloop()