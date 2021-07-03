from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import pickle
from datetime import *
from tkcalendar import *
import matplotlib.pyplot as plt
from tkinter import messagebox
#import traceback
#traceback.print_exc()

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


class TreeInfo(MyTree):
	def __init__(self, frame, animal_):
		self.sv_sexo = StringVar()
		self.sv_sexo.set("macho")
		self.animal_ = animal_
		self.lf_todos_animais = LabelFrame(frame, text="Todos animais")
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
		self.b_pesquisa_animal = Button(self.lf_pesquisa_animal, text="Pesquisar", command=self.pesquisar_animal)
		self.lf_animal_info = LabelFrame(frame, text="Informações do animal")
		self.animal_pesagens_tree = ttk.Treeview(self.lf_animal_info)
		self.generate_tree(self.animal_pesagens_tree, ("Data", "Peso (kg)"), (50, 80))
		self.rb_macho = Radiobutton(self.lf_todos_animais, text="macho", value="macho", variable=self.sv_sexo,
									command=self.update_sexo)
		self.rb_femea = Radiobutton(self.lf_todos_animais, text="femea", value="femea", variable=self.sv_sexo,
									command=self.update_sexo)

		self.l_animal = Label(self.lf_animal_info, text="Animal:", font=("Arial", 15))
		self.l_pai = Label(self.lf_animal_info, text="Pai:", font=("Arial", 15))
		self.l_mae = Label(self.lf_animal_info, text="Mãe:", font=("Arial", 15))
		self.l_dn = Label(self.lf_animal_info, text="Data de nascimento:", font=("Arial", 15))
		self.l_sexo = Label(self.lf_animal_info, text="Sexo:", font=("Arial", 15))
		self.t_obs = Text(self.lf_animal_info, font=("Arial", 12))

		self.last_animal_selected = False

		self.pack_on_frame()

	def pesquisar_animal(self, *args):
		animal_pesquisado = int(self.e_pesquisa_animal.get())
		print(animal_pesquisado)

		for i in range(len(self.tree.get_children())):
			animal = int(self.tree.set(i)["Animal"])
			if animal == animal_pesquisado:
				self.tree.selection_remove(self.tree.selection())
				self.tree.selection_add(i)
				self.animal_selected([i])
				break

	def update_sexo(self):
		self.update_frame_tree_info()
		self.update_infos_animal()
		sexo = self.sv_sexo.get()
		if sexo == "macho":
			print("Remover widgets")
		else:
			print("Colocar widgets")
		print("update")

	def go_to_pesagen(self,e):
		was_selected = what_was_selected_tree(e)
		if was_selected["regiao"] == "cell":
			cell = was_selected["cell"][0]
			tree = e.widget
			d,m,y = [int(el) for el in tree.set(cell)["Data"].split("/")]
			y += 2000
			gotoframe(self.animal_.frame_tree_peso)
			self.animal_.tree_peso.sv_sexo.set(self.sv_sexo.get())
			self.animal_.tree_peso.cal.selection_set(date(y,m,d))
			self.animal_.tree_peso.data_selecionada()

	def pack_on_frame(self):
		self.lf_animal_info.place(relwidth=0.6, relheight=1, relx=0.4)
		self.lf_pesquisa_animal.place(relwidth=0.4, relheight=0.1)
		self.lf_todos_animais.place(relwidth=0.4, relheight=0.9, rely=0.1)
		self.e_pesquisa_animal.grid(row=0, column=1, padx=20, pady=20)
		self.e_pesquisa_animal.bind("<Return>", self.pesquisar_animal)
		self.b_pesquisa_animal.grid(row=0, column=2, padx=20, pady=20)
		self.tree.place(relwidth=1, relheight=0.9, rely=0.1)
		self.tree.bind('<ButtonRelease-1>', lambda e: self.tree_info_handler(e))
		self.tree.bind()
		self.l_image = Label()
		self.animal_pesagens_tree.place(relwidth=0.40, rely=0.47, relheight=0.53)

		self.animal_pesagens_tree.bind("<Double-Button-1>",lambda e : self.go_to_pesagen(e))


		self.rb_macho.place(relx=0.1, rely=0.037)
		self.rb_femea.place(relx=0.3, rely=0.037)

		self.l_animal.place(relx=0.05, rely=0.05)
		self.l_sexo.place(relx=0.05, rely=0.25)
		self.l_dn.place(relx=0.05, rely=0.1)
		self.l_pai.place(relx=0.05, rely=0.15)
		self.l_mae.place(relx=0.05, rely=0.20)
		self.t_obs.place(relx=0.7, relheight=0.45, relwidth=0.3,rely=0.02)
		self.t_obs.bind("<FocusOut>", lambda e: self.save_obs(e))

	def save_obs(self, *args):
		if self.last_animal_selected:
			sexo = self.sv_sexo.get()
			texto = self.t_obs.get("1.0", "end-1c")
			# self.t_obs.delete("1.0","end-1c")
			self.animal_.animais_info[sexo][self.last_animal_selected]["obs"] = texto

	def tree_info_handler(self, e):
		was_selected = what_was_selected_tree(e)
		regiao = was_selected["regiao"]
		if regiao == 'heading':
			coluna = was_selected["heading"]
			coluna = int(coluna[1:]) - 1
			self.sort_by_heading(coluna)
		elif regiao == "cell":
			cells = was_selected["cell"]
			self.animal_selected(cells)

	def animal_selected(self, cells):
		animais = [int(self.tree.set(cell, 0)) for cell in cells]

		if len(animais) == 1:
			self.last_animal_selected = animais[0]
			self.generate_image(animais[0])
			self.fill_animal_pesagens(animais[0])
			self.update_infos_animal(animais[0])

	def update_infos_animal(self, animal=False):
		if not animal:
			sexo = ""
			dn = ""
			animal_num = ""
			self.l_animal.config(text=f"Animal: {animal_num}")
			mae = ""
			pai = ""

			self.l_pai.config(text=f"Pai: {pai}")
			self.l_mae.config(text=f"Mãe: {mae}")
			self.l_dn.config(text=f"Data de nascimento: {dn}")
			self.l_sexo.config(text=f"Sexo: {sexo}")

		if animal:
			sexo = self.sv_sexo.get()
			self.l_animal.config(text=f"Animal: {animal}")
			dn = self.animal_.animais_info[sexo][animal]["DN"]
			mae = self.animal_.animais_info[sexo][animal]["mae"]
			pai = self.animal_.animais_info[sexo][animal]["pai"]

			texto = self.animal_.animais_info[sexo][self.last_animal_selected]["obs"]
			self.t_obs.delete("1.0", "end-1c")
			self.t_obs.insert(END, texto)

			if pai:
				self.l_pai.config(text=f"Pai: {pai}")
			if mae:
				self.l_mae.config(text=f"Mãe: {mae}")
			if dn:
				self.l_dn.config(text=f"Data de nascimento: {dn.strftime('%d/%m/%y')}")
			if sexo:
				self.l_sexo.config(text=f"Sexo: {sexo}")

	def fill_animal_pesagens(self, animal):
		self.animal_pesagens_tree.delete(*self.animal_pesagens_tree.get_children())
		i = 0
		for data, peso in self.animal_.animais_info[self.sv_sexo.get()][animal]["pesagens"].items():
			self.animal_pesagens_tree.insert(parent="", index=END, iid=i, values=[data.strftime("%d/%m/%y"), peso])
			i += 1

	def generate_image(self, animal):
		fig = plt.figure()
		self.l_image.place_forget()
		pesos = [val for val in self.animal_.animais_info[self.sv_sexo.get()][animal]["pesagens"].values()]
		datas = [data for data in self.animal_.animais_info[self.sv_sexo.get()][animal]["pesagens"].keys()]
		plt.ylim((min(pesos) - 30, max(pesos) + 30))
		plt.xlim((min(datas) - timedelta(days=3), (max(datas)) + timedelta(days=len(datas) * 10)))
		plt.grid()
		plt.xticks(datas, [data.strftime("%d/%m/%y") for data in datas], rotation=70)
		plt.plot(datas, pesos, 'bo-')
		plt.title(f"Animal {animal}")
		plt.tight_layout()

		for peso, data in zip(pesos, datas):
			plt.annotate('{}'.format(peso), xy=(data, peso), xytext=(10, -10), ha='left',
						 textcoords='offset points')

		plt.savefig('fig.jpg', dpi=75)
		plt.close()
		self.img = ImageTk.PhotoImage(Image.open("fig.jpg"))  # .resize((426, 320), Image.ANTIALIAS))
		self.l_image = Label(self.lf_animal_info, image=self.img)
		self.l_image.place(relx=0.41, rely=0.47)

	@property
	def animais_info(self):
		return self.animal_.animais_info



	def fill_tree(self):
		self.delete_all_tree()
		for i, animal in enumerate(self.lista):
			if animal[2] == datetime(1900, 1, 1, 0, 0):
				data = "Sem pesagem"
			else:
				data = animal[2].strftime("%d/%m/%Y")
			vals = [f'{animal[0]:03}', animal[1], data, animal[3], animal[4]]
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
		for animal, data_peso_etc in self.animal_.animais_info[self.sv_sexo.get()].items():
			data_peso = data_peso_etc["pesagens"]
			pesagens = len(data_peso)
			try:
				ultima_pesagem = max(data_peso)
			except:
				pass
			peso = data_peso[ultima_pesagem]
			engorda = "Não"
			if ultima_pesagem in self.animal_.animais_info[self.sv_sexo.get()][animal]["engorda"]:
				engorda = "Sim"
			self.lista.append([animal, peso, ultima_pesagem, pesagens, engorda])

		self.lista.sort()

	def update_frame_tree_info(self, *args):
		self.generate_tree_info()
		self.fill_tree()
		self.l_image.place_forget()
		self.animal_pesagens_tree.delete(*self.animal_pesagens_tree.get_children())


class Animal:
	def __init__(self, root, animais_info, all_datas):
		self.frame_tree_peso = Frame(root,bg="#F0F0F0")
		self.frame_menu = Frame(root,bg="#F0F0F0")
		self.frame_tree_info = Frame(root,bg="#F0F0F0")
		self.frame_tree_edit = Frame(root)

		self.animais_info = animais_info
		self.obs = {}
		self.tree_info = TreeInfo(self.frame_tree_info, self)
		self.tree_peso = TreePeso(self.frame_tree_peso, self)
		self.all_datas = all_datas

		self.b_gado_macho_dados = Button(self.frame_menu, text="Dados", padx=30, pady=30,
										 command=lambda: gotoframe(self.frame_tree_info))
		self.b_gado_macho_dados.place(relx=0.5, rely=0.3, anchor=CENTER)
		self.b_pesagens = Button(self.frame_menu, text="Pesagens", padx=30, pady=30,
								 command=lambda: gotoframe(self.frame_tree_peso))
		self.b_pesagens.place(relx=0.5, rely=0.5, anchor=CENTER)
		self.b_editar_pesagens = Button(self.frame_menu, text="Editar pesagens", padx=30, pady=30,
										command=lambda: gotoframe(self.frame_tree_edit))
		self.b_editar_pesagens.place(relx=0.5, rely=0.7, anchor=CENTER)

		frames = (self.frame_tree_peso, self.frame_menu, self.frame_tree_info, self.frame_tree_edit)
		for frame in frames:
			frame.grid(row=0, column=0, sticky="nsew")

		self.frame_menu.tkraise()

		for frame in frames:
			if frame != self.frame_menu:
				b_voltar_menu = Button(frame, text="Voltar ao menu", command=lambda: gotoframe(self.frame_menu))
				b_voltar_menu.place(relx=1, rely=0, anchor=NE)
		###### binding

		self.b_pesagens.bind('<Button-1>', lambda e: self.tree_peso.update_frame_tree_peso(e))
		self.b_editar_pesagens.bind('<Button-1>', lambda e: self.tree_edit.update_frame_tree_edit(e))
		self.b_gado_macho_dados.bind('<Button-1>', lambda e: self.tree_info.update_frame_tree_info(e))

	def inserir_pesagem(self):
		was_conflict = False
		conflitos = []
		for animal, peso in self.tree_insert.lista:
			if animal in self.tree_info.animais_info.keys():
				for data_saved, peso_saved in self.animais_info[animal].items():
					if data_saved == self.tree_insert.data:
						if peso != peso_saved:
							was_conflict = True
							conflitos.append([animal, peso_saved])
			else:
				self.animais_info[animal] = {}

		if not was_conflict:
			if isinstance(self.tree_insert.data, bool):
				self.tree_insert.update_info(f"É necessário escolher uma data para a pesagem.")
				return [True]
			for animal, peso in self.tree_insert.lista:
				self.tree_info.animais_info[animal][self.tree_insert.data] = peso
				print(animal)
			if not (self.tree_insert.data in self.all_datas):
				self.all_datas.append(self.tree_insert.data)
				print("Nova data inserida")
			self.tree_insert.update_info(texto=f"Animais inseridos na base de dados: {len(self.tree_insert.lista)} ")
			self.tree_insert.lista = []
			self.tree_insert.update_frame_insert()

		else:
			self.tree_insert.update_info(f"Em {self.tree_insert.data.strftime('%d/%m/%Y')} houve conflitos {conflitos}")

		return [was_conflict, conflitos]


class TreePeso(MyTree):
	def __init__(self, frame, animal_):
		self.frame = frame
		self.animal_ = animal_
		super().__init__(self.frame)

		self.femea_tree = ttk.Treeview(frame)
		self.generate_tree(self.femea_tree, ["Animal", "Peso", "Engorda", "Prenhez"], [50, 50, 70, 50])

		self.macho_tree = ttk.Treeview(frame)
		self.generate_tree(self.macho_tree, ["Animal", "Peso", "Engorda"], [50, 50, 50])

		self.sv_sexo = StringVar()
		self.sv_sexo.set("macho")

		self.sexo = self.sv_sexo.get()

		self.rb_macho = Radiobutton(self.frame, text="macho", value="macho", variable=self.sv_sexo,
									command=self.insert_entradas)
		self.rb_femea = Radiobutton(self.frame, text="femea", value="femea", variable=self.sv_sexo,
									command=self.insert_entradas)

		self.cal = Calendar(frame, firstweekday="sunday", showweeknumbers=False, locale="pt_BR")
		self.data = False
		self.l_data_inserida = Label(frame, text="Selecione uma data", font=20)

		self.e_peso = Entry(frame)
		self.e_animal = Entry(frame)

		self.l_info_pesagem = Label(frame, text="", font=6)

		self.sv_engorda = StringVar()
		self.sv_engorda.set("Não")
		self.om_engorda = OptionMenu(frame, self.sv_engorda, *["Nao", "Sim"])
		self.l_engorda = Label(frame,text="Engorda:",font=8)

		self.sv_prenhez = StringVar()
		self.sv_prenhez.set("Não")
		self.om_prenhez = OptionMenu(frame, self.sv_prenhez, *["Nao", "Sim"])
		self.l_prenhez = Label(frame,text="Prenha:",font=8)

		self.bv_overwrite = BooleanVar()
		self.bv_overwrite.set(False)
		self.cb_overwrite = Checkbutton(frame, text="Sobrescrever pesagens sem confirmação prévia",
										variable=self.bv_overwrite, onvalue=True, offvalue=False)

		self.macho_tree_sort_col = -1
		self.macho_tree_sort_reverse = False
		self.femea_tree_sort_col = 1
		self.femea_tree_sort_reverse = False

		self.b_alteracao_massa = Button(frame,text="Confirmar alteração em massa",command=self.alteracao_massa)
		self.b_cancel_alteracao_massa = Button(frame,text="Cancelar alteração em massa",command=self.massa_to_single)

		self.b_confirma = Button(frame, text="Confirmar", command=lambda: self.tree_insert_handler(tipo="peso"))
		self.b_apagar = Button(frame, text="Apagar", command= self.apagar_entradas)


		self.tree_pesagem_info_macho1 = ttk.Treeview(frame)
		self.generate_tree(self.tree_pesagem_info_macho1, ["Animais", "Média (kg)", "Total (kg)"], [60, 60, 60])

		self.tree_pesagem_info_macho2 = ttk.Treeview(frame)
		self.generate_tree(self.tree_pesagem_info_macho2, ["Em engorda", "Média (@)", "Total (@)"], [60, 60, 60])



		self.tree_pesagem_info_femea1 = ttk.Treeview(frame)
		self.generate_tree(self.tree_pesagem_info_femea1, ["Animais", "Média (kg)", "Total (kg)"], [60, 60, 60])

		self.tree_pesagem_info_femea2 = ttk.Treeview(frame)
		self.generate_tree(self.tree_pesagem_info_femea2, ["Em engorda", "Média (@)", "Total (@)"], [60, 60, 60])

		self.pack_on_frame()



	def apagar_entradas(self):
		self.sv_prenhez.set("Não")
		self.sv_engorda.set("Não")
		self.e_animal.delete(0, "end")
		self.e_peso.delete(0, "end")


	def pack_on_frame(self):
		self.macho_tree.place(rely=0.04, relheight=0.8, relwidth=0.2)
		self.tree_pesagem_info_macho1.place(rely=0.84, relheight=0.06, relwidth=0.2)
		self.tree_pesagem_info_macho2.place(rely=0.9, relheight=0.06, relwidth=0.2)

		self.femea_tree.place(relx=0.7, rely=0.04, relwidth=0.3, relheight=0.8)
		self.tree_pesagem_info_femea1.place(relx=0.7,rely=0.84, relheight=0.06, relwidth=0.2)
		self.tree_pesagem_info_femea2.place(relx=0.7,rely=0.9, relheight=0.06, relwidth=0.2)

		self.rb_macho.place(relx=0.42, rely=0.37, anchor=CENTER)
		self.rb_femea.place(relx=0.48, rely=0.37, anchor=CENTER)

		self.cal.place(relx=0.45, rely=0.13, anchor=CENTER)
		self.cal.bind("<<CalendarSelected>>", self.data_selecionada)

		self.l_data_inserida.place(relx=0.45, rely=0.27, anchor=CENTER)

		self.e_animal.bind("<Return>", lambda e: self.tree_insert_handler(e,tipo= "animal"))
		self.e_peso.bind("<Return>", lambda e: self.tree_insert_handler(e,tipo= "peso", ))

		self.l_info_pesagem.place(relx=0.45, rely=0.32, anchor=CENTER)
		self.update_info("Data não inserida.")

		self.femea_tree.bind('<ButtonRelease-1>', lambda e: self.tree_peso_handler(e))
		self.macho_tree.bind('<ButtonRelease-1>', lambda e: self.tree_peso_handler(e))

		self.macho_tree.bind('<Delete>',lambda e: self.delete_animal(e))
		self.femea_tree.bind('<Delete>', lambda e: self.delete_animal(e))

	def delete_animal(self,e):
		tree = e.widget
		was_selected = what_was_selected_tree(e)
		if tree == self.macho_tree:
			sexo_list = "macho"
		else:
			sexo_list = "femea"


		if was_selected["regiao"] == "cell":
			cells = was_selected["cell"]

			animais = [int(tree.set(i)["Animal"]) for i in cells]

			for animal in animais:
				self.animal_.animais_info[sexo_list][animal]["pesagens"].pop(self.data)

		if sexo_list == "macho":
			self.fill_macho_tree()
		else:
			self.fill_femea_tree()

	def tree_peso_handler(self,e):
		was_selected = what_was_selected_tree(e)
		regiao = was_selected["regiao"]
		tree = e.widget
		if tree == self.macho_tree:
			sexo_list = "macho"
		else:
			sexo_list = "femea"
		self.sexo = sexo_list
		if regiao == "cell":
			cells = was_selected["cell"]

			if sexo_list == "macho":
				self.sv_sexo.set("macho")
			elif sexo_list == "femea":
				self.sv_sexo.set("femea")
				self.insert_femea_entradas()

			if len(cells) == 1:
				self.massa_to_single()
				cell = cells[0]
				dict_info = tree.set(cell)
				animal =  dict_info["Animal"]
				peso = dict_info["Peso"]
				engorda = dict_info["Engorda"]

				if sexo_list == "femea":
					self.sv_prenhez.set(dict_info["Prenhez"])
				self.insert_entradas()
				self.e_animal.delete(0,"end")
				self.e_animal.insert(0,animal)
				self.e_peso.delete(0, "end")
				self.e_peso.insert(0, peso)

				self.sv_engorda.set(engorda)

			else:
				self.delete_entrada_animal_peso()
				self.cb_overwrite.place_forget()
				self.b_alteracao_massa.place(relx=0.45, rely=0.5, anchor=CENTER)
				self.b_cancel_alteracao_massa.place(relx=0.45, rely=0.55, anchor=CENTER)
				self.rb_femea.place_forget()
				self.rb_macho.place_forget()




				self.alt_cells = cells
				self.alt_tree = tree


		elif regiao == "heading":
			coluna = int(was_selected["heading"][-1])-1
			if sexo_list == "macho":
				self.fill_macho_tree(sort=True,col=coluna)
			else:
				self.fill_femea_tree(sort=True, col=coluna)

	def massa_to_single(self):
		self.insert_entradas()
		self.b_cancel_alteracao_massa.place_forget()
		self.b_alteracao_massa.place_forget()


	def alteracao_massa(self):
		for cell in self.alt_cells:
			animal = self.alt_tree.set(cell)["Animal"]
			self.check_engorda(int(animal))
			if self.sexo == "femea":
				self.check_prenhez(int(animal))
		self.insert_entradas()
		self.massa_to_single()
		self.fill_femea_tree()
		self.fill_macho_tree()



	def update_info(self, texto=""):
		self.l_info_pesagem.config(text=texto)

	def tree_insert_handler(self, *args, tipo):
		try:
			entrada_animal = self.e_animal.get()
			entrada_peso = self.e_peso.get()
			value_animal = int(entrada_animal)
			value_peso = float(entrada_peso)
			self.e_peso.delete(0, END)
			self.e_animal.delete(0, END)
			self.insert_one(value_animal, value_peso)
		except ValueError:
			if entrada_animal != "" and entrada_peso != "":
				self.update_info("Animal e peso devem ser números.")
		if tipo == "animal":
			self.e_peso.focus()
		elif tipo == "peso":
			self.e_animal.focus()

	def fill_macho_tree(self,sort=False,col=1):
		dummy_lista = []
		try:
			self.macho_tree.delete(*self.macho_tree.get_children())
			self.tree_pesagem_info_macho1.delete(*self.tree_pesagem_info_macho1.get_children())
			self.tree_pesagem_info_macho2.delete(*self.tree_pesagem_info_macho2.get_children())
		except:
			pass
		for i, animal in enumerate(self.animal_.animais_info["macho"].keys()):
			try:
				peso = self.animal_.animais_info["macho"][animal]["pesagens"][self.data]
			except KeyError:
				continue
			if max(self.animal_.animais_info["macho"][animal]["pesagens"]) in \
					self.animal_.animais_info["macho"][animal]["engorda"]:
				engorda = "Sim"
			else:
				engorda = "Não"
			dummy_lista.append([f"{animal:03}", peso, engorda])

		if sort:
			if col == self.macho_tree_sort_col:
				self.macho_tree_sort_reverse = not self.macho_tree_sort_reverse
			else:
				self.macho_tree_sort_reverse = False
			dummy_lista = sorted(dummy_lista,key= lambda x:x[col],reverse=self.macho_tree_sort_reverse)
			self.macho_tree_sort_col = col

		for i,lista in enumerate(dummy_lista):
			self.macho_tree.insert(parent="", index=END, iid=i, values=lista)

		quantidade = len(dummy_lista)
		soma = 0
		for el in dummy_lista:
			soma+= el[1]

		try:
			media = soma / quantidade
		except ZeroDivisionError:
			media = 0

		self.tree_pesagem_info_macho1.insert(parent="", index=END, iid=1, values=[
			quantidade,
			f"{media:.2f}",
			soma			])

		sum_engorda = 0

		for animal in dummy_lista:
			if animal[2] == "Sim":
				sum_engorda += 1

		self.tree_pesagem_info_macho2.insert(parent="", index=END, iid=1, values=[
			sum_engorda,
			f"{media/30:.2f}",
			f"{soma/30:.2f}"	])


	def fill_femea_tree(self,sort=False,col=1):
		dummy_lista = []
		try:
			self.femea_tree.delete(*self.femea_tree.get_children())
			self.tree_pesagem_info_femea1.delete(*self.tree_pesagem_info_femea1.get_children())
			self.tree_pesagem_info_femea2.delete(*self.tree_pesagem_info_femea2.get_children())
		except:
			pass
		for i, animal in enumerate(self.animal_.animais_info["femea"].keys()):
			try:
				peso = self.animal_.animais_info["femea"][animal]["pesagens"][self.data]
			except KeyError:
				continue
			if max(self.animal_.animais_info["femea"][animal]["pesagens"]) in \
					self.animal_.animais_info["femea"][animal]["engorda"]:
				engorda = "Sim"
			else:
				engorda = "Não"

			if max(self.animal_.animais_info["femea"][animal]["pesagens"]) in \
					self.animal_.animais_info["femea"][animal]["prenhez"]:
				prenhez = "Sim"
			else:
				prenhez = "Não"
			dummy_lista.append([f"{animal:03}", peso, engorda,prenhez])

		if sort:
			if col == self.femea_tree_sort_col:
				self.femea_tree_sort_reverse = not self.femea_tree_sort_reverse
			else:
				self.femea_tree_sort_reverse = False
			dummy_lista = sorted(dummy_lista, key=lambda x: x[col], reverse=self.femea_tree_sort_reverse)
			self.femea_tree_sort_col = col

		for i, lista in enumerate(dummy_lista):
			self.femea_tree.insert(parent="", index=END, iid=i, values=lista)

		quantidade = len(dummy_lista)
		soma = 0
		for el in dummy_lista:
			soma += el[1]

		try:
			media = soma / quantidade
		except ZeroDivisionError:
			media = 0

		self.tree_pesagem_info_femea1.insert(parent="", index=END, iid=1, values=[
			quantidade,
			f"{media:.2f}",
			soma		])

		sum_engorda = 0

		for animal in dummy_lista:
			if animal[2] == "Sim":
				sum_engorda += 1

		self.tree_pesagem_info_femea2.insert(parent="", index=END, iid=1, values=[
			sum_engorda,
			f"{media/30:.2f}",
			f"{soma/30:.2f}"	])


	def data_selecionada(self, *args):
		self.b_cancel_alteracao_massa.place_forget()
		self.b_alteracao_massa.place_forget()
		self.data = self.cal2date(self.cal)
		self.l_data_inserida.config(text=self.data.strftime("%d/%m/%y"))
		self.update_info("Data selecionada")

		self.fill_femea_tree()
		self.fill_macho_tree()

		self.insert_entradas()

	def insert_entradas(self):
		self.rb_macho.place(relx=0.42, rely=0.37, anchor=CENTER)
		self.rb_femea.place(relx=0.48, rely=0.37, anchor=CENTER)
		self.sexo = self.sv_sexo.get()
		if self.data:
			self.cb_overwrite.place(relx=0.45, rely=0.45, anchor=CENTER)
			self.insert_entrada_animal_peso()
			self.om_engorda.place(relx=0.45, rely=0.65, relwidth=0.1, anchor=CENTER)
			self.l_engorda.place(relx=0.37, rely=0.65, relwidth=0.1, anchor=CENTER)

			if self.sv_sexo.get() == "macho":
				self.insert_macho_entradas()
				self.delete_femea_entradas()
			else:
				self.insert_femea_entradas()
				self.delete_macho_entradas()

	def insert_entrada_animal_peso(self):
		self.e_peso.place(relx=0.48, rely=0.40, relwidth=0.05, anchor=CENTER)
		self.e_animal.place(relx=0.42, rely=0.40, relwidth=0.05, anchor=CENTER)
		self.b_confirma.place(relx=0.42 , rely=0.52, relwidth=0.05, anchor=CENTER)
		self.b_apagar.place(relx=0.48, rely=0.52, relwidth=0.05, anchor=CENTER)

	def delete_entrada_animal_peso(self):
		self.e_peso.place_forget()
		self.e_animal.place_forget()
		self.b_confirma.place_forget()
		self.b_apagar.place_forget()

	def delete_data(self):
		self.data = False
		self.l_data_inserida.config(text="Selecione uma data")

	def update_frame_tree_peso(self, *args):
		self.delete_data()
		self.delete_both_trees()
		self.delete_entradas()
		self.update_info("")
	def delete_macho_entradas(self):
		pass

	def delete_femea_entradas(self):
		self.om_prenhez.place_forget()
		self.l_prenhez.place_forget()

	def insert_macho_entradas(self):
		pass

	def insert_femea_entradas(self):
		self.om_prenhez.place(relx=0.45, rely=0.70, relwidth=0.1, anchor=CENTER)
		self.l_prenhez.place(relx=0.37, rely=0.70, relwidth=0.1, anchor=CENTER)

	def delete_entradas(self):
		self.delete_entrada_animal_peso()
		self.delete_macho_entradas()
		self.delete_femea_entradas()

	def delete_both_trees(self, delete_macho=True, delete_femea=True):
		if delete_macho:
			try:
				self.sum_tree.delete(*self.macho_tree.get_children())
			except:
				pass
		if delete_femea:
			try:
				self.sum_tree.delete(*self.femea_tree.get_children())
			except:
				pass


	def check_engorda(self,animal):
		if self.sv_engorda.get() == "Sim":
			if self.data not in self.animal_.animais_info[self.sexo][animal]["engorda"]:
				self.animal_.animais_info[self.sexo][animal]["engorda"].append(self.data)
		else:
			if self.data in self.animal_.animais_info[self.sexo][animal]["engorda"]:
				self.animal_.animais_info[self.sexo][animal]["engorda"].remove(self.data)


	def check_prenhez(self,animal):
		if self.sv_engorda.get() == "Sim":
			if self.data not in self.animal_.animais_info[self.sexo][animal]["prenhez"]:
				self.animal_.animais_info[self.sexo][animal]["prenhez"].append(self.data)
		else:
			if self.data in self.animal_.animais_info[self.sexo][animal]["prenhez"]:
				self.animal_.animais_info[self.sexo][animal]["prenhez"].remove(self.data)


	def insert_one(self, animal, peso):
		ok_overwrite = False
		try:
			peso_saved = self.animal_.animais_info[self.sexo][animal]["pesagens"][self.data]
			if peso != peso_saved and not self.bv_overwrite.get():
				ok_overwrite = messagebox.askquestion('Sobrescrever animal',
													  f'Em {self.data.strftime("%d/%m/%y")} já há uma pesagem do animal {self.sexo} {animal} pesando {peso_saved} kg. Deseja sobrescrever essa pesagem?',
													  icon='warning')

				ok_overwrite = True if (ok_overwrite == "yes") else False

			if ok_overwrite or self.bv_overwrite.get():
				self.animal_.animais_info[self.sexo][animal]["pesagens"][self.data] = peso
			self.check_engorda(animal)
			if self.sv_sexo.get() == "femea":
				self.check_prenhez(animal)


		except KeyError:
			if animal not in self.animal_.animais_info.keys():
				self.create_new_animal(animal)
				self.animal_.animais_info[self.sexo][animal]["pesagens"][self.data] = peso
				self.check_engorda(animal)
				if self.sv_sexo.get() == "femea":
					self.check_prenhez(animal)

		if self.sexo == "macho":
			self.fill_macho_tree()
		else:
			self.fill_femea_tree()

	def create_new_animal(self, animal):
		self.animal_.animais_info[self.sexo][animal] = {}
		self.animal_.animais_info[self.sexo][animal]["pesagens"] = {}
		self.animal_.animais_info[self.sexo][animal]["DN"] = None
		self.animal_.animais_info[self.sexo][animal]["pai"] = None
		self.animal_.animais_info[self.sexo][animal]["mae"] = None
		self.animal_.animais_info[self.sexo][animal]["obs"] = ""
		self.animal_.animais_info[self.sexo][animal]["engorda"] = []

		if self.sexo == "femea":
			self.animal_.animais_info["femea"][animal]["prenhez"] = []

	def insert_femea(self, animal, peso):
		pass