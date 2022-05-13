from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image,ImageTk
import math
import configparser
from os.path import exists
import json

config = configparser.ConfigParser()
config.read('config.ini')


#Startup Window
root = Tk()
root.title("Startup")
root.resizable(False, False)

map = None
mapname = None

def on_closing():
    try:
        driver.close()
    finally:
        root.destroy()
        exit()
root.protocol("WM_DELETE_WINDOW", on_closing)

fileentryframe = Frame(root, bd=1, relief="groove")
fileentryframe.grid(column=0, row=0, sticky="EW")
settingsframe = Frame(root, bd=1, relief="groove")
settingsframe.grid(column=0, row=1, sticky="EW")

def FILEENTRYCMD():
    global browser, input
    input = fileentry.get()
    if clicked.get() == "Set Browser":
        messagebox.showinfo(message='Web browser not selected.')
    else:
        browser = clicked.get()
    if exists(input):
        global map, mapname, events
        mapfile = open(input, "r")
        mapdata = json.loads(mapfile.read())
        events = mapdata[0]
        map = mapdata[1]
        mapfile.close()
        mapname = input.replace(".map","")
        config['STORED VARIABLES']['last_used_map'] = input
        config['STORED VARIABLES']['browser'] = clicked.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()
        root.destroy()
    else:
        messagebox.showinfo(message='File not found. Write name like "example.map" or input file path.')

fileentrylabel = Label(fileentryframe, text="Map File Path: ")
fileentrylabel.grid(row=0,column=0)
fileentry = Entry(fileentryframe, width = 50)
fileentry.grid(row=0,column=1,columnspan=2)

if config['STORED VARIABLES']['last_used_map'] != "None":
    if exists(config['STORED VARIABLES']['last_used_map']):
        fileentry.insert(0,config['STORED VARIABLES']['last_used_map'])

#Move this down
fielentrybutton = Button(fileentryframe, text = "Begin",command=FILEENTRYCMD)
fielentrybutton.grid(row=0,column=4)

browserlabel = Label(settingsframe, text="Web Browser: ")
browserlabel.grid(row=0,column=0)
clicked = StringVar()
if config["STORED VARIABLES"]["browser"] == "None":
    clicked.set("Set Browser")
else:
    clicked.set(config["STORED VARIABLES"]["browser"])
browserdropdown = OptionMenu(settingsframe,clicked,"Chrome", "Firefox", "Edge", "Brave*", "Chromium*")
browserdropdown.grid(row=0,column=1)

#Note:Create Entry for setting window scale
'''
windowscalelabel = Label(settingsframe, text="Window Scale (Default is 400): ")
windowscalelabel.grid(row=0,column=2)
windowscaleentry = Entry(fileentryframe, width = 4)
windowscaleentry.grid(row=0,column=1,columnspan=3)
'''

root.mainloop()

#Tkinter Setup
root = Tk()

root.title("Holo Companion")
window_scale = int(config["SETTINGS"]["window_scale"])
rframe_height = math.ceil(window_scale/20)
cframe_height = math.ceil(window_scale/8)
root.resizable(False, False)

rngframe = Frame(root, bd=1, relief="groove", height=rframe_height, width=window_scale)
rngframe.grid(column=0, row=0, sticky="EW", columnspan=2)
mapframe = Frame(root, height=window_scale, width=window_scale)
mapframe.grid(column=0, row=1, columnspan=2)
controlframe = Frame(root, height=cframe_height,width=window_scale/2)
controlframe.grid(column=0, row=2)
cheatsframe = Frame(root, bd=1, relief="groove", width=window_scale/2)
cheatsframe.grid(column=1, row=2, sticky="NEWS")

#Set Global Variables
document_text = None
descriptions_enabled = config["STORED VARIABLES"]["descriptions_enabled"]
events_enabled = config["STORED VARIABLES"]["events_enabled"]

def SHOWERROR(errormessage):
    messagebox.showerror("Error", errormessage)
    root.destroy
    try:
        driver.close()
    finally:
        exit()


#Startup Browser
drivererrorhad = 0
try:
    if browser == "Chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif browser == "Firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif browser == "Edge":
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    elif browser == "Chromium*":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    elif browser == "Brave*":
        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
    else:
        drivererrorhad = 1
except:
    SHOWERROR("ERROR: Error setting up browser driver. config.ini missing or unreadable?")
if drivererrorhad == 1:
    SHOWERROR("ERROR: Browser set incorrectly in config.ini.")


driver.get("https://writeholo.com/home")

#Wait for home page to load
try:
    WebDriverWait(driver, 120).until(EC.url_matches("https://writeholo.com/home"))
except:
    SHOWERROR("ERROR: Could not load writeholo.com/home or page took too long to load.")

#Function that waits for the story to be open
def WAITFORSTORYPAGE(timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains("https://writeholo.com/write/"))
    except:
        SHOWERROR("ERROR: Could not load writeholo.com/write or failed to open story before program timeout.")

WAITFORSTORYPAGE(600)

def CHECKPAGE():
    try:
        if driver.current_url.find("https://writeholo.com/write/") == -1:
            SHOWERROR("ERROR: Could not detect story page. Closing program.")
    except:
        root.destroy
        exit()
#Wait for the story to be opened

def DOCREAD():
    WAITFORSTORYPAGE(120)
    document = ""
    prosemirror = driver.find_element(By.CLASS_NAME, 'ProseMirror')
    elements = prosemirror.find_elements(By.TAG_NAME, 'p')
    for e in elements:
        if driver.find_element(By.CLASS_NAME, 'ProseMirror') == 0:
            document = document+e.text
        else:
            document = document+"\n"+e.text
    return document

def DOCGET():
    WAITFORSTORYPAGE(120)
    return driver.find_element(By.CLASS_NAME, 'ProseMirror')

def DOCADD(String):
    WAITFORSTORYPAGE(120)
    global document_text
    document_text = DOCREAD()+String

#Check and cancel the action if more than one instance of the string exists.
#Obsolete Function, don't bother for now.
def DOCSWAP(Old_Substring, New_Substring):
    WAITFORSTORYPAGE(120)
    global document_text
    document_text = DOCREAD().replace(Old_Substring, New_Substring)

def DOCUPDATE():
    WAITFORSTORYPAGE(120)
    global document_text
    DOCGET().clear()
    DOCGET().send_keys(document_text)

def DOCAPPEND(StringToAppend):
    WAITFORSTORYPAGE(120)
    global document_text
    DOCGET().send_keys(Keys.CONTROL, Keys.END)
    DOCGET().send_keys(StringToAppend)

'''def TKUPDATE():
   root.after(1000, TKUPDATE)'''

def on_closing():
    try:
        driver.close()
    finally:
        root.destroy()
        exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

#Setting up the map
current_position = [events["origin"][0], events["origin"][1]]
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
        tlist[y].grid(column=x, row=y)
    tile.append(tlist)

l = []
def RENDERMAP():
    global map,mapx,mapy,current_position,tile,l
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

#RNG Section
successlist = [["Your attempt to "," is successful."],["You successfully ","."],["You ","."],["You try, with success, to ","."]]
failurelist = [["Your attempt to "," fails."],["Your attempt to "," is unsuccessful."],["Despite your attempt, you fail to ","."],["You fail to ","."],["You try to ",", which results in failure."]]
def ROLLFUNCT(attempt,successrate):
    global successlist, failurelist
    attempt = attempt.replace("\n","")
    if random.randint(1,100) <= int(successrate):
        listi = random.randint(0,len(successlist)-1)
        return successlist[listi][0]+attempt+successlist[listi][1]
    else:
        listi = random.randint(0,len(failurelist)-1)
        return failurelist[listi][0]+attempt+failurelist[listi][1]

rng = []

def BUTTONROLL():
    CHECKPAGE()
    global rng
    if DOCREAD().find("\n", len(DOCREAD())-1) == -1:
        DOCAPPEND("\n")
    DOCAPPEND(ROLLFUNCT(rng[1].get("1.0",END), rng[4].get()))


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

tfont = ("Arial", math.ceil(window_scale/44))
rng.append(Label(rngframe, text = "Attempt: ",font=tfont)) #rng[0] Attempt label
rng.append(Text(rngframe, height=2, width=25,font=tfont)) #rng[1] Text input
rng.append(Scrollbar(rngframe)) #rng[2] Scroll bar
rng.append(Label(rngframe, text = " Success %: ",font=tfont)) #rng[3] Success Label
rng.append(Entry(rngframe, width = 3,font=tfont,validate="key", validatecommand=vcmd)) #rng[4] Percent Entry
rng.append(Button(rngframe, text = "ROLL", command = BUTTONROLL,font=tfont)) #rng[5] Roll Button
rng[1].insert(END, 'Insert phrase like "jump the gap"...')
rng[1].configure(yscrollcommand=rng[2].set)
for i in range(6):
    rng[i].grid(row=0,column=i,padx=math.ceil(window_scale/200))
rng[2].config(command=rng[1].yview)

#Saving Position
def SAVEPOS():
    global events
    events["origin"]=[current_position[0],current_position[1]]
    mapfile = open(input, "w")
    mapfile.write(json.dumps([events, map]))
    mapfile.close()

#Control Keys
def MOVEUP():
    CHECKPAGE()
    if current_position[1]-1 >= 0 and "N" in map[current_position[1]][current_position[0]]["travel"]:
        moving_position = [current_position[0],current_position[1]-1]
        eventstab = map[moving_position[1]][moving_position[0]]["events"]
        RNG = random.randint(1, 100)
        if eventstab[0] != "" and int(eventstab[1]) > RNG and events_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(events[eventstab[0]])
            if eventstab[2] == "O":
                eventstab[1] = "0"
        elif map[moving_position[1]][moving_position[0]]["description"] != "" and descriptions_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(map[moving_position[1]][moving_position[0]]["description"])
        if eventstab[0] == "" or int(eventstab[1]) <= RNG or eventstab[3] == "M" or events_enabled == 'False':
            current_position[1] = current_position[1]-1
            RENDERMAP()
        SAVEPOS()
def MOVEDOWN():
    CHECKPAGE()
    if current_position[1]+1 <= mapy-1 and "S" in map[current_position[1]][current_position[0]]["travel"]:
        moving_position = [current_position[0],current_position[1]+1]
        eventstab = map[moving_position[1]][moving_position[0]]["events"]
        RNG = random.randint(1, 100)
        if eventstab[0] != "" and int(eventstab[1]) > RNG and events_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(events[eventstab[0]])
            if eventstab[2] == "O":
                eventstab[1] = "0"
        elif map[moving_position[1]][moving_position[0]]["description"] != "" and descriptions_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(map[moving_position[1]][moving_position[0]]["description"])
        if eventstab == "" or int(eventstab[1]) <= RNG or eventstab[3] == "M" or events_enabled == 'False':
            current_position[1] = current_position[1]+1
            RENDERMAP()
        SAVEPOS()
def MOVELEFT():
    CHECKPAGE()
    if current_position[0]-1 >= 0 and "W" in map[current_position[1]][current_position[0]]["travel"]:
        moving_position = [current_position[0]-1,current_position[1]]
        eventstab = map[moving_position[1]][moving_position[0]]["events"]
        RNG = random.randint(1, 100)
        if eventstab[0] != "" and int(eventstab[1]) > RNG and events_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(events[eventstab[0]])
            if eventstab[2] == "O":
                eventstab[1] = "0"
        elif map[moving_position[1]][moving_position[0]]["description"] != "" and descriptions_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(map[moving_position[1]][moving_position[0]]["description"])
        if eventstab == "" or int(eventstab[1]) <= RNG or eventstab[3] == "M" or events_enabled == 'False':
            current_position[0] = current_position[0]-1
            RENDERMAP()
        SAVEPOS()
def MOVERIGHT():
    CHECKPAGE()
    if current_position[0]+1 <= mapx-1 and "E" in map[current_position[1]][current_position[0]]["travel"]:
        moving_position = [current_position[0]+1,current_position[1]]
        eventstab = map[moving_position[1]][moving_position[0]]["events"]
        RNG = random.randint(1, 100)
        if eventstab[0] != "" and int(eventstab[1]) > RNG and events_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(events[eventstab[0]])
            if eventstab[2] == "O":
                eventstab[1] = "0"
        elif map[moving_position[1]][moving_position[0]]["description"] != "" and descriptions_enabled == 'True':
            DOCAPPEND("\n")
            DOCAPPEND(map[moving_position[1]][moving_position[0]]["description"])
        if eventstab == "" or int(eventstab[1]) <= RNG or eventstab[3] == "M" or events_enabled == 'False':
            current_position[0] = current_position[0]+1
            RENDERMAP()
        SAVEPOS()

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

#cheats

#Disable Reading
readingswitchbutton = Button(cheatsframe,text="Location Descriptions Enabled.")
readingswitchbutton.grid(row=0,column=0,pady=2)
def disablereadingswitch():
    global descriptions_enabled
    if descriptions_enabled == 'True':
        readingswitchbutton.config(text="Location Descriptions Disabled.",fg="red")
        config["STORED VARIABLES"]["descriptions_enabled"] = 'False'
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()
        descriptions_enabled = 'False'
    else:
        readingswitchbutton.config(text="Location Descriptions Enabled.", fg="black")
        config["STORED VARIABLES"]["descriptions_enabled"] = 'True'
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()
        descriptions_enabled = 'True'
readingswitchbutton.config(command=disablereadingswitch)
if descriptions_enabled == 'False':
    readingswitchbutton.config(text="Location Descriptions Disabled.", fg="red")
#Disable Random Events
reswitchbutton = Button(cheatsframe,text="Random Events Enabled.")
reswitchbutton.grid(row=1,column=0,pady=2)
def disableeventsswitch():
    global events_enabled
    if events_enabled == 'True':
        reswitchbutton.config(text="Random Events Disabled.",fg="red")
        config["STORED VARIABLES"]["events_enabled"] = 'False'
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()
        events_enabled = 'False'
    else:
        reswitchbutton.config(text="Random Events Enabled.", fg="black")
        config["STORED VARIABLES"]["events_enabled"] = 'True'
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()
        events_enabled = 'True'
reswitchbutton.config(command=disableeventsswitch)
if events_enabled == 'False':
    reswitchbutton.config(text="Random Events Disabled.", fg="red")

root.mainloop()