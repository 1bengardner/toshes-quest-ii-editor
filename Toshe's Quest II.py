#Toshe's Underwater Adventures 1.1

"""
File: Toshe's Quest II.py
Author: Ben Gardner
Created: December 25, 2012
Revised: February 13, 2018
"""

 
from Tkinter import *
import tkFont
import tkMessageBox
from TUAMain import Main
from TUADialog import OpenFileDialog


class Window:
    """Contains the game window."""

    def __init__(self, master):
        gameFrame = Frame(master, bg=DEFAULT_BG, relief=SUNKEN, bd=4)
        gameFrame.grid()

        gameFrame.bind_all('m', self.clickMapButton)
        gameFrame.bind_all('M', self.clickMapButton)
        
        self.levelUpFrame = Frame(master, bg=LEVEL_UP_BG, relief=RIDGE, bd=10)
        self.levelUpFrame.grid(row=0)
        self.levelUpFrame.grid_remove()

        self.mercenaryUpFrame = Frame(master, bg=MERCENARY_UP_BG,
                                      relief=RIDGE, bd=10)
        self.mercenaryUpFrame.grid(row=0)
        self.mercenaryUpFrame.grid_remove()
        
        self.lootFrame = Frame(master, bg=LOOT_BG, relief=RIDGE, bd=10)
        self.lootFrame.grid(row=0)
        self.lootFrame.grid_remove()
        
        levelUpLabel = Label(self.levelUpFrame, text="LEVEL UP!", font=font5,
                             bg=LEVEL_UP_BG, fg=LEVEL_UP_FG)
        levelUpLabel.grid()
        levelUpLabel.bind("<Button-1>", self.removeLevelUpFrame)
        
        self.mercenaryUpLabel = Label(self.mercenaryUpFrame,
                                 text="MERC. UP!",
                                 font=font7,
                                 bg=MERCENARY_UP_BG, fg=MERCENARY_UP_FG)
        self.mercenaryUpLabel.grid()
        self.mercenaryUpLabel.bind("<Button-1>", self.removeMercenaryUpFrame)
        
        lootLabel = Label(self.lootFrame, text="LOOT!", font=font5,
                          bg=LOOT_BG, fg=LOOT_FG)
        lootLabel.grid()
        lootLabel.bind("<Button-1>", self.removeLootFrame)
        
        self.makeChildren(gameFrame)
        
        gameFrame.bind_all('<Control-m>',
                           self.topFrame.topRightFrame.clickMarkMapButton)
        gameFrame.bind_all('<Control-M>',
                           self.topFrame.topRightFrame.clickMarkMapButton)

    def makeChildren(self, master):
        self.topFrame = TopFrame(master)
        self.bottomFrame = BottomFrame(master)

    def removeLevelUpFrame(self, event=None):
        self.levelUpFrame.grid_remove()

    def gridMercenaryUpFrame(self, name):
        self.mercenaryUpLabel.config(text="%s UP!" % name.upper())
        self.mercenaryUpFrame.grid()

    def removeMercenaryUpFrame(self, event=None):
        self.mercenaryUpFrame.grid_remove()

    def removeLootFrame(self, event=None):
        self.lootFrame.grid_remove()

    def clickMapButton(self, event=None):
        if main.character is not None:
            main.printMap()


class TopFrame:
    """Contains the upper portion of the game window."""

    def __init__(self, master):
        frameA = Frame(master, bg=DEFAULT_BG)
        frameA.grid()
        self.makeChildren(frameA)

    def makeChildren(self, master):        
        self.topLeftFrame = TopLeftFrame(master)
        self.topCenterFrame = TopCenterFrame(master)
        self.topRightFrame = TopRightFrame(master)
    

class BottomFrame:
    """Contains the lower portion of the game window."""

    def __init__(self, master):
        frameB = Frame(master, bg=DEFAULT_BG)
        frameB.grid()
        self.makeChildren(frameB)

    def makeChildren(self, master):
        self.bottomLeftFrame = BottomLeftFrame(master)
        self.bottomRightFrame = BottomRightFrame(master)


class TopLeftFrame:
    """Contains frames for vital stats and inventory.

    Only one is displayed at a time.
    """

    def __init__(self, master):
        frameC = Frame(master, width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                       bg=DEFAULT_BG)
        frameC.grid()
        frameC.grid_propagate(0)
        self.makeFrameElements(frameC)

    def makeFrameElements(self, master):
        """Creates labelframes for vital stats and inventory.

        Vital stats displays: character name, level, XP, HP, EP
        Inventory displays: items, item stats for selected item, equip button
        """
        self.vitalStats = LabelFrame(master, text="Vital Stats", font=font3,
                                     width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                                     bg=DEFAULT_BG)
        self.vitalStats.grid()
        self.vitalStats.grid_propagate(0)
    
        self.levelLabel = Label(self.vitalStats, text="1", font=font2,
                                width=2, bg=DEFAULT_BG, relief=RIDGE)
        self.levelLabel.grid(column=1, padx=10, pady=10, sticky=E)
        self.nameLabel = Label(self.vitalStats, text="Toshe", font=italicFont4,
                               fg=BLACK, bg=DEFAULT_BG)
        self.nameLabel.grid(row=0, column=0, columnspan=2)
        self.xpBarLabel = Label(self.vitalStats, image=xpBars[6], bg=WHITE,
                                relief=SUNKEN, bd=1, compound=CENTER,
                                font=font8, fg=BLACK)
        self.xpBarLabel.grid(row=1, columnspan=2)
        self.tosheLabel = Label(self.vitalStats, image=tosheImage, bg=LIGHTCYAN,
                                relief=RIDGE, bd=4)
        self.tosheLabel.grid(columnspan=2, pady=20)
        self.hpBarLabel = Label(self.vitalStats, image=hpBars[4], bg=DEFAULT_BG,
                                relief=SUNKEN, bd=1)
        self.hpBarLabel.grid(row=4, columnspan=2)
        self.hpWord = Label(self.vitalStats, text="HP",
                            bg=DEFAULT_BG, font=font1, bd=0)
        self.hpWord.grid(row=3, column=0, sticky=W)
        self.hpLabel = Label(self.vitalStats, text="100/100",
                                  bg=DEFAULT_BG, font=font1, bd=0)
        self.hpLabel.grid(row=3, column=1, sticky=E)
        self.epBarLabel = Label(self.vitalStats, image=epBars[2], bg=DEFAULT_BG,
                                relief=SUNKEN, bd=1)
        self.epBarLabel.grid(row=5, columnspan=2)
        self.epWord = Label(self.vitalStats, text="EP",
                            bg=DEFAULT_BG, font=font1, bd=0)
        self.epWord.grid(row=6, column=0, sticky=W)
        self.epLabel = Label(self.vitalStats, text="100/100",
                                  bg=DEFAULT_BG, font=font1, bd=0)
        self.epLabel.grid(row=6, column=1, sticky=E)


        self.inventory = LabelFrame(master, text="Inventory", font=font3,
                                    width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                                    bg=DEFAULT_BG)
        self.inventory.grid(row=0)
        self.inventory.grid_propagate(0)

        # Inventory checkbutton variable
        self.v1 = IntVar()
        self.itemButtons = makeItemButtons(self.inventory, self.v1, 0)
        self.itemNameLabel = Label(self.inventory, text="Name", font=font2,
                                   bg=DEFAULT_BG)
        self.itemNameLabel.grid(columnspan=3, sticky=W)
        self.itemCategoryLabel = Label(self.inventory, text="Category",
                                       font=font2, bg=DEFAULT_BG)
        self.itemCategoryLabel.grid(columnspan=3, sticky=W)
        self.itemValueLabel = Label(self.inventory, text="X Euros", font=font1,
                                    bg=DEFAULT_BG)
        self.itemValueLabel.grid(columnspan=3, sticky=W)
        self.itemRequirementLabel = Label(self.inventory, text="Requires X Y",
                                          font=font1, bg=DEFAULT_BG)
        self.itemRequirementLabel.grid(columnspan=3, sticky=W)
        self.itemQualityLabel = Label(self.inventory,
                                      text="X Power/X Defence", font=font1,
                                      bg=DEFAULT_BG)
        self.itemQualityLabel.grid(columnspan=3, sticky=W)
        self.itemCBRateLabel = Label(self.inventory, text=
                                     "X% Critical Chance/X% Block Chance",
                                     font=font1, bg=DEFAULT_BG)
        # CB represents critical/block
        self.itemCBRateLabel.grid(columnspan=3, sticky=W)
        self.itemElementLabel = Label(self.inventory,
                                      text=
                                      "Imbued with X/Reduces X Damage by Y%",
                                      font=font1, bg=DEFAULT_BG)
        self.itemElementLabel.grid(columnspan=3, sticky=W)
        self.equipButton = Button(self.inventory, text="Equip", font=font2,
                                  fg=BUTTON_FG, bg=BUTTON_BG,
                                  command=self.clickEquipButton)
        self.equipButton.grid(columnspan=3, sticky=E+W)
        self.sellButton = Button(self.inventory, text="Sell", font=font2,
                                 fg=BUTTON_FG, bg=BUTTON_BG,
                                 command=self.clickSellButton)
        self.sellButton.grid(row=10, columnspan=3, sticky=E+W)
        self.sellButton.grid_remove()
        self.dropButton = Button(self.inventory, text="Drop", font=font2,
                                 fg=BUTTON_FG, bg=BUTTON_BG,
                                 command=self.clickDropButton)
        self.dropButton.grid(row=10, columnspan=3, sticky=E+W)
        self.dropButton.grid_remove()

    def clickEquipButton(self):
        main.character.equip(self.v1.get())
        window.topFrame.topRightFrame.updateOtherStats()
        self.equipButton['state'] = DISABLED
        self.updateInventory()
        if main.view == "battle":
            interfaceActions = main.equipItem()
            window.bottomFrame.bottomRightFrame.clickBackButton()
            updateInterface(interfaceActions)
        
    def clickSellButton(self):
        main.sell(self.v1.get())
        self.sellButton['state'] = DISABLED
        self.updateInventory()
        window.topFrame.topRightFrame.buyButton['state'] = DISABLED
        window.topFrame.topRightFrame.updateStore()

    def clickDropButton(self):
        if self.v1.get() in main.character.equippedItemIndices.values():
            main.character.equip(self.v1.get())
        main.character.removeItem(self.v1.get())
        main.character.addItem(main.tempItem)
        window.bottomFrame.bottomRightFrame.clickCancelDropButton()

    def updateVitalStats(self):
        """Change the current level, xp, hp and ep of the character shown in the
        Vital Stats frame to correspond to the character's actual values of
        these stats.
        """
        c = main.character
        
        self.levelLabel['text'] = c.level
        if c.xp > c.xpTnl:
            self.xpBarLabel['image'] = xpBars[-1]
        else:
            self.xpBarLabel['image'] = xpBars[int(float(c.xp) / c.xpTnl *
                                                  (NUMBER_OF_BARS - 1))]
        self.xpBarLabel['text'] = "%d/%d" % (c.xp, c.xpTnl)
        if c.hp <= 0:
            self.hpBarLabel['image'] = hpBars[0]
        elif float(c.hp) < float(c.maxHp) / NUMBER_OF_BARS:
            self.hpBarLabel['image'] = hpBars[1]
        else:
            self.hpBarLabel['image'] = hpBars[int(float(c.hp) / c.maxHp *
                                                  (NUMBER_OF_BARS - 1))]
        self.hpBarLabel['text'] = "%d/%d" % (c.hp, c.maxHp)
        self.hpLabel['text'] = "%d/%d" % (c.hp, c.maxHp)
        if c.ep <= 0:
            self.epBarLabel['image'] = epBars[0]
        elif float(c.ep) < float(c.maxEp) / NUMBER_OF_BARS:
            self.epBarLabel['image'] = epBars[1]
        else:
            self.epBarLabel['image'] = epBars[int(float(c.ep) / c.maxEp *
                                                  (NUMBER_OF_BARS - 1))]
        self.epBarLabel['text'] = "%d/%d" % (c.ep, c.maxEp)
        self.epLabel['text'] = "%d/%d" % (c.ep, c.maxEp)

    def updateInventory(self):
        """Show the current images for the character's inventory in the
        Inventory frame.
        """
        clearItemStats(self, store=False)
        self.v1.set(-1)
        for i in range(0, 3):
            for j in range(0, 3):
                if not main.character.items[i*3+j]:
                    self.itemButtons[i*3+j].config(image=noItemImage,
                                                   state=DISABLED,
                                                   bg=BLACK)
                elif i*3+j in main.character.equippedItemIndices.values():
                    try:
                        itemImage = itemImages[
                            main.character.items[i*3+j].IMAGE_NAME]
                    except KeyError as e:
                        print "Missing image: %s" % e
                        itemImage = defaultImage
                    self.itemButtons[i*3+j].config(image=itemImage,
                                                   state=NORMAL,
                                                   bg=LIGHTCYAN)
                elif i*3+j not in main.character.equippedItemIndices.values():
                    try:
                        itemImage = itemImages[
                            main.character.items[i*3+j].IMAGE_NAME]
                    except KeyError as e:
                        print "Missing image: %s" % e
                        itemImage = defaultImage
                    self.itemButtons[i*3+j].config(image=itemImage,
                                                   state=NORMAL,
                                                   bg=BLACK)
        self.equipButton['text'] = "Equip"

        
class TopCenterFrame:
    """Displays title and area image."""

    def __init__(self, master):
        frameD = Frame(master, width=348, height=FRAME_C_HEIGHT, bg=DEFAULT_BG)
        frameD.grid(row=0, column=1)
        frameD.grid_columnconfigure(0, weight=1)
        frameD.grid_rowconfigure(1, weight=1)
        frameD.grid_propagate(0)
        self.makeFrameElements(frameD)

    def makeFrameElements(self, master):
        self.titleLabel = Label(master, text="\nToshe's Quest II", font=font6,
                                bg=DEFAULT_BG, bd=0)
        self.titleLabel.grid()
        self.areaButton = Button(master, image=welcomeImage, bg=DEFAULT_BG,
                                 relief=RAISED, bd=6, command=self.openFile)
        self.areaButton.grid()

    def changeTitle(self, newTitle):
        self.titleLabel['text'] = newTitle

    def openFile(self):
        d = OpenFileDialog(root, "Start Game")
        try:
            self.loadFile(d.entryValue)
        except IOError:
            self.createFile(d.entryValue)
##        except TypeError as error:
##            window.bottomFrame.bottomLeftFrame.insertOutput(
##                "There was an error loading the file (TypeError: "+str(error)+").")
##        except EOFError as error:
##            window.bottomFrame.bottomLeftFrame.insertOutput(
##                "There was an error loading the file (EOFError: "+str(error)+").")
##        except KeyError as error:
##            window.bottomFrame.bottomLeftFrame.insertOutput(
##                "There was an error loading the file (KeyError: "+str(error)+").")
##        except AttributeError:
##            window.bottomFrame.bottomLeftFrame.insertOutput(
##                "C'mon, I won't bite.")

    def saveFile(self):
        if tkMessageBox.askokcancel("Save Game", "Do you want to save?",
                                    parent=root):
            main.saveGame()

    def loadFile(self, name=None):
        window.bottomFrame.bottomLeftFrame.clearOutputBox
        if not name:
            window.bottomFrame.bottomRightFrame.okButton['command'] = \
                window.bottomFrame.bottomRightFrame.clickOkButton
            window.bottomFrame.bottomRightFrame.bindChoices()
            name = main.fileName
        main.loadGame(name)
        interfaceActions = main.getInterfaceActions(justFought=True)
        updateInterface(interfaceActions)
        window.bottomFrame.bottomRightFrame.centerButton['state'] = NORMAL
        self.areaButton['command'] = self.saveFile
        window.topFrame.topRightFrame.logMovement.set(
            main.character.flags['Config']['Log Movement'])
        window.topFrame.topRightFrame.automap.set(
            main.character.flags['Config']['Automap On'])
        root.title("Toshe's Quest II | "+name)
        

    def createFile(self, name):
        main.startNewGame(name)
        interfaceActions = main.getInterfaceActions(justFought=True)
        updateInterface(interfaceActions)
        window.bottomFrame.bottomRightFrame.centerButton['state'] = NORMAL
        self.areaButton['command'] = self.saveFile
        root.title("Toshe's Quest II | "+name)

        
class TopRightFrame:
    """Contains frames for other stats, enemy stats and store items

    Only one is displayed at a time.
    """

    def __init__(self, master):
        frameE = Frame(master, width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                       bg=DEFAULT_BG)
        frameE.grid(row=0, column=2)
        frameE.grid_propagate(0)
        self.makeFrameElements(frameE)

    def makeFrameElements(self, master):
        """Create labelframes for other stats, enemy stats and store items.

        Other stats displays: various character information
        Enemy stats displays: enemy name, image, HP
        Store displays: items for sale, selected item stats, buy button
        """        
        self.otherStats = LabelFrame(master, text="Other Stats", font=font3,
                                     width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                                     bg=DEFAULT_BG)
        self.otherStats.grid()
        self.otherStats.grid_propagate(0)
        
        self.strengthLabel = Label(self.otherStats, text="Strength", font=font2,
                                   bg=DEFAULT_BG)
        self.strengthLabel.grid(sticky=W)
        self.strengthValueButton = Button(self.otherStats, text="5", font=font1,
                                          bg=DEFAULT_BG,
                                          disabledforeground=BLACK, relief=FLAT,
                                          state=DISABLED,
                                          command=self.increaseStrength)
        self.strengthValueButton.grid(row=0, column=1, sticky=E)
        self.powerLabel = Label(self.otherStats, text="Base Damage", font=font2,
                                bg=DEFAULT_BG)
        self.powerLabel.grid(row=1, column=3, sticky=W)
        self.powerValueLabel = Label(self.otherStats, text="10", font=font1,
                                bg=DEFAULT_BG)
        self.powerValueLabel.grid(row=1, column=4, sticky=E)
        
        self.dexterityLabel = Label(self.otherStats, text="Dexterity",
                                    font=font2, bg=DEFAULT_BG)
        self.dexterityLabel.grid(row=1, column=0, sticky=W)
        self.dexterityValueButton = Button(self.otherStats, text="5",
                                           font=font1, bg=DEFAULT_BG,
                                           disabledforeground=BLACK,
                                           relief=FLAT, state=DISABLED,
                                           command=self.increaseDexterity)
        self.dexterityValueButton.grid(row=1, column=1, sticky=E)
        self.damageLabel = Label(self.otherStats, text="Avg Damage", font=font2,
                                 bg=DEFAULT_BG)
        self.damageLabel.grid(row=2, column=3, sticky=W)
        self.damageValueLabel = Label(self.otherStats, text="50", font=font1,
                                      bg=DEFAULT_BG)
        self.damageValueLabel.grid(row=2, column=4, sticky=E)
        
        self.wisdomLabel = Label(self.otherStats, text="Wisdom",
                                       font=font2, bg=DEFAULT_BG)
        self.wisdomLabel.grid(row=2, column=0, sticky=W)
        self.wisdomValueButton = Button(self.otherStats, text="5",
                                              font=font1, bg=DEFAULT_BG,
                                              disabledforeground=BLACK,
                                              relief=FLAT, state=DISABLED,
                                              command=self.increaseWisdom)
        self.wisdomValueButton.grid(row=2, column=1, sticky=E)
        self.accuracyLabel = Label(self.otherStats, text="Accuracy", font=font2,
                                   bg=DEFAULT_BG)
        self.accuracyLabel.grid(row=0, column=3, sticky=W)
        self.accuracyValueLabel = Label(self.otherStats, text="85%", font=font1,
                                        bg=DEFAULT_BG)
        self.accuracyValueLabel.grid(row=0, column=4, sticky=E)
        

        self.statPointsLabel = Label(self.otherStats,
                                     text="5\nStat Points",
                                     font=font2, bg=DEFAULT_BG, relief=FLAT)
        self.statPointsLabel.grid(rowspan=2, columnspan=2, padx=6,
                                     sticky=N+S+E+W)
        
        self.critChanceLabel = Label(self.otherStats, text="Crit Chance",
                                     font=font2, bg=DEFAULT_BG)
        self.critChanceLabel.grid(row=3, column=3, sticky=W)
        self.critChanceValueLabel = Label(self.otherStats, text="5%",
                                          font=font1, bg=DEFAULT_BG)
        self.critChanceValueLabel.grid(row=3, column=4, sticky=E)
        
        self.critDamageLabel = Label(self.otherStats, text="Crit Damage",
                                     font=font2, bg=DEFAULT_BG)
        self.critDamageLabel.grid(row=4, column=3, sticky=W)
        self.critDamageValueLabel = Label(self.otherStats, text="2000%",
                                          font=font1, bg=DEFAULT_BG)
        self.critDamageValueLabel.grid(row=4, column=4, sticky=E)

        self.earthLabel = Label(self.otherStats, text="Earth", font=font2,
                                bg=DEFAULT_BG)
        self.earthLabel.grid(row=6, sticky=W)
        self.earthValueLabel = Label(self.otherStats, text="0%", font=font1,
                                     bg=DEFAULT_BG)
        self.earthValueLabel.grid(row=6, column=1, sticky=E)
        self.defenceLabel = Label(self.otherStats, text="Defence", font=font2,
                                  bg=DEFAULT_BG)
        self.defenceLabel.grid(row=6, column=3, sticky=W)
        self.defenceValueLabel = Label(self.otherStats, text="75", font=font1,
                                       bg=DEFAULT_BG)
        self.defenceValueLabel.grid(row=6, column=4, sticky=E)

        self.waterLabel = Label(self.otherStats, text="Water", font=font2,
                                bg=DEFAULT_BG)
        self.waterLabel.grid(sticky=W)
        self.waterValueLabel = Label(self.otherStats, text="5%", font=font1,
                                     bg=DEFAULT_BG)
        self.waterValueLabel.grid(row=7, column=1, sticky=E)
        self.blockChanceLabel = Label(self.otherStats, text="Block Chance",
                                      font=font2, bg=DEFAULT_BG)
        self.blockChanceLabel.grid(row=7, column=3, sticky=W)
        self.blockChanceValueLabel = Label(self.otherStats, text="53%",
                                           font=font1, bg=DEFAULT_BG)
        self.blockChanceValueLabel.grid(row=7, column=4, sticky=E)

        self.fireLabel = Label(self.otherStats, text="Fire", font=font2,
                               bg=DEFAULT_BG)
        self.fireLabel.grid(sticky=W)
        self.fireValueLabel = Label(self.otherStats, text="0%", font=font1,
                                    bg=DEFAULT_BG)
        self.fireValueLabel.grid(row=8, column=1, sticky=E)
        self.eurosLabel = Label(self.otherStats, image=euroImage, text="5",
                                font=font2, bg=DEFAULT_BG, compound=RIGHT)
        self.eurosLabel.grid(row=8, column=3, columnspan=2, sticky=E)


        self.weaponElementLabel = Label(self.otherStats, text="Water Weapon",
                                        font=font2, bg=DEFAULT_BG,
                                        relief=GROOVE)
        self.weaponElementLabel.grid(row=9, columnspan=5, sticky=E+W, ipady=3)

        self.logMovement = IntVar()
        self.logMovement.set(1)
        self.toggleMovementCheck = Checkbutton(self.otherStats,
                                               text="Log movement",
                                               variable=self.logMovement,
                                               bg=DEFAULT_BG,
                                               font=font2, bd=0,
                                               command=\
                                               self.toggleConfigLogMovement)
        self.toggleMovementCheck.grid(row=10, columnspan=5, sticky=W)

        self.automap = IntVar()
        self.automap.set(1)
        self.toggleAutomapCheck = Checkbutton(self.otherStats,
                                              text="Show automap",
                                              variable=self.automap,
                                              bg=DEFAULT_BG, font=font2, bd=0,
                                              command=\
                                              self.toggleConfigAutomapOn)
        self.toggleAutomapCheck.grid(row=11, columnspan=5, sticky=W)
        self.mapButton = Button(self.otherStats,
                                text="Mark/Unmark Map",
                                font=font2,
                                fg=BUTTON_FG,
                                bg=BUTTON_BG,
                                command=self.clickMarkMapButton)
        self.mapButton.grid(row=12, columnspan=5, sticky=E+W)

        self.vBorderLabel1 = Label(self.otherStats, image=vBorderImage1,
                                  bg=DEFAULT_BG, bd=0)
        self.vBorderLabel1.grid(row=0, column=2, rowspan=5)
        self.vBorderLabel2 = Label(self.otherStats, image=vBorderImage2,
                                  bg=DEFAULT_BG, bd=0)
        self.vBorderLabel2.grid(row=6, column=2, rowspan=3)
        self.hBorderLabel = Label(self.otherStats, image=hBorderImage,
                                 bg=DEFAULT_BG, bd=0)
        self.hBorderLabel.grid(row=5, columnspan=5, pady=8)



        self.enemyStats = LabelFrame(master, text="Enemy", font=font3,
                                     width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                                     bg=DEFAULT_BG)
        self.enemyStats.grid(row=0)
        self.enemyStats.grid_propagate(0)
        self.enemyNameLabel = Label(self.enemyStats, text="Richard Titball",
                                    font=italicFont4, fg=BLACK, bg=DEFAULT_BG)
        self.enemyNameLabel.grid(row=0, column=0, columnspan=2)
        self.enemyLevelLabel = Label(self.enemyStats, text="17", font=font2,
                                     width=2, bg=DEFAULT_BG, relief=RIDGE)
        self.enemyLevelLabel.grid(row=0, column=1, padx=10, pady=10, sticky=E)
        self.enemyImageLabel = Label(self.enemyStats, image=None, bg=RED,
                                     relief=RIDGE, bd=4)
        self.enemyImageLabel.grid(columnspan=2, pady=20)
        self.enemyHpBarLabel = Label(self.enemyStats, image=hpBars[20],
                                     bg=DEFAULT_BG, relief=SUNKEN, bd=1)
        self.enemyHpBarLabel.grid(row=3, columnspan=2)
        self.enemyHpWord = Label(self.enemyStats, text="HP",
                            bg=DEFAULT_BG, font=font1, bd=0)
        self.enemyHpWord.grid(row=2, column=0, sticky=W)
        self.enemyHpLabel = Label(self.enemyStats, text="100/100",
                                  bg=DEFAULT_BG, font=font1, bd=0)
        self.enemyHpLabel.grid(row=2, column=1, sticky=E)



        self.store = LabelFrame(master, text="Store", font=font3,
                                width=FRAME_C_WIDTH, height=FRAME_C_HEIGHT,
                                bg=DEFAULT_BG)
        self.store.grid(row=0)
        self.store.grid_propagate(0)

        # Store checkbutton variable
        self.v2 = IntVar()
        self.storeButtons = makeItemButtons(self.store, self.v2, 1)
        self.itemNameLabel = Label(self.store, text="Name", font=font2,
                                   bg=DEFAULT_BG)
        self.itemNameLabel.grid(columnspan=3, sticky=W)
        self.itemCategoryLabel = Label(self.store, text="Category", font=font2,
                                       bg=DEFAULT_BG)
        self.itemCategoryLabel.grid(columnspan=3, sticky=W)
        self.itemValueLabel = Label(self.store, text="X Euros", font=font1,
                                    bg=DEFAULT_BG)
        self.itemValueLabel.grid(columnspan=3, sticky=W)
        self.itemRequirementLabel = Label(self.store, text="Requires X Y",
                                          font=font1, bg=DEFAULT_BG)
        self.itemRequirementLabel.grid(columnspan=3, sticky=W)
        self.itemQualityLabel = Label(self.store,
                                      text="X Power/X Defence", font=font1,
                                      bg=DEFAULT_BG)
        self.itemQualityLabel.grid(columnspan=3, sticky=W)
        self.itemCBRateLabel = Label(self.store, text=
                                     "X% Critical Chance/X% Block Chance",
                                     font=font1, bg=DEFAULT_BG)
        self.itemCBRateLabel.grid(columnspan=3, sticky=W)
        self.itemElementLabel = Label(self.store,
                                      text=
                                      "Imbued with X/Reduces X Damage by Y%",
                                      font=font1, bg=DEFAULT_BG)
        self.itemElementLabel.grid(columnspan=3, sticky=W)
        self.buyButton = Button(self.store, text="Buy", font=font2,
                                fg=BUTTON_FG, bg=BUTTON_BG,
                                command=self.clickBuyButton)
        self.buyButton.grid(columnspan=3, sticky=E+W)

    def increaseStrength(self):
        main.character.strength += 1
        main.character.statPoints -= 1
        self.updateOtherStats()

    def increaseDexterity(self):
        main.character.dexterity += 1
        main.character.statPoints -= 1
        self.updateOtherStats()

    def increaseWisdom(self):
        main.character.wisdom += 1
        main.character.statPoints -= 1
        self.updateOtherStats()

    def clickMarkMapButton(self, event=None):
        main.markMap()
        print "Map marked.\n"

    def clickBuyButton(self):
        main.buy(self.v2.get())
        window.topFrame.topLeftFrame.sellButton['state'] = DISABLED
        window.topFrame.topLeftFrame.updateInventory()
        self.buyButton['state'] = DISABLED
        self.updateStore()

    def updateOtherStats(self):
        """Change the Other Stats frame so its values reflect the character's
        current stats.
        """
        c = main.character

        self.strengthValueButton['text'] = c.strength
        self.powerValueLabel['text'] = c.damage
        self.dexterityValueButton['text'] = c.dexterity
        self.damageValueLabel['text'] = int(
            (c.accuracy if c.accuracy < 100 else 100) / 100. *
            (c.damage *
             (((c.cRate if c.cRate < 100 else 100) / 100.) *
              (c.cDamage / 100. - 1) + 1))
            )
        self.wisdomValueButton['text'] = c.wisdom
        if c.accuracy > 100:
            self.accuracyValueLabel['text'] = "100%"
        else:
            self.accuracyValueLabel['text'] = str(c.accuracy) + "%"
        
        if c.equippedWeapon.ELEMENT == "Physical":
            self.weaponElementLabel['relief'] = FLAT
            self.weaponElementLabel['text'] = ""
        else:
            self.weaponElementLabel['relief'] = GROOVE
            self.weaponElementLabel['text'] = (c.equippedWeapon.ELEMENT
                                               +" Weapon")
        self.critChanceValueLabel['text'] = str(c.cRate) + "%"
        self.critDamageValueLabel['text'] = str(c.cDamage) + "%"
        self.earthValueLabel['text'] = str(c.earthReduction) + "%"
        self.defenceValueLabel['text'] = str(c.defence)
        self.waterValueLabel['text'] = str(c.waterReduction) + "%"
        self.blockChanceValueLabel['text'] = str(c.bRate) + "%"
        self.fireValueLabel['text'] = str(c.fireReduction) + "%"
        self.eurosLabel['text'] = c.euros
        pluralOrNah = ("" if c.statPoints <= 1 else "s")
        if c.statPoints > 0:
            self.statPointsLabel['relief'] = RIDGE
            self.statPointsLabel['text'] = (str(c.statPoints) +
                                            "\nStat Point%s"
                                            % pluralOrNah)
            self.strengthValueButton.config(state=NORMAL, relief=RAISED)
            self.dexterityValueButton.config(state=NORMAL, relief=RAISED)
            self.wisdomValueButton.config(state=NORMAL, relief=RAISED)
        else:
            self.statPointsLabel['relief'] = FLAT
            self.statPointsLabel['text'] = ""
            self.strengthValueButton.config(state=DISABLED, relief=FLAT)
            self.dexterityValueButton.config(state=DISABLED, relief=FLAT)
            self.wisdomValueButton.config(state=DISABLED, relief=FLAT)

    def updateEnemyStats(self):
        """Show the level, name, hp bar, and hp of the current enemy in the
        enemy frame.
        """
        e = main.battle.enemy
        
        self.enemyLevelLabel['text'] = e.LEVEL
        self.enemyNameLabel['text'] = e.NAME
        self.enemyImageLabel['image'] = enemyImages[e.IDENTIFIER]
        if e.hp <= 0:
            self.enemyHpBarLabel['image'] = hpBars[0]
        elif float(e.hp) < float(e.maxHp) / (NUMBER_OF_BARS - 1):
            self.enemyHpBarLabel['image'] = hpBars[1]
        else:
            self.enemyHpBarLabel['image'] = hpBars[int(float(e.hp) / e.maxHp *
                                                       (NUMBER_OF_BARS - 1))]
        self.enemyHpBarLabel['text'] = "%d/%d" % (e.hp, e.maxHp)
        self.enemyHpLabel['text'] = "%d/%d" % (e.hp, e.maxHp)

    def updateStore(self):
        """Change images in the Store frame to match current store items."""
        clearItemStats(self, store=True)
        self.v2.set(-1)
        for i in range(0, 3):
            for j in range(0, 3):
                if not main.store[i*3+j]:
                    self.storeButtons[i*3+j].config(image=noItemImage,
                                                    state=DISABLED)
                else:
                    itemImage = itemImages[main.store[i*3+j].IMAGE_NAME]
                    self.storeButtons[i*3+j].config(image=itemImage,
                                                    state=NORMAL)

    def toggleConfigLogMovement(self, event=None):
        """Toggle in the character config
        flag whether movement should be logged."""
        main.character.flags['Config']['Log Movement'] =\
            int(not main.character.flags['Config']['Log Movement'])

    def toggleConfigAutomapOn(self, event=None):
        """Toggle in the character
        config flag whether the automap should be displayed."""
        main.character.flags['Config']['Automap On'] =\
            int(not main.character.flags['Config']['Automap On'])
        if main.character.flags['Config']['Automap On']:
            print "Automap on.\n"
        else:
            print "Automap off.\n"


class BottomLeftFrame:
    """Contains an output box with scrollbar."""

    def __init__(self, master):
        frameF = Frame(master, bg=DEFAULT_BG)
        frameF.grid()
        self.makeFrameElements(frameF)

    def makeFrameElements(self, master):
        self.outputBox = Text(master, font=font2, width=68, height=12,
                              wrap=WORD, bg=TEXTBOX_BG, relief=GROOVE)
        self.outputBox.grid()
        self.outputBox.tag_config("italicize", font=italicFont2)
        self.outputBox.tag_config("grey", foreground=GREY)
        self.outputBox.tag_config("highlight", foreground=BLACK)
        self.outputBox.insert(END,
                              ("Welcome. Click on the turtle to "+
                               "embark on your quest.\n"), "italicize")
        self.outputBox['state'] = DISABLED
        
        self.outputScrollbar = Scrollbar(master, bg=DEFAULT_BG,
                                         command=self.outputBox.yview)
        self.outputScrollbar.grid(row=0, column=1, sticky=N+S)
        
        self.outputBox.config(yscrollcommand=self.outputScrollbar.set)

        self.borderButton = Button(master, image=waveBorderImage, bg=DEFAULT_BG,
                                   relief=FLAT, bd=0,
                                   command=self.clearOutputBox)
        self.borderButton.grid(row=0, column=2)

    def clearOutputBox(self):
        self.outputBox['state'] = NORMAL
        self.outputBox.delete(0.0, END)
        self.outputBox['state'] = DISABLED

    def insertOutput(self, text, formatTag=None):
        """Add a string of text to the output box."""
        self.outputBox['state'] = NORMAL
        self.outputBox.insert(END, "\n"+text, (formatTag, "grey", "highlight"))
        self.outputBox.yview(END)
        self.outputBox['state'] = DISABLED

    def unhighlightOutputBox(self):
        """Change the output box contents to its original background colour."""
        self.outputBox['state'] = NORMAL
        self.outputBox.tag_remove("highlight", 1.0, END)
        self.outputBox['state'] = DISABLED


class BottomRightFrame:
    """Contains a menu box, a select/OK button, navigation arrows and a button
    to view the inventory.
    """

    def __init__(self, master):
        frameG = Frame(master, bg=DEFAULT_BG)
        frameG.grid(row=0, column=1)
        self.makeFrameElements(frameG)
        self.lastOkButtonState = None
        self.lastUpButtonState = None
        self.lastLeftButtonState = None
        self.lastRightButtonState = None
        self.lastDownButtonState = None

    def makeFrameElements(self, master):
        self.upButton = Button(master, image=upImage, relief=FLAT, bd=0,
                               bg=DEFAULT_BG, activebackground=DEFAULT_BG,
                               state=DISABLED, command=self.clickUpButton)
        self.upButton.bind_all('w', self.clickUpButton)
        self.upButton.bind_all('W', self.clickUpButton)
        self.upButton.grid(column=1)
        self.leftButton = Button(master, image=leftImage, relief=FLAT, bd=0,
                                 bg=DEFAULT_BG, activebackground=DEFAULT_BG,
                                 state=DISABLED, command=self.clickLeftButton)
        self.leftButton.bind_all('a', self.clickLeftButton)
        self.leftButton.bind_all('A', self.clickLeftButton)
        self.leftButton.grid(column=0, sticky=E)
        self.centerButton = Button(master, image=inventoryImage, relief=FLAT,
                                   bd=0, bg=DEFAULT_BG,
                                   activebackground=DEFAULT_BG, state=DISABLED,
                                   command=self.clickInventoryButton)
        self.centerButton.grid(row=1, column=1, pady=0)
        self.rightButton = Button(master, image=rightImage, relief=FLAT, bd=0,
                                  bg=DEFAULT_BG, activebackground=DEFAULT_BG,
                                  state=DISABLED, command=self.clickRightButton)
        self.rightButton.bind_all('d', self.clickRightButton)
        self.rightButton.bind_all('D', self.clickRightButton)
        self.rightButton.grid(row=1, column=2, sticky=W)
        self.downButton = Button(master, image=downImage, relief=FLAT, bd=0,
                                 bg=DEFAULT_BG, activebackground=DEFAULT_BG,
                                 state=DISABLED, command=self.clickDownButton)
        self.downButton.bind_all('s', self.clickDownButton)
        self.downButton.bind_all('S', self.clickDownButton)
        self.downButton.grid(column=1)
        self.defendButton = Button(master, image=defendImage, relief=FLAT,
                                   bd=0, bg=DEFAULT_BG,
                                   activebackground=DEFAULT_BG, state=DISABLED,
                                   command=self.clickDefendButton)
        self.defendButton.bind_all('j', self.clickDefendButton)
        self.defendButton.bind_all('J', self.clickDefendButton)
        self.defendButton.grid(row=1, column=0, sticky=E)
        self.defendButton.grid_remove()
        self.attackButton = Button(master, image=attackImage, relief=FLAT,
                                   bd=0, bg=DEFAULT_BG,
                                   activebackground=DEFAULT_BG, state=DISABLED,
                                   command=self.clickAttackButton)
        self.attackButton.bind_all('k', self.clickAttackButton)
        self.attackButton.bind_all('K', self.clickAttackButton)
        self.attackButton.grid(row=0, column=1)
        self.attackButton.grid_remove()
        self.fleeButton = Button(master, image=fleeImage, relief=FLAT,
                                 bd=0, bg=DEFAULT_BG,
                                 activebackground=DEFAULT_BG, state=DISABLED,
                                 command=self.clickFleeButton)
        self.fleeButton.bind_all('l', self.clickFleeButton)
        self.fleeButton.bind_all('L', self.clickFleeButton)
        self.fleeButton.grid(row=1, column=2, sticky=W)
        self.fleeButton.grid_remove()
        
        self.menuBox = Listbox(master, font=font2, width=40, height=4,
                               fg=BLACK, bg=TEXTBOX_BG, relief=GROOVE,
                               selectmode=SINGLE, exportselection=0)
        self.bindChoices()
        self.enableMenuBox()
        self.menuBox.grid(columnspan=3)

        self.okButton = Button(master, text="Select", font=font2,
                               fg=BUTTON_FG, bg=BUTTON_BG, state=DISABLED,
                               command=self.clickOkButton)
        self.okButton.grid(columnspan=3, sticky=E+W)
        self.skillButton = Button(master, text="Use Skill", font=font2,
                                  fg=BUTTON_FG, bg=BUTTON_BG, state=DISABLED,
                                  command=self.clickSkillButton)
        self.skillButton.grid(row=4, columnspan=3, sticky=E+W)
        self.skillButton.grid_remove()

    def clickUpButton(self, event=None):
        if self.upButton['state'] == NORMAL:
            interfaceActions = main.move("up")
            if window.topFrame.topRightFrame.logMovement.get():
                interfaceActions['text'] = \
                            self.updateText(interfaceActions, "forward")
            if window.topFrame.topRightFrame.automap.get():
                main.printMap()
            updateInterface(interfaceActions)

    def clickLeftButton(self, event=None):
        if self.leftButton['state'] == NORMAL:
            interfaceActions = main.move("left")
            if window.topFrame.topRightFrame.logMovement.get():
                interfaceActions['text'] = \
                            self.updateText(interfaceActions, "left")
            if window.topFrame.topRightFrame.automap.get():
                main.printMap()
            updateInterface(interfaceActions)
            
    def clickRightButton(self, event=None):
        if self.rightButton['state'] == NORMAL:
            interfaceActions = main.move("right")
            if window.topFrame.topRightFrame.logMovement.get():
                interfaceActions['text'] = \
                            self.updateText(interfaceActions, "right")
            if window.topFrame.topRightFrame.automap.get():
                main.printMap()
            updateInterface(interfaceActions)

    def clickDownButton(self, event=None):
        if self.downButton['state'] == NORMAL:
            interfaceActions = main.move("down")
            if window.topFrame.topRightFrame.logMovement.get():
                interfaceActions['text'] = \
                            self.updateText(interfaceActions, "backward")
            if window.topFrame.topRightFrame.automap.get():
                main.printMap()
            updateInterface(interfaceActions)

    def clickInventoryButton(self, event=None):
        if self.centerButton['state'] == NORMAL:
            # Save OK Button state for when the Back Button is pressed
            self.lastOkButtonState = self.okButton['state']
            
            self.centerButton.config(image=backImage,
                                     command=self.clickBackButton)
            self.centerButton.bind_all('i', self.clickBackButton)
            self.centerButton.bind_all('I', self.clickBackButton)
            self.enableDirectionButtons([])
            self.attackButton['state'] = DISABLED
            self.defendButton['state'] = DISABLED
            self.fleeButton['state'] = DISABLED
            self.okButton['state'] = DISABLED
            self.disableMenuBox()
            enableInventoryView()

    def clickBackButton(self, event=None):
        if self.centerButton['state'] == NORMAL:
            self.centerButton.config(image=inventoryImage,
                                     command=self.clickInventoryButton)
            self.centerButton.bind_all('i', self.clickInventoryButton)
            self.centerButton.bind_all('I', self.clickInventoryButton)
            self.enableDirectionButtons(main.enabledDirections)
            self.enableMenuBox()
            self.okButton['state'] = self.lastOkButtonState
            views[main.view]()

    def clickCancelDropButton(self):
        self.centerButton.config(image=inventoryImage,
                                 command=self.clickInventoryButton)
        self.centerButton.bind_all('i', self.clickInventoryButton)
        self.centerButton.bind_all('I', self.clickInventoryButton)
        self.enableDirectionButtons(main.enabledDirections)
        self.upButton.grid_remove()
        self.leftButton.grid_remove()
        self.rightButton.grid_remove()
        self.downButton.grid_remove()
        self.enableMenuBox()
        views[main.view]()

    def clickCancelForgetButton(self):
        self.centerButton.config(image=inventoryImage,
                                 command=self.clickInventoryButton)  
        self.okButton['command'] = self.clickOkButton
        self.okButton['state'] = DISABLED
        self.upButton['state'] = self.lastUpButtonState
        self.leftButton['state'] = self.lastLeftButtonState
        self.rightButton['state'] = self.lastRightButtonState
        self.downButton['state'] = self.lastDownButtonState
        self.modifyMenu(self.tempMenu)
        self.bindChoices()
        views[main.view]()

    def clickAttackButton(self, event=None):
        if self.attackButton['state'] == NORMAL:
            interfaceActions = main.attack()
            updateInterface(interfaceActions)

    def clickDefendButton(self, event=None):
        if self.defendButton['state'] == NORMAL:
            interfaceActions = main.defend()
            updateInterface(interfaceActions)

    def clickFleeButton(self, event=None):
        if self.fleeButton['state'] == NORMAL:
            interfaceActions = main.flee()
            updateInterface(interfaceActions)

    def clickOkButton(self):
        selection = int(self.menuBox.curselection()[0])
        interfaceActions = main.select(selection)
        updateInterface(interfaceActions)

    def clickSkillButton(self):
        selection = int(self.menuBox.curselection()[0])
        interfaceActions = main.useSkill(main.character.skills[selection])
        updateInterface(interfaceActions)

    def clickForgetButton(self):
        selection = int(self.menuBox.curselection()[0])
        main.character.forgetSkill(main.character.skills[selection])
        main.character.learnSkill(main.tempSkill)
        main.character.euros -= main.tempCost
        self.clickCancelForgetButton()

    def enableMenuBox(self):
        self.menuBox.bind('<<ListboxSelect>>', self.enableOkButton)
        self.menuBox.bind('<<ListboxSelect>>', self.enableSkillButton, 1)
        self.menuBox['state'] = NORMAL

    def disableMenuBox(self):
        self.menuBox.unbind('<<ListboxSelect>>')
        self.menuBox['state'] = DISABLED

    def bindSkills(self):
        self.menuBox.bind_all('1', self.selectSkill)
        self.menuBox.bind_all('2', self.selectSkill)
        self.menuBox.bind_all('3', self.selectSkill)
        self.menuBox.bind_all('4', self.selectSkill)

    def bindChoices(self):
        self.menuBox.bind_all('1', self.selectChoice)
        self.menuBox.bind_all('2', self.selectChoice)
        self.menuBox.bind_all('3', self.selectChoice)
        self.menuBox.bind_all('4', self.selectChoice)

    def selectChoice(self, event=None):
        if self.menuBox['state'] != DISABLED:
            tempSelection = self.menuBox.curselection()
            for i in range(0, 4):
                self.menuBox.selection_clear(i)
            self.menuBox.selection_set(int(event.char)-1)
            if self.menuSelectionIsValid():
                self.clickOkButton()
            elif bool(tempSelection):
                self.menuBox.selection_set(int(tempSelection[0]))

    def selectSkill(self, event=None):
        if self.menuBox['state'] != DISABLED:
            tempSelection = self.menuBox.curselection()
            for i in range(0, 4):
                self.menuBox.selection_clear(i)
            self.menuBox.selection_set(int(event.char)-1)
            if self.menuSelectionIsValid():
                self.clickSkillButton()
            elif bool(tempSelection):
                self.menuBox.selection_set(int(tempSelection[0]))

    def menuSelectionIsValid(self):
        return bool(self.menuBox.curselection())

    def endBattle(self, event=None):
        if self.menuBox['state'] != DISABLED:
            bottomFrame = window.bottomFrame.bottomRightFrame
            bottomFrame.bindChoices()
            bottomFrame.okButton['command'] = bottomFrame.clickOkButton
            interfaceActions = main.getInterfaceActions(justFought=True)
            if ('text' in interfaceActions and
                interfaceActions['text'] is not None):
                interfaceActions['text'] = "\n"+interfaceActions['text'].strip()
            updateInterface(interfaceActions)

    def enableDirectionButtons(self, enabledDirections):
        """Set the state of specified direction buttons to NORMAL."""        
        if "up" in enabledDirections:
            self.upButton['state'] = NORMAL
        else:
            self.upButton['state'] = DISABLED
        if "left" in enabledDirections:
            self.leftButton['state'] = NORMAL
        else:
            self.leftButton['state'] = DISABLED
        if "right" in enabledDirections:
            self.rightButton['state'] = NORMAL
        else:
            self.rightButton['state'] = DISABLED
        if "down" in enabledDirections:
            self.downButton['state'] = NORMAL
        else:
            self.downButton['state'] = DISABLED

    def enableOkButton(self, event=None):
        if self.menuSelectionIsValid():
            self.okButton['state'] = NORMAL

    def enableSkillButton(self, event=None):
        if self.menuSelectionIsValid():
            self.skillButton['state'] = NORMAL

    def modifyMenu(self, menuItems):
        """Remove all items from the menu box, then add new ones in sequence."""
        self.menuBox.delete(0, END)
        if menuItems:
            for i in menuItems:
                self.menuBox.insert(END, i)

    def updateText(self, actions, direction):
        movementPhrase = "You %s %s." % (main.currentArea.movementVerb,
                                         direction)
        if 'text' in actions and actions['text']:
            textWithMovement = movementPhrase+"\n"+actions['text']
            return textWithMovement
        return movementPhrase


def makeItemButtons(master, var, inStore):
    """Create 9 buttons to represent either inventory or store items.

    inStore indicates that the buttons are being made in the store frame if its
    value is 1.
    """
    itemButtons = []
    commands = [displayItemStats, displayStoreItemStats]
    for i in range(0, 3):   # Item radiobutton values range from 0 to 8
        for j in range(0, 3):
            itemButton = Radiobutton(master, image=defaultImage,
                                     variable=var, value=i*3+j, width=64,
                                     height=64, bg=BLACK, indicatoron=0, bd=4,
                                     command=commands[inStore])
            itemButton.grid(row=i, column=j)
            itemButtons.append(itemButton)
    return itemButtons


def displayItemStats():
    """Display the stats of the selected item in the Inventory frame."""
    frame = window.topFrame.topLeftFrame
    item = main.character.items[frame.v1.get()]
    
    frame.itemNameLabel.config(text=item.NAME, font=italicFont2)
    
    frame.itemCategoryLabel['text'] = item.CATEGORY
    
    frame.itemValueLabel['text'] = "Worth "+str(item.SELL_PRICE)+" Euros"
    
    if item.CATEGORY == "Miscellaneous" and "*" not in item.INFORMATION:
        frame.itemRequirementLabel['text'] = item.INFORMATION
    elif item.CATEGORY == "Miscellaneous" and "*" in item.INFORMATION:
        frame.itemRequirementLabel['text'] = item.INFORMATION.split("*")[0]
    else:
        frame.itemRequirementLabel['text'] = ("Requires",
                                              item.REQUIREMENT_VALUE,
                                              item.REQUIREMENT_TYPE)

    if item.CATEGORY == "Armour" or item.CATEGORY == "Shield":
        frame.itemQualityLabel['text'] = item.DEFENCE, "Defence"
    elif item.CATEGORY == "Miscellaneous" and "*" not in item.INFORMATION:
        frame.itemQualityLabel['text'] = ""
    elif item.CATEGORY == "Miscellaneous" and "*" in item.INFORMATION:        
        frame.itemQualityLabel['text'] = item.INFORMATION.split("*")[1]
    else:
        frame.itemQualityLabel['text'] = item.POWER, "Power"
        
    if item.CATEGORY == "Shield":
        frame.itemCBRateLabel['text'] = str(item.B_RATE)+"% Block Chance"
    elif item.CATEGORY in ("Armour", "Miscellaneous"):
        frame.itemCBRateLabel['text'] = ""
    else:
        frame.itemCBRateLabel['text'] = str(item.C_RATE)+"% Critical Chance"
        
    if ((item.CATEGORY == "Shield" or item.CATEGORY == "Armour") and
        item.REDUCTION != 0):
        frame.itemElementLabel['text'] = ("Reduces", item.ELEMENT, "Damage",
                                          "by",
                                          str(item.REDUCTION)+str("%"))
    elif (item.CATEGORY != "Miscellaneous" and
          item.CATEGORY != "Shield" and
          item.CATEGORY != "Armour" and
          item.ELEMENT != "Physical"):
        frame.itemElementLabel['text'] = ("Item imbued with "+
                                          str(item.ELEMENT))
    else:
        frame.itemElementLabel['text'] = ""

    if ((item.CATEGORY == "Bow" and
         main.character.equippedShield.NAME != "Nothing") or
        (item.CATEGORY == "Shield" and
         main.character.equippedWeapon.CATEGORY == "Bow")):
        frame.itemCategoryLabel['fg'] = RED
    else:
        frame.itemCategoryLabel['fg'] = BLACK
        
    if (item.CATEGORY == "Miscellaneous" or
        (item.REQUIREMENT_TYPE == "Strength" and
         main.character.strength >= item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Dexterity" and
         main.character.dexterity >= item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Wisdom" and
         main.character.wisdom >= item.REQUIREMENT_VALUE)):
        frame.itemRequirementLabel['fg'] = BLACK
    else:
        frame.itemRequirementLabel['fg'] = RED

    if frame.v1.get() in main.character.equippedItemIndices.values():
        frame.equipButton['text'] = "Unequip"
        frame.sellButton['state'] = DISABLED
    else:
        frame.equipButton['text'] = "Equip"
        frame.sellButton['state'] = NORMAL

    if (item.CATEGORY == "Miscellaneous" or
        (item.REQUIREMENT_TYPE == "Strength" and
         main.character.strength < item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Dexterity" and
         main.character.dexterity < item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Wisdom" and
         main.character.wisdom < item.REQUIREMENT_VALUE) or
        (item.CATEGORY == "Bow" and
         main.character.equippedShield.NAME != "Nothing") or
        (item.CATEGORY == "Shield" and
         main.character.equippedWeapon.CATEGORY == "Bow")):
        frame.equipButton['state'] = DISABLED
    else:
        frame.equipButton['state'] = NORMAL

    frame.dropButton['state'] = NORMAL


def displayStoreItemStats():
    """Display the stats of the selected item in the Store frame."""
    frame = window.topFrame.topRightFrame
    item = main.store[frame.v2.get()]

    frame.itemNameLabel.config(text=item.NAME, font=italicFont2)
    
    frame.itemCategoryLabel['text'] = item.CATEGORY
    
    frame.itemValueLabel['text'] = "%d / %d Euros" % (item.PRICE,
                                                      main.character.euros)
    
    if item.CATEGORY == "Miscellaneous" and "*" not in item.INFORMATION:
        frame.itemRequirementLabel['text'] = item.INFORMATION
    elif item.CATEGORY == "Miscellaneous" and "*" in item.INFORMATION:
        frame.itemRequirementLabel['text'] = item.INFORMATION.split("*")[0]
    else:
        frame.itemRequirementLabel['text'] = ("Requires",
                                              item.REQUIREMENT_VALUE,
                                              item.REQUIREMENT_TYPE)
    
    if item.CATEGORY == "Armour" or item.CATEGORY == "Shield":
        frame.itemQualityLabel['text'] = item.DEFENCE, "Defence"
    elif item.CATEGORY == "Miscellaneous" and "*" not in item.INFORMATION:
        frame.itemQualityLabel['text'] = ""
    elif item.CATEGORY == "Miscellaneous" and "*" in item.INFORMATION:        
        frame.itemQualityLabel['text'] = item.INFORMATION.split("*")[1]
    else:
        frame.itemQualityLabel['text'] = item.POWER, "Power"
        
    if item.CATEGORY == "Shield":
        frame.itemCBRateLabel['text'] = str(item.B_RATE)+"% Block Chance"
    elif item.CATEGORY in ("Armour", "Miscellaneous"):
        frame.itemCBRateLabel['text'] = ""
    else:
        frame.itemCBRateLabel['text'] = str(item.C_RATE)+"% Critical Chance"
        
    if ((item.CATEGORY == "Shield" or item.CATEGORY == "Armour") and
        item.REDUCTION != 0):
        frame.itemElementLabel['text'] = ("Reduces", item.ELEMENT, "Damage",
                                          "by",
                                          str(item.REDUCTION)+str("%"))
    elif (item.CATEGORY != "Miscellaneous" and
          item.CATEGORY != "Shield" and
          item.CATEGORY != "Armour" and
          item.ELEMENT != "Physical"):
        frame.itemElementLabel['text'] = ("Item imbued with "+
                                          str(item.ELEMENT))
    else:
        frame.itemElementLabel['text'] = ""

    if ((item.CATEGORY == "Bow" and
         main.character.equippedShield.NAME != "Nothing") or
        (item.CATEGORY == "Shield" and
         main.character.equippedWeapon.CATEGORY == "Bow")):
        frame.itemCategoryLabel['fg'] = RED
    else:
        frame.itemCategoryLabel['fg'] = BLACK

    if main.character.euros < item.PRICE:
        frame.itemValueLabel['fg'] = RED
    else:
        frame.itemValueLabel['fg'] = BLACK
            
    if (item.CATEGORY == "Miscellaneous" or
        (item.REQUIREMENT_TYPE == "Strength" and
         main.character.strength >= item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Dexterity" and
         main.character.dexterity >= item.REQUIREMENT_VALUE) or
        (item.REQUIREMENT_TYPE == "Wisdom" and
         main.character.wisdom >= item.REQUIREMENT_VALUE)):
        frame.itemRequirementLabel['fg'] = BLACK
    else:
        frame.itemRequirementLabel['fg'] = RED

    if main.character.euros < item.PRICE or not main.character.hasRoom():
        frame.buyButton['state'] = DISABLED
    else:
        frame.buyButton['state'] = NORMAL


def clearItemStats(frame, store):
    frame.itemNameLabel.config(text="Select an item.", font=italicFont2)
    if main.character.hasNoItems() and not store:
        frame.itemNameLabel.config(text="Your inventory is empty.",
                                   font=italicFont2)
    frame.itemCategoryLabel['text'] = ""
    frame.itemValueLabel['text'] = ""
    frame.itemRequirementLabel['text'] = ""
    frame.itemQualityLabel['text'] = ""
    frame.itemCBRateLabel['text'] = ""
    frame.itemElementLabel['text'] = ""


def flash():
    topCenterFrame = window.topFrame.topCenterFrame
    for i in range(0, 6):
        topCenterFrame.areaButton.flash()


def updateInterface(updates):
    """Update the interface to reflect current game events.

    actions is a dictionary that may contain updates to the textbox, menu,
    center image, or current view.
    """
        
    bottomRightFrame = window.bottomFrame.bottomRightFrame
    topRightFrame = window.topFrame.topRightFrame
    topCenterFrame = window.topFrame.topCenterFrame
    bottomLeftFrame = window.bottomFrame.bottomLeftFrame

    # Flash must occur before battle view is shown and area button is disabled
    if ('flash' in updates):
        flash()

    bottomLeftFrame.unhighlightOutputBox()
    topCenterFrame.changeTitle("\n%s" % main.currentArea.name)
    views[updates['view']]()
            
    while main.character.hasLeveledUp():
        if not updates['text']:
            updates['text'] = ""
        updates['text'] += "\nToshe has reached level "+str(
            main.character.level)+"!"
        window.levelUpFrame.grid()
        root.after(4000, window.removeLevelUpFrame)

    for mercenary in main.character.mercenaries:
        while mercenary.hasLeveledUp():
            if not updates['text']:
                updates['text'] = ""
            updates['text'] += "\n%s has reached level %s!" % (mercenary.NAME,
                                                               mercenary.level)
            window.gridMercenaryUpFrame(mercenary.NAME)
            root.after(3000, window.removeMercenaryUpFrame)
            
    if ('game over' == updates['view']):
        if not updates['text']:
            updates['text'] = ""
        updates['enabled directions'] = []
        updates['text'] += ("\nToshe has died.\nToshe's quest ends here.")
        updates['menu'] = ["Exit."]
        updates['italic text'] = None
        updates['image index'] = None
    if ('enabled directions' in updates) and (updates['enabled directions']
                                              is not None):
        bottomRightFrame.enableDirectionButtons(
            updates['enabled directions'])
    if ('image index' in updates) and (updates['image index'] is not None):
        topCenterFrame.areaButton['image'] =\
            areaImages[main.currentArea.name][updates['image index']]
    if ('menu' in updates) and (updates['menu'] is not None):
        bottomRightFrame.modifyMenu(updates['menu'])
        bottomRightFrame.okButton['state'] = DISABLED
    if ('overloaded' in updates) and (updates['overloaded'] == "items"):
        enableDropItemView()
    elif ('overloaded' in updates) and (updates['overloaded'] == "skills"):
        enableForgetSkillView()
    if (('item' in updates) and (updates['item'] is not None)):
        window.lootFrame.grid()
        root.after(2500, window.removeLootFrame)
    if 'save' in updates and updates['save'] is not None:
        main.saveGame()
        if not updates['text']:
            updates['text'] = ""
        updates['text'] += ("\nGame saved.")
    if ('text' in updates) and (updates['text'] is not None):
        if 'format text' in updates:
            bottomLeftFrame.insertOutput(updates['text'],
                                         updates['format text'])
        else:
            bottomLeftFrame.insertOutput(updates['text'])
    if ('italic text' in updates) and (updates['italic text'] is not None):
        bottomLeftFrame.insertOutput(updates['italic text'], "italicize")
    topRightFrame.updateOtherStats()
        

def enableTravelView():
    window.topFrame.topCenterFrame.areaButton['state'] = NORMAL
    leftFrame = window.topFrame.topLeftFrame
    rightFrame = window.topFrame.topRightFrame
    leftFrame.vitalStats.grid()
    leftFrame.inventory.grid_remove()
    rightFrame.otherStats.grid()
    rightFrame.enemyStats.grid_remove()
    rightFrame.store.grid_remove()
    leftFrame.updateVitalStats()
    rightFrame.updateOtherStats()

    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.centerButton['state'] = NORMAL
    bottomFrame.upButton.grid()
    bottomFrame.leftButton.grid()
    bottomFrame.rightButton.grid()
    bottomFrame.downButton.grid()
    bottomFrame.centerButton.grid(pady=0)
    bottomFrame.centerButton.bind_all('i', bottomFrame.clickInventoryButton)
    bottomFrame.centerButton.bind_all('I', bottomFrame.clickInventoryButton)
    bottomFrame.okButton.grid()
    bottomFrame.attackButton.grid_remove()
    bottomFrame.defendButton.grid_remove()
    bottomFrame.fleeButton.grid_remove()
    bottomFrame.skillButton.grid_remove()


def enableBattleView():
    window.topFrame.topCenterFrame.areaButton['state'] = DISABLED
    leftFrame = window.topFrame.topLeftFrame
    rightFrame = window.topFrame.topRightFrame
    leftFrame.vitalStats.grid()
    leftFrame.inventory.grid_remove()
    rightFrame.otherStats.grid_remove()
    rightFrame.enemyStats.grid()
    rightFrame.store.grid_remove()
    leftFrame.updateVitalStats()
    rightFrame.updateEnemyStats()

    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.upButton['state'] = DISABLED
    bottomFrame.leftButton['state'] = DISABLED
    bottomFrame.rightButton['state'] = DISABLED
    bottomFrame.downButton['state'] = DISABLED
    bottomFrame.upButton.grid_remove()
    bottomFrame.leftButton.grid_remove()
    bottomFrame.rightButton.grid_remove()
    bottomFrame.downButton.grid_remove()
    bottomFrame.okButton.grid_remove()
    bottomFrame.centerButton['state'] = NORMAL
    bottomFrame.attackButton['state'] = NORMAL
    bottomFrame.defendButton['state'] = NORMAL
    bottomFrame.fleeButton['state'] = NORMAL
    bottomFrame.centerButton.grid(pady=(0, 34))
    bottomFrame.attackButton.grid()
    bottomFrame.defendButton.grid()
    bottomFrame.fleeButton.grid()
    bottomFrame.skillButton.grid()
    
    bottomFrame.bindSkills()
    
    skills = []
    bottomFrame.skillButton['state'] = DISABLED
    for skill in main.character.skills:
        skills.append(skill.NAME)
    bottomFrame.modifyMenu(skills)


def enableBattleOverView():
    enableBattleView()
    frame = window.bottomFrame.bottomRightFrame
    frame.centerButton['state'] = DISABLED
    frame.attackButton['state'] = DISABLED
    frame.defendButton['state'] = DISABLED
    frame.fleeButton['state'] = DISABLED
    frame.skillButton.grid_remove()
    frame.menuBox.bind_all('1', frame.endBattle)
    frame.modifyMenu(["Proceed."])
    frame.okButton.grid()
    frame.okButton['state'] = DISABLED
    frame.okButton['command'] = frame.endBattle


def enableGameOverView():
    topFrame = window.topFrame.topCenterFrame
    topFrame.areaButton.config(state=NORMAL, image=gameOverImage,
                               command=topFrame.loadFile)
    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.centerButton['state'] = DISABLED
    bottomFrame.attackButton['state'] = DISABLED
    bottomFrame.defendButton['state'] = DISABLED
    bottomFrame.fleeButton['state'] = DISABLED
    bottomFrame.skillButton.grid_remove()
    bottomFrame.menuBox.unbind_all('1')
    bottomFrame.okButton.grid()
    bottomFrame.okButton['state'] = DISABLED
    bottomFrame.okButton['command'] = root.destroy
    bottomFrame.centerButton['state'] = DISABLED
    window.topFrame.topLeftFrame.updateVitalStats()
    window.topFrame.topRightFrame.updateEnemyStats()


def enableInventoryView():
    window.topFrame.topCenterFrame.areaButton['state'] = DISABLED
    leftFrame = window.topFrame.topLeftFrame
    rightFrame = window.topFrame.topRightFrame
    bottomFrame = window.bottomFrame.bottomRightFrame
    leftFrame.vitalStats.grid_remove()
    leftFrame.inventory.grid()
    rightFrame.otherStats.grid()
    rightFrame.enemyStats.grid_remove()
    rightFrame.store.grid_remove()
    leftFrame.updateInventory()
    rightFrame.updateOtherStats()

    leftFrame.sellButton.grid_remove()
    leftFrame.dropButton.grid_remove()
    leftFrame.equipButton.grid()
    leftFrame.equipButton['state'] = DISABLED


def enableStoreView():
    window.topFrame.topCenterFrame.areaButton['state'] = NORMAL
    leftFrame = window.topFrame.topLeftFrame
    rightFrame = window.topFrame.topRightFrame
    leftFrame.vitalStats.grid_remove()
    leftFrame.inventory.grid()
    leftFrame.updateInventory()
    rightFrame.otherStats.grid_remove()
    rightFrame.enemyStats.grid_remove()
    rightFrame.store.grid()
    leftFrame.updateInventory()
    rightFrame.updateStore()

    leftFrame.equipButton.grid_remove()
    leftFrame.dropButton.grid_remove()
    leftFrame.sellButton.grid()
    leftFrame.sellButton['state'] = DISABLED
    rightFrame.buyButton['state'] = DISABLED

    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.upButton.grid()
    bottomFrame.leftButton.grid()
    bottomFrame.rightButton.grid()
    bottomFrame.downButton.grid()
    bottomFrame.centerButton.grid(pady=0)
    bottomFrame.okButton.grid()
    bottomFrame.attackButton.grid_remove()
    bottomFrame.defendButton.grid_remove()
    bottomFrame.fleeButton.grid_remove()
    bottomFrame.skillButton.grid_remove()
    bottomFrame.centerButton['state'] = NORMAL


def enableDropItemView():
    enableInventoryView()
    window.topFrame.topCenterFrame.areaButton['state'] = DISABLED
    leftFrame = window.topFrame.topLeftFrame
    leftFrame.equipButton.grid_remove()
    leftFrame.sellButton.grid_remove()
    leftFrame.dropButton.grid()
    leftFrame.dropButton['state'] = DISABLED

    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.okButton['state'] = DISABLED
    bottomFrame.attackButton.grid_remove()
    bottomFrame.defendButton.grid_remove()
    bottomFrame.fleeButton.grid_remove()
    bottomFrame.centerButton.config(state=NORMAL, image=backImage,
                                    command=bottomFrame.clickCancelDropButton)
    bottomFrame.centerButton.unbind_all('i')
    bottomFrame.centerButton.unbind_all('I')
    bottomFrame.centerButton.grid(pady=34)
    bottomFrame.upButton['state'] = DISABLED
    bottomFrame.leftButton['state'] = DISABLED
    bottomFrame.rightButton['state'] = DISABLED
    bottomFrame.downButton['state'] = DISABLED
    bottomFrame.upButton.grid_remove()
    bottomFrame.leftButton.grid_remove()
    bottomFrame.rightButton.grid_remove()
    bottomFrame.downButton.grid_remove()
    bottomFrame.disableMenuBox()


def enableForgetSkillView():
    enableTravelView()
    bottomFrame = window.bottomFrame.bottomRightFrame
    bottomFrame.okButton.config(state=DISABLED,
                                command=bottomFrame.clickForgetButton)
    bottomFrame.enableMenuBox()
    bottomFrame.lastUpButtonState = bottomFrame.upButton['state']
    bottomFrame.lastLeftButtonState = bottomFrame.leftButton['state']
    bottomFrame.lastRightButtonState = bottomFrame.rightButton['state']
    bottomFrame.lastDownButtonState = bottomFrame.downButton['state']
    bottomFrame.upButton['state'] = DISABLED
    bottomFrame.leftButton['state'] = DISABLED
    bottomFrame.centerButton.config(state=NORMAL, image=backImage,
                                    command=bottomFrame.clickCancelForgetButton)
    bottomFrame.rightButton['state'] = DISABLED
    bottomFrame.downButton['state'] = DISABLED
    bottomFrame.tempMenu = list(bottomFrame.menuBox.get(0, END))
    skills = []
    for skill in main.character.skills:
        skills.append(skill.NAME)
    bottomFrame.modifyMenu(skills)
    bottomFrame.menuBox.unbind_all('1')
    bottomFrame.menuBox.unbind_all('2')
    bottomFrame.menuBox.unbind_all('3')
    bottomFrame.menuBox.unbind_all('4')


def hideSideFrames():
    leftFrame = window.topFrame.topLeftFrame
    rightFrame = window.topFrame.topRightFrame
    leftFrame.vitalStats.grid_remove()
    leftFrame.inventory.grid_remove()
    rightFrame.otherStats.grid_remove()
    rightFrame.enemyStats.grid_remove()
    rightFrame.store.grid_remove()


def makeWindow(event=None):
    global window
    
    temporaryFrame.grid_remove()
    window = Window(root)
    hideSideFrames()
    main.initializeSound()


def doNothing(event=None):
    pass


def displayLoadingScreen(event=None):
    global loading
    global loadingProgressBar
    
    loading = Toplevel()
    loading.title("Loading...")
    loading.protocol('WM_DELETE_WINDOW', doNothing)
    loading.overrideredirect(1)
    loading.resizable(0, 0)
    loadingProgressBar = Label(loading, relief=RIDGE, bd=3, bg=BROWN)
    loadingProgressBar.grid()


def updateLoadingScreen(event=None):
    global loading
    
    loadingProgressBar['image'] = epBars[
        int(float(NUMBER_OF_BARS - 1) / fullProgress * loadProgress + 0.1)]
    if int(loadProgress + 0.1) != fullProgress:
        root.after(30, updateLoadingScreen)
    else:
        loading.destroy()
    
    
def loadAssets(event=None):
    global loadProgress
    
    root.update()
    for i in range(1, NUMBER_OF_BARS):
        xpBars.append(PhotoImage(file="images\\bars\\xpbar"+
                                 str(i)+".gif"))
        hpBars.append(PhotoImage(file="images\\bars\\hpbar"+
                                 str(NUMBER_OF_BARS - i - 1)+".gif"))
        epBars.append(PhotoImage(file="images\\bars\\epbar"+
                                 str(NUMBER_OF_BARS - i - 1)+".gif"))

    loadProgress += 7
    root.update()

    for weaponName in main.weapons:
        itemImages[main.weapons[weaponName].IMAGE_NAME] = (
            PhotoImage(file="images\\weapons\\"+weaponName+".gif"))
    for armourName in main.armour:
        itemImages[main.armour[armourName].IMAGE_NAME] = (
            PhotoImage(file="images\\armour\\"+armourName+".gif"))
    for shieldName in main.shields:
        itemImages[main.shields[shieldName].IMAGE_NAME] = (
            PhotoImage(file="images\\shields\\"+shieldName+".gif"))
    for itemName in main.miscellaneousItems:
        itemImages[main.miscellaneousItems[itemName].IMAGE_NAME] = (
            PhotoImage(file="images\\miscellaneous\\"+itemName+".gif"))
    loadProgress += 3
    root.update()

    for enemyId in main.enemies:
        enemyImages[enemyId] = (PhotoImage(file="images\\enemies\\"+
                                           main.enemies[enemyId].IMAGE+".gif"))    
    loadProgress += 10
    root.update()
    
    for area in main.areas.itervalues():
        areaImages[area.name] = []
        while 1:
            try:
                for i in range(0, 99):
                    areaImages[area.name].append(PhotoImage
                                                 (file="images\\areas\\"+area.name+
                                                  "\\"+str(i)+".gif"))
            except TclError:
                break
        loadProgress += 80./len(main.areas)
        root.update()
    
    root.after(1, makeWindow)


main = Main()

WINDOW_WIDTH = 822
WINDOW_HEIGHT = 642
FRAME_C_WIDTH = 233
FRAME_C_HEIGHT = 426

NUMBER_OF_BARS = 46

BEIGE = "#ebdec0"
DARKBEIGE = "#d1c29d"
BROWN = "#704F16"
LIGHTBEIGE = "#f4ead2"
RED = "#90000d"
MAROON = "#510020"
CYAN = "#24828b"
BLACK = "#000000"
BLUE = "#0093DC"
GREY = "#888888"
LIGHTCYAN = "#7bb4b9"
YELLOW = "#ffcc00"
WHITE = "#ffffff"
#GREEN = "#00ff00"
#DARKGREEN = "#006400"

DEFAULT_BG = BEIGE
BUTTON_BG = DARKBEIGE
BUTTON_FG = BROWN
TEXTBOX_BG = LIGHTBEIGE
LEVEL_UP_BG = CYAN
LEVEL_UP_FG = LIGHTCYAN
MERCENARY_UP_BG = YELLOW
MERCENARY_UP_FG = BROWN
LOOT_BG = DARKBEIGE
LOOT_FG = BROWN

root = Tk()

# Initialize variables
font1 = tkFont.Font(family="Garamond", size=10)
font2 = tkFont.Font(family="Garamond", size=11)
italicFont2 = tkFont.Font(family="Garamond", size=11, slant="italic", weight="bold")
font3 = tkFont.Font(family="Garamond", size=12, weight="bold")
font4 = tkFont.Font(family="Garamond", size=14)
italicFont4 = tkFont.Font(family="Garamond", size=14, slant="italic")
font5 = tkFont.Font(family="Garamond", size=80, weight="bold")
font6 = tkFont.Font(family="Garamond", size=18)
font7 = tkFont.Font(family="Garamond", size=66, weight="bold")
font8 = tkFont.Font(family="Garamond", size=14, weight="bold")

welcomeImage = PhotoImage(file="images\\other\\turtle.gif")
tosheImage = PhotoImage(file="images\\other\\toshe.gif")
gameOverImage = PhotoImage(file="images\\other\\gameover.gif")

euroImage = PhotoImage(file="images\\icons\\euro.gif")
vBorderImage1 = PhotoImage(file="images\\other\\border21.gif")
vBorderImage2 = PhotoImage(file="images\\other\\border22.gif")
hBorderImage = PhotoImage(file="images\\other\\border3.gif")
waveBorderImage = PhotoImage(file="images\\other\\border1.gif")

upImage = PhotoImage(file="images\\icons\\up.gif")
leftImage = PhotoImage(file="images\\icons\\left.gif")
rightImage = PhotoImage(file="images\\icons\\right.gif")
downImage = PhotoImage(file="images\\icons\\down.gif")
inventoryImage = PhotoImage(file="images\\icons\\inventory.gif")
backImage = PhotoImage(file="images\\icons\\back.gif")
attackImage = PhotoImage(file="images\\icons\\attack.gif")
defendImage = PhotoImage(file="images\\icons\\defend.gif")
fleeImage = PhotoImage(file="images\\icons\\flee.gif")

noItemImage = PhotoImage(file="images\\other\\empty.gif")
defaultImage = PhotoImage(file="images\\other\\default.gif")

xpBars = []
hpBars = []
epBars = []
areaImages = {}
itemImages = {}
enemyImages = {}
window = None
loadProgress = 0
fullProgress = 100

xpBars.append(PhotoImage(file="images\\bars\\xpbar"+
                         str(0)+".gif"))
hpBars.append(PhotoImage(file="images\\bars\\hpbar"+
                         str(NUMBER_OF_BARS - 1)+".gif"))
epBars.append(PhotoImage(file="images\\bars\\epbar"+
                         str(NUMBER_OF_BARS - 1)+".gif"))
        
views = {'travel': enableTravelView,
         'battle': enableBattleView,
         'inventory': enableInventoryView,
         'store': enableStoreView,
         'battle over': enableBattleOverView,
         'game over': enableGameOverView}

root.iconbitmap("images\\icons\\tq.ico")
root.title("Toshe's Quest II")
root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
root.resizable(0, 0)
temporaryFrame = Label(root, bg=DEFAULT_BG, relief=SUNKEN, bd=4)
temporaryFrame.grid(ipadx=406, ipady=308)
root.after(0, displayLoadingScreen)
root.after(0, updateLoadingScreen)
root.after(0, loadAssets)
root.update()
root.mainloop()