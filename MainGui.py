# improvements
##########
#  TODO  #
##########
'''

create a window to show the plots
adding formulas to determine the accretion  

dm/dt

dm: given

i = 1
dt = [time[i] - time[i-1]]

'''
#!/usr/bin python
import sys
from Tkinter import *
from ttk import Frame, Style
import DatabasConfig as DB
import plot_creation as plotting
import numpy as np
from scipy.stats import gaussian_kde

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import mlab, cm
from matplotlib.mlab import griddata
import testPlot as ts

class BaseBHFrame(Tk):
	''' controller for managiging frames '''
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		container = Frame(self)
		container.pack()
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (DB_acess, ListBoxChoice_Tables, Mathplotlib):
			frame = F(container, self)
			self.frames[F] = frame
			
			frame.grid(row=0,column=0, sticky="nsew")

		self.show_frame(Mathplotlib)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		frame.event_generate("<<ShowFrame>>")
	
	def click_ok(self, child ,event=None):
		me = self
		dictionary = {}
		dictionary['host']      = child.host.get()
		dictionary['user']      = child.username.get()
		dictionary['passwd']    = child.password.get()
		dictionary['db']        = child.Database.get()

		np.save('saved_database_info', dictionary)
		# if exist continue
		self.show_frame(ListBoxChoice_Tables)
		# self.destroy()

	def click_cancel(self, event=None):
		print("The user clicked 'Cancel'")
		self.destroy()

class DB_acess(Frame):
	def createWidgets(self, parent, controller):
		# Creating Empty local objects 
		me       = self
		# Making the frame
		dialog_frame = Frame(me)
		dialog_frame.grid(row=0, column=0, padx=20, pady=70)
		# Making label
		Label(dialog_frame, text='host:'    ).grid(row=0, column=0, sticky='w')
		Label(dialog_frame, text='username:').grid(row=1, column=0, sticky='w')
		Label(dialog_frame, text='password:').grid(row=2, column=0, sticky='w')
		Label(dialog_frame, text='Database:').grid(row=3, column=0, sticky='w')
		# Making entries where the user can write their info
		host     = me.host      = Entry(dialog_frame, background='white', width=24)
		username = me.username  = Entry(dialog_frame, background='white', width=24)
		password = me.password  = Entry(dialog_frame, background='white', width=24, show='*')
		Database = me.Database  = Entry(dialog_frame, background='white', width=24)
		# Aligning the elements on the frame
		host.grid(    row=0, column=1, sticky='w')
		username.grid(row=1, column=1, sticky='w')
		password.grid(row=2, column=1, sticky='w')
		Database.grid(row=3, column=1, sticky='w')
		# automaticaly selected on the host field
		host.focus_set()
		button_ok     = Button(self, text='OK',     height=1, width=7, default='active', command= lambda: controller.click_ok(me)).grid(row=3, column=0, sticky='e', padx=1)
		button_cancel = Button(self, text='Cancel', height=1, width=8, command= lambda: controller.click_cancel()).grid(row=3, column=2, sticky='e', padx=1)

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		controller.minsize(width=450, height=300)
		controller.title("Black Hole Simulation Data Analysis")
		# self.pack()
		self.createWidgets(parent, controller)

class ListBoxChoice_Tables(Frame):
    def __init__(self, parent, controller):
    	Frame.__init__(self, parent)
        self.bind("<<ShowFrame>>", self.on_show_frame)
        button_ok     = Button(self, text='Choose', height=1, width=6, default='active', command= lambda: self.select_table(controller)).pack(side='right', padx=10)
        button_cancel = Button(self, text='Cancel', height=1, width=6, command= lambda: controller.click_cancel()).pack(side='right', padx=10)

    def on_show_frame(self, event):
    	dialog_frame = Frame(self)
        label        = Label(dialog_frame, text='Tables:'    )
        self.listbox = Listbox(dialog_frame, selectmode="Extended")
        tables       = DB.get_DB_tables_List()

    	dialog_frame.pack(padx=20, pady=80, anchor='w')
        label.pack()
        self.listbox.pack()

        for (table_name,) in tables:
        	self.listbox.insert(END, table_name)

    def select_table(self, parent):
        value = str(self.listbox.get(self.listbox.curselection()))
        set_table_selection(value)
        parent.show_frame(Mathplotlib)

# improvements
##########
#  TODO  #
##########
'''
2) clean the code
3) remove unused variables
4) increase code efficiency
'''

class Mathplotlib(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller
		self.bind("<<ShowFrame>>", self.on_show_frame)

	def on_show_frame(self, event):
		# setting the size of the frame 
		self.controller.minsize(width=750, height=600)
		self.show_plot()
		self.dialog_frame = Frame(self)
		self.dialog_frame.grid(column=1, row=0, columnspan = 2, sticky="nsew")
		self.ListBoxChoice_BH_ID()
		lists_fields = DB.get_all_fields()
		self.drop_menu_x_axis(lists_fields)
		self.drop_menu_y_axis(lists_fields)
		self.drop_menu_plot_type()
		self.selectButton()
		self.cancelButton()

	def show_plot(self):
		f            = Figure(figsize=(5,5), dpi =100)
		f.set_tight_layout(True)
		self.subplot = f.add_subplot(111)
		self.line,   = self.subplot.plot([0],[0], linewidth=2)
		self.canvas  = FigureCanvasTkAgg(f, self)
		self.canvas.show()
		self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")
		self.canvas._tkcanvas.grid(column=0, row=0, rowspan=2, sticky="nsew")
		toolbar = NavigationToolbar2TkAgg(self.canvas, self.controller)
		toolbar.update()

	def ListBoxChoice_BH_ID(self):
		label        = Label(self.dialog_frame,   text='Unique BH IDs:').grid(column=1, row=0, sticky="nsew", columnspan=2)
		self.listbox = Listbox(self.dialog_frame, selectmode="Extended")
		self.listbox.grid(column=1, row=1, columnspan = 2)
		BH_IDs       = DB.get_BH_list_ID()
		for ids in BH_IDs:
			self.listbox.insert(END, ids['BHiord'])
		# selected the first entry by default	
		self.listbox.select_set(0)
	
	### x axis menu
	def drop_menu_x_axis(self, optionList):
		self.x_axis_selection = StringVar()
		self.x_axis_selection.set(optionList[0])
		drop_Menu_x = OptionMenu(self.dialog_frame, self.x_axis_selection, *optionList)
		drop_Menu_x.grid(column=1, row=3, sticky="news", columnspan = 2)
		label       = Label(self.dialog_frame, text='x axis' ).grid(column=1, row=2, sticky="new",  columnspan = 2)

	def selected_plot(self):
		# getting the selected option to determine the type plot
		selected_option =  self.plot_selection.get()
		# creating a dictionarie to execute the selected plot
		options = {'contour': self.contour_plot,
				   'line'   : self.line_plot}
		# executing the selected plot 
		options[selected_option]()

	def line_plot(self):
		x_axis  = self.x_axis_selection.get()
		y_axis  = self.y_axis_selection.get()
		user_bh_id_selection = self.get_bh_id_selection()
		rows = DB.get_axis_by_id(user_bh_id_selection, x_axis, y_axis)

		x = []; y = []

		plotting.format_axis(rows, x , y)
		self.line.set_data(x, y)
		ax = self.canvas.figure.axes[0]
		ax.set_title('Black Hole ID: ' + user_bh_id_selection + ' ')
		ax.set_xlabel(x_axis)
		ax.set_ylabel(y_axis)
		ax.set_xlim(min(x), max(x))
		ax.set_ylim(min(y), max(y))

		# ax.set_xscale("log")
		# ax.set_yscale("log")
		self.canvas.draw()

	def contour_plot(self):
		'''
		data = np.clip(randn(250, 250), -1, 1)
		cax = self.subplot.imshow(data, interpolation='nearest', cmap=cm.afmhot)
		colorbar = f.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
		colorbar.remove()
		'''
		# plt.colorbar()
		ts.test()

	def get_bh_id_selection(self):
		value             = str(self.listbox.get(self.listbox.curselection()))
		return value
	### y axis menu
	def drop_menu_y_axis(self, optionList):
		self.y_axis_selection = StringVar()
		self.y_axis_selection.set(optionList[1])
		drop_Menu_y = OptionMenu(self.dialog_frame, self.y_axis_selection, *optionList)
		drop_Menu_y.grid(column=1, row=5, sticky="news", columnspan = 2)
		label       = Label(self.dialog_frame, text='y axis' ).grid(column=1, row=4, sticky="new", columnspan = 2)
	### plotting type 	
	def drop_menu_plot_type(self):
		self.plot_selection   = StringVar()
		self.plot_selection.set('line')
		optionList  = ['contour','line']
		drop_Menu_x = OptionMenu(self.dialog_frame, self.plot_selection, *optionList)
		drop_Menu_x.grid(column=1, row=7, sticky="news", columnspan = 2)
		label       = Label(self.dialog_frame, text='Plot Type' ).grid(column=1, row=6, sticky="new",  columnspan = 2)
	### Select button
	def selectButton(self):
		button    = Button(self.dialog_frame, text="Select", anchor=W, padx=15, command=self.selected_plot)
		button.grid(column=1, row=8, sticky="nsew", pady=30)
	### Cancel button
	def cancelButton(self):
		quitButton = Button(self.dialog_frame, text='Cancel',  anchor=W, padx=10, command= lambda: self.controller.click_cancel())
		quitButton.grid(column=2, row=8, sticky="nsew", pady=30)

# Allow the class to run stand-alone.
if __name__ == "__main__":
	TkFrame = BaseBHFrame()
	TkFrame.geometry("300x280+300+300")
	TkFrame.mainloop()