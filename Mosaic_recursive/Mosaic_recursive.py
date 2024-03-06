from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import *
from math import *
import os 

# detalles:
# mosaicos tienen que tener forma correcta
# 

class Aplication(Frame):
    
    def __init__(self):
        a = 0

    def __init__(self, parent):
        self.parent = parent

        # llama a constructor padre
        super().__init__(parent)
        self.create_main_frames()
        self.create_toolbar_widgets()

    def create_main_frames(self):
        # Create left and right frames
        self.left_frame = Frame(self.parent, width=200, height=700, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.parent, width=650, height=700, bg='grey')
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
        self.main_image = Image.open(self.to_edit_image_fp)
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)

        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image)
        
        # Frames images labels
        self.main_image_label = Label(self.right_frame, image=self.main_image_tk)
        self.main_image_label.grid(row=0,column=0, padx=5, pady=5)


        self.mini_image_label = Label(self.left_frame, image=self.main_image_tk)
        self.mini_image_label.grid(row=1, column=0, padx=5, pady=5)

        # Refreshing main image
        self.autorefresh_main_image()
        self.autorefresh_mini_image()
        
        # Progress label
        self.program_state = Label(self.left_frame, text = 'state')
        self.program_state.grid(row=1, column=1, padx=5, pady=5)

        # Create tool bar frame
        self.tool_bar = Frame(self.left_frame, width=300, height=300, bg='red')
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # f.photoMosaic(p,p,pixelMap,width, length, self.to_edit_images_fps)
        
    def create_toolbar_widgets(self):
        self.button_revert_img = Button(
            self.tool_bar, text="Revert", command=self.revertChanges)
        self.button_revert_img.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        self.open_button = Button(
            self.tool_bar,
            text='Open a File',
            command=self.reselect_image
        )
        self.open_button.grid(row=0, column=3, padx=5, pady=3, ipadx=10)

        self.save_button = Button(
            self.tool_bar,
            text='Save the File',
            command=self.save_image
        ).grid(row=0, column=4, padx=5, pady=3, ipadx=10)


        self.gray_recursive_button = Button(
        self.tool_bar, text="Create color recursive html", command=self.createColorHtmlPhotomosaic)
        self.gray_recursive_button.grid(row=5, column=2, padx=5, pady=3, ipadx=10)
        
        self.color_recursive_button = Button(
        self.tool_bar, text="Create gray recursive html", command=self.createGrayHtmlPhotomosaic)
        self.color_recursive_button.grid(row=5, column=3, padx=5, pady=3, ipadx=10)
        # Entries
        self.mosaic_length = Label(self.tool_bar, text="Mosaic Length:")
        self.mosaic_length.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        self.mosaic_length = Label(self.tool_bar, text="Mosaic Width:")
        self.mosaic_length.grid(row=7, column=0, padx=5, pady=3, ipadx=10)
        
        self.mosaic_length_box = Entry(self.tool_bar, text='Length', width = 4)
        self.mosaic_length_box.grid(row=6, column=3, padx=5, pady=3, ipadx=10)

        self.mosaic_width_box = Entry(self.tool_bar, text='Width', width = 4)
        self.mosaic_width_box.grid(row=7, column=3, padx=5, pady=3, ipadx=10)

    def reselect_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            initialdir = '~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        self.to_edit_image_fp = fp
        self.main_image = Image.open(fp)
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)

        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image_resized)
        
        # Frames images labels
        self.main_image_label.config(image=self.main_image_tk)

        self.mini_image_label.config(image=self.main_image_resized_tk)

        self.parent.update_idletasks()

    def select_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            initialdir = '~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        return fp
    
    def select_mosaics(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fps = fd.askopenfilenames(
            title='Select mosaic images',
            initialdir = '~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fps
        )
        self.filters.process_mosaics(fps)

        return fps

    def save_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        save_fp = fd.asksaveasfile(
            title='Open a file',
            initialdir = '~/',
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
    
    def autorefresh_mini_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    
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
        self.main_image = Image.open(self.to_edit_image_fp)
        self.update_main_image()
    


    def select_file(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        file = fd.askopenfilename(
            title='Open a file',
            initialdir = '~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.to_edit_image_fp
        )
        return file
    
    def createGrayHtmlPhotomosaic(self):
        try:
            
            self.filters.grayRecursive(
                                    self.to_edit_image_fp
                                    ,int(self.mosaic_width_box.get())
                                    ,int(self.mosaic_length_box.get())
                                    )
            self.update.set("Html terminado en: ./")
        except ValueError as error:
            showerror(title='Error', message=error)
    def createColorHtmlPhotomosaic(self):
        
        try:
            
            self.filters.colorRecursive(
                                    self.to_edit_image_fp
                                    ,int(self.mosaic_width_box.get())
                                    ,int(self.mosaic_length_box.get())
                                    )
            self.update.set("Html terminado en: ./")
        except ValueError as error:
            showerror(title='Error', message=error)


    
class Filters():
    def __init__(self, update_string):
        self.update_string = update_string


    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        for n in range(width):
            for m in range(length):
                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
    
    def process_mosaics(self, filespaths_list):
        
    

        promiddle = [0,0,0]

        # Clear file
        open('imagen.idx', 'w').close()

        for f in range(len(filespaths_list)):
            file_path = filespaths_list[f]

            self.update_string.set("processing mosaic: " + file_path
            +" " +str(int((f/len(filespaths_list))*100)) + '/100%')

            buffer_image = Image.open(file_path)
            buffer_pixelmap = buffer_image.load()

            for x in range(buffer_image.size[0]):
                for y in range(buffer_image.size[1]):
                    promiddle[0] = ((promiddle[0]) + (buffer_pixelmap[x,y][0]))//2
                    promiddle[1] = ((promiddle[1]) + (buffer_pixelmap[x,y][1]))//2
                    promiddle[2] = ((promiddle[2]) + (buffer_pixelmap[x,y][2]))//2
            

            with open('./imagen.idx', 'a') as f:
                f.write("\n" + str(promiddle) + ":" + file_path)
        with open('./imagen.idx', 'a') as f:
                f.write("\n")
        self.update_string.set("processing mosaic: " + '100/100%')


    def color_creator(self, input_fp, output_fp):
        print('color c')
        buffer_image = Image.open(input_fp)
        buffer_pixelmap = buffer_image.load()
        width = buffer_image.size[0]
        length = buffer_image.size[1]
        interval = 70
        for r in range(0,255,interval):
            for g in range(0,255,interval):
                for b in range (0,255,interval):
                    # for x in range(width):
                    #     for y in range(length):
                    #         buffer_pixelmap[x,y] = (r,g,b)
                    # self.blend(buffer_pixelmap, r,g,b,width,length)
                    self.blend(buffer_pixelmap, r,g,b,width,length)
                    print((r,g,b))
                    name = str((r,g,b))+".jpg"
                    buffer_image.save(output_fp+name)
                    buffer_image = Image.open(input_fp)
                    buffer_pixelmap = buffer_image.load()
    def search_nearest_color_fp(self, color_to_compare, colors_list, metric_function):
        better_fp = ''
        min_metric_value = 500
        color = [0,0,0]
        with open('./imagen.idx','r') as f:
            dictionary = f.readlines()
        for i in range(1,len(dictionary),1):
            
            
            color_string = (str((dictionary[i].split(':')[0])[1:-1]).split(','))
            color = [0,0,0]
            
            for v in range(3):
                color[v] = int(color_string[v])




            buffer_value = metric_function(color_to_compare,color)

            if(buffer_value <= min_metric_value):
                min_metric_value = buffer_value
                better_fp = (dictionary[i].split(':'))[1][:-1]
        
        return better_fp
            
    def blend(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (int(rChannel *(r/255))
                                            ,int(gChannel *(g/255))
                                            ,int(bChannel *(b/255))
                                            ,255
                                            )

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    
    def mica(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (int(r * (rChannel/255))
                                            ,int(g * (gChannel/255))
                                            ,int(b * (bChannel/255))
                                            )
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    def bright(self, array, width, length, brightness):
        def fourTupleFunction(r,g,b):
            return (r+brightness
                    ,g+brightness
                    ,b+brightness
                    )
        
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    
    # more optimal with file sizes
    def grayRecursive(self, photo_fp, sqOgWidth, sqOgLength):
        og_image = Image.open(photo_fp)
        width = og_image.size[0]
        length = og_image.size[1]
        array = og_image.load()
        
        path = 'gray_buffer'

        try:
            os.rmdir(path)
        except OSError as error:
            print("Error occured: %s : %s" % (path, error.strerror))


        try: 
            os.mkdir(path) 
        except OSError as error: 
            print("Error occured: %s : %s" % (path, error.strerror))

        if (sqOgLength>width or sqOgWidth > length):
            return

        
        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = 0
        
        open("gray_recursive.html", 'w').close()
        with open('gray_recursive.html', 'a') as f:
                    f.write("<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">")


        sqLength = sqOgLength
        for m in range(rowsOfSquares):

            self.update_string.set("html color recursive creation:"+str(int((m/rowsOfSquares)*100)) + '/100%')

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            # line break
            with open('gray_recursive.html', 'a') as f:
                    f.write("<tr><td><nobr>")

            sqWidth = sqOgWidth
            for n in range(columnsOfSquares):

                # Refreshes the square size each column iteration

                # Modifies range of j for if last column
                if (n == (columnsOfSquares-1)):
                    sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)
                    
                if(sqLength == 0 or sqWidth == 0):
                    break
                
                # Creates mosaic recursive image
                image_buffer = Image.open(photo_fp).resize((sqWidth,sqLength))
                mosaic_buffer = image_buffer.load()


                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        promiddleOfSquare = ((array[x,y])[0] + promiddleOfSquare)//2
                
                # substitute mosaic by image
                fp_substitute_mosaic_image = './gray_buffer/'+str((m,n))+".jpg"
                self.toGrayPromiddle(mosaic_buffer, sqWidth, sqLength)
                self.bright(mosaic_buffer, sqWidth, sqLength, promiddleOfSquare)


                image_buffer.save(fp_substitute_mosaic_image)

                table_cell = "<img src=\"{fp}\" width=\"{widt}\" height=\"{height}\">".format(fp = fp_substitute_mosaic_image, widt = sqOgWidth, height = sqOgLength)
                with open('gray_recursive.html', 'a') as f:
                    f.write(table_cell)
            with open('gray_recursive.html', 'a') as f:
                    f.write("</nobr></td></tr> \n")
        with open('gray_recursive.html', 'a') as f:
                    f.write("</table>")
        self.update_string.set('100/100')
    
    
    def colorRecursive(self, photo_fp, sqOgWidth, sqOgLength):
        og_image = Image.open(photo_fp)
        width = og_image.size[0]
        length = og_image.size[1]
        # set default sqOg values
        if(sqOgWidth>width or sqOgLength>length):
            sqOgLength =width/20
            sqOgWidth=length/20
        path = 'color_buffer'
        try:
            os.rmdir(path)
        except OSError as error:
            print("Error occured: %s : %s" % (path, error.strerror))


        try: 
            os.mkdir(path) 
        except OSError as error: 
            print("Error occured: %s : %s" % (path, error.strerror))
        
        array = og_image.load()

        if (sqOgLength>width or sqOgWidth > length):
            return

        
        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]
        
        open("color_recursive.html", 'w').close()
        with open('color_recursive.html', 'a') as f:
                    f.write('<table border="0" cellspacing="0" cellpadding="0">')


        sqLength = sqOgLength
        for m in range(rowsOfSquares):

            self.update_string.set("html color recursive creation:"+str(int((m/rowsOfSquares)*100)) + '/100%')

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            # line break
            with open('color_recursive.html', 'a') as f:
                    f.write("<tr><td><nobr>")

            sqWidth = sqOgWidth
            for n in range(columnsOfSquares):
                
                if(sqLength == 0 or sqWidth == 0):
                    break
                
                # Creates mosaic recursive image
                image_buffer = Image.open(photo_fp).resize((sqWidth,sqLength))
                mosaic_buffer = image_buffer.load()



                # Refreshes the square size each column iteration

                # Modifies range of j for if last column
                if (n == (columnsOfSquares-1)):
                    sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)

                promiddleOfSquare = [0,0,0]

                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        promiddleOfSquare[0] = ((array[x,y])[0] + promiddleOfSquare[0])//2
                        promiddleOfSquare[1] = ((array[x,y])[1] + promiddleOfSquare[1])//2
                        promiddleOfSquare[2] = ((array[x,y])[2] + promiddleOfSquare[2])//2
                
                # substitute mosaic by image

                fp_substitute_mosaic_image = './color_buffer/'+str((m,n))+".jpg"
                self.toGrayPromiddle(mosaic_buffer, sqWidth, sqLength)
                self.mica(mosaic_buffer,promiddleOfSquare[0], promiddleOfSquare[1], promiddleOfSquare[2],sqWidth, sqLength)

                image_buffer.save(fp_substitute_mosaic_image)

                table_cell = "<img src=\"{fp}\" width=\"{widt}\" height=\"{height}\">".format(fp = fp_substitute_mosaic_image, widt = sqOgWidth, height = sqOgLength)
                with open('color_recursive.html', 'a') as f:
                    f.write(table_cell)
            with open('color_recursive.html', 'a') as f:
                    f.write("</nobr></td></tr> \n")
        with open('color_recursive.html', 'a') as f:
                    f.write("</table>")
        self.update_string.set('100/100')
    
    def toGrayPromiddle(self, array, width, length):
        fourTupleFunction = lambda r, g, b: ((r+g+b)//3,(r+g+b)//3,(r+g+b)//3,255)

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)



root = Tk()  # create root window
root.title("Proyecto Final")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color
app = Aplication(root)
root.mainloop()

