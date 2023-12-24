import json
import shutil

class PointerFix:
	
	def __init__(self):
		pass

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

	# nl_clean removes the \n (new line) character from every object in an array
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

	def list_to_string(self, listt):
		stringy = ''
		for l in listt:
			stringy += l
		return stringy

	def rename_part(self, file, ref, torename, replace):
		opt = self.options()
		if opt["backup_smd"]:
			directory = file.rstrip('.smd') + 'B.smd'
			shutil.copy(file, directory)
		mdl = open(file, 'r')
		mdl_smd = self.nl_clean(mdl.readlines())
		if ref.startswith('*'):
			check_end = True
			find_spec = False
			ref = ref[-1:]
		elif ref.endswith('*'):
			check_end = False
			find_spec = False
		else:
			find_spec = True
			print("Format Error: '*' is not at the start nor end of reference variable")
		count = -1
		if check_end:
			for l in mdl_smd:
				count += 1
				if l.endswith(ref):
					mdl_smd[count] = l.replace(torename, replace)
			mdl = open(file, 'w')
			mdl_smd = self.nl_insert(mdl_smd)
			mdl.write(self.list_to_string(mdl_smd))
			mdl.close()
			print("SMD Written")
		elif not find_spec:
			pass

	def add_bmp(self, file, ref):
		opt = self.options()
		if opt["backup_smd"]:
			directory = file[:-4] + 'B.smd'
			shutil.copy(file, directory)
		mdl = open(file, 'r')
		mdl_smd = self.nl_clean(mdl.readlines())
		skip_line = True
		triangles = False
		if ref == '*':
			count = -1
			mini_c = 0
			for l in mdl_smd:
				count += 1
				if skip_line:
					if l == 'triangles':
						skip_line = False
						triangles = True
						continue
					elif l == 'version 1':
						skip_line = True
						continue
					elif count >= len(mdl_smd) - 2:
						continue
					elif skip_line and triangles:
						mini_c += 1
						if mini_c == 3:
							mini_c = 0
							skip_line = False
						continue
					elif skip_line:
						continue
				mdl_smd[count] = l + '.bmp'
				skip_line = True
		else:
			count = -1
			mini_c = 0
			for l in mdl_smd:
				count += 1
				if skip_line:
					if l == 'triangles':
						skip_line = False
						triangles = True
						continue
					elif l == 'version 1':
						skip_line = True
						continue
					elif count >= len(mdl_smd) - 2:
						continue
					elif skip_line and triangles:
						mini_c += 1
						if mini_c == 3:
							mini_c = 0
							skip_line = False
						continue
					elif skip_line:
						continue
				if l == ref:
					mdl_smd[count] = l + '.bmp'
					skip_line = True

		mdl = open(file, 'w')
		mdl.write(self.list_to_string(self.nl_insert(mdl_smd)))
		mdl.close()
		print('SMD Written')
