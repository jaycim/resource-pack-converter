"""json_editor.py: aims to provide a tkinter based graphical json editor"""

__author__   = "Nicholas Cline"
__license__  = "GNU GPL v3.0"

import os, json, tkinter
from tkinter import filedialog,messagebox

versions = json.load(open("versions.json"))
root = None

fgcolour="#dcdcdc"
bgcolour="#232323"
bgaccent="#121212"
#todo: colour config

def updatecolours(widget):
    _list = [widget]
    for w in _list:
        if w.winfo_children():
            _list.extend(w.winfo_children())
        if isinstance(w,tkinter.Menu):
            w.configure(bg=bgaccent)
        elif isinstance(w,tkinter.Entry):
            w.configure(bg=bgaccent,highlightcolor=fgcolour,highlightbackground=bgcolour,borderwidth=0)
        else:
            w.configure(bg=bgcolour)
        try:
            w.configure(fg=fgcolour)
        except (tkinter.TclError):
            continue
    
def setcolourscheme(self, fgc, bgc, bga):
    global fgcolour, bgcolour, bgaccent
    fgcolour = fgc
    bgcolour = bgc
    bgaccent = bga

class JsonElement:
    def __init__(self,master):
        self.master = master
        self.value = None
        self.type = None
    
    def __str__(self):
        _v = self.value
        if (type(_v) is str):
            return "\"{}\"".format(_v)
        if (_v is None):
            return "null"
        if (_v is True):
            return "true"
        if (_v is False):
            return "false"
        return str(_v)

class JsonArray(JsonElement):
    def __init__(self,master):
        self.master = master
        self.children = []
    
    def __str__(self):
        _clist = []
        for item in self.children:
            _clist.append(str(item["element"]))
        return "["+','.join(_clist)+"]"
    
    def addchildren(self,child):
        children.append({"element":child})

class JsonObject(JsonArray):
    def __init__(self,master):
        self.master = master
        self.children = []
    
    def __str__(self):
        _clist = []
        for item in self.children:
            _clist.append("\"{}\":{}".format(item["key"],str(item["element"])))
        return "{"+','.join(_clist)+"}"
    
    def addchildren(self,child,key=None):
        children.append({"key":key,"element":child})

class JsonRoot(JsonObject):
    def __init__(self,master):
        self.master = master
        self.children = []

class aJSONArray:
    def __init__(self, master, children=[]):
        self.children = children
        self.widget = tkinter.Frame(master=master)
        self.widget.columnconfigure(0, weight=1)
    
    def __str__(self):
        _clist = []
        for item in self.children:
            _clist.append(str(item["child"]))
        return "{"+','.join(_clist)+"}"
    
    def validate(self):
        return True
        
    def addchild(self, childtype):
        _frame = tkinter.Frame(master=self.widget)
        if (childtype == "text"):
            c = None
            _child = tkinter.Entry(master=_frame,width=20)
        if (childtype == "number"):
            c = None
            _child = tkinter.Entry(master=_frame,width=10)
        if (childtype == "boolean"):
            c = None
            _child = tkinter.Entry(master=_frame,width=5)
        if (childtype == "null"):
            c = None
            _child = tkinter.Entry(master=_frame,width=1,diabled=True)
        if (childtype == "object"):
            c = aJSONObject(self.widget)
            _child = c.widget
        if (childtype == "array"):
            c = aJSONArray(self.widget)
            _child = c.widget
        _child.pack(side="left")
        self.children.append({"child":c,"childframe":_frame})
        _frame.pack(fill="x")

class aJSONObject:
    def __init__(self, master, children=[]):
        self.children = children
        self.widget = tkinter.Frame(master=master)
    
    def __str__(self):
        _clist = []
        for item in self.children:
            _clist.append("\"{}\":{}".format(item["key"],str(item["child"])))
        return "{"+','.join(_clist)+"}"
    
    def validate(self):
        return True
        
    def addchild(self, childtype, key=None):
        _row,_col = 0,0
        for c in self.children:
            c["comma"].configure(text=",")
        _frame = tkinter.Frame(master=self.widget)
        _key = tkinter.Entry(master=_frame,width=20,text=key)
        #_key.pack(side="left")
        _key.grid(row=_row,column=_col,sticky="nw");_col+=1
        _colon = tkinter.Label(master=_frame,text=":")
        #_colon.pack(side="left")
        _colon.grid(row=_row,column=_col,sticky="nw");_col+=1
        if (childtype == "text"):
            c = None
            _child = tkinter.Entry(master=_frame,width=20)
        if (childtype == "number"):
            c = None
            _child = tkinter.Entry(master=_frame,width=10)
        if (childtype == "boolean"):
            c = None
            _child = tkinter.Entry(master=_frame,width=5)
        if (childtype == "null"):
            c = None
            _child = tkinter.Entry(master=_frame,width=1,diabled=True)
        if (childtype == "object"):
            _open = tkinter.Label(master=_frame,text="{")
            _open.grid(row=_row,column=_col,sticky="nw");_row+=1;_col=0
            c = aJSONObject(_frame)
            _child = c.widget
            _close = tkinter.Label(master=_frame,text="}")
            _close.grid(row=_row+1,column=_col)
        if (childtype == "array"):
            _open = tkinter.Label(master=_frame,text="[")
            _open.grid(row=_row,column=_col,sticky="nw");_row+=1;_col=0
            c = aJSONArray(_frame)
            _child = c.widget
            _close = tkinter.Label(master=_frame,text="]")
            _close.grid(row=_row+1,column=_col)
        _child.grid(row=_row,column=_col,sticky="nw");_col+=1
        _comma = tkinter.Label(master=_frame,text="")
        #_comma.pack(side="left")
        _comma.grid(row=_row,column=_col,sticky="nw")
        self.children.append({"key":key,"child":c,"childframe":_frame,"comma":_comma})
        _frame.pack(fill="x")

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Manager")
        self.master.bind('<Control-n>',self.newfile)
        self.master.bind('<Control-o>',self.openfile)
        self.master.bind('<Control-s>',self.savefile)
        self.master.bind('<Control-Shift-s>',self.savefileas)
        self.master.bind('<Control-w>',self.closefile)
        self.master.bind('<Control-q>',self.exitwindow)

        self.menubar = tkinter.Menu(master=self.master, borderwidth=0)
        self.master.config(menu=self.menubar)

        self.filemenu = tkinter.Menu(self.menubar, borderwidth=0)
        self.filemenu.add_command(label="New", command=self.newfile, accelerator="Ctrl+N")
        self.filemenu.add_command(label="Open", command=self.openfile, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save", command=self.savefile, accelerator="Ctrl+S")
        self.filemenu.add_command(label="Save As...", command=self.savefileas, accelerator="Ctrl+Shift+S")
        self.filemenu.add_command(label="Close", command=self.closefile, accelerator="Ctrl+W")
        self.filemenu.add_command(label="Exit", command=self.exitwindow, accelerator="Ctrl+Q")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.mainframe = tkinter.Frame(master=self.master, borderwidth=0)
        self.mainframe.grid(sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.bracesframe = tkinter.Frame(master=self.mainframe, borderwidth=0)
        self.contentframe = tkinter.Frame(master=self.mainframe, borderwidth=0)
        self.bracesframe.grid(row=0, column=0, sticky="nsew")
        self.contentframe.grid(row=0, column=1, sticky="nsew")
        self.contentframe.rowconfigure(0, weight=1)
        self.contentframe.columnconfigure(0, weight=1)

        self.openbrace = tkinter.Label(master=self.bracesframe,text="{")
        self.openbrace.pack()
        self.closebrace = tkinter.Label(master=self.bracesframe,text="}")
        self.closebrace.pack(side="bottom")

        self.mainframe.rowconfigure(0,weight=1)
        self.mainframe.columnconfigure(0,weight=0)
        self.mainframe.columnconfigure(1,weight=100)

        self.unsavedchanges = True
        self.jsonFile = None
        self.parentobject = aJSONObject(master=self.contentframe)
        self.parentobject.widget.grid(sticky="nsew")
        self.parentobject.addchild("text")
        self.parentobject.addchild("object")
        self.parentobject.children[1]["child"].addchild("text")

        updatecolours(self.master)
    
    def confirmdataloss(self):
        return messagebox.askokcancel("Question","Doing this could cause you to lose unsaved data.\nAre you sure?")

    def blank(self):
        if (self.unsavedchanges and not self.confirmdataloss()):
            return False
        return True
    
    def newfile(self,event=None):
        if not self.blank():
            return
        self.jsonFile = None
        return
    
    def openfile(self,event=None):
        if not self.blank():
            return
        self.jsonFile = filedialog.askopenfilename(initialdir=os.getcwd(),title="Open file...",filetypes = (("JSON files","*.json"),("all files","*")))
        return

    def savefile(self,event=None):
        return
    
    def savefileas(self,event=None):
        self.jsonFile = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save file as...",filetypes=(("JSON files","*.json"),("all files","*")))
        self.savefile()
        return
    
    def closefile(self,event=None):
        if not self.blank():
            return
        self.jsonFile = None
        return
    
    def exitwindow(self,event=None):
        if not self.blank():
            return
        self.master.destroy()

def main():
    global versions, root
    root = tkinter.Tk()
    root.option_add('*tearOff', False)
    root.geometry("{}x{}".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    gui = SettingsWindow(root)
    root.mainloop()
    return
    

if __name__ == "__main__":
    main()