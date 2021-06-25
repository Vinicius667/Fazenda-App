from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from datetime import *
from tkcalendar import *
import matplotlib.pyplot as plt



def gotoframe(frame):
	frame.tkraise()


def what_was_selected_tree(e):
	tree = e.widget
	dic = {}
	regiao = tree.identify_region(e.x, e.y)
	dic["regiao"] = regiao
	if regiao == 'heading':
		coluna = tree.identify_column(e.x)
		dic["heading"] = coluna
	elif regiao == "cell":
		cells = [int(cell) for cell in tree.selection()]
		dic["cell"] = cells
	return dic

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
	def generate_tree(tree, columns, width):
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
	def __init__(self, frame, animal_):
		super().__init__(frame)
		self.animal_ = animal_
		self.l_info_pesagem = Label(frame, text="", bg="grey")
		self.generate_tree(self.tree, ("Animal", "Peso (kg)"), (50, 80))
		self.data = False
		self.l_data_inserida = Label(frame, text="", bg="grey")
		self.stringvar = StringVar(frame)
		self.stringvar.set("Selecione uma data")
		self.optionmenu = OptionMenu(frame, self.stringvar, *["Selecione uma data"])
		self.update_option_menu()
		self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
		self.b_selecionar_data_edit = Button(frame, text="Alterar data da pesagem",
											 command=lambda: self.data_selecionada_edit())
		self.dummy_lista = []
		self.data_option = False
		self.e_peso = Entry(frame)
		self.b_editar_peso = Button(frame, text="Editar peso", command=self.editar_peso)
		self.b_editar_data = Button(frame, text="Editar data", command=self.editar_data)
		self.l_info_edit = Label(frame)
		self.b_concluir = Button(frame, text="Concluir", command=self.concluir_alteracao)
		self.pack_on_frame()

	def editar_peso(self):
		self.e_peso.place(relwidth=0.05, relx=0.5, rely=0.5, anchor=CENTER)
		self.b_concluir.place(relwidth=0.05, relx=0.5, rely=0.6, anchor=CENTER)
		self.b_editar_peso.place_forget()
		self.b_editar_data.place_forget()

	def editar_data(self):
		self.cal.place(relx=0.5, rely=0.3, anchor=CENTER)
		self.b_selecionar_data_edit.place(relx=0.7, rely=0.3, anchor=CENTER)
		self.b_editar_peso.place_forget()
		self.b_editar_data.place_forget()

	def concluir_alteracao(self):
		self.b_editar_peso.place(relwidth=0.05, relx=0.45, rely=0.5, anchor=CENTER)
		self.b_editar_data.place(relwidth=0.05, relx=0.55, rely=0.5, anchor=CENTER)
		self.e_peso.place_forget()
		self.cal.place_forget()

	def pack_on_frame(self):
		# self.l_data_inserida.pack()
		self.optionmenu.place(relheight=0.07, relwidth=0.1, relx=0.5, rely=0.3, anchor=CENTER)
		self.tree.place(relwidth=0.2, relheight=1)
		self.stringvar.trace("w", self.update_tree)
		self.tree.bind("<Delete>", lambda e: self.tree_dummy_handler_delete(e))
		self.b_editar_peso.place(relwidth=0.05, relx=0.45, rely=0.5, anchor=CENTER)
		self.b_editar_data.place(relwidth=0.05, relx=0.55, rely=0.5, anchor=CENTER)

	def tree_dummy_handler_delete(self, e):
		was_selected = what_was_selected_tree(e)
		if was_selected["regiao"] == "cell":
			cells = was_selected["cell"]
			self.delete_list_cells(cells)

	def delete_list_cells(self, cells):
		self.delete_all_tree()
		for cell in cells:
			animal = self.dummy_lista[cell][0]
			self.animal_.animais_data_peso[animal].pop(self.data_option)
			if len(self.animal_.animais_data_peso[animal]) == 0:
				self.animal_.animais_data_peso.pop(animal)
		self.update_tree()

	def update_option_menu(self):
		"""Update self.optionmenu de acordo com self.animal_.all_datas"""
		self.optionmenu['menu'].delete(0, 'end')
		for date in self.animal_.all_datas:
			data = date.strftime("%d/%m/%Y")
			self.optionmenu['menu'].add_command(label=data, command=lambda value=data: self.stringvar.set(value))

	def update_tree(self, *args):
		try:
			"""Atualiza self.dummy_lista de acordo com animais_data_peso e preenche self.tree"""
			d, m, a = [int(el) for el in self.stringvar.get().split("/")]
			self.data_option = datetime(a, m, d)
			self.dummy_lista = []
			for animal, data_peso_ in self.animal_.animais_data_peso.items():
				try:
					self.dummy_lista.append([animal, data_peso_[self.data_option]])
				except KeyError:
					pass
			self.fill_tree()
		except ValueError:
			pass

	def fill_tree(self):
		"""Preenche self.tree com self.dummy_lista"""
		self.delete_all_tree()
		i = 0
		for animal, peso in self.dummy_lista:
			self.tree.insert(parent="", index=END, iid=i, values=[animal, peso])
			i += 1

	def data_selecionada_edit(self):
		self.data = self.cal2date(self.cal)
		self.l_data_inserida.config(text=self.data.strftime("%d/%m/%y"))
		was_conflict = False
		was_conflict_list = []
		for animal, peso in self.dummy_lista:
			try:
				peso_saved = self.animal_.animais_data_peso[animal][self.data]
				if peso_saved != peso:
					was_conflict = True
					was_conflict_list.append((animal, peso_saved))
			except KeyError:
				pass

		if not was_conflict:
			for animal, peso in self.dummy_lista:
				peso_saved = self.animal_.animais_data_peso[animal][self.data_option]
				self.animal_.animais_data_peso[animal][self.data] = peso_saved
			print("Data alterada")

		else:
			print("Houve conflitos")
			print(was_conflict_list)

	def update_frame_tree_edit(self,*args):
		self.update_option_menu()
		self.update_tree()


class TreeDummy(MyTree):
	"""Controla as treeinfos e a lista das treeinfos"""

	def __init__(self, frame, animal_):
		super().__init__(frame)
		self.animal_ = animal_
		self.lista = []
		self.l_info_pesagem = Label(frame, text="", bg="grey")
		self.generate_tree(self.tree, ("Animal", "Peso (kg)"), (50, 50))
		self.sum_tree = ttk.Treeview(frame)
		self.generate_tree(self.sum_tree, ("Quantidade", "Peso total"), (50, 50))
		self.data = False
		self.l_data_inserida = Label(frame, text="", bg="grey")
		self.e_animal = Entry(frame)
		self.e_peso = Entry(frame)
		self.l_animal = Label(frame, text="Animal", bg="grey")
		self.l_peso = Label(frame, text="Peso", bg="grey")
		self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
		self.b_pesagens = Button(frame, text="Pesagens", padx=30, pady=30, command=lambda: gotoframe(frame))
		self.b_selecionar_data_dummy = Button(frame, text="Seleciona data", command=self.data_selecionada_dummy)
		self.b_inserir_pesagem = Button(frame, text="Inserir pesagem", command=self.animal_.inserir_pesagem)
		self.pack_on_frame()

	def data_selecionada_dummy(self):
		self.data = self.cal2date(self.cal)
		self.l_data_inserida.config(text=self.data.strftime("%d/%m/%y"))

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
		self.e_peso.bind("<Return>", lambda e: self.tree_dummy_handler(e, "peso", ))
		self.tree.bind("<Delete>", lambda e: self.tree_dummy_handler_delete(e))

	def tree_dummy_handler_delete(self, e):
		was_selected = what_was_selected_tree(e)
		if was_selected[0] == "cell":
			cells = was_selected["cell"]
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

	def update_frame_dummy(self, *args):
		self.fill_tree()
		self.update_sum_tree()
		self.data = False
		self.l_data_inserida.config(text="")

	def fill_tree(self):
		if len(self.tree.get_children()) > 0:
			self.delete_all_tree()
		for i, item in enumerate(self.lista):
			self.tree.insert(parent="", index=END, iid=i, values=item)

	def delete_list_cells(self, cells):
		self.delete_all_tree()
		for i in sorted(cells, reverse=True):
			self.lista.pop(i)
		self.fill_tree()

	def insert_one(self, animal, peso):
		if animal in [animal[0] for animal in self.lista]:
			self.update_info(f"Animal {animal} já foi adicionado!")
			return [False, animal]
		self.delete_all_tree()
		self.lista.append([animal, peso])
		self.fill_tree()
		self.update_info()
		self.update_sum_tree()
		return True

	def update_info(self, texto=""):
		self.l_info_pesagem.config(text=texto)

	def update_sum_tree(self):
		soma = 0
		for animal, peso in self.lista:
			soma += peso
		self.sum_tree.delete(*self.sum_tree.get_children())
		self.sum_tree.insert(parent="", index=END, iid=0, values=[len(self.lista), soma])


class TreeInfo(MyTree):
	def __init__(self, frame, animal_):
		self.animal_ = animal_
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
		self.e_pesquisa_animal = Entry(self.lf_pesquisa_animal, text="Animal a ser pesquisado (Ex: 71)", width=15,
									   font=60)
		self.b_pesquisa_animal = Button(self.lf_pesquisa_animal, text="Pesquisar")
		self.lf_animal_info = LabelFrame(frame, text="Informações do animal", bg="red")
		self.animal_pesagens = ttk.Treeview(self.lf_animal_info)
		self.generate_tree(self.animal_pesagens, ("Data", "Peso (kg)"), (50, 80))



		self.pack_on_frame()

	def pack_on_frame(self):
		self.lf_animal_info.place(relwidth=0.6, relheight=1, relx=0.4)
		self.lf_pesquisa_animal.place(relwidth=0.4, relheight=0.1)
		self.lf_todos_animais.place(relwidth=0.4, relheight=0.9, rely=0.1)
		self.e_pesquisa_animal.grid(row=0, column=1, padx=20, pady=20)
		self.b_pesquisa_animal.grid(row=0, column=2, padx=20, pady=20)
		self.tree.place(relwidth=1, relheight=0.9, rely=0.1)
		self.tree.bind('<Button-1>', lambda e: self.tree_info_handler(e))
		self.tree.bind()
		self.l_image = Label()
		self.animal_pesagens.place(relwidth=0.5)

	def tree_info_handler(self, e):
		was_selected = what_was_selected_tree(e)
		regiao = was_selected["regiao"]
		if regiao == 'heading':
			coluna = was_selected["heading"]
			coluna = int(coluna[1:]) - 1
			self.sort_by_heading(coluna)
		elif regiao == "cell":
			cells = was_selected["cell"]
			self.tree_info_selected(cells)

	def tree_info_selected(self, cells):
		animais = [int(self.tree.set(cell,0)) for cell in cells]

		if len(animais) == 1:
			self.gerate_image(animais[0])
			self.fill_animal_pesagens(animais[0])

	def fill_animal_pesagens(self,animal):
		self.animal_pesagens.delete(*self.animal_pesagens.get_children())
		i =0
		for data,peso in self.animal_.animais_data_peso[animal].items():
			self.animal_pesagens.insert(parent="", index=END, iid=i, values=[data.strftime("%d/%m/%y"),peso])
			i+= 1
	def gerate_image(self,animal):
		fig = plt.figure()
		self.l_image.place_forget()
		pesos = [val for val in self.animal_.animais_data_peso[animal].values()]
		datas = [data for data in self.animal_.animais_data_peso[animal].keys()]
		plt.ylim((min(pesos)-30,max(pesos)+30))
		plt.xlim((min(datas) - timedelta(days=3), (max(datas)) + timedelta(days=len(datas)*10)))
		plt.grid()
		plt.xticks(datas,[data.strftime("%d/%m/%y") for data in datas],rotation=70)
		plt.plot(datas, pesos, 'bo-')
		plt.title(f"Animal {animal}")
		plt.tight_layout()

		for peso, data in zip(pesos,datas):
			plt.annotate('{}'.format(peso), xy=(data, peso), xytext=(10, -10), ha='left',
						textcoords='offset points')

		plt.savefig('fig.jpg', dpi=75)
		plt.close()
		self.img = ImageTk.PhotoImage(Image.open("fig.jpg"))#.resize((426, 320), Image.ANTIALIAS))
		self.l_image= Label(self.lf_animal_info,image=self.img)
		self.l_image.place(relx=0.5,rely=0.7,anchor=CENTER)








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

	def sort_by_heading(self, col):
		if self.tree_info_col_sort == col:
			self.tree_info_reverse_sort = not self.tree_info_reverse_sort
		else:
			self.tree_info_reverse_sort = True
		self.tree_info_col_sort = col
		self.delete_all_tree()
		self.lista = sorted(self.lista, key=lambda x: x[col], reverse=self.tree_info_reverse_sort)
		self.fill_tree()

	def generate_tree_info(self):
		try:
			self.delete_all_tree()
			self.lista = []
		except AttributeError:
			pass
		for animal, data_peso in self.animal_.animais_data_peso.items():
			pesagens = len(data_peso)
			ultima_pesagem = max(data_peso)
			peso = data_peso[ultima_pesagem]
			self.lista.append([animal, peso, ultima_pesagem, pesagens, "Não"])

		self.lista.sort()

	def update_frame_tree_info(self,*args):
		self.generate_tree_info()
		self.fill_tree()
		self.l_image.place_forget()


class Animal:
	def __init__(self, root, animais_data_peso, all_datas):
		self.frame_tree_dummy = Frame(root, bg="grey")
		self.frame_menu = Frame(root, bg="red")
		self.frame_tree_info = Frame(root, bg="green")
		self.frame_tree_edit= Frame(root, bg="blue")

		self.animais_data_peso = animais_data_peso
		self.tree_info = TreeInfo(self.frame_tree_info, self)
		self.tree_dummy = TreeDummy(self.frame_tree_dummy, self)
		self.all_datas = all_datas
		self.tree_edit = TreeEdit(self.frame_tree_edit, self)

		self.b_gado_macho_dados = Button(self.frame_menu, text="Dados", padx=30, pady=30,
									command=lambda: gotoframe(self.frame_tree_info))
		self.b_gado_macho_dados.place(relx=0.5, rely=0.3, anchor=CENTER)
		self.b_pesagens = Button(self.frame_menu, text="Pesagens", padx=30, pady=30,
							command=lambda: gotoframe(self.frame_tree_dummy))
		self.b_pesagens.place(relx=0.5, rely=0.5, anchor=CENTER)
		self.b_editar_pesagens = Button(self.frame_menu, text="Editar pesagens", padx=30, pady=30,
								   command=lambda: gotoframe(self.frame_tree_edit))
		self.b_editar_pesagens.place(relx=0.5, rely=0.7, anchor=CENTER)
		

		frames = (self.frame_tree_dummy,self.frame_menu,self.frame_tree_info,self.frame_tree_edit)
		for frame in frames:
			frame.grid(row=0, column=0, sticky="nsew")

		self.frame_menu.tkraise()

		for frame in frames:
			if frame != self.frame_menu:
				b_voltar_menu = Button(frame, text="Voltar ao menu", command=lambda: gotoframe(self.frame_menu))
				b_voltar_menu.place(relx=1, rely=0, anchor=NE)
		###### binding

		self.b_pesagens.bind('<Button-1>', lambda e: self.tree_dummy.update_frame_dummy(e))
		self.b_editar_pesagens.bind('<Button-1>', lambda e: self.tree_edit.update_frame_tree_edit(e))
		self.b_gado_macho_dados.bind('<Button-1>', lambda e: self.tree_info.update_frame_tree_info(e))

	def inserir_pesagem(self):
		was_conflict = False
		conflitos = []
		for animal, peso in self.tree_dummy.lista:
			if animal in self.tree_info.animais_data_peso.keys():
				for data_saved, peso_saved in self.animais_data_peso[animal].items():
					if data_saved == self.tree_dummy.data:
						if peso != peso_saved:
							was_conflict = True
							conflitos.append([animal, peso_saved])
			else:
				self.animais_data_peso[animal] = {}

		if not was_conflict:
			if isinstance(self.tree_dummy.data, bool):
				self.tree_dummy.update_info(f"É necessário escolher uma data para a pesagem.")
				return [True]
			for animal, peso in self.tree_dummy.lista:
				self.tree_info.animais_data_peso[animal][self.tree_dummy.data] = peso
				print(animal)
			if not (self.tree_dummy.data in self.all_datas):
				self.all_datas.append(self.tree_dummy.data)
				print("Nova data inserida")
			self.tree_dummy.update_info(texto=f"Animais inseridos na base de dados: {len(self.tree_dummy.lista)} ")
			self.tree_dummy.lista = []
			self.tree_dummy.update_frame_dummy()

		else:
			self.tree_dummy.update_info(f"Em {self.tree_dummy.data.strftime('%d/%m/%Y')} houve conflitos {conflitos}")

		return [was_conflict, conflitos]
