import json
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
# from tkinter import font
from SMDBone import Dupe
from SMDMat import PointerFix
import os
from os.path import *
import importlib.machinery
import importlib.util
from pathlib import Path
# OH MY GOD MARIO REFERENCE!!?!
import webbrowser as browser
import sys
from urllib.request import urlopen

selected_scr = ''
scr_dat = ''

class Flags:

    def __init__(self):
        self.pyinstaller = True

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
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		self.scripts = []
		if getattr(sys, 'frozen', False):
			EXE_LOCATION = os.path.dirname( sys.executable )
		else:
			EXE_LOCATION = os.path.dirname( os.path.realpath( __file__ ) )
		scr_dir = os.path.join(EXE_LOCATION, "scripts")
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
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		jsf = open('save/options.json', 'r')
		js = jsf.read()
		self.options = json.loads(js)

		self.b_smd_val = BooleanVar(frame, value=self.options["backup_smd"])
		print(self.b_smd_val.get())
		b_smd = Checkbutton(frame, text="Backup SMDs", variable=self.b_smd_val, command=self.set_backup_smd)
		b_smd.grid(column=1, row=1, sticky=(S), padx=50, pady=40)

		"""self.s_vals_val = BooleanVar(frame, value=self.options["save_paths"])
		s_vals = Checkbutton(frame, text="Save User Inputs", variable=self.s_vals_val, command=self.set_save_values)
		s_vals.grid(column=1, row=1, sticky=(S), padx=50, pady=60)"""

		select_scr = Button(frame, text="Confirm", command=self.confirm_opts)
		select_scr.grid(column=1, row=6, sticky=(S))
	
	def set_backup_smd(self):
		self.options["backup_smd"] = self.b_smd_val.get()
		print(self.options["backup_smd"])
	
	def set_save_values(self):
		self.options["save_paths"] = self.s_vals_val.get()
		print(self.options["backup_smd"])
	
	def confirm_opts(self):
		newjson = json.dumps(self.options, sort_keys=True, indent=5)
		opts = open('save/options.json', 'w')
		opts.write(newjson)
		opts.close()
		self.nroot.destroy()

"""class PluginWarning:

	def __init__(self, plugin_to_run):
		self.nroot = Tk()
		self.win(plugin_to_run)
		self.nroot.mainloop()

	def win(self, plugin_to_run):
		global guii
		self.nroot.title("PLUGIN WARNING")
		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)
		self.filename = plugin_to_run

		b_smd = Label(frame, text="WARNING: You are about to run a plugin, plugins are loaded as normal python modules with no checks for security!\nIf you trust the author of this plugin, click confirm, otherwise click deny if you believe that the plugin could be malicious.\nBY CLICKING CONFIRM YOU COULD RISK RUNNING A MALICIOUS SCRIPT, I SHOULD NOT BE HELD LIABLE FOR ANY DAMAGE A MALICIOUS PLUGIN MAY CAUSE TO YOUR SYSTEM")
		b_smd.grid(column=1, row=1, sticky=(S), padx=25, pady=25)

		select_scr = Button(frame, text="Confirm", command=self.run_plugin)
		select_scr.grid(column=1, row=6, sticky=(S), padx=(0, 75))

		select_scr = Button(frame, text="Deny", command=self.deny)
		select_scr.grid(column=1, row=6, sticky=(S), padx=(75, 0))
	
	def run_plugin(self):
		self.nroot.destroy()
		# We do this for the plugin file as the importing function uses an absolute path (e.g. "C://something/")
		script_dir = Path(__file__).parent
		mymodule_path = str(script_dir.joinpath('plugins', self.filename + '.py'))
		# Import plugin file as a normal .py script
		loader = importlib.machinery.SourceFileLoader(self.filename, mymodule_path)
		plugin = importlib.util.spec_from_loader(self.filename, loader)
		exec_plugin = importlib.util.module_from_spec(plugin)
		loader.exec_module(exec_plugin)
	
	def deny(self):
		self.nroot.destroy()"""

class GetNewVersion:

	def __init__(self, version):
		self.nroot = Tk()
		v = version.split("-")[0]
		self.win(v)
		self.nroot.mainloop()

	def win(self, ver):
		self.nroot.title(f"Version {ver} is out!")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)
		buttons = Frame(frame, borderwidth=2)
		buttons.grid(column=1, row=1, sticky=(S), columnspan=10)

		text = Label(frame, text="A new version of PostScript's SMD Tools has been released,\n do you want to update to the new version?")
		text.grid(column=1, row=0, padx=50, pady=40)

		self.dlButton = Button(buttons, text="Yes", command=self.releasesPage)
		self.dlButton.grid(column=0, row=1, sticky=(S))
		self.noButton = Button(buttons, text="No", command=self.closeWin)
		self.noButton.grid(column=1, row=1, sticky=(S))
	
	def releasesPage(self):
		browser.open_new_tab("https://github.com/PostScriptReal/PS-SMD-Tools/releases/latest")
		self.nroot.destroy()
	
	def closeWin(self):
		self.nroot.destroy()
	
	def confirm_opts(self):
		newjson = json.dumps(self.options, sort_keys=True, indent=5)
		opts = open('save/options.json', 'w')
		opts.write(newjson)
		opts.close()
		self.nroot.destroy()

class About:

	def __init__(self, ver):
		self.nroot = Tk()
		self.win(ver)
		self.nroot.mainloop()

	def win(self, ver):
		self.nroot.title("About PS's SMD Tools")
		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		b_smd = Label(frame, text=f"PostScript's SMD Tools {ver}")
		b_smd.grid(column=1, row=1, sticky=(S), padx=25, pady=25)

		select_scr = Button(frame, text="Close", command=self.close)
		select_scr.grid(column=1, row=6, sticky=(S))
	
	def close(self):
		self.nroot.destroy()

class GUI:
	def get_options(self):
		jsf = open('save/options.json', 'r')
		js = jsf.read()
		jsf.close()
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
	
	def check_version(self):
		url = "https://github.com/PostScriptReal/PS-SMD-Tools/raw/refs/heads/main/version.txt"
		webVer = urlopen(url).read().decode('utf-8')
		print(webVer)

		# Don't you dare make a Fortnite joke
		vFile = open("version.txt", "r")
		curVer = vFile.read()

		if curVer != webVer:
			a = GetNewVersion(webVer)

	def __init__(self, root):
		# Set Window title
		root.title("PostScript's SMD Tools")
		if sys.platform == 'linux':
			self.fixGUI = True
		else:
			self.fixGUI = False
		# print(font.nametofont('TkDefaultFont').actual())
		
		# Get Options
		self.get_options()
		if self.options["save_paths"]:
			self.save_paths = True
			js = open("save/paths.json", 'r')
			self.sPaths = json.loads(js.read())
			self.bonez = self.sPaths["bonez"]
			self.matfix = self.sPaths["matFix"]
		else:
			self.save_paths = False

		# Create Window
		frame = Frame(root, borderwidth=2, relief="sunken")
		frame.grid(column=6, row=2, sticky=(N, E, S, W))
		header = Frame(frame, borderwidth=2)
		header.grid(column=1, row=1, sticky=(N), columnspan=10)
		mtbtns = Frame(frame, borderwidth=2)
		mtbtns.grid(column=1, row=9, sticky=(S), columnspan=10)
		root.columnconfigure(6, weight=1)
		root.rowconfigure(2, weight=1)

		# Create Header Buttons
		self.dupe_button = Button(header, text="Bone Dupe", command=self.bd_menu)
		self.dupe_button.grid(column=1, row=1, sticky=(N))

		self.mat_button = Button(header, text="Material Fix", command=self.mnc_menu)
		self.mat_button.grid(column=2, row=1, sticky=(N))

		# Getting rid of this because I don't think I could reasonably create something like this
		"""fakeweight = Button(frame, text="Soft Weights", command=self.fakesoft)
		fakeweight.grid(column=3, row=1, sticky=(N), padx=(0, 195))"""

		self.scripts = Button(header, text="Scripts", command=self.scripts)
		self.scripts.grid(column=3, row=1, sticky=(N))
		
		self.options = Button(header, text="Options", command=self.optionsMenu)
		self.options.grid(column=5, row=1, sticky=(N))

		self.help = Button(header, text="Help", command=self.help)
		self.help.grid(column=6, row=1, sticky=(N))
		
		self.aboutB = Button(header, text="About", command=self.about)
		self.aboutB.grid(column=4, row=1, sticky=(N))

		self.tile_label = Label(frame, text="Path to SMDs")
		self.tile_label.grid(column=2, row=3)

		self.path = StringVar()
		if self.save_paths and not self.bonez["path"] == "":
			self.path.set(self.bonez["path"])
		self.tname_entry = Entry(frame, textvariable=self.path, width=50)
		self.tname_entry.grid(column=3, row=3, sticky=(E, W))

		self.save_button = Button(frame, text="File", command=self.openfile)
		self.save_button.grid(column=5, row=3, sticky=(S))

		self.dir_button = Button(frame, text="Folder", command=self.opendir)
		self.dir_button.grid(column=7, row=3, sticky=(S))

		self.base_label = Label(frame, text="Select Base Bone")
		self.base_label.grid(column=2, row=5, sticky=(S))

		self.b_bone = StringVar()
		self.bname_entry = Entry(frame, textvariable=self.b_bone, width=50)
		self.bname_entry.grid(column=3, row=5, sticky=(N))

		self.new_label = Label(frame, text="Select New Bone")
		self.new_label.grid(column=2, row=6, sticky=(S))

		self.n_bone = StringVar()
		self.nname_entry = Entry(frame, textvariable=self.n_bone, width=50)
		self.nname_entry.grid(column=3, row=6, sticky=(N))

		self.parent_label = Label(frame, text="Select Parent Bone")
		self.parent_label.grid(column=2, row=7, sticky=(S))

		self.p_bone = StringVar()
		self.pname_entry = Entry(frame, textvariable=self.p_bone, width=50)
		self.pname_entry.grid(column=3, row=7, sticky=(N, E, W))

		self.action_button = Button(mtbtns, text="Dupe", command=self.dupe)
		self.action_button.grid(column=1, row=9, sticky=(S))

		self.bmp_button = Button(mtbtns, text="File Ext", command=self.bmp)
		self.matrn_button = Button(mtbtns, text="Fix Pointer", command=self.matrename)

		self.ref_label = Label(frame, text="Type Finder Value")

		self.ref = StringVar()
		self.ref_entry = Entry(frame, textvariable=self.ref, width=50)

		self.rename_label = Label(frame, text="String Part To Rename")

		self.rename = StringVar()
		self.rename_entry = Entry(frame, textvariable=self.rename, width=50)

		self.replace_label = Label(frame, text="String Part To Replace")

		self.replace = StringVar()
		self.replace_entry = Entry(frame, textvariable=self.replace, width=50)

		# Objects to add whitespace to borders
		ws = Label(frame, text='   ')
		ws.grid(column=8, row=1, sticky=(S))
		ws5 = Label(frame, text='   ')
		ws5.grid(column=1, row=2, sticky=(S))
		ws2 = Label(frame, text='   ')
		ws2.grid(column=1, row=4, sticky=(S))
		self.ws3 = Label(frame, text='   ')
		self.ws3.grid(column=1, row=8, sticky=(S))
		self.ws4 = Label(frame, text='   ')
		self.ws6 = Label(mtbtns, text='       ')
		ws7 = Label(frame, text='   ')
		ws7.grid(column=4, row=3, sticky=(S))
		ws8 = Label(frame, text='   ')
		ws8.grid(column=6, row=3, sticky=(S))
		vnum = open('version.txt', "r")
		self.ver = vnum.read().replace("(OS)", sys.platform)
		version = Label(frame, text=self.ver)
		version.grid(column=2, row=69, sticky=(W, S), columnspan=2)
		self.check_version()

	def help(self):
		browser.open_new_tab('https://github.com/PostScriptReal/PS-SMD-Tools/wiki')
	
	def about(self):
		a = About(self.ver)
	
	def openfile(self):
		# startdir = self.options["startFolder"]
		startDir = os.path.expanduser("~/Documents")
		self.path.set(askopenfilename(title="Select SMD", initialdir=startDir))
	def opendir(self):
		# startdir = self.options["startFolder"]
		startDir = os.path.expanduser("~/Documents")
		self.path.set(askdirectory(title="Select Anims Folder", initialdir=startDir))

	def dupe(self):
		# Initialising Bone Duping function
		inst = Dupe()
		# Grabbing all values from input boxes
		loc = self.path.get()
		base = self.b_bone.get()
		new = self.n_bone.get()
		parent = self.p_bone.get()
		# Checking if specified location is a folder or file, batch dupe is performed if a folder, otherwise a single dupe is performed
		if loc.endswith('.smd'):
			inst.single_dupe(loc, base, new, parent)
		else:
			inst.batch_dupe(loc, base, new, parent)
	def dupe_scr(self, base, new, parent):
		# Alternate bone duping function for scripts
		inst = Dupe()
		loc = self.path.get()
		if loc.endswith('.smd'):
			inst.single_dupe(loc, base, new, parent)
		else:
			inst.batch_dupe(loc, base, new, parent)

	""" Switches menu to the Bone Dupe Menu """
	def bd_menu(self):
		# Displaying Bone Dupe options
		self.base_label.grid(column=2, row=5, sticky=(S))
		self.bname_entry.grid(column=3, row=5, sticky=(N, E, W))
		self.new_label.grid(column=2, row=6, sticky=(S,))
		self.nname_entry.grid(column=3, row=6, sticky=(N, E, W))
		self.parent_label.grid(column=2, row=7, sticky=(S))
		self.pname_entry.grid(column=3, row=7, sticky=(N, E, W))
		self.action_button.grid(column=1, row=9, sticky=(S), padx=(0, 0), columnspan=5)
		self.ws3.grid(column=1, row=8, sticky=(S))
		# Removing SMD Mat options
		self.bmp_button.grid_remove()
		self.matrn_button.grid_remove()
		self.ref_label.grid_remove()
		self.ref_entry.grid_remove()
		self.ws4.grid_remove()
		self.rename_label.grid_remove()
		self.rename_entry.grid_remove()
		self.replace_label.grid_remove()
		self.replace_entry.grid_remove()
		self.ws6.grid_remove()
		# Fix centering for Header buttons
		"""self.dupe_button.grid(column=2, row=1, sticky=(N), padx=(110, 0))
		if not self.fixGUI:
			self.mat_button.grid(column=2, row=1, sticky=(N), padx=(280, 0))
		else:
			self.mat_button.grid(column=2, row=1, sticky=(N), padx=(316, 0))
		if not self.fixGUI:
			self.scripts.grid(column=3, row=1, sticky=(N), padx=(0, 208))
		else:
			self.scripts.grid(column=3, row=1, sticky=(N), padx=(0, 262))
		if not self.fixGUI:
			self.options.grid(column=3, row=1, sticky=(N), padx=(0, 108))
		else:
			self.options.grid(column=3, row=1, sticky=(N), padx=(0, 110))
		if not self.fixGUI:
			self.help.grid(column=3, row=1, sticky=(N), padx=(0, 20))
		else:
			self.help.grid(column=3, row=1, sticky=(N), padx=(28, 0))"""
		
	
	""" Switches menu to SMD Material options """
	def mnc_menu(self):
		# Removing Bone Dupe options
		self.base_label.grid_remove()
		self.bname_entry.grid_remove()
		self.new_label.grid_remove()
		self.nname_entry.grid_remove()
		self.parent_label.grid_remove()
		self.pname_entry.grid_remove()
		self.action_button.grid_remove()
		self.ws3.grid_remove()
		# Displaying SMD Mat options
		self.bmp_button.grid(column=0, row=9, sticky=(S))
		self.ws6.grid(column=1, row=9, sticky=(S))
		self.matrn_button.grid(column=2, row=9, sticky=(S))
		self.ref_label.grid(column=2, row=5, sticky=(S))
		self.ref_entry.grid(column=3, row=5, sticky=(N, E, W))
		self.ws4.grid(column=1, row=8, sticky=(S))
		self.rename_label.grid(column=2, row=6, sticky=(S, W))
		self.rename_entry.grid(column=3, row=6, sticky=(N, E, W))
		self.replace_label.grid(column=2, row=7, sticky=(S, W))
		self.replace_entry.grid(column=3, row=7, sticky=(N, E, W))
		# Fixing Centering for Header Buttons
		"""self.dupe_button.grid(column=2, row=1, sticky=(N), padx=(50, 0))
		if not self.fixGUI:
			self.mat_button.grid(column=2, row=1, sticky=(N), padx=(190, 0))
		else:
			self.mat_button.grid(column=2, row=1, sticky=(N), padx=(256, 0))
		if not self.fixGUI:
			self.scripts.grid(column=3, row=1, sticky=(N), padx=(0, 134))
		else:
			self.scripts.grid(column=3, row=1, sticky=(N), padx=(0, 156))
		if not self.fixGUI:
			self.options.grid(column=3, row=1, sticky=(N), padx=(0, 35))
		else:
			self.options.grid(column=3, row=1, sticky=(N), padx=(0, 3))
		if not self.fixGUI:
			self.help.grid(column=3, row=1, sticky=(N), padx=(55, 0))
		else:
			self.help.grid(column=3, row=1, sticky=(N), padx=(134, 0))"""
	
	def bmp(self):
		# Initialising Pointer fix function
		# We're using it for the .bmp extension function
		inst = PointerFix()
		loc = self.path.get()
		ref = self.ref.get()
		inst.add_bmp(loc, ref)
	
	def bmp_scr(self, ref):
		# Alternate function for scripts
		inst = PointerFix()
		loc = self.path.get()
		inst.add_bmp(loc, ref)

	def matrename(self):
		# Material Pointer Fixing function
		inst = PointerFix()
		loc = self.path.get()
		ref = self.ref.get()
		torename = self.rename.get()
		replace = self.replace.get()
		inst.rename_part(loc, ref, torename, replace)
	
	def matrename_scr(self, ref, torename, replace):
		# Alternate function for scripts
		inst = PointerFix()
		loc = self.path.get()
		inst.rename_part(loc, ref, torename, replace)
	
	def scripts(self):
		# Opens Script selection window
		inst = ScriptWin()

	def optionsMenu(self):
		# Opens options window
		inst = OptWin()
	
	def exec_script(self, script):
		# Script parsing and execution function
		print('Executing script')
		values = []
		mode = script[0]
		# If in duping mode
		if mode == 'd':
			for d in script[1]:
				if d == '-':
					self.dupe_scr(values[0], values[1], values[2])
					values = []
					continue
				else:
					values.append(d)
		# If in pointer fix mode
		elif mode == 'm':
			for d in script[1]:
				if d == '-':
					self.matrename_scr(values[0], values[1], values[2])
					values = []
					continue
				else:
					values.append(d)
		# If in bitmap ext mode
		elif mode == 'b':
			for d in script[1]:
				if d == '-':
					self.bmp_scr(values[0])
					values = []
					continue
				else:
					values.append(d)
		"""# If in plugin initialising mode
		elif mode == 'p':
			print(script)
			filename = script[1][0]
			w = PluginWarning(filename)"""



root = Tk()
guii = GUI(root)
root.mainloop()