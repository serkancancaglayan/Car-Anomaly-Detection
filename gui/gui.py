import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
import os
from analyse_image import analyse_image


W_HEIGHT = 900
W_WIDTH = 500

filepath = ""

def analyse(filepath, anomaly_factor):
    analyse = analyse_image()
    info_text = tk.Label(frame1)
    if filepath == "":
        messagebox.showerror('Hata','Input görüntü okunamadı veya input görüntü seçilmedi.')
    else:
        if not analyse.car_or_not(filepath = filepath):
            messagebox.showerror('Görüntüde Araç Tespit Edilemedi', 'Görüntüde araç olduğundan '+
                'eminseniz farklı bir açı ile veya farklı bir ışıklandırma ile ' +
                'çekilmiş bir görüntü ile tekrar deneyiniz.')
        else:
            if not analyse.damaged_or_not(filepath):
                messagebox.showerror('Hasarsız Araç', 'Görüntüdeki araçta hasar tespit edilemedi. '+
                'Görüntüdeki aracın hasarlı olduğundan eminseniz farklı bir açı ile vaya '+
                'farklı bir ışıklandırma ile çekilmiş bir görüntü ile tekrar deneyiniz.')
            else:
                text = "Hasar Katsayısı :%" + str(anomaly_factor)
                text += "\nHasar Konumu: " + analyse.damage_location(filepath)
                text += "\nHasar Boyutu: %" + analyse.damage_severity(filepath, anomaly_factor)
                label1.configure(text = text, font=(('Courier', 14)))
                

def browse():
    global filepath
    file = askopenfilename(filetypes = [ ('JPEG', '.JPEG'),('PNG', '.png'), ('JPG', '.jpg')])
    filepath = file
    image = Image.open(file)
    image = image.resize((400,500))
    image = ImageTk.PhotoImage(image)
    label.configure(image = image)
    label.image = image


#root
root = tk.Tk()
root.title('Araç Hasar Tespit')

#Arka Plan ve Canvas
canvas = tk.Canvas(root, height=W_HEIGHT, width= W_WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file = 'C:/Users/serka/Desktop/gui/back_ground.png')
background_label = tk.Label(root, image = background_image)
background_label.place(x = 0, y = 0, relwidth = 1, relheight= 1)

#Fotografin gosterilecegi frame
frame = tk.Frame(root)
frame.place(relwidth = 0.8, relheight = 0.3, relx = 0.1, rely= 0.05)

label = tk.Label(frame)
label.pack(side = 'bottom')

#Gozat Butonu
image = Image.open('C:/Users/serka/Desktop/gui/button_background.png')
image = image.resize((116,37))
image = ImageTk.PhotoImage(image)

button = tk.Button(root, image = image, width = 116, height = 37, command=lambda:browse())
button.pack()
button.place(x = 200, y = 320)

#Hata katsayisi slider
v1 = DoubleVar()
slider = tk.Scale(root, from_ = -50, to = 50, orient=HORIZONTAL, variable= v1, length = 300)
slider.place(x = 100, y = 420)
slider_label = tk.Label(root, text = "Hasar Katsayısı")
slider_label.config(font = ("Courier", 12))
slider_label.place(x = 180, y = 400)

#Analiz Butonu
image1 = Image.open('C:/Users/serka/Desktop/gui/analiz_button_background.jpg')
image1 = image1.resize((116, 37))
image1 = ImageTk.PhotoImage(image1)

button1 = tk.Button(root, image = image1, width = 116, height=37,command=lambda:analyse(filepath, v1.get()))
button1.place(x = 200, y = 470)


#Aracin hasar konumu ve hasar orani hakkinda bilgilerin yazdirilacagi frame
frame1 = tk.Frame(root)
frame1.place(relwidth = 0.8, relheight = 0.3, relx = 0.1, rely= 0.6)

label1 = tk.Label(frame1)
label1.pack(side = 'top')

root.mainloop()
