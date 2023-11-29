from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os.path


def pointcalculation(itemsdict, ratingdict, necessitydict):
    itempoint = {}
    choice = open("radiobutton", "r").read()
    if choice == "1":
        for name, price in itemsdict.items():
            point = len(itemsdict)
            for k, v in itemsdict.items():
                if float(price) > float(v):
                    point -= 1
            point *= 3
            itempoint.update({name: point})
        for name, pricepoint in itempoint.items():
            for item, necessity in necessitydict.items():
                point = len(itemsdict)
                for k, v in necessitydict.items():
                    if float(necessity) < float(v):
                        point -= 1
                point *= 2
                if item == name:
                    pricepoint += point
                    itempoint.update({name: pricepoint})
            for itemname, rating in ratingdict.items():
                point = len(itemsdict)
                for k, v in ratingdict.items():
                    if float(rating) < float(v):
                        point -= 1
                if itemname == name:
                    pricepoint += point
                    itempoint.update({name: pricepoint})
    elif choice == "2":
        for name, price in itemsdict.items():
            point = len(itemsdict)
            for k, v in itemsdict.items():
                if float(price) > float(v):
                    point -= 1
            itempoint.update({name: point})
        for name, pricepoint in itempoint.items():
            for item, necessity in necessitydict.items():
                point = len(itemsdict)
                for k, v in necessitydict.items():
                    if float(necessity) < float(v):
                        point -= 1
                point *= 2
                if item == name:
                    pricepoint += point
                    itempoint.update({name: pricepoint})
            for itemname, rating in ratingdict.items():
                point = len(itemsdict)
                for k, v in ratingdict.items():
                    if float(rating) < float(v):
                        point -= 1
                point *= 3
                if itemname == name:
                    pricepoint += point
                    itempoint.update({name: pricepoint})
    return itempoint


class PriceComparisonCalculator(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Price Comparison Calculator")
        self.geometry("400x600")
        self.config(bg="#F5F5F5")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(600, weight=1)
        self.menu = Menu(self)
        self.menuOperation = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="option", menu=self.menuOperation)
        self.menuOperation.add_command(label="Save as", command=self.saveAs)
        self.menuOperation.add_command(label="Load", command=self.load)
        self.menuOperation.add_command(label="Preference setting", command=self.preferencesetting)
        self.config(menu=self.menu)
        self.listbox = Listbox(self)
        self.listbox.grid(row=3, column=0, columnspan=2, rowspan=599, sticky="NSEW", padx=10, pady=5)
        self.listbox.bind('<Double-1>', self.edit)
        self.listscrollbar = Scrollbar(self.listbox, orient="vertical")
        self.listscrollbar.pack(side=RIGHT, fill=Y)
        self.addItemBT = Button(self, width=5, height=2, text="+", font=("Arial", 10), command=self.additem)
        self.addItemBT.grid(row=1, column=400, sticky="E", padx=10, pady=10)
        self.clearItemBT = Button(self, width=5, height=2, text="clear", font=("Arial", 10), command=self.clear)
        self.clearItemBT.grid(row=2, column=400, sticky="E", padx=10, pady=10)
        self.calcBy = ["Price only", "Piece", "Weight", "Volume"]
        self.selection = StringVar()
        self.selection.set("Calculate by...")
        self.HowToCalc = OptionMenu(self, self.selection, *self.calcBy)
        self.HowToCalc.grid(row=1, column=0, sticky="WS", padx=10)
        self.text = Label(self, text="List of items:", font=("Arial", 10))
        self.text.grid(row=1, column=0, sticky="WN", padx=10, pady=10)
        self.execute = Button(self, width=7, height=3, text="Execute", font=("Arial", 10), command=self.calculate)
        self.execute.grid(row=600, column=400, sticky="SE", padx=10, pady=10)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.writefirstpref = open("radiobutton", "w")
        self.writefirstpref.write("1")
        self.writefirstpref.close()
        self.preference = StringVar()
        self.prefdisplay()
        self.preferencedisplay = Label(self, textvariable=self.preference, font=("Arial", 10), fg="red")
        self.preferencedisplay.grid(row=2, column=0, sticky="WNS", padx=10, pady=5)

    def prefdisplay(self):
        file = open("radiobutton", "r")
        pref = file.read()
        if pref == "1":
            self.preference.set("Price is being prioritised")
        elif pref == "2":
            self.preference.set("Quality is being prioritised")

    def additem(self):
        Add(root, self)

    def edit(self, event):
        EditInfo(root, self)

    def quit(self):
        if os.path.isfile("radiobutton"):
            os.remove("radiobutton")
        if os.path.isfile("itemdetail"):
            os.remove("itemdetail")
        self.master.destroy()

    def preferencesetting(self):
        Preference(root, self)

    def calculate(self):
        try:
            file = open("itemdetail", "r")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Please enter some items")
            return None
        if self.selection.get() == "Calculate by...":
            messagebox.showwarning("Warning", "Please choose a method of calculation")
        elif self.selection.get() == "Price only":
            itemAndPrice = {}
            rating = {}
            necessity = {}
            lines = file.readlines()
            for line in range(len(lines)):
                if ("weight:" in lines[line]) or ("volume:" in lines[line]) or ("piece per container:" in lines[line]):
                    k, v = lines[line].split(": ")
                    if v != "\n":
                        messagebox.showwarning("Warning",
                                               "The list contain item(s) with properties not matching the calculation method")
                        return None
                elif "item name" in lines[line]:
                    k1, v1 = lines[line].split(": ")
                    k2, v2 = lines[line + 1].split(": ")
                    k3, v3 = lines[line + 4].split(": ")
                    k4, v4 = lines[line + 2].split(": ")
                    k5, v5 = lines[line + 3].split(": ")
                    key = f"{v1.strip()}({v2.strip()})"
                    value1 = v3.strip()
                    value2 = v4.strip()
                    value3 = v5.strip()
                    itemAndPrice.update({key: value1})
                    rating.update({key: value3})
                    necessity.update({key: value2})
            self.point = pointcalculation(itemAndPrice, rating, necessity)
            Result(root, self)

        elif self.selection.get() == "Piece":
            itemAndPrice = {}
            rating = {}
            necessity = {}
            lines = file.readlines()
            for line in range(len(lines)):
                if "item name" in lines[line]:
                    k1, v1 = lines[line].split(": ")
                    k2, v2 = lines[line + 1].split(": ")
                    k3, v3 = lines[line + 4].split(": ")
                    k4, v4 = lines[line + 2].split(": ")
                    k5, v5 = lines[line + 3].split(": ")
                    k6, v6 = lines[line + 6].split(": ")
                    key = f"{v1.strip()}({v2.strip()})"
                    try:
                        value1 = float(v3.strip()) / float(v6.strip())
                    except ValueError:
                        messagebox.showwarning("Warning",
                                               "The list contain item(s) with properties not matching the calculation method")
                        return None
                    value2 = v4.strip()
                    value3 = v5.strip()
                    itemAndPrice.update({key: value1})
                    rating.update({key: value3})
                    necessity.update({key: value2})
            self.point = pointcalculation(itemAndPrice, rating, necessity)
            Result(root, self)

        elif self.selection.get() == "Weight":
            itemAndPrice = {}
            rating = {}
            necessity = {}
            lines = file.readlines()
            for line in range(len(lines)):
                if "item name" in lines[line]:
                    k1, v1 = lines[line].split(": ")
                    k2, v2 = lines[line + 1].split(": ")
                    k3, v3 = lines[line + 4].split(": ")
                    k4, v4 = lines[line + 2].split(": ")
                    k5, v5 = lines[line + 3].split(": ")
                    k6, v6 = lines[line + 5].split(": ")
                    key = f"{v1.strip()}({v2.strip()})"
                    try:
                        value1 = float(v3.strip()) / float(v6.strip())
                    except ValueError:
                        messagebox.showwarning("Warning",
                                               "The list contain item(s) with properties not matching the calculation method")
                        return None
                    value2 = v4.strip()
                    value3 = v5.strip()
                    itemAndPrice.update({key: value1})
                    rating.update({key: value3})
                    necessity.update({key: value2})
            self.point = pointcalculation(itemAndPrice, rating, necessity)
            Result(root, self)
        elif self.selection.get() == "Volume":
            itemAndPrice = {}
            rating = {}
            necessity = {}
            lines = file.readlines()
            for line in range(len(lines)):
                if "item name" in lines[line]:
                    k1, v1 = lines[line].split(": ")
                    k2, v2 = lines[line + 1].split(": ")
                    k3, v3 = lines[line + 4].split(": ")
                    k4, v4 = lines[line + 2].split(": ")
                    k5, v5 = lines[line + 3].split(": ")
                    k6, v6 = lines[line + 7].split(": ")
                    key = f"{v1.strip()}({v2.strip()})"
                    try:
                        value1 = float(v3.strip()) / float(v6.strip())
                    except ValueError:
                        messagebox.showwarning("Warning",
                                               "The list contain item(s) with properties not matching the calculation method")
                        return None
                    value2 = v4.strip()
                    value3 = v5.strip()
                    itemAndPrice.update({key: value1})
                    rating.update({key: value3})
                    necessity.update({key: value2})
            self.point = pointcalculation(itemAndPrice, rating, necessity)
            Result(root, self)

    def clear(self):
        self.listbox.delete(0, "end")
        if os.path.isfile("itemdetail"):
            os.remove("itemdetail")

    def saveAs(self):
        path = filedialog.asksaveasfilename()
        fileToSave = open("itemdetail", "r")
        infoToSave = fileToSave.read()
        saveas = open(path, "w")
        saveas.write(infoToSave)
        saveas.close()

    def load(self):
        path = filedialog.askopenfilename()
        try:
            fileToLoad = open(path, "r")
        except FileNotFoundError:
            return None
        self.listbox.delete(0, "end")
        infoToLoad = fileToLoad.read()
        load = open("itemdetail", "w")
        load.write(infoToLoad)
        load.close()
        listload = open("itemdetail", "r")
        lines = listload.readlines()
        for line in range(len(lines) - 1):
            if "item name:" in lines[line]:
                self.listbox.insert(END, f"{(lines[line]).strip()},  {(lines[line + 1]).strip()}")
        listload.close()


class Add(Toplevel):
    def __init__(self, master, other):
        Toplevel.__init__(self, master)
        self.title("Add Item")
        self.geometry("700x400")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(450, weight=1)
        self.other = other
        self.name = StringVar()
        self.storename = StringVar()
        self.priceinbaht = StringVar()
        self.weight = StringVar()
        self.volume = StringVar()
        self.rating = StringVar()
        self.score = StringVar()
        self.pieceperbox = StringVar()
        self.itemNameLabel = Label(self, text="Item Name:")
        self.itemNameLabel.grid(row=1, column=0, sticky="W", padx=10)
        self.itemName = Entry(self, textvariable=self.name, fg="red")
        self.itemName.insert(0, "*require")
        self.itemName.grid(row=1, column=1, columnspan=700, sticky="EW", pady=10, padx=10)
        self.itemName.bind("<FocusOut>", self.addrequireitemname)
        self.itemName.bind("<FocusIn>", self.removerequireitemname)
        self.itemStoreLabel = Label(self, text="Brand Name:")
        self.itemStoreLabel.grid(row=2, column=0, sticky="W", padx=10, pady=10)
        self.store = Entry(self, textvariable=self.storename, fg="red")
        self.store.insert(0, "*require")
        self.store.grid(row=2, column=1, columnspan=700, sticky="EW", padx=10)
        self.store.bind("<FocusOut>", self.addrequirestorename)
        self.store.bind("<FocusIn>", self.removerequirestorename)
        self.itemPriceLabel = Label(self, text="Price(in Baht):")
        self.itemPriceLabel.grid(row=3, column=0, sticky="W", padx=10, pady=10)
        self.price = Entry(self, textvariable=self.priceinbaht, fg="red")
        self.price.insert(0, "*require")
        self.price.grid(row=3, column=1, columnspan=700, sticky="EW", padx=10)
        self.price.bind("<FocusOut>", self.addrequireitemprice)
        self.price.bind("<FocusIn>", self.removerequireitemprice)
        self.scoreLabel = Label(self, text="Item's necessity score (Out of 5): ")
        self.scoreLabel.grid(row=4, column=0, sticky="W", padx=10, pady=10)
        self.itemScore = Entry(self, textvariable=self.score, fg="red")
        self.itemScore.insert(0, "*require")
        self.itemScore.grid(row=4, column=1, columnspan=700, sticky="EW", padx=10)
        self.itemScore.bind("<FocusOut>", self.addrequireitemScore)
        self.itemScore.bind("<FocusIn>", self.removerequireitemScore)
        self.storeRatingLabel = Label(self, text="Item's rating (Out of 5): ")
        self.storeRatingLabel.grid(row=5, column=0, sticky="W", padx=10, pady=10)
        self.storeRating = Entry(self, textvariable=self.rating, fg="red")
        self.storeRating.insert(0, "*require (Can be opinion-based or online rating-based)")
        self.storeRating.grid(row=5, column=1, columnspan=700, sticky="EW", padx=10)
        self.storeRating.bind("<FocusOut>", self.addrequireitemRating)
        self.storeRating.bind("<FocusIn>", self.removerequireitemRating)
        self.itemPieceperConLabel = Label(self, text="Number of pieces per container:")
        self.itemPieceperConLabel.grid(row=7, column=0, sticky="W", padx=10, pady=10)
        self.itemPieceperCon = Entry(self, textvariable=self.pieceperbox)
        self.itemPieceperCon.grid(row=7, column=1, columnspan=700, sticky="EW", padx=10)
        self.itemWeightLabel = Label(self, text="Weight(in grams):")
        self.itemWeightLabel.grid(row=8, column=0, sticky="W", padx=10, pady=10)
        self.itemWeight = Entry(self, textvariable=self.weight)
        self.itemWeight.grid(row=8, column=1, columnspan=700, sticky="EW", padx=10)
        self.itemVolumeLabel = Label(self, text="Volume (in milliliter):")
        self.itemVolumeLabel.grid(row=9, column=0, sticky="W", padx=10, pady=10)
        self.itemVolume = Entry(self, textvariable=self.volume)
        self.itemVolume.grid(row=9, column=1, columnspan=700, sticky="EW", padx=10)
        self.warning = Label(self,
                             text="For weight, volume, or number of pieces per container: \nPlease fill in at most 'ONE' field.",
                             fg="red")
        self.warning.grid(row=450, column=0, sticky="W", pady=10, padx=10)
        self.add = Button(self, width=7, height=2, text="add", font=("Arial", 10), command=self.appenditemtolist)
        self.add.grid(row=450, column=2, sticky="E", pady=10, padx=10)

    def appenditemtolist(self):
        if self.name.get() != "*require" and self.priceinbaht.get() != "*require" and self.score.get() != "*require" and self.storename.get() != "*require" and self.rating.get() != "*require (Can be opinion-based or online rating-based)":
            if (self.weight.get() != "" and self.volume.get() != "") or (
                    self.weight.get() != "" and self.pieceperbox.get() != "") or (
                    self.volume.get() != "" and self.pieceperbox.get() != "") or (
                    self.weight.get() != "" and self.pieceperbox.get() != "" and self.volume.get() != ""):
                messagebox.showwarning("Warning",
                                       "Only one field of Weight, Volume, or Number of pieces per container should be filled")
            else:
                x = self.validity()
                if x == None:
                    return None
                self.other.listbox.insert(END, f"item name: {self.name.get()},  brand: {self.storename.get()}")
                itemdic = {"item name": self.name.get(), "brand": self.storename.get(), "score": self.score.get(),
                           "rating": self.rating.get(), "price": self.priceinbaht.get(), "weight": self.weight.get(),
                           "piece per container": self.pieceperbox.get(), "volume": self.volume.get()}
                try:
                    writeitemdetail = open("itemdetail", "a")
                except FileNotFoundError:
                    writeitemdetail = open("itemdetail", "w")
                    writeitemdetail.close()
                    writeitemdetail = open("itemdetail", "a")
                for key, value in itemdic.items():
                    writeitemdetail.write(f"{key}: {value}\n")
                writeitemdetail.write("\n")
                writeitemdetail.close()
                self.destroy()
        else:
            messagebox.showwarning("Warning", "Required fields not fill")

    def validity(self):
        try:
            float(self.priceinbaht.get())
            float(self.score.get())
            float(self.rating.get())
        except ValueError:
            messagebox.showwarning("Warning",
                                   "Invalid information entered\nHint: Entries other than names and brands should be in decimals or integers.")
            return None
        if float(self.score.get()) < 0 or float(self.score.get()) > 5:
            messagebox.showwarning("Warning", "Please enter a valid necessity score")
            return None
        if float(self.rating.get()) < 0 or float(self.rating.get()) > 5:
            messagebox.showwarning("Warning", "Please enter a valid rating")
            return None
        if self.pieceperbox.get() != "":
            try:
                float(self.pieceperbox.get())
            except ValueError:
                messagebox.showwarning("Warning",
                                       "Invalid information entered\nHint: Entries other than names and brands should be in decimals or integers.")
                return None
        if self.weight.get() != "":
            try:
                float(self.weight.get())
            except ValueError:
                messagebox.showwarning("Warning",
                                       "Invalid information entered\nHint: Entries other than names and brands should be in decimals or integers.")
                return None
        if self.volume.get() != "":
            try:
                float(self.volume.get())
            except ValueError:
                messagebox.showwarning("Warning",
                                       "Invalid information entered\nHint: Entries other than names and brands should be in decimals or integers.")
                return None
        return 1

    def removerequireitemname(self, event):
        if self.name.get() == "*require":
            self.itemName.delete(0, "end")
            self.itemName.config(fg="black")

    def addrequireitemname(self, event):
        if self.name.get() == "":
            self.itemName.insert(0, "*require")
            self.itemName.config(fg="red")

    def removerequirestorename(self, event):
        if self.storename.get() == "*require":
            self.store.delete(0, "end")
            self.store.config(fg="black")

    def addrequirestorename(self, event):
        if self.storename.get() == "":
            self.store.insert(0, "*require")
            self.store.config(fg="red")

    def removerequireitemprice(self, event):
        if self.priceinbaht.get() == "*require":
            self.price.delete(0, "end")
            self.price.config(fg="black")

    def addrequireitemprice(self, event):
        if self.priceinbaht.get() == "":
            self.price.insert(0, "*require")
            self.price.config(fg="red")

    def removerequireitemScore(self, event):
        if self.score.get() == "*require":
            self.itemScore.delete(0, "end")
            self.itemScore.config(fg="black")

    def addrequireitemScore(self, event):
        if self.score.get() == "":
            self.itemScore.insert(0, "*require")
            self.itemScore.config(fg="red")

    def removerequireitemRating(self, event):
        if self.rating.get() == "*require (Can be opinion-based or online rating-based)":
            self.storeRating.delete(0, "end")
            self.storeRating.config(fg="black")

    def addrequireitemRating(self, event):
        if self.rating.get() == "":
            self.storeRating.insert(0, "*require (Can be opinion-based or online rating-based)")
            self.storeRating.config(fg="red")


class Preference(Toplevel):
    def __init__(self, master, other):
        Toplevel.__init__(self, master)
        self.title("Preference setting")
        self.geometry("300x150")
        self.other = other
        self.var = IntVar()
        readpref = open("radiobutton", "r")
        value = readpref.read()
        self.var.set(int(value))
        self.R1 = Radiobutton(self, text="Prioritize the Price", variable=self.var, value=1)
        self.R1.pack(pady=10)
        self.R2 = Radiobutton(self, text="Prioritize the Quality", variable=self.var, value=2)
        self.R2.pack(pady=10)
        self.prefButton = Button(self, width=5, height=2, text="Apply", font=("Arial", 10), command=self.prefChoice)
        self.prefButton.pack(side=RIGHT, padx=10, pady=10)

    def prefChoice(self):
        if self.var.get() == 1:
            writefirstpref = open("radiobutton", "w")
            writefirstpref.write("1")
            writefirstpref.close()
            self.other.preference.set("Price is being prioritised")
        elif self.var.get() == 2:
            writefirstpref = open("radiobutton", "w")
            writefirstpref.write("2")
            writefirstpref.close()
            self.other.preference.set("Quality is being prioritised")
        self.destroy()


class EditInfo(Add):
    def __init__(self, master, other):
        super().__init__(master, other)
        self.title("Edit Item")
        self.other = other
        self.itemdict = self.readlines()
        self.itemName.delete(0, "end")
        self.itemName.config(fg="black")
        self.itemName.insert(0, self.itemdict.get("item name"))
        self.store.delete(0, "end")
        self.store.config(fg="black")
        self.store.insert(0, self.itemdict.get("brand"))
        self.price.delete(0, "end")
        self.price.config(fg="black")
        self.price.insert(0, self.itemdict.get("price"))
        self.itemScore.delete(0, "end")
        self.itemScore.config(fg="black")
        self.itemScore.insert(0, self.itemdict.get("score"))
        self.storeRating.delete(0, "end")
        self.storeRating.config(fg="black")
        self.storeRating.insert(0, self.itemdict.get("rating"))
        self.itemPieceperCon.config(fg="black")
        self.itemPieceperCon.insert(0, self.itemdict.get("piece per container"))
        self.itemWeight.config(fg="black")
        self.itemWeight.insert(0, self.itemdict.get("weight"))
        self.itemVolume.config(fg="black")
        self.itemVolume.insert(0, self.itemdict.get("volume"))
        self.delete = Button(self, width=7, height=2, text="delete", font=("Arial", 10), command=self.delete)
        self.delete.grid(row=400, column=1, sticky="E", pady=10)
        self.update = Button(self, width=7, height=2, text="update", font=("Arial", 10), command=self.appenditemtolist)
        self.update.grid(row=400, column=2, sticky="E", pady=10, padx=10)

    def readlines(self):
        theitemdic = {}
        name, brand = self.other.listbox.get(self.other.listbox.curselection()).split(",  ")
        title1, select1 = name.split(": ")
        title2, select2 = brand.split(": ")
        file = open("itemdetail", "r")
        lines = file.readlines()
        count = 0
        for line in range(len(lines) - 1):
            if lines[line] != "":
                try:
                    k, v = lines[line].strip().split(": ")
                    k2, v2 = lines[line + 1].strip().split(": ")
                except ValueError:
                    v = ""
                    v2 = ""
                if v == select1 and v2 == select2:
                    for i in range(count, count + 8):
                        try:
                            key, value = lines[i].strip().split(": ")
                        except ValueError:
                            key = lines[i][0:len(lines[i]) - 3]
                            value = ""
                        theitemdic.update({key: value})
                    break
            count += 1
        return theitemdic

    def appenditemtolist(self):
        if self.name.get() != "*require" and self.priceinbaht.get() != "*require" and self.score.get() != "*require" and self.storename.get() != "*require" and self.rating.get() != "*require (Can be opinion-based or online rating-based)":
            if (self.weight.get() != "" and self.volume.get() != "") or (
                    self.weight.get() != "" and self.pieceperbox.get() != "") or (
                    self.volume.get() != "" and self.pieceperbox.get() != "") or (
                    self.weight.get() != "" and self.pieceperbox.get() != "" and self.volume.get() != ""):
                messagebox.showwarning("Warning",
                                       "Only one field of Weight, Volume, or Number of pieces per container should be filled")
            else:
                x = self.validity()
                if x == None:
                    return None
                indexneeded = self.other.listbox.get(0, END).index(
                    f"item name: {self.itemdict.get('item name')},  brand: {self.itemdict.get('brand')}")
                self.other.listbox.delete(indexneeded)
                self.other.listbox.insert(indexneeded, f"item name: {self.name.get()},  brand: {self.storename.get()}")
                newitemdic = {"item name": self.name.get(), "brand": self.storename.get(), "score": self.score.get(),
                              "rating": self.rating.get(), "price": self.priceinbaht.get(), "weight": self.weight.get(),
                              "piece per container": self.pieceperbox.get(), "volume": self.volume.get()}
                key = ["item name", "brand", "score", "rating", "price", "weight", "piece per container", "volume"]
                count = 0
                indexcount = 0
                file = open("itemdetail", "r")
                lines = file.readlines()
                writeitemdetail = open("itemdetail", "w")
                while count != len(lines):
                    if lines[count] == f"item name: {self.itemdict.get('item name')}\n" and lines[
                        count + 1] == f"brand: {self.itemdict.get('brand')}\n":
                        count += 8
                        for i in range(8):
                            writeitemdetail.write(f"{key[indexcount]}: {newitemdic.get(key[indexcount])}\n")
                            indexcount += 1
                    else:
                        writeitemdetail.write(lines[count])
                        count += 1
                writeitemdetail.close()
                self.destroy()
        else:
            messagebox.showwarning("Warning", "Required fields not fill")

    def delete(self):
        indextodelete = self.other.listbox.get(0, END).index(
            f"item name: {self.itemdict.get('item name')},  brand: {self.itemdict.get('brand')}")
        self.other.listbox.delete(indextodelete)
        file = open("itemdetail", "r")
        lines = file.readlines()
        writefile = open("itemdetail", "w")
        count = 0
        while count != (len(lines) - 1):
            if lines[count] == f"item name: {self.itemdict.get('item name')}\n" and lines[
                count + 1] == f"brand: {self.itemdict.get('brand')}\n":
                count += 8
            else:
                writefile.write(lines[count])
                count += 1
        writefile.close()
        self.destroy()


class Result(Toplevel):
    def __init__(self, master, other):
        Toplevel.__init__(self, master)
        self.title("Result")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.other = other
        self.point = self.other.point
        self.topresult = StringVar()
        self.displayingpointtop()
        self.runnerup = self.displaypointrunnerup()
        self.otherframe = Frame(self)
        self.otherframe.grid(row=2, column=0, columnspan=200, rowspan=100, sticky="NSWE", padx=10, pady=10)
        self.otherframe.grid_columnconfigure(0, weight=1)
        self.otherframe.grid_rowconfigure(0, weight=1)
        self.otherplace = Text(self.otherframe, font=("Arial", 15), fg="#4A4A4A")
        self.otherplace.insert(END, self.runnerup)
        self.otherplace.config(state=DISABLED)
        self.otherplace.grid(row=0, column=0, rowspan=100, sticky="NWSE", padx=5, pady=5)
        self.frame = LabelFrame(self, bg="white")
        self.frame.grid(row=0, column=0, columnspan=200, rowspan=2, sticky="ENW", padx=10)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(300, weight=1)
        self.mostrecommendedLabel = Label(self.frame, text="1st place recommendation: ", font=("Arial", 18), bg="white")
        self.mostrecommendedLabel.grid(row=0, column=0, columnspan=200, sticky="NEW", pady=5)
        self.mostrecommended = Label(self.frame, textvariable=self.topresult, font=("Arial", 18), fg="red", bg="white")
        self.mostrecommended.grid(row=1, column=0, columnspan=200, sticky="NEW")
        self.scrollbar = Scrollbar(self.otherframe, orient="vertical")
        self.scrollbar.grid(row=0, column=300, sticky="NS")
        self.otherplace.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.otherplace.yview)

    def displayingpointtop(self):
        self.pointlist = []
        for k, v in self.point.items():
            self.pointlist.append(v)
        self.pointlist.sort()
        text = ""
        items = list(self.point.items())
        for item in range(len(items) - 1, -1, -1):
            if items[item][1] == self.pointlist[-1]:
                text += f"{items[item][0]}, "
                self.point.pop(items[item][0])
            if item == 0:
                text= text[:len(text) - 2]
                self.topresult.set(text)

    def displaypointrunnerup(self):
        rank = 1
        text = ""
        for i in range(2, len(self.pointlist) + 1):
            for name, value in self.point.items():
                if value == self.pointlist[len(self.pointlist) - i]:
                    if value == self.pointlist[len(self.pointlist) - (i - 1)]:
                        text += f"Rank {rank}: {name}\n"
                        continue
                    else:
                        rank += 1
                        text += f"Rank {rank}: {name}\n"
        return text


root = Tk()
root.withdraw()

PriceComparisonCalculator(root)
root.mainloop()
