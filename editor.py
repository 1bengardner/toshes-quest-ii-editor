# Toshe Save File Editor

from Tkinter import *
import tkFileDialog
import pickle

def setChildren(children, enabled):
    for child in children:
        if child.winfo_class() in ("Frame", "LabelFrame"):
            setChildren(child.winfo_children(), enabled)
        else:
            child.config(state=(NORMAL if enabled else DISABLED))

class EditorText(Entry):
    def __init__(self, *args, **kwargs):
        onTextChanged = kwargs.pop('onTextChanged')
        Entry.__init__(self, *args, **kwargs)
        self.v = StringVar()
        self.v.trace("w", lambda *args: onTextChanged(self))
        self.config(textvariable=self.v)
        
    def replace(self, text):
        self.delete(0, END)
        self.insert(END, text)

class StatWindow:
    def __init__(self, master):
        statFrame = Frame(master, bg=COLOURS['DEFAULT_BG'])
        statFrame.grid()
        
        levelLabel = Label(statFrame, text="Level", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        levelLabel.grid(row=0, column=0)
        self.level = EditorText(statFrame, width=2, onTextChanged=self.onTextChanged)
        self.level.grid(row=0, column=1, sticky='E')
        
        strengthLabel = Label(statFrame, text="Strength", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        strengthLabel.grid(row=1, column=0)
        self.strength = EditorText(statFrame, width=3, onTextChanged=self.onTextChanged)
        self.strength.grid(row=1, column=1, sticky='E')
        
        dexterityLabel = Label(statFrame, text="Dexterity", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        dexterityLabel.grid(row=2, column=0)
        self.dexterity = EditorText(statFrame, width=3, onTextChanged=self.onTextChanged)
        self.dexterity.grid(row=2, column=1, sticky='E')
        
        wisdomLabel = Label(statFrame, text="Wisdom", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        wisdomLabel.grid(row=3, column=0)
        self.wisdom = EditorText(statFrame, width=3, onTextChanged=self.onTextChanged)
        self.wisdom.grid(row=3, column=1, sticky='E')
        
        eurosLabel = Label(statFrame, image=IMAGES['EURO'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        eurosLabel.grid(row=4, column=0)
        self.euros = EditorText(statFrame, width=6, onTextChanged=self.onTextChanged)
        self.euros.grid(row=4, column=1, sticky='E')
        
        self.save = Button(statFrame, text="Save", width=8, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
        self.save.grid(columnspan=2, pady=8)
        
        self.children = statFrame.winfo_children()
        setChildren(self.children, False)
        
    def updateWidgets(self, character):
        setChildren(self.children, True)
        self.level.replace(character.level)
        self.strength.replace(character.strength)
        self.dexterity.replace(character.dexterity)
        self.wisdom.replace(character.wisdom)
        self.euros.replace(character.euros)
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=RAISED, state=DISABLED)
        
    def onTextChanged(self, widget):
        widget.replace(widget.v.get()[0:widget['width']])
        self.save.config(text="Save stats", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)
            
    def saveData(self):
        def dumpStats(character):
            character.level = int(self.level.get())
            character.strength = int(self.strength.get())
            character.dexterity = int(self.dexterity.get())
            character.wisdom = int(self.wisdom.get())
            character.euros = int(self.euros.get())
            
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        dumpStats(character)
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
        print "Saved stats."
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)

class ItemWindow:
    def __init__(self, master):
        itemFrame = Frame(master, bg=COLOURS['DEFAULT_BG'])
        itemFrame.grid()
        
        buttonsFrame = Frame(itemFrame, bg=COLOURS['DEFAULT_BG'])
        buttonsFrame.grid()
        self.itemVar = IntVar()
        self.itemVar.set(-1)
        self.buttons = []
        for i in range(9):
            rb = Radiobutton(
                buttonsFrame,
                image=IMAGES['DEFAULT'],
                variable=self.itemVar,
                value=i,
                width=64,
                height=64,
                bg=COLOURS['BLACK'],
                indicatoron=0,
                bd=4,
                command=self.select
            )
            rb.grid(row=i//3, column=i%3)
            self.buttons.append(rb)
        
        self.save = Button(itemFrame, text="Save", width=8, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
        self.save.grid(pady=8)
        
        self.children = itemFrame.winfo_children()
        setChildren(self.children, False)
        
    def select(self):
        self.items[self.itemVar.get()]
        
    def updateWidgets(self, character):
        setChildren(self.children, True)
        self.items = character.items
        self.itemVar.set(-1)
        directories = {
            "Armour" : "armour",
            "Shield" : "shields",
            "Miscellaneous" : "miscellaneous",
            "Bow" : "weapons",
            "Sword" : "weapons",
            "Axe" : "weapons",
            "Club" : "weapons",
            "Spear" : "weapons",
            "Wand" : "weapons",
        }
        for i, item in enumerate(self.items):
            if item is None:
                self.buttons[i].config(image=IMAGES['DEFAULT'])
            else:
                if item.IMAGE_NAME not in IMAGES:
                    IMAGES[item.IMAGE_NAME] = PhotoImage(file="images\\"+directories[item.CATEGORY]+"\\"+item.IMAGE_NAME+".gif")
                self.buttons[i].config(image=IMAGES[item.IMAGE_NAME])
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=RAISED, state=DISABLED)
            
    def saveData(self):
        def dumpStats(character):
            #TODO
            pass
            
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        dumpStats(character)
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
        print "Saved items."
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)
        
class MainWindow:
    def __init__(self, master):
        xPaddingAmount = 4
        yPaddingAmount = 4
        self.createMenu(master)
        mainFrame = Frame(master, bg=COLOURS['DEFAULT_BG'], relief=SUNKEN, bd=4, padx=xPaddingAmount, pady=yPaddingAmount)
        mainFrame.grid()
        nameFrame = Frame(mainFrame, bg=COLOURS['DEFAULT_BG'])
        nameFrame.grid(columnspan=2, pady=yPaddingAmount)
        self.characterName = Label(nameFrame, text="Load a character. (Ctrl+O)", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        self.characterName.grid(row=0, column=0, ipadx=2)
        statFrame = LabelFrame(mainFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=xPaddingAmount, text="Stats")
        statFrame.grid(row=1, column=0, padx=xPaddingAmount, pady=yPaddingAmount)
        itemFrame = LabelFrame(mainFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=xPaddingAmount, text="Items")
        itemFrame.grid(row=1, column=1, padx=xPaddingAmount, pady=yPaddingAmount)
        self.stats = StatWindow(statFrame)
        self.items = ItemWindow(itemFrame)
        self.canSaveAll = False
       
    def createMenu(self, master):
        menubar = Menu(master)
        master.config(menu=menubar)
        
        self.fileMenu = Menu(menubar, tearoff=False)
        self.fileMenu.add_command(label="Open", command=self.load, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Save All", command=self.save, state=DISABLED, accelerator="Ctrl+S")
        master.bind("<Control-o>", lambda _: self.load())
        master.bind("<Control-s>", lambda _: self.save())
        self.fileMenu.insert_separator(2)
        self.fileMenu.add_command(label="Exit", command=master.destroy)
        
        menubar.add_cascade(label="File", menu=self.fileMenu)
        
    def load(self):
        path = tkFileDialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Toshe's Quest Files", "*.tq"), ("All Files", "*.*")))
        with open(path, "r") as gameFile:
            character = pickle.load(gameFile)
            self.characterName.config(relief=GROOVE, text=path.rsplit('/', 1)[-1])
            self.stats.path = path
            self.stats.updateWidgets(character)
            self.items.path = path
            self.items.updateWidgets(character)
            self.fileMenu.entryconfig(1, state=NORMAL)
            self.canSaveAll = True
            
    def save(self):
        if self.canSaveAll:
            self.stats.saveData()
            self.items.saveData()

def init():
    global IMAGES
    IMAGES = {
        "EURO" : PhotoImage(file="images\\icons\\euro.gif"),
        "DEFAULT" : PhotoImage(file="images\\other\\empty.gif"),
    }
    # itemImages = {
        # "weapondata" : "weapons",
        # "armourdata" : "armour",
        # "shielddata" : "shields",
        # "miscellaneousitemdata" : "miscellaneous",
    # }
    # for dataString, imageString in itemImages.items():
        # with open("data\\"+dataString+".txt", "r") as rFile:
            # rFile.readline()
            # for line in rFile:
                # name = line.strip().split("\t")[0]
                # IMAGES[name] = PhotoImage(file="images\\"+imageString+"\\"+name+".gif")
            
    global COLOURS
    COLOURS = {
        "DEFAULT_BG" : "#24828b",
        "DEFAULT_FG" : "#f4ead2",
        "BLACK" : "#000000",
    }

def start():
    root = Tk()
    
    init()
    
    root.iconbitmap("images\\icons\\tq.ico")
    root.title("File Editor")
    root.resizable(0, 0)

    window = MainWindow(root)

    root.update()
    root.mainloop()

start()
