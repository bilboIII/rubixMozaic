from bdb import effective
import tkinter
from tkinter import messagebox
from tkinter.constants import DISABLED
from typing import MappingView, Sequence
from PIL import ImageTk,Image,ImageOps,ImageColor
from tkinter import Button, filedialog,simpledialog,colorchooser

class rubix_GUI():

    def __init__(self):
        self.root = tkinter.Tk()

        self.files = [("jpg files", "*.jpg"), ("png files", "*.png"), ("image files", "*img"), ("All files", "*.*")]

        self.picture_frame = tkinter.Frame()
        self.buttom_frame = tkinter.Frame()

        self.picture_var = tkinter.StringVar

        #sets up the buttons
        self.file_button = tkinter.Button(self.buttom_frame, text="Open file", bg="cyan", command=self.open)
        self.file_button.pack(side="top")

        self.reset_button = tkinter.Button(self.buttom_frame, text="Reset Photo", command=self.reset)
        self.reset_button.pack(side="top")

        self.grayscale_button = tkinter.Button(self.buttom_frame, text="Grayscale", command=self.grayscale)
        self.grayscale_button.pack(side="top")


        self.pixel_button = tkinter.Button(self.buttom_frame, text="Pixelate", command=self.pixelate)
        self.pixel_button.pack(side='top')


        self.poster_button = tkinter.Button(self.buttom_frame, text='posterize', command=self.poster)
        self.poster_button.pack(side='top')

        self.color_button = tkinter.Button(self.buttom_frame, text="Colorize", command=self.colorize, state=DISABLED)
        self.color_button.pack(side='top')

        self.save_exit_button = tkinter.Button(self.buttom_frame, text="Exit", background="red", command=self.root.destroy)
        self.save_exit_button.pack(side='bottom')

        self.save_exit_button = tkinter.Button(self.buttom_frame, text="Save as", background="green", command=self.save_exit)
        self.save_exit_button.pack(side='bottom')


        
        self.buttom_frame.pack(side='left')
        self.picture_frame.pack(side='left')

        self.root.bind("<Return>", self.display_pic)

        self.root.mainloop()

    def open(self):
        #opens file 
        self.root = filedialog.askopenfilename(title="select a File", filetypes= self.files)
        img = Image.open(self.root)

        #this down sizes the image so its workable
        img.thumbnail((600,600))

        #saves images as "mod.png" this will be the photo we modify
        # and saves as "og.png" so that if you want to restart you can        
        img.save('mod.png')
        img.save('og.png')

        #runs the funcion to display the photo
        self.display_pic('mod.png')

    def reset(self):
        #resets photo back to the orignal
        og = Image.open("og.png")
        #resets colorize button 
        self.color_button['state'] = 'disable'
        self.change_img(og)

    def grayscale(self):
        self.gs_image = Image.open('mod.png').convert('L')
        
        #enables colorize button
        self.color_button['state'] = 'normal'

        #updates the imgage
        self.change_img(self.gs_image)

    def pixelate(self):
        img = Image.open("mod.png")
        w = simpledialog.askinteger("Input", "What is the Width of the image?")
        h = simpledialog.askinteger("Input", "What is the height of the image?")
        imgSmall = img.resize((w, h), resample=Image.BILINEAR)
        pixel = imgSmall.resize(img.size,Image.NEAREST)
        #updates the imgage
        self.change_img(pixel)

    def poster(self):
        answer = simpledialog.askinteger("Input", "What color do you want?", minvalue=1, maxvalue=8)

        # creating a image1 object 
        im1 = Image.open("mod.png") 
        
        # applying posterize method 
        im2 = ImageOps.posterize(im1, answer)
        #updates the imgage
        self.change_img(im2) 

    def colorize(self):
        
        # colors = [0] * answer
        colors = [(0, 0, 255), (255, 0, 0), (255, 153, 0), (255, 255, 0), (255, 255, 255)] #this shoud be the base colors, also idea the initialcolor for the colorchooser
        msgBox = messagebox.askyesno('Change Colors', 'Would you like to change the 5 default colors?')
        if msgBox == True:
            #loops through and ask what colors they would like
            for i in range(len(colors)):
                name = str('Color choice ' + str(i + 1))
                rgb_color, web_color = colorchooser.askcolor(title=name ,initialcolor=(colors[i]))
                r,g,b = rgb_color
                colors[i] = (int(r),int(g),int(b))
            #sorts colors if user decides they want different colors darkest to lightest 
            colors.sort()
       
        #get a list of the picture
        img = Image.open("mod.png")
        img.convert("RGB")
        sequence_of_pixels = img.getdata()
        
        #take img and colorize it
        newPic = []

        for x in sequence_of_pixels:
            #blue the first color in 'colors' list
            if x in range(0, 91):
                color = colors[0]
                #red the second color in 'colors' list
            elif x in range(91, 121):
                color = colors[1]
                #orange the third color in 'colors' list
            elif x in range(121, 151):
                color = colors[2]
                #yellow the forth color in 'colors' list
            elif x in range(151, 180):
                color = colors[3]
                #white the fith color in 'colors' list
            else:
                color = colors[4]
            ### legacy code
            """
            for x in sequence_of_pixels:
            #looks for the min distance for the gs list ant that of the pixel in question 
            minNum = gs[min(range(len(gs)), key = lambda i:abs(gs[i]-x))]
            for i in range(len(colors)):
                
                if minNum == gs[i]:
                    color = colors[i]
            """

            newPic.append(color)

        #creats new image and saves the new data to said image
        img1 = Image.new("RGB", (img.size), (255, 255, 255))
        
        img1.putdata(newPic)
        self.change_img(img1)


    def save_exit(self):
        photo = Image.open("mod.png")
        file = filedialog.asksaveasfilename(title="Save Photo", defaultextension=".png", filetypes = self.files)
        photo.save(file)
        #self.root.destroy()

    def display_pic(self, pic):
        #displays file "might need to make this into it's own function"
        self.my_image = ImageTk.PhotoImage(Image.open(pic))
        self.display_label = tkinter.Label(self.picture_frame, image=self.my_image)
        self.display_label.pack()
        
    def change_img(self, pic):
        pic.save('mod.png')
        pic = 'mod.png'
        #gets new photo
        my_image = ImageTk.PhotoImage(Image.open(pic))
        #sets new photo
        self.display_label.configure(image=my_image)
        self.display_label.image=my_image
        

run = rubix_GUI()