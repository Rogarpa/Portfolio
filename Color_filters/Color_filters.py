from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

class Aplicacion(Frame):

    
    def __init__(self, parent):
        self.parent = parent

        # llama a constructor padre
        super().__init__(parent)
        self.create_main_frames()
        self.create_toolbar_widgets()

    def create_main_frames(self):
    
        # Create left and right frames
        self.left_frame = Frame(self.parent, width=50, height=700, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.parent, width=900, height=900, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create frames and labels in left_frame
        Label(self.left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

        # Select image
        self.to_edit_image_fp = self.select_image()
        print(self.to_edit_image_fp)

        # Update status of filter 
        self.update = StringVar(self.parent,'hola', "s1")
        self.update.trace('w', self.setUpdate)
        self.filters = Filters(self.update)
        
        # Open images
        self.main_image = Image.open(self.to_edit_image_fp).resize((650,400))
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)


        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image_resized)
        
        # Frames images labels
        self.main_image_label = Label(self.right_frame, image=self.main_image_tk)
        self.main_image_label.grid(row=0,column=0, padx=5, pady=5)


        self.mini_image_label = Label(self.left_frame, image=self.main_image_resized_tk)
        self.mini_image_label.grid(row=1, column=0, padx=5, pady=5)

        # Refreshing main image
        self.autorefresh_main_image()
        
        # Progress label
        self.program_state = Label(self.left_frame, text = 'state')
        self.program_state.grid(row=1, column=1, padx=5, pady=5)

        # Create tool bar frame
        self.tool_bar = Frame(self.left_frame, width=100, height=100, bg='red')
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

    def create_toolbar_widgets(self):
        
        
        self.button_gray_filter = Button(
            self.tool_bar, text="ToGray", command=self.applyToGray)
        self.button_gray_filter.grid(row=1, column=1, padx=5, pady=3, ipadx=10)

        self.button_mosaic_filter = Button(
            self.tool_bar, text="Mosaic", command=self.applyToMosaic)
        self.button_mosaic_filter.grid(row=1, column=2, padx=5, pady=3, ipadx=10)

        
        self.button_revert_img = Button(
            self.tool_bar, text="Revert", command=self.revertChanges)
        self.button_revert_img.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        self.open_button = Button(
            self.tool_bar,
            text='Open a Image',
            command=self.reselect_image
        )
        self.open_button.grid(row=0, column=3, padx=5, pady=3, ipadx=10)

        self.save_button = Button(
            self.tool_bar,
            text='Save the Image',
            command=self.save_image
        ).grid(row=0, column=4, padx=5, pady=3, ipadx=10)

        


        self.mosaic_length = Label(self.tool_bar, text="Mosaic Length:")
        self.mosaic_length.grid(row=3, column=0, padx=5, pady=3, ipadx=10)

        self.mosaic_length = Label(self.tool_bar, text="Mosaic Width:")
        self.mosaic_length.grid(row=4, column=0, padx=5, pady=3, ipadx=10)
        
        self.mosaic_length_box = Entry(self.tool_bar, text='Length', width = 4)
        self.mosaic_length_box.grid(row=3, column=3, padx=5, pady=3, ipadx=10)

        self.mosaic_width_box = Entry(self.tool_bar, text='Width', width = 4)
        self.mosaic_width_box.grid(row=4, column=3, padx=5, pady=3, ipadx=10)

            # 5th row

        self.button_toGrayRedChannel_filter = Button(
        self.tool_bar, text="toGrayRedChannel", command=self.applyToGrayRedChannel)
        self.button_toGrayRedChannel_filter.grid(row=5, column=0, padx=5, pady=3, ipadx=10)

        self.button_toGrayGreenChannel_filter = Button(
        self.tool_bar, text="toGrayGreenChannel", command=self.applyToGrayGreenChannel)
        self.button_toGrayGreenChannel_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.button_toGrayBlueChannel_filter = Button(
        self.tool_bar, text="toGrayBlueChannel", command=self.applyToGrayBlueChannel)
        self.button_toGrayBlueChannel_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)

        self.button_mica_filter = Button(
        self.tool_bar, text="Colour Filter", command=self.applyMica)
        self.button_mica_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

            # 6th row
        self.red_channel_label = Label(self.tool_bar, text="Red component (0-255):")
        self.red_channel_label.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        self.red_channel_box = Entry(self.tool_bar, width = 4)
        self.red_channel_box.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

            # 7th row
    
        self.green_channel_label = Label(self.tool_bar, text="Green component (0-255):")
        self.green_channel_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.green_channel_box = Entry(self.tool_bar, width = 4)
        self.green_channel_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)
        
            # 8th row
        self.blue_channel_label = Label(self.tool_bar, text="Blue component (0-255):")
        self.blue_channel_label.grid(row=8, column=0, padx=5, pady=3, ipadx=10)

        self.blue_channel_box = Entry(self.tool_bar, width = 4)
        self.blue_channel_box.grid(row=8, column=1, padx=5, pady=3, ipadx=10)
            # 9th row
        self.inverse_button = Button(
        self.tool_bar, text="inverse", command=self.applyinverse)
        self.inverse_button.grid(row=9, column=1, padx=5, pady=3, ipadx=10)

        self.highContrast_button = Button(
        self.tool_bar, text="highContrast", command=self.applyhighContrast)
        self.highContrast_button.grid(row=9, column=2, padx=5, pady=3, ipadx=10)

        self.bright_button = Button(
        self.tool_bar, text="bright", command=self.applybright)
        self.bright_button.grid(row=9, column=3, padx=5, pady=3, ipadx=10)
        # For 9th row entry
        self.brightness_value_label = Label(self.tool_bar, text="High contrast value(0-255):")
        self.brightness_value_label.grid(row=10, column=0, padx=5, pady=3, ipadx=10)

        self.brightness_value_box = Entry(self.tool_bar, width = 4)
        self.brightness_value_box.grid(row=10, column=1, padx=5, pady=3, ipadx=10)

        # For 10th row entry
        self.high_contrast_value_label = Label(self.tool_bar, text="Brightness value(0-255):")
        self.high_contrast_value_label.grid(row=11, column=0, padx=5, pady=3, ipadx=10)
        

        self.high_contrast_value_box = Entry(self.tool_bar, width = 4)
        self.high_contrast_value_box.grid(row=11, column=1, padx=5, pady=3, ipadx=10)




    def select_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            initialdir='~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        return fp

    def reselect_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        self.to_edit_image_fp = fp
        self.main_image = Image.open(fp).resize((650,400))

        self.update_mini_image()
        self.update_main_image()
        
        self.parent.update_idletasks()

    def save_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        save_fp = fd.asksaveasfile(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/',
            filetypes=filetypes
            )

        showinfo(
            title='Selected File',
            message="Guardado"
        )
        self.main_image.save(save_fp)
        
    def autorefresh_main_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    # no need
    # def autorefresh_mini_image(self):
    #     self.update_mini_image()
    #     self.parent.update_idletasks()
    #     self.parent.after(500, self.autorefresh_mini_image)
    
    def setUpdate(self, a=None,b=None,c=None):
        self.program_state.config(text = self.update.get())
        self.parent.update_idletasks()
        self.parent.after(0, self.setUpdate)

    def update_main_image(self):
        self.refreshed_image = ImageTk.PhotoImage(self.main_image)
        self.main_image_label.config(image=self.refreshed_image)

    def update_mini_image(self):
        self.refreshed_resized_image = ImageTk.PhotoImage(self.main_image.resize((300,300)))
        self.mini_image_label.config(image=self.refreshed_resized_image)

    def revertChanges(self):
        self.update.set('Reverting changes')

        self.main_image = Image.open(self.to_edit_image_fp)
        self.update_main_image()
        self.update.set('Image reverted')






    def applyToMosaic(self):
        self.revertChanges()
        try:
            self.filters.mosaicFilter(
                                    int(self.mosaic_length_box.get())
                                    ,int(self.mosaic_width_box.get())
                                    ,(self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyToGray(self):
        self.revertChanges()
        try:
            self.filters.toGrayPromiddle(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    ,(self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyToGrayRedChannel(self):
        self.revertChanges()
        try:
            self.filters.toGrayRedChannel(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyToGrayGreenChannel(self):
        
        self.revertChanges()
        try:
            self.filters.toGrayGreenChannel(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyToGrayBlueChannel(self):
        self.revertChanges()
        try:
            self.filters.toGrayBlueChannel(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyinverse(self):
        self.revertChanges()
        try:
            self.filters.inverse(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyhighContrast(self):
        self.revertChanges()
        try:
            self.filters.toGrayPromiddle(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
            self.filters.highContrast(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    , int(self.high_contrast_value_box.get()))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applybright(self):
        self.revertChanges()
        try:
            self.filters.bright(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    , int(self.brightness_value_box.get()))

        except ValueError as error:
            showerror(title='Error', message=error)


    def applyMica(self):
        self.revertChanges()
        try:
            self.filters.mica(
                                    (self.main_image.load())
                                    ,int(self.red_channel_box.get())
                                    ,int(self.green_channel_box.get())
                                    ,int(self.blue_channel_box.get())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)



class Filters:
    
    def __init__(self, update_string):
        self.update_string = update_string




    def mosaicFilter(self,sqOgLength, sqOgWidth, array, width, length):
        if (sqOgLength>width or sqOgWidth > length):
            return

        
        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]


        sqWidth = sqOgWidth
        for n in range(columnsOfSquares):
            self.update_string.set(str(int((n/columnsOfSquares)*100)) + '/100%')
            
            # Refreshes the square size each column iteration
            sqLength = sqOgLength

            # Modifies range of j for if last column
            if (n == (columnsOfSquares-1)):
                sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)

            for m in range(rowsOfSquares):
                
                # Modifies range of j for if last row
                if (m == (rowsOfSquares-1)):
                    sqLength = length - ((rowsOfSquares-1)*sqOgLength)

                promiddleOfSquare = [0,0,0]

                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        promiddleOfSquare[0] = ((array[x,y])[0] + promiddleOfSquare[0])//2
                        promiddleOfSquare[1] = ((array[x,y])[1] + promiddleOfSquare[1])//2
                        promiddleOfSquare[2] = ((array[x,y])[2] + promiddleOfSquare[2])//2
                
                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        (array[x,y]) = (promiddleOfSquare[0], promiddleOfSquare[1], promiddleOfSquare[2])
        self.update_string.set('100/100%')
    
    # Modifies the received array of pixels [(r,g,b,brightness),...]
    # to make it look like a chess table
    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        for n in range(width):
            self.update_string.set(     str(int((n/width)*100)) + '/100%')
            for m in range(length):

                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
        self.update_string.set('100/100%')
        
    
    def toGrayPromiddle(self, array, width, length):
        fourTupleFunction = lambda r, g, b: ((r+g+b)//3,(r+g+b)//3,(r+g+b)//3,255)
                                
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayRedChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (r,r,r)
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayGreenChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (g,g,g)
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayBlueChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (b,b,b)
        self.update_string.set("processing mosaic: " + '100/100%')

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    

    def inverse(self, array, width, length):
        def fourTupleFunction(r,g,b):
            return (255-r,255-g,255-b) 
        
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    def highContrast(self, array, width, length, contrast):
        def fourTupleFunction(r,g,b):
            new_gray = int((r/contrast)*255)
            return(new_gray,new_gray, new_gray)
        
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    def bright(self, array, width, length, brightness):
        def fourTupleFunction(r,g,b):
            return (r+brightness
                    ,g+brightness
                    ,b+brightness
                    )
        
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    

    def mica(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (rChannel and r
                                            , gChannel and g
                                            , bChannel and b
                                            ,255
                                            )

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)




root = Tk()  # create root window
root.title("P1")  # title of the GUI window
# root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()
