# Toshe Save File Editor

from Tkinter import *
import tkFileDialog
import pickle


class Window:
    def __init__(self, master):
        mainFrame = Frame(master, bg=DEFAULT_BG, relief=SUNKEN, bd=4, padx=50)
        mainFrame.grid()
        self.createMenu(master)
        self.createWidgets(mainFrame)
       
    def createMenu(self, master):
        menubar = Menu(master)
        master.config(menu=menubar)
        
        self.fileMenu = Menu(menubar, tearoff=False)
        self.fileMenu.add_command(label="Load", command=self.load)
        self.fileMenu.add_command(label="Save", command=self.save, state=DISABLED)
        self.fileMenu.insert_separator(2)
        self.fileMenu.add_command(label="Exit", command=exit)
        
        menubar.add_cascade(label="File", menu=self.fileMenu)
        
    def createWidgets(self, master):
        nameFrame = Frame(master, bg=DEFAULT_BG)
        nameFrame.grid(pady=4)
        
        self.characterName = Label(nameFrame, text="Load a character.", bg=DEFAULT_BG, fg=DEFAULT_FG)
        self.characterName.grid(row=0, column=0, ipadx=2)
    

        statFrame = Frame(master, bg=DEFAULT_BG)
        statFrame.grid()
        
        levelLabel = Label(statFrame, text="Level", bg=DEFAULT_BG, fg=DEFAULT_FG)
        levelLabel.grid(row=0, column=0)
        self.level = Text(statFrame, height=1, width=2)
        self.level.grid(row=0, column=1, sticky='E')
        
        strengthLabel = Label(statFrame, text="Strength", bg=DEFAULT_BG, fg=DEFAULT_FG)
        strengthLabel.grid(row=1, column=0)
        self.strength = Text(statFrame, height=1, width=3)
        self.strength.grid(row=1, column=1, sticky='E')
        
        dexterityLabel = Label(statFrame, text="Dexterity", bg=DEFAULT_BG, fg=DEFAULT_FG)
        dexterityLabel.grid(row=2, column=0)
        self.dexterity = Text(statFrame, height=1, width=3)
        self.dexterity.grid(row=2, column=1, sticky='E')
        
        wisdomLabel = Label(statFrame, text="Wisdom", bg=DEFAULT_BG, fg=DEFAULT_FG)
        wisdomLabel.grid(row=3, column=0)
        self.wisdom = Text(statFrame, height=1, width=3)
        self.wisdom.grid(row=3, column=1, sticky='E')
        
        eurosLabel = Label(statFrame, image=IMAGES['EURO'], bg=DEFAULT_BG, fg=DEFAULT_FG)
        eurosLabel.grid(row=4, column=0)
        self.euros = Text(statFrame, height=1, width=6)
        self.euros.grid(row=4, column=1, sticky='E')
        
        self.save = Button(master, width=8, bg=DEFAULT_BG, fg=DEFAULT_FG, relief=FLAT, state=DISABLED, command=self.save)
        self.save.grid(pady=8)
        
    def updateWidgets(self, character):
        self.level.delete(0.0, END)
        self.level.insert(END, character.level)
        self.strength.delete(0.0, END)
        self.strength.insert(END, character.strength)
        self.dexterity.delete(0.0, END)
        self.dexterity.insert(END, character.dexterity)
        self.wisdom.delete(0.0, END)
        self.wisdom.insert(END, character.wisdom)
        self.euros.delete(0.0, END)
        self.euros.insert(END, character.euros)
        self.characterName.config(relief=GROOVE, text=self.path.rsplit('/', 1)[-1])
        self.save.config(text="Save", bg=DEFAULT_FG, fg=DEFAULT_BG, relief=RAISED, state=NORMAL)
        self.fileMenu.entryconfig(1, state=NORMAL)
        
    def load(self):
        self.path = tkFileDialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Toshe's Quest Files", "*.tq"), ("All Files", "*.*")))
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
            self.updateWidgets(character)
            
    def save(self):
        def dumpStats(character):
            character.level = int(self.level.get("1.0", END))
            character.strength = int(self.strength.get("1.0", END))
            character.dexterity = int(self.dexterity.get("1.0", END))
            character.wisdom = int(self.wisdom.get("1.0", END))
            character.euros = int(self.euros.get("1.0", END))
            
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        dumpStats(character)
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
            print "Saved."

def init():
    global IMAGES
    IMAGES = {
        "EURO" : PhotoImage(file="images\\icons\\euro.gif")
    }
    config()
        
def config():
    global DEFAULT_BG, DEFAULT_FG
    DEFAULT_BG = "#24828b"
    DEFAULT_FG = "#f4ead2"

def start():
    root = Tk()
    
    init()
    
    root.iconbitmap("images\\icons\\tq.ico")
    root.title("File Editor")
    root.resizable(0, 0)

    window = Window(root)

    root.update()
    root.mainloop()

start()
