# Built-in python libraries, no need to install any dependencies!
import json
from os.path import basename
import os
import shutil

bones = []

# This class stores frames and allows them to be manipulated
class Anim_handler:
	def __init__(self, f_id):
		self.f_id = f_id
		self.frame = None

	def anim_options(self):
		jsf = open('options.json', 'r')
		js = jsf.read()
		count = -1
		options = json.loads(js)
		return options

	def sort_your_stuff(self, e):
		e = e.split(' ')
		return int(e[0])

	def insert_anim(self, dat):
		self.frame = dat
		# print(dat)

	def anim_add(self, tfrm):
		try:
			self.frame.append(tfrm)
			self.frame.sort()
			print(self.frame)
		except:
			print("WARNING: Data can't be found, please add data")

	def create_anim(self, dat):
		new_dat = ""
		off = ''
		count = -1
		for e in dat:
			count += 1
			if count == len(dat) - 2:
				off = ' '
			else:
				off = ''
			new_dat += e + off
			print(new_dat)
		return new_dat

	def meth(self, val1, val2):
		new_val = round(val1 + val2, 6)
		return new_val

	"""def methS(self, val1, val2):
		new_val = round(val1 - val2, 6)
		return new_val"""

	def methM(self, val1, val2):
		new_val = round(val1 * val2, 6)
		return new_val

	"""def methD(self, val1, val2):
		new_val = round(val1 / val2, 6)
		return new_val"""

	def anim_replace(self, tfrm, ogtfrm):
		print("OG Transformation: "+ str(ogtfrm))
		seperate = tfrm.split(' ')
		ogseperate = ogtfrm.split(' ')
		print("Processed line1: " + str(seperate))
		print("Processed line2: "+ str(ogseperate))
		count = 0
		for e in seperate:
			if count == 0:
				count += 1
				continue
			elif count == 1 or count == 5:
				seperate[count] = '  '
				count += 1
			elif count > 5:
				break
			else:
				count += 1
			val = ogseperate[count]
			if count == 4:
				seperate[count] = val
			else:
				seperate[count] = val + ' '
		print("before meth: "+ str(seperate))
		seperate[6] = str(round(float(seperate[6]), 6)) + ' '
		seperate[7] = str(round(float(seperate[7]), 6))
		seperate[8] = str(round(float(seperate[8]), 6))
		print("after meth: "+ str(seperate))
		new_tfrm = self.create_anim(seperate)
		indx = int(seperate[0])
		self.frame.pop(indx)
		print("transformation: " + str(new_tfrm))
		self.frame.append(new_tfrm)
		self.frame.sort(key=self.sort_your_stuff)
		# self.frame.sort()
		# print("New Frame: "+ str(self.frame) + '\n')

	def rip_trans(self, b_id):
		for b in self.frame:
			if b.startswith(str(b_id)):
				filtered_id = str(b_id)
				line = b
				line = b.lstrip(filtered_id)
				line = line.split(' ')
				line.pop(0)
				# line.pop(3)
				print(str(len(line)))
				print(str(type(line)))
				print(str(line))
				return line

	def check_exists(self, b_id):
		for b in self.frame:
			if b.startswith(str(b_id)):
				return True
		return False

	def printDat(self):
		print("\nFrame "+ str(self.f_id) + ": " + str(self.frame))

class Dupe: 
	def options(self):
		jsf = open('options.json', 'r')
		js = jsf.readlines()
		count = -1
		newjs = ''
		for l in js:
			if l.find('//') != -1:
				js.pop(count)
				continue
			newjs += l
		newjs += '}'
		options = json.loads(newjs)
		return options

	# nl_clean removes the \n (new line) character from every object in the array
	def nl_clean(self, smd):
		count = -1
		for l in smd:
			count += 1
			smd[count] = l[:-l.count("\n")]
		return smd
	def nl_insert(self, smd):
		count = -1
		for l in smd:
			count += 1
			nl = l
			nl += '\n'
			smd[count] = nl
		return smd

	def bone_list(self, smd):
		nodes = False
		for l in smd:
			if l == 'nodes':
				nodes = True
				continue
			elif l == 'end' and nodes:
				nodes = False
				break
			elif nodes:
				bones.append(l)
		return bones

	def return_bone_index(self, ref):
		global bones
		indx = ''
		for b in bones:
			if b.find(ref) != -1:
				for c in b:
					if c == '"':
						break
					indx += c
		try:
			n = int(indx)
			print("T_bone: "+ str(n))
			return n
		except:
			indx = indx.split(' ')
			return indx[0]

	def find_bone_index(self, ref):
		global bones
		indx = ''
		for b in bones:
			if b.find(ref) != -1:
				for c in b:
					if c == '"':
						break
					indx += c
		if indx == '':
			return None
		try:
			print("Found bone index")
			n = int(indx)
			return n
		except:
			print("Found bone index")
			indx = indx.split(' ')
			return indx[0]

	def get_bone_parent(self, indx):
		global bones
		parent = None
		for b in bones:
			try:
				if b.startswith(indx):
					thingy = b
					v = len(thingy) - 2
					parent = b
					parent = parent[v:]
			except:
				print("Bone not found")
		# print('Parent: '+ parent)
		# return int(parent)
		return 29

	def list_to_string(self, listt):
		stringy = ''
		for l in listt:
			stringy += l
		return stringy

	def save_smd(self, bones, anim):
		# Note to self: Bone transformation format is X1 Y1 Z1 X2 Y2 Z2, no rotation.
		global smd
		file = ['version 1\n', 'nodes\n']
		bones = self.nl_insert(bones)
		bones = self.list_to_string(bones)
		file.append(bones)
		file.append('end\n')
		file.append('skeleton\n')
		count = -1
		for f in anim:
			count += 1
			file.append('time ' + str(count) + '\n')
			anm = self.nl_insert(f.frame)
			anm = self.list_to_string(anm)
			file.append(anm)
		file.append('end\n')
		new_smd = open(self.smd, 'w')
		smdd = self.list_to_string(file)
		new_smd.write(smdd)
		new_smd.close()
		print('SMD created!')

	def save_smd2(self, bones, anim):
		# SMDeez Nuts
		global smd
		file = ['version 1\n', 'nodes\n']
		# print("Final bone list: "+ str(bones))
		bones = self.nl_insert(bones)
		bones = self.list_to_string(bones)
		file.append(bones)
		file.append('end\n')
		file.append('skeleton\n')
		count = -1
		for f in anim:
			count += 1
			file.append('time ' + str(count) + '\n')
			anm = self.nl_insert(f.frame)
			anm = self.list_to_string(anm)
			file.append(anm)
		file.append('end\n')
		new_smd = open(self.filePath, 'w')
		smdd = self.list_to_string(file)
		new_smd.write(smdd)
		new_smd.close()
		print('SMD created!')

	def add_spaces(self, listt):
		counter = -1
		new_list = listt
		print(listt)
		for e in listt:
			counter += 1
			if counter == len(listt) - 1:
				continue
			if counter == 0:
				el = e + '  '
			else:
				el = e + ' '
			new_list[counter] = el
		print(str(new_list))
		stringg = ''
		for e in new_list:
			stringg += e
		print(stringg)
		return stringg

	def flush_dat(self):
		global raw_contents
		global smd_contents
		global bones
		global t_bone
		global pp_bone
		global t_bone_parent
		global bb_bone
		global data
		global frames
		global capture
		global time_frame
		global t
		global thingyy
		global new_thing
		global tt
		global thingyyt
		global new_thingt
		raw_contents = None
		smd_contents = None
		bones = []
		t_bone = None
		pp_bone = None
		t_bone_parent = None
		bb_bone = None
		data = None
		frames = None
		capture = False
		tvalue = -1
		time_frame = None
		t = None
		thingyy = None
		new_thing = None
		tt = None
		thingyyt = None
		new_thingt = None

	# Functional part of the code (Command-line interface)
	def batch_dupe(self, smd, b_bone, n_bone, p_bone):
		opts = self.options()
		if opts["backup_smd"]:
			directory = smd + 'B'
			shutil.copy(smd, directory)
		for folderName, subfolders, filenames in os.walk(smd):
			for filename in filenames:
				self.filePath = os.path.join(folderName, filename)
				smd_file = open(self.filePath)
				raw_contents = smd_file.readlines()
				smd_contents = self.nl_clean(raw_contents)
				bones = self.bone_list(smd_contents)

				t_bone = None

				pp_bone = self.return_bone_index(p_bone)
				if self.find_bone_index(n_bone) == None:
					bones.append(str(len(bones))+ ' '  + '"'+ n_bone + '"' + ' ' + str(pp_bone))
				else:
					print('Bone already exists, skip adding a new bone to the bone id list.')
					t_bone = self.return_bone_index(n_bone)
					t_bone_parent = self.get_bone_parent(t_bone)
					bb_bone = self.return_bone_index(b_bone)
					print('Bone id: '+ str(t_bone))
					print('Bone to copy: '+ str(bb_bone))
				# print(str(smd_contents.readlines()))
				print("Bones: " + str(bones))
				data = []
				frames = []
				capture = False
				tvalue = -1
				print("Finding animation frames")
				for l in smd_contents:
					if l.startswith('time'):
						capture = True
						tvalue += 1
						try:
							time_frame.insert_anim(data)
						except:
							time_frame = Anim_handler(tvalue)
						frames.append(time_frame)
						data = []
						time_frame = Anim_handler(tvalue)
					elif l == 'end' and capture:
						time_frame.insert_anim(data)
						frames.append(time_frame)
						break
					elif capture:
						data.append(l)
				print("Amount of frames: "+ str(len(frames)))
				frames.pop(0)
				# frames[0].rip_trans(b_bone)
				for f in frames:
					t = f.rip_trans(bb_bone)
					# print(str(t_bone) + str(t))
					thingyy = self.add_spaces(t)
					new_thing = str(t_bone) + thingyy
					tt = f.rip_trans(t_bone)
					thingyyt = self.add_spaces(tt)
					new_thingt = str(t_bone) + thingyyt
					if f.check_exists(t_bone):
						f.anim_replace(new_thing, new_thingt)
				self.smd = smd
				self.save_smd2(bones, frames)
				self.flush_dat()
	def single_dupe(self, smd, b_bone, n_bone, p_bone):
		opts = self.options()
		smd_file = open(smd)
		if opts["backup_smd"]:
			directory = smd.rstrip('.smd') + 'B.smd'
			shutil.copy(smd, directory)
		raw_contents = smd_file.readlines()
		smd_contents = self.nl_clean(raw_contents)
		bones = self.bone_list(smd_contents)

		t_bone = None

		p_bone = self.return_bone_index(p_bone)
		if self.find_bone_index(n_bone) == None:
			bones.append(str(len(bones))+ ' '  + '"'+ n_bone + '"' + ' ' + str(p_bone))
		else:
			print('Bone already exists, skip adding a new bone to the bone id list.')
			t_bone = self.return_bone_index(n_bone)
			t_bone_parent = self.get_bone_parent(t_bone)
			b_bone = self.return_bone_index(b_bone)
			print('Bone id: '+ str(t_bone))
			print('Bone to copy: '+ str(b_bone))
		# print(str(smd_contents.readlines()))
		print("Bones: " + str(bones))
		data = []
		frames = []
		capture = False
		tvalue = -1
		print(smd_contents, flush=True)
		for l in smd_contents:
			if l.startswith('time'):
				capture = True
				tvalue += 1
				try:
					time_frame.insert_anim(data)
				except:
					time_frame = Anim_handler(tvalue)
				frames.append(time_frame)
				data = []
				time_frame = Anim_handler(tvalue)
			elif l == 'end' and capture:
				time_frame.insert_anim(data)
				frames.append(time_frame)
				break
			elif capture:
				data.append(l)
		print("Amount of frames: "+ str(len(frames)))
		frames.pop(0)
		# frames[0].rip_trans(b_bone)
		for f in frames:
			t = f.rip_trans(b_bone)
			# print(str(t_bone) + str(t))
			thingyy = self.add_spaces(t)
			new_thing = str(t_bone) + thingyy
			tt = f.rip_trans(t_bone)
			thingyyt = self.add_spaces(tt)
			new_thingt = str(t_bone) + thingyyt
			if f.check_exists(t_bone):
				f.anim_replace(new_thing, new_thingt)
		self.smd = smd
		self.save_smd(bones, frames)
		self.flush_dat()

class FakeSoft:
	def options(self):
		jsf = open('options.json', 'r')
		js = jsf.readlines()
		count = -1
		newjs = ''
		for l in js:
			if l.find('//') != -1:
				js.pop(count)
				continue
			newjs += l
		newjs += '}'
		options = json.loads(newjs)
		return options

	# nl_clean removes the \n (new line) character from every object in the array
	def nl_clean(self, smd):
		count = -1
		for l in smd:
			count += 1
			smd[count] = l[:-l.count("\n")]
		return smd
	def nl_insert(self, smd):
		count = -1
		for l in smd:
			count += 1
			nl = l
			nl += '\n'
			smd[count] = nl
		return smd

	def bone_list(self, smd):
		nodes = False
		for l in smd:
			if l == 'nodes':
				nodes = True
				continue
			elif l == 'end' and nodes:
				nodes = False
				break
			elif nodes:
				bones.append(l)
		return bones

	def return_bone_index(self, ref):
		global bones
		indx = ''
		for b in bones:
			if b.find(ref) != -1:
				for c in b:
					if c == '"':
						break
					indx += c
		try:
			n = int(indx)
			print("T_bone: "+ str(n))
			return n
		except:
			indx = indx.split(' ')
			return indx[0]

	def find_bone_index(self, ref):
		global bones
		indx = ''
		for b in bones:
			if b.find(ref) != -1:
				for c in b:
					if c == '"':
						break
					indx += c
		if indx == '':
			return None
		try:
			print("Found bone index")
			n = int(indx)
			return n
		except:
			print("Found bone index")
			indx = indx.split(' ')
			return indx[0]

	def get_bone_parent(self, indx):
		global bones
		parent = None
		for b in bones:
			try:
				if b.startswith(indx):
					thingy = b
					v = len(thingy) - 2
					parent = b
					parent = parent[v:]
			except:
				print("Bone not found")
		# print('Parent: '+ parent)
		# return int(parent)
		return 29

	def list_to_string(self, listt):
		stringy = ''
		for l in listt:
			stringy += l
		return stringy

	def save_smd(self, bones, anim):
		# Note to self: Bone transformation format is X1 Y1 Z1 X2 Y2 Z2, no rotation.
		global smd
		file = ['version 1\n', 'nodes\n']
		bones = self.nl_insert(bones)
		bones = self.list_to_string(bones)
		file.append(bones)
		file.append('end\n')
		file.append('skeleton\n')
		count = -1
		for f in anim:
			count += 1
			file.append('time ' + str(count) + '\n')
			anm = self.nl_insert(f.frame)
			anm = self.list_to_string(anm)
			file.append(anm)
		file.append('end\n')
		new_smd = open(self.smd, 'w')
		smdd = self.list_to_string(file)
		new_smd.write(smdd)
		new_smd.close()
		print('SMD created!')

	def save_smd2(self, bones, anim):
		# SMDeez Nuts
		global smd
		file = ['version 1\n', 'nodes\n']
		# print("Final bone list: "+ str(bones))
		bones = self.nl_insert(bones)
		bones = self.list_to_string(bones)
		file.append(bones)
		file.append('end\n')
		file.append('skeleton\n')
		count = -1
		for f in anim:
			count += 1
			file.append('time ' + str(count) + '\n')
			anm = self.nl_insert(f.frame)
			anm = self.list_to_string(anm)
			file.append(anm)
		file.append('end\n')
		new_smd = open(self.filePath, 'w')
		smdd = self.list_to_string(file)
		new_smd.write(smdd)
		new_smd.close()
		print('SMD created!')

	def add_spaces(self, listt):
		counter = -1
		new_list = listt
		print(listt)
		for e in listt:
			counter += 1
			if counter == len(listt) - 1:
				continue
			if counter == 0:
				el = e + '  '
			else:
				el = e + ' '
			new_list[counter] = el
		print(str(new_list))
		stringg = ''
		for e in new_list:
			stringg += e
		print(stringg)
		return stringg

	def flush_dat(self):
		global raw_contents
		global smd_contents
		global bones
		global t_bone
		global pp_bone
		global t_bone_parent
		global bb_bone
		global data
		global frames
		global capture
		global time_frame
		global t
		global thingyy
		global new_thing
		global tt
		global thingyyt
		global new_thingt
		raw_contents = None
		smd_contents = None
		bones = []
		t_bone = None
		pp_bone = None
		t_bone_parent = None
		bb_bone = None
		data = None
		frames = None
		capture = False
		tvalue = -1
		time_frame = None
		t = None
		thingyy = None
		new_thing = None
		tt = None
		thingyyt = None
		new_thingt = None

	# Functional part of the code (Command-line interface)
	def batch_dupe(self, smd, b_bone, n_bone, p_bone):
		opts = self.options()
		if opts["backup_smd"]:
			directory = smd + 'B'
			shutil.copy(smd, directory)
		for folderName, subfolders, filenames in os.walk(smd):
			for filename in filenames:
				self.filePath = os.path.join(folderName, filename)
				smd_file = open(self.filePath)
				raw_contents = smd_file.readlines()
				smd_contents = self.nl_clean(raw_contents)
				bones = self.bone_list(smd_contents)

				t_bone = None

				pp_bone = self.return_bone_index(p_bone)
				if self.find_bone_index(n_bone) == None:
					bones.append(str(len(bones))+ ' '  + '"'+ n_bone + '"' + ' ' + str(pp_bone))
				else:
					print('Bone already exists, skip adding a new bone to the bone id list.')
					t_bone = self.return_bone_index(n_bone)
					t_bone_parent = self.get_bone_parent(t_bone)
					bb_bone = self.return_bone_index(b_bone)
					print('Bone id: '+ str(t_bone))
					print('Bone to copy: '+ str(bb_bone))
				# print(str(smd_contents.readlines()))
				print("Bones: " + str(bones))
				data = []
				frames = []
				capture = False
				tvalue = -1
				print("Finding animation frames")
				for l in smd_contents:
					if l.startswith('time'):
						capture = True
						tvalue += 1
						try:
							time_frame.insert_anim(data)
						except:
							time_frame = Anim_handler(tvalue)
						frames.append(time_frame)
						data = []
						time_frame = Anim_handler(tvalue)
					elif l == 'end' and capture:
						time_frame.insert_anim(data)
						frames.append(time_frame)
						break
					elif capture:
						data.append(l)
				print("Amount of frames: "+ str(len(frames)))
				frames.pop(0)
				# frames[0].rip_trans(b_bone)
				for f in frames:
					t = f.rip_trans(bb_bone)
					# print(str(t_bone) + str(t))
					thingyy = self.add_spaces(t)
					new_thing = str(t_bone) + thingyy
					tt = f.rip_trans(t_bone)
					thingyyt = self.add_spaces(tt)
					new_thingt = str(t_bone) + thingyyt
					if f.check_exists(t_bone):
						f.anim_replace(new_thing, new_thingt)
				self.smd = smd
				self.save_smd2(bones, frames)
				self.flush_dat()
	def single_dupe(self, smd, b_bone, n_bone, p_bone):
		opts = self.options()
		smd_file = open(smd)
		if opts["backup_smd"]:
			directory = smd.rstrip('.smd') + 'B.smd'
			shutil.copy(smd, directory)
		raw_contents = smd_file.readlines()
		smd_contents = self.nl_clean(raw_contents)
		bones = self.bone_list(smd_contents)

		t_bone = None

		p_bone = self.return_bone_index(p_bone)
		if self.find_bone_index(n_bone) == None:
			bones.append(str(len(bones))+ ' '  + '"'+ n_bone + '"' + ' ' + str(p_bone))
		else:
			print('Bone already exists, skip adding a new bone to the bone id list.')
			t_bone = self.return_bone_index(n_bone)
			t_bone_parent = self.get_bone_parent(t_bone)
			b_bone = self.return_bone_index(b_bone)
			print('Bone id: '+ str(t_bone))
			print('Bone to copy: '+ str(b_bone))
		# print(str(smd_contents.readlines()))
		print("Bones: " + str(bones))
		data = []
		frames = []
		capture = False
		tvalue = -1
		print(smd_contents, flush=True)
		for l in smd_contents:
			if l.startswith('time'):
				capture = True
				tvalue += 1
				try:
					time_frame.insert_anim(data)
				except:
					time_frame = Anim_handler(tvalue)
				frames.append(time_frame)
				data = []
				time_frame = Anim_handler(tvalue)
			elif l == 'end' and capture:
				time_frame.insert_anim(data)
				frames.append(time_frame)
				break
			elif capture:
				data.append(l)
		print("Amount of frames: "+ str(len(frames)))
		frames.pop(0)
		# frames[0].rip_trans(b_bone)
		for f in frames:
			t = f.rip_trans(b_bone)
			# print(str(t_bone) + str(t))
			thingyy = self.add_spaces(t)
			new_thing = str(t_bone) + thingyy
			tt = f.rip_trans(t_bone)
			thingyyt = self.add_spaces(tt)
			new_thingt = str(t_bone) + thingyyt
			if f.check_exists(t_bone):
				f.anim_replace(new_thing, new_thingt)
		self.smd = smd
		self.save_smd(bones, frames)
		self.flush_dat()
