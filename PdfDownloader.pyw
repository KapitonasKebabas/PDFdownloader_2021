import requests
import os
from tkinter import *
from tkinter import filedialog
import time

root = Tk()
root.title("PDF Downloader")

def pdfSiuntimas(listas):
    try:
        time.sleep(1)
        payload = {
            'username': usernameTxt,
            'password': pswTxt
        }

        with requests.Session() as s:
            p = s.post(url, data=payload) 
            urlUniqueCode = p.url[p.url.rfind('=')+1:]
            checkUrl = "https://leliukas.shopiteka.lt/admin/index.php?route=addons/wizzard&token=" + urlUniqueCode
            if checkUrl == p.url:
                for OrderID in listas:
                    rs = s.get(urlPDF+urlUniqueCode+urlOrder+str(OrderID))
                    with open(os.path.join(path, str(OrderID)) + ".pdf", 'wb') as f:
                        for chunk in rs.iter_content(chunk_size=8192):
                            f.write(chunk)
                labelDownload.config(text = "Downloaded")
            else:
                labelDownload.config(text = "Wrong password or username inputs")
    except:
        Erorlabel = Label(root, text="Error check Username/Password or selecte file")
        Erorlabel.grid(row=1,column=1)

def selectFileDef():
    global filepath
    filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file", filetypes=(("txt files","*.txt"),("all files", "*.*")))
    filepath = filepath.replace("/","\\")
    filepathtxt = "Selected file: " + filepath[filepath.rfind("\\")+1:]
    labelFilename = Label(root, text=filepathtxt)
    labelFilename.grid(row=3,column=1)
    userButton['state'] = ACTIVE
    return filepath

def rndListDownlaoder():
    h = open(filepath, 'r') 
    ListContent = h.readlines() 
    ListContent = map(lambda s: s.strip(), ListContent)
    pdfSiuntimas(ListContent)

"""
def ListDownlaoder():
    OrderMin = int(input("Pradzia order_id= "))
    OrderMax = int(input("Pabaiga order_id= ")) + 1

    if OrderMax>=OrderMin:
        Skirtumas = range(OrderMin, OrderMax)
        pdfSiuntimas(Skirtumas)
"""

def userSubmit():
    labelDownload.config(text = "")
    global usernameTxt
    usernameTxt = str(username.get())
    global pswTxt
    pswTxt = str(psw.get())
    startButton['state'] = ACTIVE


url = 'https://leliukas.shopiteka.lt/admin/index.php?route=sale/order/invoice&token=81c4d5b0c08033c834ff5631a5b60869&order_id=2244'
urlPDF = 'https://leliukas.shopiteka.lt/admin/index.php?route=sale/order/invoice&token='
urlOrder = '&order_id='


cwd = os.getcwd()
path = cwd + "\\Saskaitu_Fakturos"
if os.path.isdir(path) == False:
    os.mkdir(path)

for x in range(1):
    label = Label(root, text=" ")
    label.grid(row=x+1,column=0)

fileButton = Button(root, text="Select a File", command=selectFileDef)
fileButton.grid(row=3,column=0)

label = Label(root, text=" ")
label.grid(row=4,column=0)

userButton = Button(root, text="Submit", command=userSubmit, state=DISABLED)
userButton.grid(row=7,column=0)

label = Label(root, text="Username: ")
label.grid(row=5,column=0)

username = Entry(root, width=15)
username.grid(row=5,column=1)

label = Label(root, text="Password: ")
label.grid(row=6,column=0)

psw = Entry(root, width=15)
psw.grid(row=6,column=1)

startButton = Button(root, text="Start Downlaoding", command=rndListDownlaoder, state=DISABLED)
startButton.grid(row=7,column=1)

labelDownload = Label(root, text="")
labelDownload.grid(row=8,column=1)


root.geometry("300x200")   
    

root.mainloop()
