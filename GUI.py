import json
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from SMDBone import Dupe, FakeSoft
from SMDMat import PointerFix
import os
from os.path import *
import importlib.machinery
import importlib.util
from pathlib import Path

selected_scr = ''
scr_dat = ''

class Interp:

	def __init__(self, scr_ref):
		self.err = False
		self.scr_ref = "scripts/" + scr_ref + '.txt'
		if not os.path.exists(self.scr_ref):
			print("How did we get here?")
			self.err = True
		else:
			self.interp()

	def nl_clean(self, smd):
		count = -1
		for l in smd:
			count += 1
			smd[count] = l[:-l.count("\n")]
		return smd

	def interp(self):
		global scr_dat
		global guii
		scr_f = open(self.scr_ref, 'r')
		scr = self.nl_clean(scr_f.readlines())
		self.mode = ''
		if scr[0] == 'mode dupe':
			self.mode = 'd'
		elif scr[0] == 'mode mat':
			self.mode = 'm'
		elif scr[0] == 'mode bmp':
			self.mode = 'b'
		elif scr[0] == 'mode plugin':
			self.mode = 'p'
		else:
			self.mode = None
		print("Before: "+ str(scr))
		scr.pop(0)
		scr.pop(len(scr) - 1)
		print("After: "+ str(scr))
		print(scr)
		scr_dat = [self.mode, scr]
		guii.exec_script(scr_dat)

class ScriptWin:

	def __init__(self):
		self.nroot = Tk()
		self.win()
		self.nroot.mainloop()

	def win(self):
		self.nroot.title("Scripts")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=6, row=6, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		self.scripts = []
		script_dir = Path(os.sys.path[0])
		scr_dir = str(script_dir.joinpath('scripts'))
		for s in os.listdir(scr_dir):
			self.scripts.append(s.replace('.txt', ''))
		print(self.scripts)

		self.scr_list = Listbox(frame)
		self.scr_list.grid(column=1, row=1, sticky=(N, S, E, W), padx=40, pady=(40, 0), rowspan=5)
		count = 0
		for n in self.scripts:
			count += 1
			self.scr_list.insert(count, n)

		select_scr = Button(frame, text="Select", command=self.select)
		select_scr.grid(column=1, row=6, sticky=(S))

	def select(self):
		global selected_scr
		selected_scr = self.scripts[int(self.scr_list.curselection()[0])]
		print(selected_scr)
		scr_interp = Interp(selected_scr)
		self.nroot.destroy()

class OptWin:

	def __init__(self):
		self.nroot = Tk()
		self.win()
		self.nroot.mainloop()

	def win(self):
		self.nroot.title("Options")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=6, row=6, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		jsf = open('options.json', 'r')
		js = jsf.readlines()
		count = -1
		newjs = ''
		for l in js:
			if l.find('//') != -1:
				js.pop(count)
				continue
			newjs += l
		if not js[len(js)-1] == '}':
			newjs += '}'
		self.options = json.loads(newjs)

		self.b_smd_val = BooleanVar(frame, value=self.options["backup_smd"])
		print(self.b_smd_val.get())
		b_smd = Checkbutton(frame, text="Backup SMDs", variable=self.b_smd_val, command=self.set_backup_smd)
		b_smd.grid(column=1, row=1, sticky=(S), padx=50, pady=50)

		select_scr = Button(frame, text="Confirm", command=self.confirm_opts)
		select_scr.grid(column=1, row=6, sticky=(S))
	
	def set_backup_smd(self):
		self.options["backup_smd"] = self.b_smd_val.get()
		print(self.options["backup_smd"])
	
	def confirm_opts(self):
		newjson = json.dumps(self.options, sort_keys=True, indent=5)
		opts = open('options.json', 'w')
		opts.write(newjson)
		opts.close()
		self.nroot.destroy()

class GUI:
	def __init__(self, root):
		root.title("PS's SMD Tools")

		frame = Frame(root, borderwidth=2, relief="sunken")
		frame.grid(column=6, row=6, sticky=(N, E, S, W))
		root.columnconfigure(1, weight=1)
		root.rowconfigure(1, weight=1)

		dupe_button = Button(frame, text="Bone Dupe", command=self.bd_menu)
		dupe_button.grid(column=2, row=1, sticky=(N), padx=(0, 0))

		mat_button = Button(frame, text="Material Fix", command=self.mnc_menu)
		mat_button.grid(column=2, row=1, sticky=(N), padx=(140, 0))

		fakeweight = Button(frame, text="Soft Weights", command=self.fakesoft)
		fakeweight.grid(column=3, row=1, sticky=(N), padx=(0, 195))

		scripts = Button(frame, text="Scripts", command=self.scripts)
		scripts.grid(column=3, row=1, sticky=(N), padx=(0, 70))
		
		options = Button(frame, text="Options", command=self.options)
		options.grid(column=3, row=1, sticky=(N), padx=(29, 0))

		self.tile_label = Label(frame, text="Path to SMDs")
		self.tile_label.grid(column=2, row=2, sticky=(S, W))

		self.path = StringVar()
		self.tname_entry = Entry(frame, textvariable=self.path)
		self.tname_entry.grid(column=2, row=3, sticky=(N, E, W))

		self.save_button = Button(frame, text="File", command=self.openfile)
		self.save_button.grid(column=3, row=3, sticky=(S), padx=(0, 80))

		self.dir_button = Button(frame, text="Folder", command=self.opendir)
		self.dir_button.grid(column=3, row=3, sticky=(S), padx=(60, 0))

		self.base_label = Label(frame, text="Select Base Bone")
		self.base_label.grid(column=2, row=5, sticky=(S, W))

		self.b_bone = StringVar()
		self.bname_entry = Entry(frame, textvariable=self.b_bone)
		self.bname_entry.grid(column=3, row=5, sticky=(N, E, W))

		self.new_label = Label(frame, text="Select New Bone")
		self.new_label.grid(column=2, row=6, sticky=(S, W))

		self.n_bone = StringVar()
		self.nname_entry = Entry(frame, textvariable=self.n_bone)
		self.nname_entry.grid(column=3, row=6, sticky=(N, E, W))

		self.parent_label = Label(frame, text="Select Parent Bone")
		self.parent_label.grid(column=2, row=7, sticky=(S, W))

		self.p_bone = StringVar()
		self.pname_entry = Entry(frame, textvariable=self.p_bone)
		self.pname_entry.grid(column=3, row=7, sticky=(N, E, W))

		self.action_button = Button(frame, text="Dupe", command=self.dupe)
		self.action_button.grid(column=3, row=9, sticky=(S), padx=(0, 230))

		self.bmp_button = Button(frame, text="File Ext", command=self.bmp)
		self.matrn_button = Button(frame, text="Fix Pointer", command=self.matrename)

		self.ref_label = Label(frame, text="Type Finder Value")

		self.ref = StringVar()
		self.ref_entry = Entry(frame, textvariable=self.ref)

		self.rename_label = Label(frame, text="String Part To Rename")

		self.rename = StringVar()
		self.rename_entry = Entry(frame, textvariable=self.rename)

		self.replace_label = Label(frame, text="String Part To Replace")

		self.replace = StringVar()
		self.replace_entry = Entry(frame, textvariable=self.replace)

		ws = Label(frame, text='   ')
		ws.grid(column=4, row=1, sticky=(S))
		ws2 = Label(frame, text='   ')
		ws2.grid(column=1, row=4, sticky=(S))
		self.ws3 = Label(frame, text='   ')
		self.ws3.grid(column=1, row=8, sticky=(S))
		self.ws4 = Label(frame, text='   ')
	
	def openfile(self):
		self.path.set(askopenfilename(title="Select SMD"))
	def opendir(self):
		self.path.set(askdirectory(title="Select Anims Folder"))

	def dupe(self):
		inst = Dupe()
		loc = self.path.get()
		base = self.b_bone.get()
		new = self.n_bone.get()
		parent = self.p_bone.get()
		if loc.endswith('.smd'):
			inst.single_dupe(loc, base, new, parent)
		else:
			inst.batch_dupe(loc, base, new, parent)
	def dupe_scr(self, base, new, parent):
		inst = Dupe()
		loc = self.path.get()
		if loc.endswith('.smd'):
			inst.single_dupe(loc, base, new, parent)
		else:
			inst.batch_dupe(loc, base, new, parent)

	def bd_menu(self):
		self.base_label.grid(column=2, row=5, sticky=(S, W))
		self.bname_entry.grid(column=3, row=5, sticky=(N, E, W))
		self.new_label.grid(column=2, row=6, sticky=(S, W))
		self.nname_entry.grid(column=3, row=6, sticky=(N, E, W))
		self.parent_label.grid(column=2, row=7, sticky=(S, W))
		self.pname_entry.grid(column=3, row=7, sticky=(N, E, W))
		self.action_button.grid(column=3, row=9, sticky=(S), padx=(0, 230))
		self.ws3.grid(column=1, row=8, sticky=(S))
		self.bmp_button.grid_remove()
		self.matrn_button.grid_remove()
		self.ref_label.grid_remove()
		self.ref_entry.grid_remove()
		self.ws4.grid_remove()
		self.rename_label.grid_remove()
		self.rename_entry.grid_remove()
		self.replace_label.grid_remove()
		self.replace_entry.grid_remove()
	def mnc_menu(self):
		self.base_label.grid_remove()
		self.bname_entry.grid_remove()
		self.new_label.grid_remove()
		self.nname_entry.grid_remove()
		self.parent_label.grid_remove()
		self.pname_entry.grid_remove()
		self.action_button.grid_remove()
		self.ws3.grid_remove()
		self.bmp_button.grid(column=2, row=9, sticky=(S), padx=(150, 0))
		self.matrn_button.grid(column=3, row=9, sticky=(S), padx=(0, 110))
		self.ref_label.grid(column=2, row=5, sticky=(S, W))
		self.ref_entry.grid(column=3, row=5, sticky=(N, E, W))
		self.ws4.grid(column=1, row=8, sticky=(S))
		self.rename_label.grid(column=2, row=6, sticky=(S, W))
		self.rename_entry.grid(column=3, row=6, sticky=(N, E, W))
		self.replace_label.grid(column=2, row=7, sticky=(S, W))
		self.replace_entry.grid(column=3, row=7, sticky=(N, E, W))
	
	def bmp(self):
		inst = PointerFix()
		loc = self.path.get()
		ref = self.ref.get()
		inst.add_bmp(loc, ref)
	
	def bmp_scr(self, ref):
		inst = PointerFix()
		loc = self.path.get()
		inst.add_bmp(loc, ref)

	def matrename(self):
		inst = PointerFix()
		loc = self.path.get()
		ref = self.ref.get()
		torename = self.rename.get()
		replace = self.replace.get()
		inst.rename_part(loc, ref, torename, replace)
	
	def matrename_scr(self, ref, torename, replace):
		inst = PointerFix()
		loc = self.path.get()
		inst.rename_part(loc, ref, torename, replace)
	
	def scripts(self):
		inst = ScriptWin()
	
	def fakesoft(self):
		pass

	def options(self):
		inst = OptWin()
	
	def exec_script(self, script):
		print('Executing script')
		values = []
		mode = script[0]
		if mode == 'd':
			for d in script[1]:
				if d == '-':
					self.dupe_scr(values[0], values[1], values[2])
					values = []
					continue
				else:
					values.append(d)
		elif mode == 'm':
			for d in script[1]:
				if d == '-':
					self.matrename_scr(values[0], values[1], values[2])
					values = []
					continue
				else:
					values.append(d)
		elif mode == 'b':
			for d in script[1]:
				if d == '-':
					self.bmp_scr(values[0])
					values = []
					continue
				else:
					values.append(d)
		elif mode == 'p':
			print(script)
			filename = script[1][0]
			# We do this for the plugin file as the importing function uses an absolute path (e.g. "C://something/")
			script_dir = Path(__file__).parent
			mymodule_path = str(script_dir.joinpath('plugins', filename + '.py'))
			# Import plugin file as a normal .py script
			loader = importlib.machinery.SourceFileLoader(filename, mymodule_path)
			plugin = importlib.util.spec_from_loader(filename, loader)
			exec_plugin = importlib.util.module_from_spec(plugin)
			loader.exec_module(exec_plugin)



root = Tk()
guii = GUI(root)
root.mainloop()
