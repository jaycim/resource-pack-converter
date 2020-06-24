import tkinter, json
import random

versions = json.load(open("versions.json"))

class Entry:
    def __init__(self, data):
        self.data = data

class VersionEntry(Entry):
    def __init__(self, identifier, date, format, name):
        self.data = {}
        self.data[identifier] = {}
        self.data[identifier]['date'] = date
        self.data[identifier]['format'] = format
        self.data[identifier]['name'] = name
    
    @classmethod
    def load(cls, json_obj):
        key = [*json_obj][0]
        return cls(key, json_obj[key]['date'], json_obj[key]['format'], json_obj[key]['name'])

class BlockEntry(Entry):
    def __init__(self, identifier, id, texture):
        self.data = {}

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Manager")
    
    def hello(self):
        print("hello")
    
    def get_selected(self):
        return

def main():
    global versions
    #print(json.dumps((VersionEntry("b1.1.1",1000000000,-1,"beta 1.1.1").data)))
    print(json.dumps(VersionEntry.load(json.loads('{"1.12.2":{"date":1010101010,"format":3,"name":"1.12.2"}}')).data))
    return
    root = tkinter.Tk()
    gui = SettingsWindow(root)
    root.mainloop()
    return
    

if __name__ == "__main__":
    main()