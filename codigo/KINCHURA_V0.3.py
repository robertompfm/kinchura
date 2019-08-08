# import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#################################################################################################
# create heat stress limits matrix
HEAT_STRESS_LIMITS = [[30.0, 26.7, 25.0],
                      [30.6, 28.0, 25.9],
                      [31.4, 29.4, 27.9],
                      [32.2, 31.1, 30.0]]

# define activities and create activities dictionaries and lists
ACTIVITY0 = "Sentado em Repouso"
ACTIVITY1 = "Sentado, movimentos moderados com braços e tronco (ex.: datilografia)."
ACTIVITY2 = "Sentado, movimentos moderados com braços e pernas (ex.: dirigir)."
ACTIVITY3 = "De pé, trabalho leve, em máquina ou bancada, principalmente com os braços."
ACTIVITY4 = "Sentado, movimentos vigorosos com braços e pernas."
ACTIVITY5 = "De pé, trabalho leve em máquina ou bancada, com alguma movimentação."
ACTIVITY6 = "De pé, trabalho moderado em máquina ou bancada, com alguma movimentação."
ACTIVITY7 = "Em movimento, trabalho moderado de levantar ou empurrar."
ACTIVITY8 = "Trabalho intermitente de levantar, empurrar ou arrastar pesos (ex.: remoçãocom pá)."
ACTIVITY9 = "Trabalho fatigante."

ACTIVITIES_LIST = [ACTIVITY0, ACTIVITY1, ACTIVITY2, ACTIVITY3, ACTIVITY4,
                   ACTIVITY5, ACTIVITY6, ACTIVITY7, ACTIVITY8, ACTIVITY9]

ACTIVITY_KCAL = {ACTIVITY0: 100.0, ACTIVITY1: 125.0, ACTIVITY2: 150.0, ACTIVITY3: 150.0,
                 ACTIVITY4: 180.0, ACTIVITY5: 175.0, ACTIVITY6: 220.0, ACTIVITY7: 300.0,
                 ACTIVITY8: 440.0, ACTIVITY9: 550.0}

KCAL_WGBT = {175: 30.5, 200: 30.0, 250: 28.5, 300: 27.5, 350: 26.5, 400: 26.0, 450: 25.5, 500: 25.0}

ACTIVITY_CLASSIFICATION = {0: "leve", 1: "moderada", 2: "pesada"}

PERIOD_DICT = {"trabalho contínuo": "sem descanso", "45 minutos de trabalho": "15 minutos de descanso", 
               "30 minutos de trabalho": "30 minutos de descanso", "15 minutos de trabalho": "45 minutos de descanso"}


#################################################################################################
# define main functions
def get_wbgt(tw, tg, td = None):
	"""
	Obtain the Wet-Bulb Globe Temperature
	"""
	if td == None:
		return round((0.7 * tw) + (0.3 * tg), 2)
	else:
		return round((0.7 * tw) + (0.2 * tg) + (0.1 * td), 2)
	
def get_weighted_average(w1, t1, w2, t2):
	"""
	Obtain the metabolic rate
	"""
	return round(((w1 * t1) + (w2 * t2))/(t1 + t2), 2)	

def get_case1_result_string(limit, wbgt, activity, working_period, index):
	limit_str = str(limit)
	wbgt_str = str(wbgt)
	resting_period = PERIOD_DICT[working_period]
	if wbgt < limit:
		state = ("inferior", "salubre")
	elif wbgt == limit:
		state = ("igual", "salubre")
	else:
		state = ("superior", "insalubre em grau médio")
	activity_classification = ACTIVITY_CLASSIFICATION[index]

	str1 = 'De acordo com o Anexo n. 3 da Norma Regulamentadora 15 da Portaria n. 3.214/1978,'+ \
	       ' para atividade ' + activity_classification + ' ("' + activity + '"), ' + \
	       'com regime de ' + working_period + ' e ' + resting_period + ', ' + \
	       'o limite de tolerancia para exposição ao calor é de ' + limit_str + '°C (IBUTG).\n' + \
	       'Como o IBUTG obtido no local de trabalho, equivalente a ' + wbgt_str + '°C, é ' + state[0] + \
	       ' ao limite de tolerância, a atividade é então considerada ' + state[1] + ' em relação ao agente físico calor.'
	return str1

def heat_stress_col(activity):
	if activity in [ACTIVITY0, ACTIVITY1,ACTIVITY2, ACTIVITY3]:
		return 0
	elif activity in [ACTIVITY4, ACTIVITY5, ACTIVITY6, ACTIVITY7]:
		return 1
	elif activity in [ACTIVITY8, ACTIVITY9]:
		return 2

def heat_stress_row(working_period):
	working_period_list = list(PERIOD_DICT.keys())
	return working_period_list.index(working_period)

def get_wbgt_max(metabolism):
	metabolism_list = list(KCAL_WGBT.keys())
	for item in metabolism_list:
		if metabolism <= item:
			return KCAL_WGBT[item]
	return 25.0

def get_case2_result_string(limit, wbgt, metabolism):
	limit_str = str(limit)
	wbgt_str = str(wbgt)
	metabolism_str = str(metabolism)
	if wbgt < limit:
		state = ("inferior", "salubre")
	elif wbgt == limit:
		state = ("igual", "salubre")
	else:
		state = ("superior", "insalubre em grau médio")

	str1 = 'De acordo com o Anexo n. 3 da Norma Regulamentadora 15 da Portaria n. 3.214/1978,' + \
	       ' para uma taxa metabólica média ponderada de ' + metabolism_str + ' Kcal/h' + \
           ' o limite de exposição de ' + limit_str + '°C (IBUTG).\n' + \
	       'Como a média ponderada dos IBUTGs obtidos nos locais de trabalho e descanso, equivalente a ' + wbgt_str + '°C, é ' + state[0] + \
	       ' ao limite de exposição toleravel, a atividade é considerada ' + state[1] + ' em relação ao agente físico calor.'
	return str1

def invalid_input_warning(field):
	messagebox.showwarning("Aviso - Valor Invalido", 
                           "Não foi inserido valor valido no campo "+ field + 
		                   " Deve ser inserido um valor numérico no campo e a separação decimal" + 
		                   " deve ser feita utilizando ponto (ex.: 23.45)")

#################################################################################################
# create initial frame
class FirstFrame():
	def __init__(self, master):
		"""
		create the first window that will appear when the program starts
		"""
		self.master= master
		self.master.title("KINCHURA - Análise de insalubridade por exposição ao calor")

		self.content = ttk.Frame(self.master)
		self.content['padding'] = (20, 20, 20, 10)
		self.content.grid(column=0, row=0, sticky=(N, W, E, S))
		self.master.columnconfigure(0, weight=5)
		self.master.rowconfigure(0, weight=5)

		self.case = StringVar()

		self.label1_txt = "Selecione a opção que melhor se adequa ao regime trabalho analisado:"
		self.case1_txt = "Limites de Tolerância para exposição ao calor, em regime de trabalho intermitente com períodos de descanso no próprio local de prestação de serviço."
		self.case2_txt = "Limites de Tolerância para exposição ao calor, em regime de trabalho intermitente com período de descanso em outro local (local de descanso)."

		self.label1 = ttk.Label(self.content, text=self.label1_txt)
		self.case1_button = ttk.Radiobutton(self.content, text=self.case1_txt, variable=self.case, value=self.case1_txt)
		self.case2_button = ttk.Radiobutton(self.content, text=self.case2_txt, variable=self.case, value=self.case2_txt)
		self.next_button = ttk.Button(self.content, text="Avançar", command=self.next_window_call)
		self.cancel_button = ttk.Button(self.content, text="Cancelar", command=self.master.quit)

		self.label1.grid(column=1, row=0, columnspan=15, sticky=W)
		self.case1_button.grid(column=1, row=1, columnspan=20, sticky=W)
		self.case2_button.grid(column=1, row=2, columnspan=20, sticky=W)
		self.next_button.grid(column=20, row=4)
		self.cancel_button.grid(column=19, row=4, sticky=E)

		self.content.rowconfigure(3, minsize=15)

		self.master.mainloop()

	def next_window_call(self):
		if self.case.get() == self.case1_txt:
			case1_root = Toplevel()
			case1_window = Case1Frame(case1_root)
		elif self.case.get() == self.case2_txt:
			case2_root = Toplevel()
			case2_window = Case2Frame(case2_root)
		else:
			messagebox.showwarning('Aviso - Nenhuma opção selecionada',
			                       'É necessário selecionar uma das duas opções para prosseguir.')
			return

class Case1Frame():
	def __init__(self, master):
		"""
		create the window for cases in which the rest occurs at the work place
		"""
		self.master = master
		self.master.title("KINCHURA - Análise de insalubridade por exposição ao calor")

		self.content = ttk.Frame(self.master)
		self.content['padding'] = (20)
		self.content.grid(column=0, row=0, sticky=(N, W, E, S))
		
		self.time_content = ttk.Frame(self.content, padding=(5, 5, 5, 10), relief='solid')
		self.time_content.grid(column=1, row=4, columnspan=3, sticky=(N, W, E, S))
	    
		# select activity section
		self.activity_label = ttk.Label(self.content, text='Selecione o tipo de atividade exercida', anchor='center')
		self.activity_var = StringVar()
		self.activity_combobox = ttk.Combobox(self.content, textvariable=self.activity_var)
		self.activity_combobox['values'] = ACTIVITIES_LIST[1:]
		self.activity_combobox['width'] = 120
		self.activity_combobox.state(['readonly'])
		self.activity_label.grid(column=1, row=1, columnspan=3)
		self.activity_combobox.grid(column=1, row=2, columnspan=3)
		
		# select working regime
		self.regime_label = ttk.Label(self.content, text='Selecione o periodo de descanso ou de trabalho em uma hora:', padding=(0, 15, 0, 0))
		self.regime_label.grid(column=1, row=3, columnspan=3)
		self.resting_label = ttk.Label(self.time_content, text='Tempo de descanso', anchor='center', width=60)
		self.working_label = ttk.Label(self.time_content, text='Tempo de trabalho', anchor='center', width=60)
		self.resting_var = StringVar()
		self.working_var = StringVar()
		self.resting_combobox = ttk.Combobox(self.time_content, textvariable=self.resting_var, width=30)
		self.working_combobox = ttk.Combobox(self.time_content, textvariable=self.working_var, width=30)
		self.resting_combobox['values'] = list(PERIOD_DICT.values())
		self.working_combobox['values'] = list(PERIOD_DICT.keys())
		self.resting_combobox.state(['readonly'])
		self.working_combobox.state(['readonly'])
		self.resting_label.grid(column=1, row=0)
		self.working_label.grid(column=0, row=0)
		self.resting_combobox.grid(column=1, row=1)
		self.working_combobox.grid(column=0, row=1)
		self.working_combobox.bind('<<ComboboxSelected>>', self.working_period_call)
		self.resting_combobox.bind('<<ComboboxSelected>>', self.resting_period_call)

		# WBGT section
		self.wbgt_main_label = ttk.Label(self.content, text='IBUTG', padding=(0, 15, 0, 0))
		self.wbgt_main_label.grid(column=1, row=5, columnspan=3)
		self.wbgt_content = ttk.Frame(self.content, padding=(5, 5, 5, 10), relief='solid')
		self.wbgt_content.grid(column=1, row=8, columnspan=3, sticky=(N, W, E, S))

		self.wbgt_label = ttk.Label(self.wbgt_content, text='IBUTG', anchor='center', width=60)
		self.wbgt_label.grid(column=0, row=0)
		self.wbgt_var = StringVar()
		self.wbgt_text = Text(self.wbgt_content, width=10, height=1)
		self.wbgt_text.grid(column=0, row=1)
		self.tw_var = StringVar()
		self.tw_entry = ttk.Entry(self.wbgt_content, textvariable=self.tw_var, width=10)
		self.tw_entry.grid(column=1, row=1)
		self.tw_entry.state(['disabled'])
		self.tw_label = ttk.Label(self.wbgt_content, text='tbn')
		self.tw_label.grid(column=1, row=0)
		self.tw_label.state(['disabled'])
		self.tg_var = StringVar()
		self.tg_entry = ttk.Entry(self.wbgt_content, textvariable=self.tg_var, width=10)
		self.tg_entry.grid(column=2, row=1)
		self.tg_entry.state(['disabled'])
		self.tg_label = ttk.Label(self.wbgt_content, text='tg')
		self.tg_label.grid(column=2, row=0)
		self.tg_label.state(['disabled'])
		self.td_var = StringVar()
		self.td_entry = ttk.Entry(self.wbgt_content, textvariable=self.td_var, width=10)
		self.td_entry.grid(column=3, row=1)
		self.td_entry.state(['disabled'])
		self.td_label = ttk.Label(self.wbgt_content, text='ts')
		self.td_label.grid(column=3, row=0)
		self.td_label.state(['disabled'])
		self.calculate_button = ttk.Button(self.wbgt_content, text="Calcular", command=self.calculate_wbgt)
		self.calculate_button.grid(column=4, row=1)
		self.calculate_button.state(['disabled'])
		self.wbgt_calculate_var = IntVar()
		self.wbgt_checkbutton = ttk.Checkbutton(self.wbgt_content, text='Calcular IBUTG', command= lambda: self.activate_wbgt_parameters(),
		                                        variable=self.wbgt_calculate_var)
		self.wbgt_checkbutton.grid(column=0, row=2)
		self.solar_var = StringVar()
		self.solar_checkbutton = ttk.Checkbutton(self.wbgt_content, text='Ambiente com carga solar', command=self.solar_checkbutton_call,
		                                         variable=self.solar_var, onvalue='on', offvalue='off')
		self.solar_checkbutton.grid(column=2, row=2, columnspan=2)
		self.solar_checkbutton.state(['disabled'])
		self.wbgt_content.columnconfigure(0, pad=5)
		self.wbgt_content.columnconfigure(1, pad=15)
		self.wbgt_content.columnconfigure(2, pad=15)
		self.wbgt_content.columnconfigure(3, pad=15)
		self.wbgt_content.columnconfigure(4, pad=15)

		# buttons
		self.analysis_button = ttk.Button(self.content, text='Analisar', command=self.analysis_function)
		self.analysis_button.grid(column=2, row=9)
		self.content.rowconfigure(9, pad=25)

		self.master.mainloop()

	def calculate_wbgt(self):
		var = self.solar_var.get()
		td = None
		try:
			tw = float(self.tw_entry.get())
		except ValueError:
			invalid_input_warning("tbn")
			return
		try:
			tg = float(self.tg_entry.get())
		except ValueError:
			invalid_input_warning("tg")
			return
		if var == "on":
			try:
				td = float(self.td_entry.get())
			except ValueError:
				invalid_input_warning("ts")
				return
		wbgt = get_wbgt(tw, tg, td)
		self.wbgt_text.config(state='normal')
		self.wbgt_text.delete("1.0", END)
		self.wbgt_text.insert('1.0', str(wbgt))
		self.wbgt_text.config(state='disabled')

	def analysis_function(self):
		try:
			wbgt = float(self.wbgt_text.get("1.0", END))
		except ValueError:
			invalid_input_warning("IBUTG")
			return
		activity = self.activity_var.get()
		if activity == "":
			messagebox.showwarning("Aviso", "Nenhuma atividade foi selecionada.")
			return
		working_period = self.working_var.get()
		if working_period == "":
			messagebox.showwarning("Aviso", "Não foram selecionados tempo de trabalho e tempo de descanso")
			return
		heat_limits_col = heat_stress_col(activity)
		heat_limits_row = heat_stress_row(working_period)
		heat_limit = HEAT_STRESS_LIMITS[heat_limits_row][heat_limits_col]
		result_str = get_case1_result_string(heat_limit, wbgt, activity, working_period, heat_limits_col)
		
		# result
		self.result_label = ttk.Label(self.content, text='Resultado', anchor='center', padding=(0, 10, 0, 0))
		self.result_label.grid(column=1, row=10, columnspan=3)
		self.result_content = ttk.Frame(self.content, relief='solid')
		self.result_content.grid(column=1, row=11, columnspan=3, sticky=(N, W, E, S))
		
		# inserting the text
		self.result_var = StringVar()
		self.result_text = Text(self.result_content, width=92, height= 10)
		self.result_text.grid(column=0, row=0, columnspan=1, sticky=(W, N, E, S))
		self.result_text.insert('1.0', result_str)
		self.result_text['state'] = 'disabled'

	def working_period_call(self, event):
		working_period = self.working_combobox.get()
		self.resting_combobox.set(PERIOD_DICT[working_period])

	def resting_period_call(self, event):
		resting_period = self.resting_combobox.get()
		resting_list = list(PERIOD_DICT.values())
		working_list = list(PERIOD_DICT.keys())
		new_working_period = working_list[resting_list.index(resting_period)]
		self.working_combobox.set(new_working_period)

	def activate_wbgt_parameters(self):
		var = self.wbgt_calculate_var.get()
		active='active'
		disabled='disabled'
		if var == 1:
			self.tw_label.config(state=active)
			self.tw_entry.config(state=active)
			self.tg_label.config(state=active)
			self.tg_entry.config(state=active)
			if self.solar_var.get() == "on":
				self.td_label.config(state=active)
				self.td_entry.config(state=active)
			self.calculate_button.config(state=active)
			self.solar_checkbutton.config(state=active)
			self.wbgt_text.delete("1.0", END)
			self.wbgt_text.config(state=disabled)
		elif var == 0:
			self.tw_entry.delete(0, END)
			self.tw_label.config(state=disabled)
			self.tw_entry.config(state=disabled)
			self.tg_entry.delete(0, END)
			self.tg_label.config(state=disabled)
			self.tg_entry.config(state=disabled)
			self.td_entry.delete(0, END)
			self.td_label.config(state=disabled)
			self.td_entry.config(state=disabled)
			self.calculate_button.config(state=disabled)
			self.solar_checkbutton.config(state=disabled)
			self.wbgt_text.config(state='normal')

	def solar_checkbutton_call(self):
		var = self.solar_var.get()
		if var == "on":
			self.td_label.config(state='active')
			self.td_entry.config(state='active')
		elif var == "off":
			self.td_entry.delete(0, END)
			self.td_label.config(state='disabled')
			self.td_entry.config(state='disabled')


class Case2Frame():
	def __init__(self, master):
		"""
		create the window for cases in which the rest occurs at another place
		"""
		self.master = master
		self.master.title("KINCHURA - Análise de insalubridade por exposição ao calor")

		self.content = ttk.Frame(self.master)
		self.content['padding'] = (20)
		self.content.grid(column=0, row=0, sticky=(N, W, E, S))
		
		# select activity section
		self.activity_label = ttk.Label(self.content, text='Selecione o tipo de atividade de TRABALHO', anchor='center')
		self.activity_var = StringVar()
		self.activity_combobox = ttk.Combobox(self.content, textvariable=self.activity_var)
		self.activity_combobox['values'] = ACTIVITIES_LIST[1:]
		self.activity_combobox['width'] = 90
		self.activity_combobox.state(['readonly'])
		self.activity_label.grid(column=1, row=1)
		self.activity_combobox.grid(column=1, row=2)

		# select working period
		self.working_label = ttk.Label(self.content, text='Período em minutos', anchor='center')
		self.working_var = StringVar()
		self.working_spinbox = Spinbox(self.content, from_=1, to=59, textvariable=self.working_var, wrap=True, justify='center')
		self.working_var.set('59')
		self.working_spinbox['width'] = 15
		self.working_label.grid(column=2, row=1)
		self.working_spinbox.grid(column=2, row=2)
		self.working_spinbox.bind('<FocusOut>', self.adjust_resting)
		self.working_spinbox.bind('<Leave>', self.adjust_resting)
		
		# WBGT work section
		self.wbgt1_main_label = ttk.Label(self.content, text='IBUTG Área de TRABALHO', padding=(0, 10, 0, 0))
		self.wbgt1_main_label.grid(column=1, row=3, columnspan=3)
		self.wbgt1_content = ttk.Frame(self.content, padding=(5, 5, 5, 10), relief='solid')
		self.wbgt1_content.grid(column=1, row=4, columnspan=3, sticky=(N, W, E, S))

		self.wbgt1_label = ttk.Label(self.wbgt1_content, text='IBUTG', anchor='center', width=60)
		self.wbgt1_label.grid(column=0, row=0)
		self.wbgt1_var = StringVar()
		self.wbgt1_text = Text(self.wbgt1_content, width=10, height=1)
		self.wbgt1_text.grid(column=0, row=1)
		self.tw1_var = StringVar()
		self.tw1_entry = ttk.Entry(self.wbgt1_content, textvariable=self.tw1_var, width=10, justify='center')
		self.tw1_entry.grid(column=1, row=1)
		self.tw1_entry.state(['disabled'])
		self.tw1_label = ttk.Label(self.wbgt1_content, text='tbn')
		self.tw1_label.grid(column=1, row=0)
		self.tw1_label.state(['disabled'])
		self.tg1_var = StringVar()
		self.tg1_entry = ttk.Entry(self.wbgt1_content, textvariable=self.tg1_var, width=10, justify='center')
		self.tg1_entry.grid(column=2, row=1)
		self.tg1_entry.state(['disabled'])
		self.tg1_label = ttk.Label(self.wbgt1_content, text='tg')
		self.tg1_label.grid(column=2, row=0)
		self.tg1_label.state(['disabled'])
		self.td1_var = StringVar()
		self.td1_entry = ttk.Entry(self.wbgt1_content, textvariable=self.td1_var, width=10, justify='center')
		self.td1_entry.grid(column=3, row=1)
		self.td1_entry.state(['disabled'])
		self.td1_label = ttk.Label(self.wbgt1_content, text='ts')
		self.td1_label.grid(column=3, row=0)
		self.td1_label.state(['disabled'])
		self.calculate_button1 = ttk.Button(self.wbgt1_content, text="Calcular", command=self.calculate_wbgt1)
		self.calculate_button1.grid(column=4, row=1)
		self.calculate_button1.state(['disabled'])
		self.wbgt1_calculate_var = IntVar()
		self.wbgt1_checkbutton = ttk.Checkbutton(self.wbgt1_content, text='Calcular IBUTG', command= lambda: self.activate_wbgt1_parameters(),
		                                        variable=self.wbgt1_calculate_var)
		self.wbgt1_checkbutton.grid(column=0, row=2)
		self.solar1_var = StringVar()
		self.solar1_checkbutton = ttk.Checkbutton(self.wbgt1_content, text='Ambiente com carga solar', command=self.solar1_checkbutton_call,
		                                         variable=self.solar1_var, onvalue='on', offvalue='off')
		self.solar1_checkbutton.grid(column=2, row=2, columnspan=2)
		self.solar1_checkbutton.state(['disabled'])
		self.wbgt1_content.columnconfigure(0, pad=5)
		self.wbgt1_content.columnconfigure(1, pad=15)
		self.wbgt1_content.columnconfigure(2, pad=15)
		self.wbgt1_content.columnconfigure(3, pad=15)
		self.wbgt1_content.columnconfigure(4, pad=15)

		# select rest section
		self.rest_label = ttk.Label(self.content, text='Selecione o tipo de atividade de DESCANSO', anchor='center', padding=(0, 40, 0, 0))
		self.rest_var = StringVar()
		self.rest_combobox = ttk.Combobox(self.content, textvariable=self.rest_var)
		self.rest_combobox['values'] = ACTIVITIES_LIST[:4]
		self.rest_combobox['width'] = 90
		self.rest_combobox.state(['readonly'])
		self.rest_label.grid(column=1, row=5)
		self.rest_combobox.grid(column=1, row=6)

		# select resting period
		self.resting_label = ttk.Label(self.content, text='Período em minutos', anchor='center', padding=(0, 40, 0, 0))
		self.resting_var = StringVar()
		self.resting_spinbox = Spinbox(self.content, from_=1, to=59, textvariable=self.resting_var, wrap=True, justify='center')
		self.resting_spinbox['width'] = 15
		self.resting_label.grid(column=2, row=5)
		self.resting_spinbox.grid(column=2, row=6)
		self.resting_spinbox.bind('<FocusOut>', self.adjust_working)
		self.resting_spinbox.bind('<Leave>', self.adjust_working)
		
		# WBGT rest section
		self.wbgt2_main_label = ttk.Label(self.content, text='IBUTG Área de DESCANSO', padding=(0, 10, 0, 0))
		self.wbgt2_main_label.grid(column=1, row=7, columnspan=3)
		self.wbgt2_content = ttk.Frame(self.content, padding=(5, 5, 5, 10), relief='solid')
		self.wbgt2_content.grid(column=1, row=8, columnspan=3, sticky=(N, W, E, S))

		self.wbgt2_label = ttk.Label(self.wbgt2_content, text='IBUTG', anchor='center', width=60)
		self.wbgt2_label.grid(column=0, row=0)
		self.wbgt2_var = StringVar()
		self.wbgt2_text = Text(self.wbgt2_content, width=10, height=1)
		self.wbgt2_text.grid(column=0, row=1)
		self.tw2_var = StringVar()
		self.tw2_entry = ttk.Entry(self.wbgt2_content, textvariable=self.tw2_var, width=10)
		self.tw2_entry.grid(column=1, row=1)
		self.tw2_entry.state(['disabled'])
		self.tw2_label = ttk.Label(self.wbgt2_content, text='tbn')
		self.tw2_label.grid(column=1, row=0)
		self.tw2_label.state(['disabled'])
		self.tg2_var = StringVar()
		self.tg2_entry = ttk.Entry(self.wbgt2_content, textvariable=self.tg2_var, width=10)
		self.tg2_entry.grid(column=2, row=1)
		self.tg2_entry.state(['disabled'])
		self.tg2_label = ttk.Label(self.wbgt2_content, text='tg')
		self.tg2_label.grid(column=2, row=0)
		self.tg2_label.state(['disabled'])
		self.td2_var = StringVar()
		self.td2_entry = ttk.Entry(self.wbgt2_content, textvariable=self.td2_var, width=10)
		self.td2_entry.grid(column=3, row=1)
		self.td2_entry.state(['disabled'])
		self.td2_label = ttk.Label(self.wbgt2_content, text='ts')
		self.td2_label.grid(column=3, row=0)
		self.td2_label.state(['disabled'])
		self.calculate_button2 = ttk.Button(self.wbgt2_content, text="Calcular", command=self.calculate_wbgt2)
		self.calculate_button2.grid(column=4, row=1)
		self.calculate_button2.state(['disabled'])
		self.wbgt2_calculate_var = IntVar()
		self.wbgt2_checkbutton = ttk.Checkbutton(self.wbgt2_content, text='Calcular IBUTG', command= lambda: self.activate_wbgt2_parameters(),
		                                        variable=self.wbgt2_calculate_var)
		self.wbgt2_checkbutton.grid(column=0, row=2)
		self.solar2_var = StringVar()
		self.solar2_checkbutton = ttk.Checkbutton(self.wbgt2_content, text='Ambiente com carga solar', command=self.solar2_checkbutton_call,
		                                         variable=self.solar2_var, onvalue='on', offvalue='off')
		self.solar2_checkbutton.grid(column=2, row=2, columnspan=2)
		self.solar2_checkbutton.state(['disabled'])
		self.wbgt2_content.columnconfigure(0, pad=5)
		self.wbgt2_content.columnconfigure(1, pad=15)
		self.wbgt2_content.columnconfigure(2, pad=15)
		self.wbgt2_content.columnconfigure(3, pad=15)
		self.wbgt2_content.columnconfigure(4, pad=15)

		
		
		# buttons
		self.analysis_button = ttk.Button(self.content, text='Analisar', command=self.analysis_function)
		self.analysis_button.grid(column=1, row=10, columnspan=3)
		self.content.rowconfigure(9, minsize=10)
		

		self.master.mainloop()

	def adjust_resting(self, event):
		try:
			working_period = float(self.working_var.get())
		except ValueError:
			self.working_var.set('')
			return
		if working_period > 59:
			self.working_var.set('59')
			self.resting_var.set('1')
			return
		elif working_period < 1:
			self.working_var.set('1')
			self.resting_var.set('59')
			return
		new_working_var = int(round(working_period, 0))
		self.working_var.set(str(new_working_var))
		new_resting_var = 60 - new_working_var
		self.resting_var.set(str(new_resting_var))

	def adjust_working(self, event):
		try:
			resting_period = float(self.resting_var.get())
		except ValueError:
			self.resting_var.set('')
			return
		if resting_period > 59:
			self.working_var.set('1')
			self.resting_var.set('59')
			return
		elif resting_period < 1:
			self.working_var.set('59')
			self.resting_var.set('1')
			return
		new_resting_var = int(round(resting_period, 0))
		self.resting_var.set(str(new_resting_var))
		new_working_var = 60 - new_resting_var
		self.working_var.set(str(new_working_var))

	def calculate_wbgt1(self):
		var = self.solar1_var.get()
		td = None
		try:
			tw = float(self.tw1_entry.get())
		except ValueError:
			invalid_input_warning("tbn")
			return
		try:
			tg = float(self.tg1_entry.get())
		except ValueError:
			invalid_input_warning("tg")
			return
		if var == "on":
			try:
				td = float(self.td1_entry.get())
			except ValueError:
				invalid_input_warning("ts")
				return
		wbgt = get_wbgt(tw, tg, td)
		self.wbgt1_text.config(state='normal')
		self.wbgt1_text.delete("1.0", END)
		self.wbgt1_text.insert('1.0', str(wbgt))
		self.wbgt1_text.config(state='disabled')

	def solar1_checkbutton_call(self):
		var = self.solar1_var.get()
		if var == "on":
			self.td1_label.config(state='active')
			self.td1_entry.config(state='active')
		elif var == "off":
			self.td1_entry.delete(0, END)
			self.td1_label.config(state='disabled')
			self.td1_entry.config(state='disabled')

	def activate_wbgt1_parameters(self):
		var = self.wbgt1_calculate_var.get()
		if var == 1:
			self.tw1_label.config(state='active')
			self.tw1_entry.config(state='active')
			self.tg1_label.config(state='active')
			self.tg1_entry.config(state='active')
			if self.solar1_var.get() == "on":
				self.td1_label.config(state='active')
				self.td1_entry.config(state='active')
			self.calculate_button1.config(state='active')
			self.solar1_checkbutton.config(state='active')
			self.wbgt1_text.delete("1.0", END)
			self.wbgt1_text.config(state='disabled')
		elif var == 0:
			self.tw1_entry.delete(0, END)
			self.tw1_label.config(state='disabled')
			self.tw1_entry.config(state='disabled')
			self.tg1_entry.delete(0, END)
			self.tg1_label.config(state='disabled')
			self.tg1_entry.config(state='disabled')
			self.td1_entry.delete(0, END)
			self.td1_label.config(state='disabled')
			self.td1_entry.config(state='disabled')
			self.calculate_button1.config(state='disabled')
			self.solar1_checkbutton.config(state='disabled')
			self.wbgt1_text.config(state='normal')

	def calculate_wbgt2(self):
		var = self.solar2_var.get()
		td = None
		try:
			tw = float(self.tw2_entry.get())
		except ValueError:
			invalid_input_warning("tbn")
			return
		try:
			tg = float(self.tg2_entry.get())
		except ValueError:
			invalid_input_warning("tg")
			return
		if var == "on":
			try:
				td = float(self.td2_entry.get())
			except ValueError:
				invalid_input_warning("ts")
				return
		wbgt = get_wbgt(tw, tg, td)
		self.wbgt2_text.config(state='normal')
		self.wbgt2_text.delete("1.0", END)
		self.wbgt2_text.insert('1.0', str(wbgt))
		self.wbgt2_text.config(state='disabled')

	def solar2_checkbutton_call(self):
		var = self.solar2_var.get()
		if var == "on":
			self.td2_label.config(state='active')
			self.td2_entry.config(state='active')
		elif var == "off":
			self.td2_entry.delete(0, END)
			self.td2_label.config(state='disabled')
			self.td2_entry.config(state='disabled')

	def activate_wbgt2_parameters(self):
		var = self.wbgt2_calculate_var.get()
		if var == 1:
			self.tw2_label.config(state='active')
			self.tw2_entry.config(state='active')
			self.tg2_label.config(state='active')
			self.tg2_entry.config(state='active')
			if self.solar2_var.get() == "on":
				self.td2_label.config(state='active')
				self.td2_entry.config(state='active')
			self.calculate_button2.config(state='active')
			self.solar2_checkbutton.config(state='active')
			self.wbgt2_text.delete("1.0", END)
			self.wbgt2_text.config(state='disabled')
		elif var == 0:
			self.tw2_entry.delete(0, END)
			self.tw2_label.config(state='disabled')
			self.tw2_entry.config(state='disabled')
			self.tg2_entry.delete(0, END)
			self.tg2_label.config(state='disabled')
			self.tg2_entry.config(state='disabled')
			self.td2_entry.delete(0, END)
			self.td2_label.config(state='disabled')
			self.td2_entry.config(state='disabled')
			self.calculate_button2.config(state='disabled')
			self.solar2_checkbutton.config(state='disabled')
			self.wbgt2_text.config(state='normal')

	def analysis_function(self):
		try:
			wbgt1 = float(self.wbgt1_text.get("1.0", END))
		except ValueError:
			invalid_input_warning("IBUTG")
			return
		try:
			wbgt2 = float(self.wbgt2_text.get("1.0", END))
		except ValueError:
			invalid_input_warning("IBUTG")
			return
		activity = self.activity_var.get()
		rest = self.rest_var.get()
		if activity == "":
			messagebox.showwarning("Aviso", "Nenhum tipo de atividade foi selecionado.")
			return
		if rest == "":
			messagebox.showwarning("Aviso", "Nenhum tipo de descanso foi selecionado.")
			return
		if wbgt1 <= wbgt2:
			messagebox.showwarning("Aviso", "O valor do IBUTG da área de descanso deve ser inferior ao valor do IBUTG da área de trabalho.")
			return
		work_period = float(self.working_var.get())
		rest_period = float(self.resting_var.get())
		work_kcal = ACTIVITY_KCAL[activity]
		rest_kcal = ACTIVITY_KCAL[rest]

		metabolic_rate = get_weighted_average(work_kcal, work_period, rest_kcal, rest_period)
		wbgt_mean = get_weighted_average(wbgt1, work_period, wbgt2, rest_period)
		heat_limit = get_wbgt_max(metabolic_rate)
		
		result_str = get_case2_result_string(heat_limit, wbgt_mean, metabolic_rate)
		
		# result
		self.result_label = ttk.Label(self.content, text='Resultado', anchor='center', padding=(0, 10, 0, 0))
		self.result_label.grid(column=1, row=11, columnspan=3)
		self.result_content = ttk.Frame(self.content, relief='solid')
		self.result_content.grid(column=1, row=12, columnspan=3, sticky=(N, W, E, S))
		
		# inserting the text
		self.result_var = StringVar()
		self.result_text = Text(self.result_content, width=92, height= 10)
		self.result_text.grid(column=0, row=0, columnspan=1, sticky=(W, N, E, S))
		self.result_text.insert('1.0', result_str)
		self.result_text['state'] = 'disabled'

root = Tk()
window1 = FirstFrame(root)
#case1_frame()
