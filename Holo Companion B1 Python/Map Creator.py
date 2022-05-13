import time
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image,ImageTk
import math
from os.path import exists
import json



#Startup Window
root = Tk()
root.title("Startup")
root.resizable(False, False)

map = None
mapname = ""

def on_closing():
    try:
        driver.close()
    finally:
        root.destroy()
        exit()
root.protocol("WM_DELETE_WINDOW", on_closing)

fileentryframe = Frame(root, bd=1, relief="groove")
fileentryframe.grid(column=0, row=0, sticky="EW")
newmapframe = Frame(root, bd=1, relief="groove")
newmapframe.grid(column=0, row=1, sticky="EW")

def FILEENTRYCMD():
    input = fileentry.get()
    if exists(input):
        global map, mapname, events
        mapfile = open(input, "r")
        mapdata = json.loads(mapfile.read())
        events = mapdata[0]
        map = mapdata[1]
        mapfile.close()
        mapname = input.replace(".map","")
        root.destroy()
    else:
        messagebox.showinfo(message='File not found. Write name like "example.map" or input file path.')

def NEWMAPCMD():
    if newmapwentry.get() != "" and newmaphentry.get() != "":
        if int(newmapwentry.get()) != 0 and int(newmaphentry.get()) != 0:
            global map, events
            x = int(newmapwentry.get())
            y = int(newmaphentry.get())
            map = []
            mapstructure = []
            for _ in range(y):
                tlist = []
                for _ in range(x):
                    defaultentry = {"name":"","travel":[],"description":"","events":["",0,"O","M"],"icon":"icons/ico_map_0.png"}
                    tlist.append(defaultentry)
                map.append(tlist)
            events = {"origin":[0,0]}
            root.destroy()


def validate(P):
    if len(P) == 0:
        return True
    elif int(P) <= 25 and P.isdigit() and len(P) <= 2:
        return True
    else:
        return False
vcmd = (root.register(validate), '%P')


fileentrylabel = Label(fileentryframe, text="Map File Path: ")
fileentrylabel.grid(row=0,column=0)
fileentry = Entry(fileentryframe, width = 50)
fileentry.grid(row=0,column=1,columnspan=2)
fielentrybutton = Button(fileentryframe, text = "Load Map",command=FILEENTRYCMD)
fielentrybutton.grid(row=0,column=4)

newmaphlabel = Label(newmapframe, text="Create New Map:   H:")
newmaphlabel.grid(row=1,column=0)
newmaphentry = Entry(newmapframe, width = 3,validate="key", validatecommand=vcmd)
newmaphentry.grid(row=1,column=1,sticky="W")
newmapwlabel = Label(newmapframe, text="x W:")
newmapwlabel.grid(row=1,column=2,sticky="W")
newmapwentry = Entry(newmapframe, width = 3,validate="key", validatecommand=vcmd)
newmapwentry.grid(row=1,column=3,sticky="W")
fielentrybutton = Button(newmapframe, text = "Create New Map",command=NEWMAPCMD)
fielentrybutton.grid(row=1,column=4)

root.mainloop()











#Map Creator
root = Tk()
root.title("Holo Map Creator")
root.resizable(False, False)
window_scale = 400
cframe_height = math.ceil(window_scale/8)

def on_close():
    response=messagebox.askyesno('Exit','Are you sure you want to exit? Unsaved changes will be lost.')
    if response:
        root.destroy()
root.protocol('WM_DELETE_WINDOW',on_close)

mapframe = Frame(root, height=window_scale, width=window_scale)
mapframe.grid(column=0, row=0)
controlframe = Frame(root, height=cframe_height)
controlframe.grid(column=0, row=1)
setframe = Frame(root,height=window_scale+cframe_height,width=window_scale)
setframe.grid(column=1, row=0)

def SHOWERROR(errormessage):
    messagebox.showerror("Error", errormessage)
    root.destroy
    try:
        driver.close()
    finally:
        exit()



#events = {"origin":[1,1,"You start your journey on Square1."],"E1":"Event 1 has occurred! You are stopped before you can travel.","E2":"Event 2 has occurred! Although it has you continue your journey."}

current_position = [0,0]
mapx = len(map[0])
mapy = len(map)
tile = []
if mapx >= mapy:
    canvas_size = window_scale / mapx
else:
    canvas_size = window_scale / mapy

for x in range(mapx):
    tlist = []
    img = []
    for y in range(mapy):
        tlist.append(Canvas(mapframe, width=canvas_size, height=canvas_size, bd=0, highlightthickness=0))
        tlist[y].grid(column=x, row=y,sticky="NSEW")
    tile.append(tlist)
temp = []
l = []
img = []
def RENDERMAP():
    global map,current_position,tile,currenttile, temp, l, img
    img = []
    for x in range(mapy):
        temp = []
        for y in range(mapx):
            temp.append(ImageTk.PhotoImage(Image.open(map[x][y]["icon"]).resize((int(canvas_size), int(canvas_size)))))
        img.append(temp)
    larrow = ImageTk.PhotoImage(Image.open("icons/ico_left.png").resize((int(canvas_size), int(canvas_size))))
    rarrow = ImageTk.PhotoImage(Image.open("icons/ico_right.png").resize((int(canvas_size), int(canvas_size))))
    uarrow = ImageTk.PhotoImage(Image.open("icons/ico_up.png").resize((int(canvas_size), int(canvas_size))))
    darrow = ImageTk.PhotoImage(Image.open("icons/ico_down.png").resize((int(canvas_size), int(canvas_size))))
    l.append(larrow)
    l.append(rarrow)
    l.append(uarrow)
    l.append(darrow)
    for x in range(mapy):
        for y in range(mapx):
            tile[y][x].create_image(0, 0, anchor=NW, image=img[x][y])
            if "W" in map[x][y]["travel"]:
                tile[y][x].create_image(0, 0, anchor=NW, image=larrow)
            if "E" in map[x][y]["travel"]:
                tile[y][x].create_image(0, 0, anchor=NW, image=rarrow)
            if "N" in map[x][y]["travel"]:
                tile[y][x].create_image(0, 0, anchor=NW, image=uarrow)
            if "S" in map[x][y]["travel"]:
                tile[y][x].create_image(0, 0, anchor=NW, image=darrow)
    currenttile = tile[current_position[0]][current_position[1]]
    imgp = ImageTk.PhotoImage(Image.open("icons/ico_player.png").resize((int(canvas_size), int(canvas_size))))
    l.append(imgp)
    currenttile.create_image(0, 0, anchor=NW, image=imgp)
RENDERMAP()

current_event = ""

def UPDATEPANEL():
    global current_event
    tilenameentry.delete(0, last=END)
    tilenameentry.insert(0,map[current_position[1]][current_position[0]]["name"])
    #Directions
    descriptiontext.delete("1.0", END)
    descriptiontext.insert("1.0",map[current_position[1]][current_position[0]]["description"])
    traveldirectionsnbutton.config(bg="white")
    if "N" in map[current_position[1]][current_position[0]]["travel"]:
        traveldirectionsnbutton.config(bg="green")
    traveldirectionsebutton.config(bg="white")
    if "E" in map[current_position[1]][current_position[0]]["travel"]:
        traveldirectionsebutton.config(bg="green")
    traveldirectionssbutton.config(bg="white")
    if "S" in map[current_position[1]][current_position[0]]["travel"]:
        traveldirectionssbutton.config(bg="green")
    traveldirectionswbutton.config(bg="white")
    if "W" in map[current_position[1]][current_position[0]]["travel"]:
        traveldirectionswbutton.config(bg="green")
    eventsnameentry.delete(0, last=END)
    eventspercententry.delete(0, last=END)
    eventsdescriptiontext.delete("1.0", END)
    if map[current_position[1]][current_position[0]]["events"][0] != "":
        eventsnameentry.insert(0, map[current_position[1]][current_position[0]]["events"][0])
        current_event = map[current_position[1]][current_position[0]]["events"][0]
        eventspercententry.insert(0, map[current_position[1]][current_position[0]]["events"][1])
        eventsrepeatablebutton.config(bg="white")
        if map[current_position[1]][current_position[0]]["events"][2] == "R":
            eventsrepeatablebutton.config(bg="green")
        eventsmovementbutton.config(bg="white")
        if map[current_position[1]][current_position[0]]["events"][3] == "D":
            eventsmovementbutton.config(bg="green")
        eventsdescriptiontext.insert("1.0", events[map[current_position[1]][current_position[0]]["events"][0]])
    iconpathentry.delete(0, last=END)
    iconpathentry.insert(0, map[current_position[1]][current_position[0]]["icon"])
    if events["origin"] == [current_position[1],current_position[0]]:
        startingtilebutton.config(bg="Green")
    else:
        startingtilebutton.config(bg="White")


#Control Keys
def MOVEUP():
    if current_position[1]-1 >= 0:
            current_position[1] = current_position[1]-1
            UPDATEPANEL()
            RENDERMAP()
def MOVEDOWN():
    if current_position[1]+1 <= mapy-1:
            current_position[1] = current_position[1]+1
            UPDATEPANEL()
            RENDERMAP()
def MOVELEFT():
    if current_position[0]-1 >= 0:
            current_position[0] = current_position[0]-1
            UPDATEPANEL()
            RENDERMAP()
def MOVERIGHT():
    if current_position[0]+1 <= mapx-1:
            current_position[0] = current_position[0]+1
            UPDATEPANEL()
            RENDERMAP()

tfont = ("Arial", math.ceil(window_scale/44))
bwidth = math.ceil(window_scale/80)
bheight = math.ceil(window_scale/200)
upkey = Button(controlframe, text = "↑", command = MOVEUP,width=bwidth,height=bheight,font=tfont)
downkey = Button(controlframe, text = "↓", command = MOVEDOWN,width=bwidth,height=bheight,font=tfont)
leftkey = Button(controlframe, text = "←", command = MOVELEFT,width=bwidth,height=bheight,font=tfont)
rightkey = Button(controlframe, text = "→", command = MOVERIGHT,width=bwidth,height=bheight,font=tfont)
upkey.grid(row=0,column=1,padx=2)
leftkey.grid(row=1,column=0,padx=2)
downkey.grid(row=1,column=1,padx=2)
rightkey.grid(row=1,column=2,padx=2)

#Adjustable settings

#Map Name
def SAVEMAP():
    response = messagebox.askyesno('Save Map','Are you sure you want to save '+str(mapnameentry.get())+'.map? Existing files of the same name will be overwritten.')
    if response:
        mapfile = open(str(mapnameentry.get())+".map", "w")
        mapfile.write(json.dumps([events,map]))
        mapfile.close()
        mapfile = open(str(mapnameentry.get())+".bak", "w")
        mapfile.write(json.dumps([events,map]))
        mapfile.close()

mapnameframe = Frame(setframe,relief="groove",bd=2)
mapnameframe.grid(column=0, row=0,sticky="EW")
mapnamelabel = Label(mapnameframe, text="Map Name: ")
mapnamelabel.grid(column=0, row=0)
mapnameentry = Entry(mapnameframe, width = 30)
mapnameentry.grid(column=1, row=0)
mapnamebutton = Button(mapnameframe, text = "Save Map",command=SAVEMAP)
mapnamebutton.grid(column=2, row=0)

#Tile Name
def CMDSETTILENAME():
    map[current_position[1]][current_position[0]]["name"] = tilenameentry.get()

tilenameframe = Frame(setframe,relief="groove",bd=2)
tilenameframe.grid(column=0, row=1,sticky="EW")
tilenamelabel = Label(tilenameframe, text="Tile Name: ")
tilenamelabel.grid(column=0, row=0)
tilenameentry = Entry(tilenameframe, width = 30)
tilenameentry.grid(column=1, row=0)
tilenamebutton = Button(tilenameframe, text = "Set", command=CMDSETTILENAME)
tilenamebutton.grid(column=2, row=0)

#Travel Directions
def CMDSETTRAVEL(direction):
        if direction in map[current_position[1]][current_position[0]]["travel"]:
            map[current_position[1]][current_position[0]]["travel"].remove(direction)
        else:
            map[current_position[1]][current_position[0]]["travel"].append(direction)
        UPDATEPANEL()
        RENDERMAP()
traveldirectionsframe = Frame(setframe,relief="groove",bd=2)
traveldirectionsframe.grid(column=0, row=2,sticky="EW")
traveldirectionslabel = Label(traveldirectionsframe, text="Travel Directions: ")
traveldirectionslabel.grid(column=0, row=0)
traveldirectionsnbutton = Button(traveldirectionsframe, text = "North",command=lambda:CMDSETTRAVEL("N"))
traveldirectionsnbutton.grid(column=1, row=0)
traveldirectionsebutton = Button(traveldirectionsframe, text = "East",command=lambda:CMDSETTRAVEL("E"))
traveldirectionsebutton.grid(column=2, row=0)
traveldirectionssbutton = Button(traveldirectionsframe, text = "South",command=lambda:CMDSETTRAVEL("S"))
traveldirectionssbutton.grid(column=3, row=0)
traveldirectionswbutton = Button(traveldirectionsframe, text = "West",command=lambda:CMDSETTRAVEL("W"))
traveldirectionswbutton.grid(column=4, row=0)

#Description
def CMDSETDESCRIPTION():
    map[current_position[1]][current_position[0]]["description"] = descriptiontext.get("1.0",END)
descriptionframe = Frame(setframe,relief="groove",bd=2)
descriptionframe.grid(column=0, row=3,sticky="EW")
descriptionlabel = Label(descriptionframe, text="Tile description: ")
descriptionlabel.grid(column=0, row=0)
descriptionlabel2 = Label(descriptionframe, text="*Will be read every time you travel over the tile.")
descriptionlabel2.grid(column=0, row=1, columnspan=4)
descriptiontext = Text(descriptionframe, width = 35,height=4)
descriptiontext.grid(column=1, row=0)
descriptionscroll = Scrollbar(descriptionframe)
descriptionscroll.grid(column=2, row=0)
descriptiontext.configure(yscrollcommand=descriptionscroll.set)
descriptionbutton = Button(descriptionframe, text = "Set", command=CMDSETDESCRIPTION)
descriptionbutton.grid(column=3, row=0)

#Events
def validate(P):
    if len(P) == 0:
        return True
    elif len(P) <= 2 and P.isdigit():
        return True
    elif len(P) == 3 and P == "100" and P.isdigit():
        return True
    else:
        return False
vcmd = (root.register(validate), '%P')

def CMDSETCLEAREVENT():
    del events[map[current_position[1]][current_position[0]]["events"][0]]
    map[current_position[1]][current_position[0]]["events"] = ["", 0, "O", "M"]
    UPDATEPANEL()

def CMDSETEVENTS():
    if eventsnameentry.get() != "":
        map[current_position[1]][current_position[0]]["events"][0] = eventsnameentry.get()
        map[current_position[1]][current_position[0]]["events"][1] = eventspercententry.get()
        events[eventsnameentry.get()] = eventsdescriptiontext.get("1.0",END).replace("\n","")

    else:
        CMDSETCLEAREVENT()

def CMDSETREPEATABLE():
        if map[current_position[1]][current_position[0]]["events"][2] == "R":
            map[current_position[1]][current_position[0]]["events"][2] = "O"
        else:
            map[current_position[1]][current_position[0]]["events"][2] = "R"
        UPDATEPANEL()
        RENDERMAP()

def CMDSETBLOCK():
    if map[current_position[1]][current_position[0]]["events"][3] == "M":
        map[current_position[1]][current_position[0]]["events"][3] = "D"
    else:
        map[current_position[1]][current_position[0]]["events"][3] = "M"
    UPDATEPANEL()
    RENDERMAP()

def validate2(P):
    if P == "origin":
        return False
    else:
        return True
vcmd2 = (root.register(validate2), '%P')

eventsframe = Frame(setframe,relief="groove",bd=2)
eventsframe.grid(column=0, row=4,sticky="EW")
eventsnamelabel = Label(eventsframe, text="Event Name:")
eventsnamelabel.grid(column=0, row=0)
eventsnameentry = Entry(eventsframe, width = 10,validate="key", validatecommand=vcmd2)
eventsnameentry.grid(column=1, row=0)
eventspercentlabel = Label(eventsframe, text="Success%:")
eventspercentlabel.grid(column=2, row=0)
eventspercententry = Entry(eventsframe, width = 3,validate="key", validatecommand=vcmd)
eventspercententry.grid(column=3, row=0)
eventssetbutton = Button(eventsframe, text = "Set",command=CMDSETEVENTS)
eventssetbutton.grid(column=4, row=0)
eventsrepeatablebutton = Button(eventsframe, text = "Repeatable",command=CMDSETREPEATABLE)
eventsrepeatablebutton.grid(column=5, row=0)
eventsmovementbutton = Button(eventsframe, text = "Blocks Movement",command=CMDSETBLOCK)
eventsmovementbutton.grid(column=6, row=0)

eventsdescriptionlabel = Label(eventsframe, text="Event Description:")
eventsdescriptionlabel.grid(column=0, row=1)
eventsdescriptiontext = Text(eventsframe, width = 35,height=2)
eventsdescriptiontext.grid(column=1, row=1, columnspan=5)
eventsclearbutton = Button(eventsframe, text = "Clear Entry",command=CMDSETCLEAREVENT)
eventsclearbutton.grid(column=6, row=1)

eventslabel2 = Label(eventsframe, text="*Currently only one random event per tile.")
eventslabel2.grid(column=0, row=2, columnspan=7)

#Icon Path
imgp2 = None

def CMDSETICONPATH():
    if exists(iconpathentry.get()):
        map[current_position[1]][current_position[0]]["icon"] = iconpathentry.get()
        RENDERMAP()
    else:
        messagebox.showinfo(message='Icon file not found.')

iconpathframe = Frame(setframe,relief="groove",bd=2)
iconpathframe.grid(column=0, row=5,sticky="EW")
iconpathlabel = Label(iconpathframe, text="Icon file path: ")
iconpathlabel.grid(column=0, row=0)
iconpathentry = Entry(iconpathframe, width = 50)
iconpathentry.grid(column=1, row=0)
iconpathbutton = Button(iconpathframe, text = "Set",command=CMDSETICONPATH)
iconpathbutton.grid(column=2, row=0)

#Starting Tile
def CMDSETSTARTINGTILE():
    events["origin"] = [current_position[1],current_position[0]]
    UPDATEPANEL()

startingtileframe = Frame(setframe,relief="groove",bd=2)
startingtileframe.grid(column=0, row=6,sticky="EW")
startingtilebutton = Button(startingtileframe, text = "Spawn on this tile.", command=CMDSETSTARTINGTILE)
startingtilebutton.grid(column=2, row=0)

mapnameentry.delete(0, last=END)
mapnameentry.insert(0, mapname)
UPDATEPANEL()
root.mainloop()