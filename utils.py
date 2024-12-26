import os
from tkinter import *
class QCHandler:

    def __init__(self, qc):
        f = open(qc, 'r')
        self.qcf = f.readlines()
        f.close()
        self.qcLoc = os.path.dirname(qc)
	
    def get_bodygroups(self):
        capture = False
        bData = []
        bodygroup = False
        body = False
        count = 0
        for l in self.qcf:
            if not capture:
                count += 1

            if l.startswith('$body') or l.startswith('$bodygroup'):
                capture = True
                count = 0
                if l.startswith('$bodygroup'):
                    bodygroup = True
                else:
                    body = True

            if capture and bodygroup and l.startswith('}'):
                capture = False
                bData.append(l)
            elif capture and body:
                capture = False
                bData.append(l)
            elif capture:
                bData.append(l)

            if count >= 40:
                count = 0
                break
        bodydefs = []
        bcount = 0
        bGName = ''
        bSMD = []
        for b in bData:
            bName = ''
            bSMDN = ''
            bdgLine = False
            endG = False
            if body:
                for c in b:
                    if c == "\"" or c == "\'":
                        bcount += 1
                        if bcount >= 4:
                            bcount = 0
                        continue

                    if bcount == 1:
                        bName += c
                    elif bcount == 3:
                        bSMDN += c
                bodydefs.append({"name": bName, "body": bSMDN})
            elif bodygroup:
                if b.startswith('$bodygroup'):
                    bdgLine = True
                if b.startswith('}'):
                    endG = True
                for c in b:
                    if endG or b.startswith('{'):
                        break
                    elif b.startswith('blank') or b.startswith('\tblank'):
                        break
                    if c == "\"" or c == "\'":
                        bcount += 1
                        if bcount >= 2 and bdgLine:
                            bcount = 0
                        elif bcount >= 2 and not bdgLine:
                            bcount = 0
                            bSMD.append(bSMDN)
                        continue

                    if bcount == 1 and bdgLine:
                        bGName += c
                    elif bcount == 1 and not bdgLine: 
                        bSMDN += c
                if endG:
                    bodydefs.append({"name": bGName, "body": bSMD})
                    bGName = ''
                    bSMD = []
        print(bodydefs)
        self.bodies = bodydefs
    def getAnimFolder(self):
        count = -1
        fndSeq = False
        anim = ''
        qcount = 0
        while count <= len(self.qcf)-1:
            count += 1
            if self.qcf[count].startswith('$sequence'):
                fndSeq = True
                if not self.qcf[count].find('{') == -1 and self.qcf[count].find('}') == -1:
                    continue
                else:
                    for c in self.qcf[count]:
                        if c == '\"' or c == '\'':
                            qcount += 1
                            if qcount >= 4:
                                break
                            continue
                        if qcount == 3:
                            anim += c
                    anim = anim.replace('\"', '')
                    anim = anim.replace('\'', '')
                    break
            elif fndSeq:
                anim = self.qcf[count]
                anim = anim.replace('\t', '')
                anim = anim.replace('\"', '')
                anim = anim.replace('\'', '')
                print(anim)
                break
        thresh = anim.rfind('\\')
        if thresh == -1:
            thresh = anim.rfind('/')
        print(thresh)
        # If the threshold value is still not found, skip this part of the code
        if not thresh == -1:
            while len(anim) > thresh:
                anim = anim[:-1]
            anin = anim.replace('\\', '/')
        print(anim)
        self.animPath = os.path.join(self.qcLoc, anim)

class QCWin(Tk):

    def __init__(self, dat, func, mode:str, values:list, script:bool=False, scrDat:list=[]):
        super().__init__()
        # self.nroot = Tk()
        self.title("Select an SMD")
        self.func = func
        self.mode = mode
        self.values = values
        self.script = script
        self.scrDat = scrDat
        self.win(dat)
        self.mainloop()

    def win(self, dat):
        frame = Frame(self, borderwidth=2, relief="sunken")
        frame.grid(column=1, row=1, sticky=(N, E, S, W))
        btns = Frame(frame, borderwidth=2)
        btns.grid(column=0, row=69, sticky=(N, E, S, W), columnspan=69)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.dat = dat
        self.models = False

        if self.mode == 'm' or self.mode == 'b':
            self.models = True
            bdNames = []
            smds = None
            smds = dat.bodies[0]["body"]
            self.valChk = ''

            self.scr_list = Listbox(frame, listvariable=bdNames, selectmode=SINGLE)
            self.scr_list.grid(column=1, row=1, sticky=(N, S, E, W), padx=40, pady=(40, 0), rowspan=5)
            
            count = -1
            for d in dat.bodies:
                count += 1
                self.scr_list.insert(count, d["name"])
            self.scr_list.select_set(0)
            self.valChk = self.dat.bodies[self.scr_list.curselection()[0]]["name"]

            self.smd_list = Listbox(frame, listvariable=smds)
            self.smd_list.grid(column=1, row=9, sticky=(N, S, E, W), ipadx=20, padx=20, pady=10, rowspan=5)

            if not smds is str:
                count = -1
                for s in smds:
                    count += 1
                    self.smd_list.insert(count, s)
            else:
                self.smd_list.insert(0, smd)
            
            select_scr = Button(frame, text="Select", command=self.select)
            select_scr.grid(column=1, row=69, sticky=(S))

            self.update()
        elif self.mode == 'd':
            self.valChk = ''
            self.animFolder = dat.animPath
            self.anims = os.listdir(self.animFolder)

            self.scr_list = Listbox(frame, selectmode=SINGLE)
            self.scr_list.grid(column=1, row=1, sticky=(N, S, E, W), padx=40, pady=(40, 10), rowspan=5)
            
            count = -1
            for s in self.anims:
                count += 1
                self.scr_list.insert(count, s)
            self.scr_list.select_set(0)
            self.valChk = self.anims[self.scr_list.curselection()[0]]

            select_scr = Button(btns, text="Select SMD", command=self.select)
            select_scr.grid(column=0, row=0, sticky=(S))

            select_batch = Button(btns, text="Select All", command=self.select_all)
            select_batch.grid(column=1, row=0, sticky=(S))

    def update(self):
        err = False
        try:
            sel = self.scr_list.curselection()[0]
        except:
            err = True
        if not err:
            self.smds = self.dat.bodies[sel]["body"]
            self.smd_list.delete(0, END)
            if not self.smds is str:
                count = -1
                for s in self.smds:
                    count += 1
                    self.smd_list.insert(count, s)
            else:
                self.smd_list.insert(0, smd)
        self.after(20, self.update)
    
    def select(self):
        if self.models:
            self.selectedSMD = self.smd_list.curselection()
        else:
            self.selectedSMD = self.scr_list.curselection()
        if not self.script:
            self.startTask()
        else:
            self.startScript()
        self.destroy()
    def select_all(self):
        if not self.script:
            self.startTask(True)
        else:
            self.startScript(True)
        self.destroy()
    
    def startTask(self, batch:bool=False, values=None):
        if self.mode == 'd':
            if not batch:
                loc = self.anims[self.selectedSMD[0]]
                loc = f'{self.animFolder}/{loc}'
            else:
                loc = f'{self.animFolder}/'
            base = ''
            new = ''
            parent = ''
            if values == None:
                base = self.values[0]
                new = self.values[1]
                parent = self.values[2]
            else:
                base = values[0]
                new = values[1]
                parent = values[2]
            # Checking if specified location is a folder or file, batch dupe is performed if a folder, otherwise a single dupe is performed
            if not batch:
                self.func.single_dupe(loc, base, new, parent)
            else:
                self.func.batch_dupe(loc, base, new, parent)
        elif self.mode == 'm':
            loc = self.smds[self.selectedSMD[0]]
            loc = f'{self.dat.qcLoc}/{loc}.smd'
            ref = ''
            torename = ''
            replace = ''
            if values == None:
                ref = self.values[0]
                torename = self.values[1]
                replace = self.values[2]
            else:
                ref = values[0]
                torename = values[1]
                replace = values[2]
            self.func.rename_part(loc, ref, torename, replace)
        elif self.mode == 'b':
            loc = self.smds[self.selectedSMD[0]]
            loc = f'{self.dat.qcLoc}/{loc}.smd'
            ref = ''
            if values == None:
                ref = self.values[0]
            else:
                ref = values[0]
            self.func.add_bmp(loc, ref)
    
    def startScript(self, batch:bool=False):
        values = []
        # If in duping mode
        if self.mode == 'd':
            for d in self.scrDat:
                if d == '-':
                    # self.dupe_scr(values[0], values[1], values[2])
                    self.startTask(batch, [values[0], values[1], values[2]])
                    values = []
                    continue
                else:
                    values.append(d)
        # If in pointer fix mode
        elif self.mode == 'm':
            for d in self.scrDat:
                if d == '-':
                    # self.matrename_scr(values[0], values[1], values[2])
                    self.startTask(values=[values[0], values[1], values[2]])
                    values = []
                    continue
                else:
                    values.append(d)
        # If in bitmap ext mode
        elif self.mode == 'b':
            for d in self.scrDat:
                if d == '-':
                    # self.bmp_scr(values[0])
                    self.startTask(values=[values[0]])
                    values = []
                    continue
                else:
                    values.append(d)