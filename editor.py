# Toshe Save File Editor

from Tkinter import *
import tkFileDialog
import pickle
import ttk
import tkFont
import tkMessageBox
from TUAShield import Shield
from TUAArmour import Armour
from TUAMiscellaneousItem import MiscellaneousItem
from TUAWeapon import Weapon

def setChildren(children, enabled):
    for child in children:
        if child.winfo_class() == "TSeparator":
            continue
        elif child.winfo_class() in ("Frame", "LabelFrame"):
            setChildren(child.winfo_children(), enabled)
        else:
            child.config(state=(NORMAL if enabled else DISABLED))

class EditorEntry(Entry):
    def __init__(self, *args, **kwargs):
        self.v = StringVar()
        if 'onTextChanged' in kwargs:
            onTextChanged = kwargs.pop('onTextChanged')
            self.v.trace("w", lambda *args: onTextChanged(self))
        if 'constraint' in kwargs:
            self.constraint = kwargs.pop('constraint')
        else:
            self.constraint = None
        Entry.__init__(self, *args, **kwargs)
        vcmd = (self.master.register(self.validate), '%P')
        self.config(textvariable=self.v, validatecommand=vcmd, validate='key')

    def replace(self, text):
        self.delete(0, END)
        self.insert(END, text)

    def validate(self, text):
        if self.constraint == "int":
            try:
                if text not in ("") and int(text) < 0:
                    return False
            except ValueError:
                return False
        elif self.constraint == "float":
            try:
                if text not in ("", ".") and float(text) < 0:
                    return False
            except ValueError:
                return False
        return len(text) <= self['width']

class EditorDropdown(OptionMenu):
    def __init__(self, *args, **kwargs):
        self.v = StringVar()
        if 'onSelectionChanged' in kwargs:
            onSelectionChanged = kwargs.pop('onSelectionChanged')
            self.v.trace("w", lambda *args: onSelectionChanged(self.v.get()))
        OptionMenu.__init__(self, args[0], self.v, *args[1:], **kwargs)

    def replace(self, selection):
        self.v.set(selection)

    def get(self):
        return self.v.get()

class EditorText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def replace(self, text):
        self.delete(0.0, END)
        self.insert(END, text)

class StatWindow:
    def __init__(self, master):
        statFrame = Frame(master, bg=COLOURS['DEFAULT_BG'])
        statFrame.grid()

        levelLabel = Label(statFrame, text="Level", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        levelLabel.grid(row=0, column=0)
        self.level = EditorEntry(statFrame, width=2, onTextChanged=self.onTextChanged, constraint="int")
        self.level.grid(row=0, column=1, sticky='E')

        strengthLabel = Label(statFrame, text="Strength", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        strengthLabel.grid(row=1, column=0)
        self.strength = EditorEntry(statFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.strength.grid(row=1, column=1, sticky='E')

        dexterityLabel = Label(statFrame, text="Dexterity", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        dexterityLabel.grid(row=2, column=0)
        self.dexterity = EditorEntry(statFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.dexterity.grid(row=2, column=1, sticky='E')

        wisdomLabel = Label(statFrame, text="Wisdom", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        wisdomLabel.grid(row=3, column=0)
        self.wisdom = EditorEntry(statFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.wisdom.grid(row=3, column=1, sticky='E')

        eurosLabel = Label(statFrame, image=IMAGES['EURO'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        eurosLabel.grid(row=4, column=0)
        self.euros = EditorEntry(statFrame, width=6, onTextChanged=self.onTextChanged, constraint="int")
        self.euros.grid(row=4, column=1, sticky='E')

        self.save = Button(statFrame, text="Save", width=10, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
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
        self.loadedImages = {}
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
                command=self.selectItem
            )
            rb.grid(row=i//3, column=i%3)
            self.buttons.append(rb)

        ttk.Separator(itemFrame, orient=VERTICAL).grid(row=0, column=1, padx=4, sticky='NS')

        infoFrame = Frame(itemFrame, bg=COLOURS['DEFAULT_BG'])
        infoFrame.grid(row=0, column=2, sticky='nsew')
        # Image
        self.imageName = None
        self.image = Button(
                infoFrame,
                image=IMAGES['DEFAULT'],
                width=64,
                height=64,
                bg=COLOURS['LINK'],
                bd=4,
                command=lambda: self.chooseImage(master, self.category.get())
        )
        self.image.grid(row=0, column=0, padx=(0, 4), pady=(0, 4), rowspan=3, sticky='NW')
        # Name
        self.name = EditorEntry(infoFrame, width=30, onTextChanged=self.onTextChanged)
        self.name.grid(row=0, column=1, sticky='W')
        # Category
        categories = [
            "Sword",
            "Club",
            "Axe",
            "Spear",
            "Bow",
            "Wand",
            "Shield",
            "Armour",
            "Miscellaneous",
        ]
        self.category = EditorDropdown(infoFrame, *categories, onSelectionChanged=self.onCategoryChanged)
        self.category.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.category['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.category['menu'].insert_separator(6)
        self.category.grid(row=1, column=1, sticky='W')
        # Price
        priceFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        priceFrame.grid(row=1, column=1, sticky='E')
        eurosLabel = Label(priceFrame, image=IMAGES['EURO'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        eurosLabel.pack(side=LEFT)
        self.price = EditorEntry(priceFrame, width=6, onTextChanged=self.onTextChanged, constraint="int")
        self.price.pack(side=LEFT)
        # Requirement
        requirementFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        requirementFrame.grid(row=2, column=1, pady=4, sticky='W')
        self.requirementFrame = requirementFrame
        self.requirementFrame.grid_remove()
        requirementLabel = Label(requirementFrame, text="Requires", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        requirementLabel.pack(side=LEFT)
        self.reqVal = EditorEntry(requirementFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.reqVal.pack(side=LEFT)
        stats = [
            "Strength",
            "Dexterity",
            "Wisdom",
        ]
        self.reqType = EditorDropdown(requirementFrame, *stats, command=self.onSelectionChanged)
        self.reqType.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.reqType['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.reqType.pack(side=LEFT)
        # Description
        descriptionFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        descriptionFrame.grid(row=3, column=0, columnspan=2)
        self.descriptionFrame = descriptionFrame
        self.descriptionFrame.grid_remove()
        descriptionLabel = Label(descriptionFrame, text="Description", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        descriptionLabel.pack(side=TOP)
        self.description = EditorText(descriptionFrame, font="TkDefaultFont", wrap=NONE, height=2, width=40)
        self.description.pack(side=BOTTOM)
        # Defence
        defenceFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        defenceFrame.grid(row=3, column=0, pady=4, sticky='W')
        self.defenceFrame = defenceFrame
        self.defenceFrame.grid_remove()
        defenceLabel = Label(defenceFrame, text="Defence", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        defenceLabel.pack(side=LEFT)
        self.defence = EditorEntry(defenceFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.defence.pack(side=LEFT)
        # Power
        powerFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        powerFrame.grid(row=3, column=0, pady=4, sticky='W')
        self.powerFrame = powerFrame
        self.powerFrame.grid_remove()
        powerLabel = Label(powerFrame, text="Power", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        powerLabel.pack(side=LEFT)
        self.power = EditorEntry(powerFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.power.pack(side=LEFT)
        # Block chance
        blockFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        blockFrame.grid(row=3, column=1, sticky='E')
        self.blockFrame = blockFrame
        self.blockFrame.grid_remove()
        blockLabel = Label(blockFrame, text="Block %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        blockLabel.pack(side=LEFT)
        self.block = EditorEntry(blockFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.block.pack(side=LEFT)
        # Crit chance
        critFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        critFrame.grid(row=3, column=1, sticky='E')
        self.critFrame = critFrame
        self.critFrame.grid_remove()
        critLabel = Label(critFrame, text="Crit %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        critLabel.pack(side=LEFT)
        self.crit = EditorEntry(critFrame, width=5, onTextChanged=self.onTextChanged, constraint="float")
        self.crit.pack(side=LEFT)
        # Reduction
        resFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        resFrame.grid(row=4, column=0, columnspan=2, sticky='W')
        self.resFrame = resFrame
        self.resFrame.grid_remove()
        resLabel = Label(resFrame, text="Resist %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        resLabel.pack(side=LEFT)
        self.resVal = EditorEntry(resFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.resVal.pack(side=LEFT)
        resists = [
            "Physical",
            "Earth",
            "Water",
            "Fire",
            "Elemental",
        ]
        self.resType = EditorDropdown(resFrame, *resists, command=self.onSelectionChanged)
        self.resType.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.resType['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.resType.pack(side=LEFT)
        # Imbuement
        elements = [
            "Physical",
            "Earth",
            "Water",
            "Fire",
        ]
        self.imbuement = EditorDropdown(infoFrame, *elements, command=self.onSelectionChanged)
        self.imbuement.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.imbuement['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.imbuement.grid(row=4, column=0, columnspan=2, sticky='W')
        self.imbuement.grid_remove()
        # Crit damage
        damageFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        damageFrame.grid(row=4, column=1, sticky='E')
        self.damageFrame = damageFrame
        self.damageFrame.grid_remove()
        damageLabel = Label(damageFrame, text="Crit Dmg %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        damageLabel.pack(side=LEFT)
        self.damage = EditorEntry(damageFrame, width=3, onTextChanged=self.onTextChanged, constraint="int")
        self.damage.pack(side=LEFT)

        self.save = Button(infoFrame, text="Save", width=10, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
        self.save.grid(row=5, columnspan=2, pady=8)

        self.children = itemFrame.winfo_children()
        setChildren(self.children, False)

    def selectItem(self):
        setChildren(self.children, True)
        selected = self.items[self.itemVar.get()]
        if selected == None:
            self.category.replace(self.category.get())
        else:
            self.name.replace(selected.NAME)
            self.category.replace(selected.CATEGORY)
            self.imageName = selected.IMAGE_NAME
            self.image.config(image=IMAGES[self.imageName])
            self.price.replace(selected.PRICE)

            if selected.CATEGORY == "Shield":
                self.reqVal.replace(selected.REQUIREMENT_VALUE)
                self.defence.replace(selected.DEFENCE)
                self.block.replace(selected.B_RATE)
                self.resVal.replace(selected.REDUCTION)
                self.resType.replace(selected.ELEMENT)

            elif selected.CATEGORY == "Armour":
                self.reqVal.replace(selected.REQUIREMENT_VALUE)
                self.defence.replace(selected.DEFENCE)
                self.resVal.replace(selected.REDUCTION)
                self.resType.replace(selected.ELEMENT)

            elif selected.CATEGORY == "Miscellaneous":
                self.description.replace(selected.INFORMATION.replace("*", "\n"))
                # No easy way to check for Text widget modifications
                self.save.config(text="Update", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)
                return

            else:
                self.reqType.replace(selected.REQUIREMENT_TYPE)
                self.reqVal.replace(selected.REQUIREMENT_VALUE)
                self.power.replace(selected.POWER)
                self.crit.replace(selected.C_RATE)
                self.imbuement.replace(selected.ELEMENT)
                self.damage.replace(selected.C_DAMAGE)

            self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)

    def selectImage(self):
        self.image.config(image=IMAGES[self.imageVar.get()])
        self.imageName = self.imageVar.get()
        self.top.destroy()

    def chooseImage(self, master, imageCategory):
        if imageCategory == "":
            errorTitle = "Graphic selection error"
            errorMessage = "Please choose an item type before selecting a graphic."
            tkMessageBox.showerror(title=errorTitle, message=errorMessage)
            return

        imageWindow = Toplevel(master, bg=COLOURS['BLACK'])
        imageWindow.grab_set()
        imageWindow.iconbitmap("images\\icons\\tq.ico")
        imageWindow.title(imageCategory+" Graphic Select")
        helpLabel = Label(imageWindow, text="Choose an item graphic from below.", bg=COLOURS['BLACK'], fg=COLOURS['DEFAULT_FG'])
        helpLabel.grid()
        self.top = imageWindow

        mainFrame = Frame(imageWindow, bg=COLOURS['BLACK'])
        mainFrame.grid()

        if imageCategory not in self.loadedImages:
            self.loadedImages[imageCategory] = set()
            if imageCategory == "Armour":
                dataString = "armourdata"
                imageString = "armour"
            elif imageCategory == "Shield":
                dataString = "shielddata"
                imageString = "shields"
            elif imageCategory == "Miscellaneous":
                dataString = "miscellaneousitemdata"
                imageString = "miscellaneous"
            else:
                dataString = "weapondata"
                imageString = "weapons"
            with open("data\\"+dataString+".txt", "r") as rFile:
                rFile.readline()
                for line in rFile:
                    name = line.strip().split("\t")[0]
                    if name not in IMAGES:
                        IMAGES[name] = PhotoImage(file="images\\"+imageString+"\\"+name+".gif")
                    self.loadedImages[imageCategory].add(name)

        countPerRow = 10
        i = 0
        self.imageVar = StringVar()
        for name in self.loadedImages[imageCategory]:
            rb = Radiobutton(
                mainFrame,
                image=IMAGES[name],
                variable=self.imageVar,
                value=name,
                width=64,
                height=64,
                bg=COLOURS['BLACK'],
                indicatoron=0,
                bd=4,
                command=self.selectImage
            )
            rb.grid(row=i//countPerRow, column=i%countPerRow)
            i += 1

    def updateWidgets(self, character):
        setChildren(self.children, False)
        setChildren(self.buttons, True)
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
        self.save.config(text="Select item", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=RAISED, state=DISABLED)

    def onTextChanged(self, widget):
        self.save.config(text="Save item", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)

    def onSelectionChanged(self, value):
        self.save.config(text="Save item", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)

    def onCategoryChanged(self, value):
        self.image.config(image=IMAGES['DEFAULT'])
        self.imageName = None
        if value == "Shield":
            self.requirementFrame.grid()
            self.reqType.replace("Strength")
            self.reqType.config(state=DISABLED)
            self.descriptionFrame.grid_remove()
            self.defenceFrame.grid()
            self.powerFrame.grid_remove()
            self.blockFrame.grid()
            self.critFrame.grid_remove()
            self.resFrame.grid()
            self.imbuement.grid_remove()
            self.damageFrame.grid_remove()

        elif value == "Armour":
            self.requirementFrame.grid()
            self.reqType.replace("Strength")
            self.reqType.config(state=DISABLED)
            self.descriptionFrame.grid_remove()
            self.defenceFrame.grid()
            self.powerFrame.grid_remove()
            self.blockFrame.grid_remove()
            self.critFrame.grid_remove()
            self.resFrame.grid()
            self.imbuement.grid_remove()
            self.damageFrame.grid_remove()

        elif value == "Miscellaneous":
            self.requirementFrame.grid_remove()
            self.descriptionFrame.grid()
            self.defenceFrame.grid_remove()
            self.powerFrame.grid_remove()
            self.blockFrame.grid_remove()
            self.critFrame.grid_remove()
            self.resFrame.grid_remove()
            self.imbuement.grid_remove()
            self.damageFrame.grid_remove()

        else:
            self.requirementFrame.grid()
            self.reqType.config(state=NORMAL)
            self.descriptionFrame.grid_remove()
            self.defenceFrame.grid_remove()
            self.powerFrame.grid()
            self.blockFrame.grid_remove()
            self.critFrame.grid()
            self.resFrame.grid_remove()
            self.imbuement.grid()
            self.damageFrame.grid()

        self.onSelectionChanged(value)

    def saveItem(self, index):
        def showError(customMessage=None):
            errorTitle = "Item error"
            errorMessage = "Please enter a value for all item stats." if not customMessage else customMessage
            tkMessageBox.showerror(title=errorTitle, message=errorMessage)

        category = self.category.get()
        if self.imageName is None:
            return showError("Please pick an item graphic.")
        elif "" in (category, self.price.get()):
            return showError()

        if category == "Shield":
            if "" in (self.reqVal.get(), self.defence.get(), self.block.get(), self.resType.get(), self.resVal.get()):
                return showError()
            self.items[index] = Shield(
                self.name.get(),
                int(self.price.get()),
                self.resType.get(),
                int(self.reqVal.get()),
                int(self.defence.get()),
                int(self.resVal.get()),
                int(self.block.get()),
            )
        elif category == "Armour":
            if "" in (self.reqVal.get(), self.defence.get(), self.resType.get(), self.resVal.get()):
                return showError()
            self.items[index] = Armour(
                self.name.get(),
                int(self.price.get()),
                self.resType.get(),
                int(self.reqVal.get()),
                int(self.defence.get()),
                int(self.resVal.get()),
            )
        elif category == "Miscellaneous":
            self.items[index] = MiscellaneousItem(
                self.name.get(),
                int(self.price.get()),
                self.description.get(1.0, END).strip().replace("\n", "*"),
            )
        else:
            if "" in (self.reqVal.get(), self.reqType.get(), self.power.get(), self.crit.get(), self.imbuement.get(), self.damage.get()):
                return showError()
            self.items[index] = Weapon(
                self.name.get(),
                int(self.price.get()),
                self.imbuement.get(),
                int(self.reqVal.get()),
                int(self.power.get()),
                self.reqType.get(),
                category,
                float(self.crit.get()),
                int(self.damage.get()),
            )
        self.items[index].IMAGE_NAME = self.imageName
        return "Success"

    def saveData(self):
        def dumpItems(character):
            character.items = self.items

        if self.itemVar.get() == -1 or not self.saveItem(self.itemVar.get()):
            return
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        dumpItems(character)
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
        print "Saved items."
        self.updateWidgets(character)
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)

class FlagsWindow:
    def __init__(self, master):
        self.exiting = False
        self.init = False
        self.master = master

    def show(self):
        self.window.deiconify()
        self.window.grab_set()

    def release(self):
        if self.exiting:
            self.exiting = False
            self.init = False
            self.window.destroy()
        else:
            self.window.grab_release()
            self.window.withdraw()

    def updateWidgets(self, character):
        if not self.init:
            flagsWindow = Toplevel(self.master, bg=COLOURS['DEFAULT_FG'], relief=SUNKEN, bd=4)
            flagsWindow.iconbitmap("images\\icons\\tq.ico")
            flagsWindow.title("Flag Viewer")
            flagsWindow.protocol('WM_DELETE_WINDOW', self.release)
            self.window = flagsWindow
            self.init = True
            self.release()

        rows = 25
        columns = 5
        self.pages = []
        self.pageView = 1
        master = Frame(self.window, bg=COLOURS['DEFAULT_FG'])
        master.grid(row=0, column=0)
        self.pages.append(master)
        count = 0
        for flag, val in character.flags.items():
            if val is True:
                f = Label(master, text=flag)
            elif flag != "Discovered Areas" and flag != "Config" and flag != "Marked Areas" and flag != "Kills" and flag != "Buyback Items":
                f = Label(master, text="{flag}: {value}".format(flag=flag, value=val))
                if len(f['text']) > 40:
                    f['text'] = f['text'][0:40] + "..."
            else:
                continue
            f.grid(row=count%rows, column=count//rows, sticky='W', padx=2)
            f.config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
            count += 1
            if count >= rows*columns:
                master = Frame(self.window, bg=COLOURS['DEFAULT_FG'])
                master.grid(row=0, column=0)
                master.grid_remove()
                self.pages.append(master)
                count = 0
        if len(self.pages) > 1:
            self.swapButton = Button(self.window, text="1/" + str(len(self.pages)), bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], command=self.swapPage)
            self.swapButton.grid()

    def swapPage(self):
        self.pages[self.pageView-1].grid_remove()
        self.pageView = self.pageView % len(self.pages) + 1
        self.pages[self.pageView-1].grid()
        self.swapButton.config(text=str(self.pageView) + "/" + str(len(self.pages)))

class MainWindow:
    def __init__(self, master):
        xPaddingAmount = 4
        yPaddingAmount = 4
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
        self.flags = FlagsWindow(master)
        self.createMenu(master)
        self.canSaveAll = False

        master.protocol('WM_DELETE_WINDOW', lambda: self.release(master))

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

        self.viewMenu = Menu(menubar, tearoff=False)
        self.viewMenu.add_command(label="Flags", command=self.flags.show, state=DISABLED)
        menubar.add_cascade(label="View", menu=self.viewMenu)

    def load(self):
        path = tkFileDialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Toshe's Quest Files", "*.tq"), ("All Files", "*.*")))
        with open(path, "r") as gameFile:
            character = pickle.load(gameFile)
            self.characterName.config(relief=GROOVE, text=path.rsplit('/', 1)[-1])
            self.stats.path = path
            self.stats.updateWidgets(character)
            self.items.path = path
            self.items.updateWidgets(character)
            if self.flags.init:
                self.flags.exiting = True
                self.flags.release()
            self.flags.path = path
            self.flags.updateWidgets(character)
            self.fileMenu.entryconfig(1, state=NORMAL)
            self.viewMenu.entryconfig(0, state=NORMAL)
            self.canSaveAll = True

    def save(self):
        if self.canSaveAll:
            self.stats.saveData()
            self.items.saveData()

    def release(self, master):
        self.flags.exiting = True
        self.flags.release()
        master.destroy()

def init():
    global IMAGES
    IMAGES = {
        "EURO" : PhotoImage(file="images\\icons\\euro.gif"),
        "DEFAULT" : PhotoImage(file="images\\other\\empty.gif"),
    }
    global COLOURS
    COLOURS = {
        "DEFAULT_BG" : "#24828b",
        "DEFAULT_FG" : "#f4ead2",
        "BLACK" : "#000000",
        "LINK" : "#0000ff",
    }

    tkFont.nametofont("TkDefaultFont").configure(size=10)
    tkFont.nametofont("TkTextFont").configure(size=10)

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
