from json import load, dump

class Branch:
    def __init__(self, db, name:str, key:str, branches:dict={}) -> None:
        self.name = name
        self.key = key
        self.db = db
        self.branches = branches
        self.debug=False
    def get(self):
        return self.db.get()[self.key]
    def set(self, d):
        self.db.update({self.key:d})
    def update(self, d):
        _d = self.get()
        _d.update(d)
        self.set(_d)
    def get_by_key(self, key:str):
        d = self.get()
        if key in d:
            try:
                return d[key]
            except KeyError:
                return None
                
    def add_branch(self, name:str, key:str=None, init_val=None):
        if isinstance(self.get(), dict):
            key = name if key == None else key
            self.branches[name] = Branch(self, name, key)
            if key not in self.get():
                self.update({key:init_val})
            return self.branches[name]
        elif self.debug:
            print(f"Add branch FAIL - super branch ({self.name}) was not type dict")

class JsonHandler:
    def __init__(self, filename:str, branches={}) -> None:
        self.filename = filename
        self.branches = branches
        self.debug = False
    
    def setIfEmpty(self, d):
        with open(self.filename, "r") as f:
            if f.read().strip() == "":
                self.set(d)

    def get(self):
        with open(self.filename, "r") as f:
            if self.debug:
                d = load(f)
                print(f"{self.filename} data load : {d}")
                return d
            return load(f)
    def set(self, d):
        with open(self.filename, "w") as f:
            if self.debug:
                print(f"{self.filename} data dump: {d}")
            dump(d, f)
    def update(self, d:dict):
        _data = self.get()
        _data.update(d)
        self.set(_data)
    def get_by_key(self, key):
        d = self.get()
        if key in d:
            return d["key"]
    def add_branch(self, name:str, key:str=None, init_val=None) -> Branch:
        key = name if key==None else key
        self.branches[name] = Branch(self, name, key)
        if key not in self.get():
            self.update({key:init_val})
        if self.debug: print(f"Added branch {name} | key={key} | filename={self.filename}")
        return self.branches[name]
    
    def reset(self):
        self.set({})
        

class MemoryDB(JsonHandler):
    def __init__(self, init_d={}, branches={}) -> None:
        self.d = init_d 
        self.branches = branches
        self.debug = False
    def get(self): return self.d
    def set(self, d): self.d=d
    def add_branch(self, name:str, key:str=None, init_val=None) -> Branch:
        key = name if key==None else key
        self.branches[name] = Branch(self, name, key)
        if key not in self.get():
            self.update({key:init_val})
        if self.debug: print(f"Added branch {name} | key={key} |")
        return self.branches[name]


