# improvements
##########
#  TODO  #
##########
'''

create a window to show the plots

'''
#!/usr/bin python
import sys
from Tkinter import *
from ttk import Frame, Style
import DatabasConfig as DB
import plot_creation as plotting
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import mlab, cm
from matplotlib.mlab import griddata

user_table_selection = ''
def get_table_selection():
	return user_table_selection

def set_table_selection(selection):
	user_table_selection = selection

class BaseBHFrame(Tk):
	''' controller for managiging frames '''
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		container = Frame(self)
		container.pack()
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (MainFrame, DB_acess, ListBoxChoice_Tables, Mathplotlib):
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

class MainFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text=" Start Page ")
		label.pack(pady = 10, padx=10)

		buttonTest = Button(self, text = " Test",command= lambda: controller.show_frame(DB_acess))
		buttonTest.pack()

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
        parent.show_frame(ListBoxChoice_BH_ID)

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
		self.show_plot()
		self.bind("<<ShowFrame>>", self.on_show_frame)

	def on_show_frame(self, event):
		self.dialog_frame = Frame(self)
		self.dialog_frame.grid(column=1, row=0, columnspan = 2, sticky="nsew")
		label        = Label(self.dialog_frame, text='Unique BH IDs:'    ).grid(column=1, row=0, sticky="nsew", columnspan=2)
		self.listbox = Listbox(self.dialog_frame, selectmode="Extended")
		self.listbox.grid(column=1, row=1, columnspan = 2)
		BH_IDs       = DB.get_BH_list_ID()

		for ids in BH_IDs:
			self.listbox.insert(END, ids['BHiord'])

		self.controller.minsize(width=750, height=600)
        # Label(dialog_frame, text='host:'    ).grid(row=0, column=0, sticky='w')
		self.x_axis_selection = StringVar()
		self.y_axis_selection = StringVar()
		array                 = DB.get_all_fields()
		self.drop_menu_x_axis(array)
		self.drop_menu_y_axis(array)
		self.selectButton()
		self.cancelButton()


	def refresh_Plots(self):
		x_axis  = self.x_axis_selection.get()
		y_axis  = self.y_axis_selection.get()
		user_bh_id_selection = self.get_bh_id_selection()

		rows = DB.get_axis_by_id(user_bh_id_selection, x_axis, y_axis)

		# self.subplot.contourf(x,y,a, np.linspace(-1,1,11))

		delta = 0.025
		x = np.arange(-3.0, 3.0, delta)
		y = np.arange(-2.0, 2.0, delta)
		X, Y = np.meshgrid(x, y)
		Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
		Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
		# difference of Gaussians
		Z = 10.0 * (Z2 - Z1)
		ax = self.canvas.figure.axes[0]

		CS = ax.contour(X, Y, Z)

		xvalues = plotting.format_axis(rows ,x_axis)
		yvalues = plotting.format_axis(rows ,y_axis)

		manual_locations = zip(xvalues, yvalues)
		# manual_locations = [(-1, -1.4), (-0.62, -0.7), (-2, 0.5), (1.7, 1.2), (2.0, 1.4), (2.4, 1.7)]
		self.subplot.clabel(CS, inline=1, fontsize=10, manual=manual_locations)

		'''
		x = plotting.format_axis(rows ,x_axis)
		y = plotting.format_axis(rows ,y_axis)

		# self.line.set_data(x, y)

		ax = self.canvas.figure.axes[0]

		ax.set_title('Black Hole ID: ' + user_bh_id_selection + ' ')
		ax.set_xlabel(x_axis)
		ax.set_ylabel(y_axis)
		ax.set_xlim(min(x), max(x))
		ax.set_ylim(min(y), max(y))

		# ax.set_xscale("log")
		# ax.set_yscale("log")
		ax.contour(x,y,a)
		'''     
		self.canvas.draw()

	def show_plot(self):
		f            = Figure(figsize=(5,5), dpi =100)
		self.subplot = f.add_subplot(111)
		# self.line,   = subplot.plot([0],[0], linewidth=2)
		self.canvas  = FigureCanvasTkAgg(f, self)
		self.canvas.show()
		self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")
		self.canvas._tkcanvas.grid(column=0, row=0, rowspan=2, sticky="nsew")
		toolbar = NavigationToolbar2TkAgg(self.canvas, self.controller)
		toolbar.update()

	def get_bh_id_selection(self):
		value             = str(self.listbox.get(self.listbox.curselection()))
		return value
	### x axis menu
	def drop_menu_x_axis(self, optionList):
		drop_Menu_x = OptionMenu(self.dialog_frame, self.x_axis_selection, *optionList)
		drop_Menu_x.grid(column=1, row=3, sticky="news", columnspan = 2)
		label       = Label(self.dialog_frame, text='x axis' ).grid(column=1, row=2, sticky="new",  columnspan = 2)
	### y axis menu
	def drop_menu_y_axis(self, optionList):
		drop_Menu_y = OptionMenu(self.dialog_frame, self.y_axis_selection, *optionList)
		drop_Menu_y.grid(column=1, row=5, sticky="news", columnspan = 2)
		label       = Label(self.dialog_frame, text='y axis' ).grid(column=1, row=4, sticky="new", columnspan = 2)
	### Select button
	def selectButton(self):
		button    = Button(self.dialog_frame, text="Select", anchor=W, padx=15, command=self.refresh_Plots)
		button.grid(column=1, row=6, sticky="nsew", pady=30)
	### Cancel button
	def cancelButton(self):
		quitButton = Button(self.dialog_frame, text='Cancel',  anchor=W, padx=10, command= lambda: self.controller.click_cancel())
		quitButton.grid(column=2, row=6, sticky="nsew", pady=30)

# Allow the class to run stand-alone.
if __name__ == "__main__":
	TkFrame = BaseBHFrame()
	TkFrame.geometry("300x280+300+300")
	TkFrame.mainloop()