# Toshe Save File Editor

from Tkinter import *
import tkFileDialog
import pickle
import ttk
import tkFont
from TUAShield import Shield
from TUAArmour import Armour
from TUAMiscellaneousItem import MiscellaneousItem
from TUAWeapon import Weapon
import converter

def setChildren(children, enabled):
    for child in children:
        if child.winfo_class() == "TSeparator":
            continue
        elif child.winfo_class() in ("Frame", "Labelframe"):
            setChildren(child.winfo_children(), enabled)
        else:
            child.config(state=(NORMAL if enabled else DISABLED))

def selectAll(event):
    if event.widget.winfo_class() == "Entry":
        event.widget.select_range(0, END)
    elif event.widget.winfo_class() == "Text":
        event.widget.tag_add(SEL, 0.0, END)

def findCharacterByName(data, name):
    for mercenary in [data] + (data.mercenaries if hasattr(data, "mercenaries") else []):
        if mercenary.NAME == name:
            return mercenary
    return None

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
        if self.constraint and ("int" in self.constraint or "float" in self.constraint):
            self.config(justify=RIGHT)

    def set(self, text):
        self.delete(0, END)
        self.insert(END, text)

    def validate(self, text):
        if not self.constraint:
            return True
        if "int" in self.constraint:
            try:
                if text not in ("") and int(text) < 0:
                    return False
            except ValueError:
                return False
        elif "float" in self.constraint:
            try:
                if text not in ("", ".") and float(text) < 0:
                    return False
            except ValueError:
                return False
        if "length" in self.constraint:
            return len(text) <= self['width']
        return True

class EditorDropdown(OptionMenu):
    def __init__(self, *args, **kwargs):
        self.v = StringVar()
        if 'onSelectionChanged' in kwargs:
            onSelectionChanged = kwargs.pop('onSelectionChanged')
            self.v.trace("w", lambda *args: onSelectionChanged(self.v.get()))
        OptionMenu.__init__(self, args[0], self.v, *args[1:], **kwargs)

    def set(self, selection):
        self.v.set(selection)

    def get(self):
        return self.v.get()

class EditorText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def set(self, text):
        self.delete(0.0, END)
        self.insert(END, text)

class StatWindow:
    def __init__(self, master):
        charFrame = Frame(master, bg=COLOURS['DEFAULT_BG'])
        charFrame.grid()
        collectiblesFrame = Frame(charFrame, bg=COLOURS['DEFAULT_BG'])
        collectiblesFrame.grid()
        self.statsFrame = LabelFrame(charFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], text="Stats")
        self.statsFrame.grid(pady=8)

        eurosLabel = Label(collectiblesFrame, image=IMAGES['EURO'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        eurosLabel.grid(row=0, column=0)
        self.euros = EditorEntry(collectiblesFrame, width=6, onTextChanged=self.onStatModified, constraint="length,int")
        self.euros.grid(row=0, column=1, sticky='E')

        potionLabel = Label(collectiblesFrame, image=IMAGES['POTION'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        potionLabel.grid(row=1, column=0)
        self.potions = EditorEntry(collectiblesFrame, width=3, onTextChanged=self.onStatModified, constraint="length,int")
        self.potions.grid(row=1, column=1, sticky='E')

        levelLabel = Label(self.statsFrame, text="Level", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        levelLabel.grid(row=0, column=0, padx=32)
        self.level = EditorEntry(self.statsFrame, width=2, onTextChanged=self.onStatModified, constraint="length,int")
        self.level.grid(row=0, column=1, sticky='E')

        strengthLabel = Label(self.statsFrame, text="Strength", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        strengthLabel.grid(row=1, column=0)
        self.strength = EditorEntry(self.statsFrame, width=3, onTextChanged=self.onStatModified, constraint="length,int")
        self.strength.grid(row=1, column=1, sticky='E')

        dexterityLabel = Label(self.statsFrame, text="Dexterity", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        dexterityLabel.grid(row=2, column=0)
        self.dexterity = EditorEntry(self.statsFrame, width=3, onTextChanged=self.onStatModified, constraint="length,int")
        self.dexterity.grid(row=2, column=1, sticky='E')

        wisdomLabel = Label(self.statsFrame, text="Wisdom", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        wisdomLabel.grid(row=3, column=0)
        self.wisdom = EditorEntry(self.statsFrame, width=3, onTextChanged=self.onStatModified, constraint="length,int")
        self.wisdom.grid(row=3, column=1, sticky='E')

        self.save = Button(charFrame, text="Save", width=10, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
        self.save.grid(columnspan=2)

        self.children = charFrame.winfo_children()
        setChildren(self.children, False)

    def updateWidgets(self, character):
        setChildren(self.children, True)
        self.name = character.NAME
        self.level.set(character.level)
        self.strength.set(character.strength)
        self.dexterity.set(character.dexterity)
        self.wisdom.set(character.wisdom)
        if character.NAME == self.name:
            self.euros['state'] = NORMAL
            self.euros.set(character.euros)
            self.potions['state'] = NORMAL
            self.potions.set(character.potions)
        else:
            self.euros.set("")
            self.euros['state'] = DISABLED
            self.potions.set("")
            self.potions['state'] = DISABLED
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=RAISED, state=DISABLED)

    def onStatModified(self, widget):
        self.save.config(text="Save", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)

    def saveData(self):
        def dumpStats(character):
            character.level = int(self.level.get())
            character.strength = int(self.strength.get())
            character.dexterity = int(self.dexterity.get())
            character.wisdom = int(self.wisdom.get())
            if character.NAME == self.name:
                character.euros = int(self.euros.get())
                character.potions = int(self.potions.get())

        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        dumpStats(findCharacterByName(character, self.name))
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
        infoFrame.grid(row=0, column=2, sticky='news')
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
        self.name = EditorEntry(infoFrame, width=30, onTextChanged=self.onItemModified)
        self.name.grid(row=0, column=1, sticky='W')
        # Category
        categories = [
            "Sword",
            "Bludgeon",
            "Axe",
            "Spear",
            "Bow",
            "Wand",
            "Gun",
            "Shield",
            "Armour",
            "Miscellaneous",
        ]
        self.category = EditorDropdown(infoFrame, *categories, onSelectionChanged=self.onCategoryChanged)
        self.category.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.category['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.category['menu'].insert_separator(categories.index("Shield"))
        self.category.grid(row=1, column=1, sticky='W')
        # Price
        priceFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        priceFrame.grid(row=1, column=1, sticky='E')
        eurosLabel = Label(priceFrame, image=IMAGES['EURO'], bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        eurosLabel.pack(side=LEFT)
        self.price = EditorEntry(priceFrame, width=6, onTextChanged=self.onItemModified, constraint="length,int")
        self.price.pack(side=LEFT)
        # Requirement
        requirementFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        requirementFrame.grid(row=2, column=1, pady=4, sticky='W')
        self.requirementFrame = requirementFrame
        self.requirementFrame.grid_remove()
        requirementLabel = Label(requirementFrame, text="Requires", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        requirementLabel.pack(side=LEFT)
        self.reqVal = EditorEntry(requirementFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.reqVal.pack(side=LEFT)
        stats = [
            "Strength",
            "Dexterity",
            "Wisdom",
        ]
        self.reqType = EditorDropdown(requirementFrame, *stats, command=self.onItemModified)
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
        self.defence = EditorEntry(defenceFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.defence.pack(side=LEFT)
        # Power
        powerFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        powerFrame.grid(row=3, column=0, pady=4, sticky='W')
        self.powerFrame = powerFrame
        self.powerFrame.grid_remove()
        powerLabel = Label(powerFrame, text="Power", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        powerLabel.pack(side=LEFT)
        self.power = EditorEntry(powerFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.power.pack(side=LEFT)
        # Block chance
        blockFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        blockFrame.grid(row=3, column=1, sticky='E')
        self.blockFrame = blockFrame
        self.blockFrame.grid_remove()
        blockLabel = Label(blockFrame, text="Block %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        blockLabel.pack(side=LEFT)
        self.block = EditorEntry(blockFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.block.pack(side=LEFT)
        # Crit chance
        critFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        critFrame.grid(row=3, column=1, sticky='E')
        self.critFrame = critFrame
        self.critFrame.grid_remove()
        critLabel = Label(critFrame, text="Crit %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        critLabel.pack(side=LEFT)
        self.crit = EditorEntry(critFrame, width=5, onTextChanged=self.onItemModified, constraint="length,float")
        self.crit.pack(side=LEFT)
        # Reduction
        resFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        resFrame.grid(row=4, column=0, columnspan=2, sticky='W')
        self.resFrame = resFrame
        self.resFrame.grid_remove()
        resLabel = Label(resFrame, text="Resist %", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        resLabel.pack(side=LEFT)
        self.resVal = EditorEntry(resFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.resVal.pack(side=LEFT)
        resists = [
            "Physical",
            "Earth",
            "Water",
            "Fire",
            "Elemental",
        ]
        self.resType = EditorDropdown(resFrame, *resists, command=self.onItemModified)
        self.resType.config(bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], activebackground=COLOURS['DEFAULT_FG'], activeforeground=COLOURS['DEFAULT_BG'])
        self.resType['menu'].config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        self.resType.pack(side=LEFT)
        # Imbuement
        elements = [
            "Physical",
            "Earth",
            "Water",
            "Fire",
            "Frostfire",
            "Lightning",
        ]
        self.imbuement = EditorDropdown(infoFrame, *elements, command=self.onItemModified)
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
        self.damage = EditorEntry(damageFrame, width=3, onTextChanged=self.onItemModified, constraint="length,int")
        self.damage.pack(side=LEFT)

        interactionFrame = Frame(infoFrame, bg=COLOURS['DEFAULT_BG'])
        interactionFrame.grid(row=5, columnspan=2, pady=(12, 0))
        self.save = Button(interactionFrame, text="Save", width=10, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=FLAT, command=self.saveData)
        self.save.grid(row=0, column=1, padx=8)
        self.erase = Button(interactionFrame, text="Delete", width=10, bg=COLOURS['DEFAULT_BG'], relief=FLAT, command=self.eraseItem)
        self.erase.grid(row=0, column=2)
        errorFrame = Frame(interactionFrame, bg=COLOURS['DEFAULT_BG'])
        errorFrame.grid(row=0, column=0)
        self.error = Label(errorFrame, bg=COLOURS['ERROR_BG'], fg=COLOURS['ERROR_FG'], width=18, height=3, relief=RIDGE, wraplength=100, font=("TkDefaultFont", 8))
        self.error.grid(row=0, column=0)
        self.error.grid_remove()
        errorFrame.config(width=self.error.winfo_reqwidth(), height=self.error.winfo_reqheight())

        self.children = itemFrame.winfo_children()
        setChildren(self.children, False)

    def selectItem(self):
        setChildren(self.children, True)
        selected = self.items[self.itemVar.get()]
        if selected == None:
            self.category.set(self.category.get())
            self.erase.config(state=DISABLED, bg=COLOURS['DEFAULT_BG'])
        else:
            self.name.set(selected.NAME)
            self.category.set(selected.CATEGORY)
            self.imageName = selected.IMAGE_NAME
            self.image.config(image=IMAGES[self.imageName])
            self.price.set(selected.PRICE)

            if selected.CATEGORY == "Shield":
                self.reqVal.set(selected.REQUIREMENT_VALUE)
                self.defence.set(selected.DEFENCE)
                self.block.set(selected.B_RATE)
                self.resVal.set(selected.REDUCTION)
                self.resType.set(selected.ELEMENT)

            elif selected.CATEGORY == "Armour":
                self.reqVal.set(selected.REQUIREMENT_VALUE)
                self.defence.set(selected.DEFENCE)
                self.resVal.set(selected.REDUCTION)
                self.resType.set(selected.ELEMENT)

            elif selected.CATEGORY == "Miscellaneous":
                self.description.set(selected.INFORMATION.replace("*", "\n"))
                # No easy way to check for Text widget modifications
                self.save.config(text="Update", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)
                self.erase.config(bg=COLOURS['DEFAULT_FG'])
                return

            else:
                self.reqType.set(selected.REQUIREMENT_TYPE)
                self.reqVal.set(selected.REQUIREMENT_VALUE)
                self.power.set(selected.POWER)
                self.crit.set(selected.C_RATE)
                self.imbuement.set(selected.ELEMENT)
                self.damage.set(selected.C_DAMAGE)

            self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)
            self.erase.config(bg=COLOURS['DEFAULT_FG'])

    def selectImage(self):
        self.image.config(image=IMAGES[self.imageVar.get()])
        self.imageName = self.imageVar.get()
        self.onItemModified(self.image);
        self.top.destroy()

    def chooseImage(self, master, imageCategory):
        if imageCategory == "":
            errorTitle = "Graphic selection error"
            errorMessage = "Please choose an item type before selecting a graphic."
            self.showError(errorMessage, errorTitle)
            return

        imageWindow = Toplevel(master, bg=COLOURS['BLACK'])
        imageWindow.grab_set()
        imageWindow.focus()
        imageWindow.bind("<Control-w>", lambda _: imageWindow.destroy())
        imageWindow.bind("<Escape>", lambda _: imageWindow.destroy())
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

    def getItems(self, character):
        self.items = character.items

    def updateWidgets(self, character):
        self.error.grid_remove()
        setChildren(self.children, False)
        setChildren(self.buttons, True)
        self.getItems(character)
        self.itemVar.set(-1)
        directories = {
            "Armour" : "armour",
            "Shield" : "shields",
            "Miscellaneous" : "miscellaneous",
            "Bow" : "weapons",
            "Sword" : "weapons",
            "Axe" : "weapons",
            "Bludgeon" : "weapons",
            "Spear" : "weapons",
            "Wand" : "weapons",
            "Gun" : "weapons",
        }
        for i, item in enumerate(self.items):
            if i >= len(self.buttons):
                break
            elif item is None:
                self.buttons[i].config(image=IMAGES['DEFAULT'])
            else:
                if item.IMAGE_NAME not in IMAGES:
                    IMAGES[item.IMAGE_NAME] = PhotoImage(file="images\\"+directories[item.CATEGORY]+"\\"+item.IMAGE_NAME+".gif")
                self.buttons[i].config(image=IMAGES[item.IMAGE_NAME])
        self.save.config(text="Save", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], relief=RAISED, state=DISABLED)
        self.erase.config(fg=COLOURS['ERROR_BG'], bg=COLOURS['DEFAULT_BG'], relief=RAISED, state=DISABLED)

    def onItemModified(self, widget):
        self.save.config(text="Save", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=NORMAL)
        self.error.grid_remove()

    def onCategoryChanged(self, value):
        self.image.config(image=IMAGES['DEFAULT'])
        self.imageName = None
        if value == "Shield":
            self.requirementFrame.grid()
            self.reqType.set("Strength")
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
            self.reqType.set("Strength")
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

        self.onItemModified(self.category)

    def eraseItem(self):
        self.items[self.itemVar.get()] = None
        self.buttons[self.itemVar.get()].config(image=IMAGES['DEFAULT'])
        self.selectItem()
        self.saveData(True)

    def saveItem(self, index):
        def showError(customMessage=None):
            if not self.image.winfo_viewable():
                return
            errorTitle = "Item error"
            errorMessage = "Please enter a value for all item stats." if not customMessage else customMessage
            self.showError(errorMessage, errorTitle)

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
        self.buttons[index].config(image=IMAGES[self.imageName])
        self.erase.config(state=NORMAL, bg=COLOURS['DEFAULT_FG'])
        return "Success"

    def dumpItems(self, character):
        character.items = self.items

    def saveData(self, deleting=False):
        if not deleting and (self.itemVar.get() == -1 or not self.saveItem(self.itemVar.get())):
            return
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        self.dumpItems(character)
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
        print "Saved items."
        if deleting:
            return
        if self.items[self.itemVar.get()].CATEGORY == "Miscellaneous":
            self.save.config(text="Update")
        else:
            self.save.config(text="Saved", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], state=DISABLED)

    def showError(self, message, title=None):
        self.error.config(text=message)
        self.error.grid()
        self.error.config(bg=COLOURS['ERROR_FG'])
        self.error.after(75, lambda: self.error.config(bg=COLOURS['ERROR_BG']))

class VendorWindow(ItemWindow):
    def __init__(self, *args, **kwargs):
        ItemWindow.__init__(self, *args, **kwargs)

    def dumpItems(self, character):
        if 'Buyback Items' in character.flags:
            character.flags['Buyback Items'] = self.items

    def getItems(self, character):
        if 'Buyback Items' in character.flags:
            self.items = character.flags['Buyback Items']
        else:
            self.items = [None, None, None, None, None, None, None, None, None]

class EditWindow(object):
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

    def terminate(self):
        if self.init:
            self.exiting = True
            self.release()

    def updateWidgets(self, character):
        if not self.init:
            self.initWindow(queryChangedCallback)

        self.rows = 15
        self.columns = 4
        self.pageFrame.grid_remove()
        for page in self.pages:
            page.destroy()
        self.pages = []
        self.pageView = 1
        master = self.createPanel()
        self.pages.append(master)
        self.count = 0
        self.var = StringVar()
        self.radiobuttons = {}
        self.initRadioButtons(master)
        
    def initWindow(self, character):
        mainWindow = Toplevel(self.master, bg=COLOURS['DEFAULT_FG'], relief=SUNKEN, bd=4)
        self.window = mainWindow
        self.release()
        mainWindow.bind('<Control-Key-a>', selectAll)
        mainWindow.bind("<Control-s>", lambda _: self.save.invoke())
        mainWindow.bind("<Control-w>", lambda _: self.release())
        mainWindow.bind("<Escape>", lambda _: self.release())
        mainWindow.iconbitmap("images\\icons\\tq.ico")
        mainWindow.protocol('WM_DELETE_WINDOW', self.release)
        mainWindow.title("Edit Window")
        self.mainFrame = Frame(mainWindow, bg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        self.mainFrame.grid()
        queryFrame = Frame(self.mainFrame, bg=COLOURS['DEFAULT_FG'], relief=RIDGE, bd=2)
        queryFrame.grid(row=0, column=0, sticky='E')
        queryLabel = Label(queryFrame, text="Search: ", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        queryLabel.pack(side=LEFT)
        def onQueryChanged(widget):
            self.updateWidgets(character)
        self.queryEntry = EditorEntry(queryFrame, onTextChanged=onQueryChanged)
        self.queryEntry.pack(side=LEFT)
        saveFrame = Frame(self.mainFrame, bg=COLOURS['DEFAULT_FG'])
        saveFrame.grid(row=2, column=0, sticky='SE')
        self.unsaved = Label(saveFrame, text="You have unsaved changes.", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        self.unsaved.grid(row=0, column=0, padx=8)
        self.unsaved.grid_remove()
        self.save = Button(saveFrame, text="Saved", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=DISABLED, command=self.saveData)
        self.save.grid(row=0, column=1)
        self.flagsFrame = self.mainFrame
        self.pages = []
        self.pageFrame = Frame(self.flagsFrame, bg=COLOURS['DEFAULT_FG'])
        self.pageFrame.grid(row=2, column=0, sticky='S')
        prevButton = Button(self.pageFrame, text="<<", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], command=self.prevPage)
        prevButton.pack(side=LEFT)
        self.pageCount = Label(self.pageFrame, text="1/2", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        self.pageCount.pack(side=LEFT)
        nextButton = Button(self.pageFrame, text=">>", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], command=self.nextPage)
        nextButton.pack(side=LEFT)
        self.init = True

    def saveData(self):
        if not self.init or self.save['state'] == DISABLED:
            return
        with open(self.path, "r") as gameFile:
            character = pickle.load(gameFile)
        character.flags = self.flags
        with open(self.path, "w") as gameFile:
            pickle.dump(character, gameFile)
        self.save.config(text="Saved", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'], state=DISABLED)
        self.unsaved.grid_remove()
        print "Saved flags."
        
    def initRadioButtons(self, panel):
        raise NotImplementedError()

    def createPanel(self):
        master = Frame(self.flagsFrame, bg=COLOURS['DEFAULT_FG'], width=900, height=450, pady=8)
        master.grid(row=1, column=0)
        master.grid_propagate(False)
        return master
        
    def createGenericRadiobutton(self, master, txt, var, val, cmd):
        rb = Radiobutton(
            master,
            text=txt,
            variable=var,
            value=val,
            indicatoron=0,
            command=cmd
        )
        rb.config(bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
        rb.grid(row=self.count%self.rows, column=self.count//self.rows, sticky='W', padx=PADDING['DEFAULT'])
        self.radiobuttons[val] = rb
        self.count += 1
        if self.count >= self.rows*self.columns:
            master = self.createPanel()
            master.grid_remove()
            self.pages.append(master)
            self.count = 0
            if len(self.pages) == 2:
                self.pageFrame.grid()
            self.pageCount.config(text=str(self.pageView) + "/" + str(len(self.pages)))
        return rb, master

    def nextPage(self):
        self.swapPage(1)

    def prevPage(self):
        self.swapPage(-1)

    def swapPage(self, inc):
        self.pages[self.pageView-1].grid_remove()
        self.pageView = (self.pageView-1 + inc) % len(self.pages) + 1
        self.pages[self.pageView-1].grid()
        self.pageCount.config(text=str(self.pageView) + "/" + str(len(self.pages)))

class FlagsWindow(EditWindow):
    def updateWidgets(self, character):
        self.flags = character.flags
        if not self.init:
            super(FlagsWindow, self).initWindow(character)
            self.initWindow()
        super(FlagsWindow, self).updateWidgets(character)
            
    def initWindow(self):
        entryFrame = Frame(self.mainFrame, bg=COLOURS['DEFAULT_FG'], relief=RIDGE, bd=2)
        entryFrame.grid(row=0, column=0, sticky='W')
        flagLabel = Label(entryFrame, text="New flag: ", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        flagLabel.pack(side=LEFT)
        self.flagEntry = Entry(entryFrame)
        self.flagEntry.pack(side=LEFT)
        addButton = Button(entryFrame, text="Add", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], command=self.addFlag)
        addButton.pack(side=LEFT)
        self.flagEntry.bind("<Return>", lambda _: addButton.invoke())
        helpLabel = Label(self.mainFrame, text="Click on a flag to delete it.", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        helpLabel.grid(row=0, column=0)
        self.window.title("Flags")

    def initRadioButtons(self, panel):
        for flag, val in self.flags.items():
            if val is True and self.queryEntry.get().lower() in flag.lower():
                panel = self.createRadiobutton(panel, flag, self.var, self.deleteFlag)

    def createRadiobutton(self, master, flag, var, cmd):
        rb, master = self.createGenericRadiobutton(
            master,
            flag + " x",
            var,
            flag,
            cmd)
        rb.config(activebackground=COLOURS['ERROR_BG'])
        return master

    def deleteFlag(self):
        del self.flags[self.var.get()]
        self.radiobuttons[self.var.get()].destroy()
        self.save.config(text="Save Changes", bg=COLOURS['DEFAULT_BG'], fg="green", relief=RAISED, state=NORMAL)
        self.unsaved.grid()

    def addFlag(self):
        if self.flagEntry.get() != "" and self.flagEntry.get() not in self.flags:
            self.queryEntry.set("")
            self.createRadiobutton(self.pages[-1], self.flagEntry.get(), self.var, self.deleteFlag)
            self.flags[self.flagEntry.get()] = True
            self.save.config(text="Save Changes", bg=COLOURS['DEFAULT_BG'], fg="green", relief=RAISED, state=NORMAL)
            self.unsaved.grid()

class KillsWindow(EditWindow):
    def __init__(self, master):
        super(KillsWindow, self).__init__(master)
        self.killsKey = "Kills"

    def updateWidgets(self, character):
        self.flags = character.flags
        if not self.init:
            super(KillsWindow, self).initWindow(character)
            self.initWindow()
        super(KillsWindow, self).updateWidgets(character)
        
    def initWindow(self):
        entryFrame = Frame(self.mainFrame, bg=COLOURS['DEFAULT_FG'], relief=RIDGE, bd=2)
        entryFrame.grid(row=0, column=0, sticky='W')
        enemyLabel = Label(entryFrame, text="New enemy: ", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        enemyLabel.pack(side=LEFT)
        self.enemyEntry = Entry(entryFrame)
        self.enemyEntry.pack(side=LEFT)
        addButton = Button(entryFrame, text="Add", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], command=self.addEnemy)
        addButton.pack(side=LEFT)
        self.enemyEntry.bind("<Return>", lambda _: addButton.invoke())
        helpLabel = Label(self.mainFrame, text="Click on a name to reset your kills for that enemy.", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        helpLabel.grid(row=0, column=0)
        self.window.title("Kill Counts")

    def initRadioButtons(self, panel):
        for enemy, killCount in self.flags[self.killsKey].items():
            if self.queryEntry.get().lower() in enemy.lower():
                rb, panel = self.createGenericRadiobutton(panel, "%s: %s" % (enemy, killCount), self.var, enemy, self.deleteEnemy)
                rb.config(activebackground=COLOURS['ERROR_BG'])

    def addEnemy(self):
        if self.enemyEntry.get() != "" and self.enemyEntry.get() not in self.flags[self.killsKey]:
            self.queryEntry.set("")
            self.createGenericRadiobutton(self.pages[-1], "%s: %s" % (self.enemyEntry.get(), 1), self.var, self.enemyEntry.get(), self.deleteEnemy)
            self.flags[self.killsKey][self.enemyEntry.get()] = 1
            self.save.config(text="Save Changes", bg=COLOURS['DEFAULT_BG'], fg="green", relief=RAISED, state=NORMAL)
            self.unsaved.grid()

    def deleteEnemy(self):
        del self.flags[self.killsKey][self.var.get()]
        self.radiobuttons[self.var.get()].destroy()
        self.save.config(text="Save Changes", bg=COLOURS['DEFAULT_BG'], fg="green", relief=RAISED, state=NORMAL)
        self.unsaved.grid()

class MapWindow(EditWindow):
    def __init__(self, master):
        super(MapWindow, self).__init__(master)
        self.mapKey = "Discovered Areas"

    def updateWidgets(self, character):
        self.flags = character.flags
        if not self.init:
            super(MapWindow, self).initWindow(character)
            self.initWindow()
        super(MapWindow, self).updateWidgets(character)
        
    def initWindow(self):
        helpLabel = Label(self.mainFrame, text="Click on a location to clear it from your map.", bg=COLOURS['DEFAULT_FG'], fg=COLOURS['BLACK'])
        helpLabel.grid(row=0, column=0)
        self.window.title("Mapped Locations")

    def initRadioButtons(self, panel):
        for area in self.flags[self.mapKey]:
            if self.queryEntry.get().lower() in area.lower():
                rb, panel = self.createGenericRadiobutton(panel, "%s x" % area, self.var, area, self.deleteArea)
                rb.config(activebackground=COLOURS['ERROR_BG'])

    def deleteArea(self):
        del self.flags[self.mapKey][self.var.get()]
        self.radiobuttons[self.var.get()].destroy()
        self.save.config(text="Save Changes", bg=COLOURS['DEFAULT_BG'], fg="green", relief=RAISED, state=NORMAL)
        self.unsaved.grid()

class MainWindow:
    def swapInventories(self, revert=False):
        swapTextB = "<< Your Items"
        if self.vendorItemSwap['text'] == self.swapTextA and not revert:
            self.vendorItemSwap['text'] = swapTextB
            self.itemFrame.grid_remove()
            self.vendorFrame.grid()
        else:
            self.vendorItemSwap['text'] = self.swapTextA
            self.itemFrame.grid()
            self.vendorFrame.grid_remove()

    def __init__(self, master):
        master.bind('<Control-Key-a>', selectAll)
        mainFrame = Frame(master, bg=COLOURS['DEFAULT_BG'], relief=SUNKEN, bd=4, padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        mainFrame.grid()
        nameFrame = Frame(mainFrame, bg=COLOURS['DEFAULT_BG'], pady=PADDING['DEFAULT'])
        nameFrame.grid(columnspan=2)
        self.characterName = Label(nameFrame, text="Load a character. (Ctrl+O)", bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
        self.characterName.grid(row=0, column=0, ipadx=2)
        portraitFrame = Frame(mainFrame, bg=COLOURS['DEFAULT_BG'])
        portraitFrame.grid(row=0, column=0, padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        self.charVar = StringVar()
        self.portraits = {}
        for i, character in enumerate(["Toshe", "Qendresa", "Barrie"]):
            rb = Radiobutton(
                portraitFrame,
                image=IMAGES[character.upper()],
                variable=self.charVar,
                value=character,
                width=42,
                height=64,
                bg=COLOURS['DEFAULT_BG'],
                selectcolor=COLOURS['DEFAULT_FG'],
                indicatoron=0,
                bd=4,
                command=self.switchCharacter,
                state=DISABLED
            )
            rb.grid(row=0, column=i)
            self.portraits[character] = rb
        statFrame = Frame(mainFrame, bg=COLOURS['DEFAULT_BG'])
        statFrame.grid(row=1, column=0)
        self.itemFrame = LabelFrame(mainFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], text="Items")
        self.itemFrame.grid(row=1, column=1, padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        self.vendorFrame = LabelFrame(mainFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], padx=PADDING['DEFAULT'], text="Merchant Items")
        self.vendorFrame.grid(row=1, column=1, padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        self.vendorFrame.grid_remove()
        self.swapTextA = "Hidden Passage Vendor >>"
        self.vendorItemSwap = Button(mainFrame, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'], text=self.swapTextA, command=self.swapInventories, state=DISABLED)
        self.vendorItemSwap.grid(row=0, column=1, sticky='E', padx=PADDING['DEFAULT'], pady=PADDING['DEFAULT'])
        self.stats = StatWindow(statFrame)
        self.items = ItemWindow(self.itemFrame)
        self.vendorItems = VendorWindow(self.vendorFrame)
        self.flags = FlagsWindow(master)
        self.kills = KillsWindow(master)
        self.map = MapWindow(master)
        self.createMenu(master)
        self.editWindows = [self.flags, self.kills, self.map]

        master.protocol('WM_DELETE_WINDOW', lambda: self.release(master))

    def switchCharacter(self):
        with open(self.stats.path, "r") as gameFile:
            character = pickle.load(gameFile)
        self.stats.updateWidgets(findCharacterByName(character, self.charVar.get()))
        self.stats.statsFrame.config(text="{name}'s Stats".format(name=self.charVar.get()))

    def createMenu(self, master):
        menubar = Menu(master)
        master.config(menu=menubar)

        self.fileMenu = Menu(menubar, tearoff=False)
        self.fileMenu.add_command(label="Open...", command=self.openLoadDialog, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Save All", command=self.save, state=DISABLED, accelerator="Ctrl+S")
        master.bind("<Control-o>", lambda _: self.openLoadDialog())
        master.bind("<Control-s>", lambda _: self.save())
        master.bind("<Control-w>", lambda _: master.destroy())
        self.fileMenu.insert_separator(2)
        self.fileMenu.add_command(label="Exit", command=master.destroy, accelerator="Ctrl+W")
        menubar.add_cascade(label="File", menu=self.fileMenu)

        self.viewMenu = Menu(menubar, tearoff=False)
        self.viewMenu.add_command(label="Flags", command=self.flags.show, state=DISABLED)
        self.viewMenu.add_command(label="Kills", command=self.kills.show, state=DISABLED)
        self.viewMenu.add_command(label="Map", command=self.map.show, state=DISABLED)
        menubar.add_cascade(label="Edit", menu=self.viewMenu)

    def openLoadDialog(self):
        path = tkFileDialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Toshe's Quest Files", "*.tq"), ("All Files", "*.*")))
        if path:
            self.load(path)

    def load(self, path):
        with open(path, "r") as gameFile:
            character = pickle.load(gameFile)
        try:
            self.characterName.config(relief=GROOVE, text=path.rsplit('/', 1)[-1], font=("TkDefaultFont", 16))
            unlockedPortraits = ["Toshe"]
            self.portraits["Toshe"]['value'] = character.NAME
            if hasattr(character, "mercenaries"):
                unlockedPortraits += [mercenary.NAME for mercenary in character.mercenaries]
            for portrait in self.portraits:
                self.portraits[portrait].config(state=(NORMAL if portrait in unlockedPortraits else DISABLED))
            self.charVar.set(character.NAME)
            self.stats.path = path
            self.stats.updateWidgets(character)
            self.switchCharacter()
            self.items.path = path
            self.items.updateWidgets(character)
            self.vendorItems.path = path
            self.vendorItems.updateWidgets(character)
            if 'Buyback Items' in character.flags:
                self.vendorItemSwap.config(state=NORMAL, bg=COLOURS['DEFAULT_FG'], fg=COLOURS['DEFAULT_BG'])
            else:
                self.vendorItemSwap.config(state=DISABLED, bg=COLOURS['DEFAULT_BG'], fg=COLOURS['DEFAULT_FG'])
                self.swapInventories(True)
            for editWindow in self.editWindows:
                editWindow.terminate()
                editWindow.path = path
                editWindow.updateWidgets(character)
        except:
            print "Unable to read file. Attempting version upgrade to 2.0...",
            with open(path, "r") as gameFile:
                success = converter.update(gameFile, path) is True
                if success:
                    print "Done!"
                else:
                    print "Unable to upgrade."
            if success:
                self.load(path)
        self.fileMenu.entryconfig(1, state=NORMAL)
        for i in range(len(self.editWindows)):
            self.viewMenu.entryconfig(i, state=NORMAL)

    def save(self):
        self.stats.save.invoke()
        for editWindow in self.editWindows:
            if editWindow.init:
                editWindow.save.invoke()
        self.items.save.invoke()
        self.vendorItems.save.invoke()

    def release(self, master):
        for editWindow in self.editWindows:
            editWindow.terminate()
        master.destroy()

def init():
    global IMAGES
    IMAGES = {
        "EURO" : PhotoImage(file="images\\icons\\euro.gif"),
        "POTION" : PhotoImage(file="images\\icons\\potion.gif"),
        "DEFAULT" : PhotoImage(file="images\\other\\empty.gif"),
        "TOSHE" : PhotoImage(file="images\\other\\toshe.gif").zoom(3).subsample(4),
        "QENDRESA" : PhotoImage(file="images\\areas\\pec\\11.gif").subsample(3),
        "BARRIE" : PhotoImage(file="images\\areas\\pristina\\26.gif"),
    }
    global COLOURS
    COLOURS = {
        "DEFAULT_BG" : "#24828b",
        "DEFAULT_FG" : "#f4ead2",
        "BLACK" : "#000000",
        "LINK" : "blue",
        "ERROR_BG" : "red",
        "ERROR_FG" : "white",
    }
    global PADDING
    PADDING = {
        "DEFAULT" : 4,
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
