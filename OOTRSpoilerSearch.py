import json
from pathlib import Path
from tkinter import filedialog
import requests
from tkinter import *
from tkinter import Tk, ttk


def connect():
    global spoiler
    spoiler = requests.get("https://ootrandomizer.com/spoilers/get?id={}".format(seed.get())).json()["locations"]
    seedText.config(text="ID accepted")


def itemSearch():
    result_var = []
    testlist_var = []
    temp_list = []
    string = ""
    if typeBox.get() == "Item":
        itemSpoiler = {}
        for k,v in spoiler.items():
            try:
                itemSpoiler[v] = itemSpoiler.get(v, []) + [k]
            except TypeError:
                itemSpoiler[v['item']] = itemSpoiler.get(v['item'], []) + [k]
                #print(f"{k} : {v['item']}")
                #pass
        for i in itemSpoiler:
            if searchName.get().lower() in i.lower():
                result_var.append(itemSpoiler[i])
        for i in result_var:
            for item in i:
                testlist_var.append(item)
                temp_list.append(item)
                string += f"\n{item}"

    elif typeBox.get() == "Location":
        for i in spoiler:
            if searchName.get().lower() in i.lower():
                try:
                    testlist_var.append(spoiler[i]['item'])
                    result_var.append(spoiler[i]['item'])
                except:
                    testlist_var.append(spoiler[i])
                    result_var.append(spoiler[i])
        for item in result_var:
            temp_list.append(item)
            string += f"\n{item}"
    testlist.set(testlist_var)


def closeProgram():
    root.destroy()


def saveFile():
    try:
        filename = Path(filedialog.asksaveasfilename(filetypes=[("JSON file","*.json")],defaultextension=".json", initialfile=seed.get()))
        spoilerReplaced = str(spoiler).replace("{'", "{\"").replace("'}", "\"}").replace(" '", " \"").replace("':", "\":").replace("',", "\",")
        filename.write_bytes(bytes(spoilerReplaced, encoding='utf-8'))
    except NameError:
        pass
    

def openFile():
    global spoiler
    openedFile = filedialog.askopenfile()
    try:
        spoiler = dict(json.load(openedFile))["locations"]
    except KeyError:
        with open(openedFile.name) as spoilerTemp:
            spoiler = json.load(spoilerTemp)

    seedText.config(text="File opened")
    openedFile.close


root = Tk()
root.geometry("295x372")
root.resizable(FALSE, FALSE)
root.title("Spoiler Search")
seed = StringVar()
searchType = StringVar(value="Item")
searchName = StringVar()
testlist=StringVar()
padding_left = 10
root.option_add("*tearOff", FALSE)
menubar = Menu(root)
root["menu"] = menubar
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label="File")
menu_file.add_command(label="Open...", command=openFile)
menu_file.add_command(label="Save As...", command=saveFile)
menu_file.add_separator()
menu_file.add_command(label="Close", command=closeProgram)
seedLabel = ttk.Entry(root, textvariable=seed)
seedLabel.grid(row=0, column=0, padx=[padding_left,0],pady=[5,0], sticky=W+E)
seedBtn = ttk.Button(root, text="Enter ID", command=connect)
seedBtn.grid(row=0, column=1, padx=[10,5], pady=[5,0])
seedText = ttk.Label(root, text="No ID entered")
seedText.grid(row=1, column=1, padx=[10,5], pady=[5,0])
typeBox = ttk.Combobox(root, values=["Item", "Location"],textvariable=searchType, state="readonly")
typeBox.grid(row=2, column=0, padx=[padding_left,0], sticky=E+W)
searchEntry = ttk.Entry(root, textvariable=searchName)
searchEntry.grid(row=3, column=0, padx=[padding_left,0], pady=[5,0], sticky=W+E)
searchButton = ttk.Button(root, text="Search", command=itemSearch)
searchButton.grid(row=3, column=1, padx=[10,5], pady=[5,0])
resultList = Listbox(root, listvariable=testlist, height= 15, width=45)
resultList.grid(row=4, column=0, columnspan=3, padx=padding_left, pady=15, sticky=N+E+W+S)
root.mainloop()