from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import *
class Filters:
    def __init__(self, update_string):
        self.update_string = update_string

    def atandt(self, array, width, length, bar_length, wave_padding):
        calculated_wave_padding = wave_padding

        for y in range(0,length,bar_length):
            self.update_string.set("atandt:"+str(int((y/length)*100)) + '/100%')
            
            if((length-y) < wave_padding):
                calculated_wave_padding = length-y

            for x in range(width):
                for white_padding in range(calculated_wave_padding):
                    array[x,y+white_padding] = (255,255,255)
            y = y + wave_padding
            if(y>length):
                y = length

            for x in range(width):
                    
                padding_y_down = length-y
                if(padding_y_down > bar_length):
                    padding_y_down = bar_length
                

                number_of_black_pixels = 0

                for l in range(padding_y_down):
                    array[x,y+l]
                    
                    if(array[x,y+l][0] == 0):
                        number_of_black_pixels += 1
                    # cuenta pero no pone blanco
                    array[x,y+l] = (255,255,255)
                vertical_centering = ((padding_y_down-number_of_black_pixels)//2)
                for black in range(number_of_black_pixels):
                        array[x,vertical_centering+y+black] = (0,0,0)
        self.update_string.set('100/100')
        
    def sepia(self, array, width, length):
        sepia_pixel_function = lambda r, g, b: (int(0.393*r + 0.769*g + 0.189*b)
                                                ,int(0.349*r + 0.686*g + 0.168*b)
                                                ,int(0.272*r + 0.534*g + 0.131*b)
                                            )
        self.pixelPerPixelFilter(array, width, length,sepia_pixel_function)

    def dithering(self, array, width, length, propagation_matrix):
        error_buffer = [[0 for x in range(length)] for y in range(width)]
        black = (255,255,255)
        white = (0,0,0)

        radio = len(propagation_matrix)//2


        for x in range(width):
            self.update_string.set(str(int((x/width)*100)) + '/100%')

            for y in range(length):
                
                start_matrix_coordinate = [0,0]
                start_kernel_coordinate = [0,0]

                padding_x_left = x
                if(padding_x_left > radio):
                    padding_x_left = radio
                padding_x_right = (width-x)-1
                if(padding_x_right > radio):
                    padding_x_right = radio
                padding_y_up = y
                if(padding_y_up > radio):
                    padding_y_up = radio
                padding_y_down = (length - y)-1
                if(padding_y_down > radio):
                    padding_y_down = radio


                start_matrix_coordinate = [x - padding_x_left, y-padding_y_up]
                start_kernel_coordinate = [radio-padding_x_left, radio-padding_y_up]
            
                x_range = padding_x_left + padding_x_right + 1
                y_range = padding_y_up + padding_y_down + 1

                error = array[x,y][0] + error_buffer[x][y]

                if(error-0 < (255-error)):
                    array[x,y] = white
                else:
                    array[x,y] = black

                for i in range(x_range):
                    for j in range(y_range):
                        propagation_factor = (propagation_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                        if(propagation_factor == 0):
                            break
                        else:
                            error_buffer[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)] = propagation_factor * error
        self.update_string.set('100/100')
            


    def blackAndWhite(self, array, width, length):
        div = 1/48
        jarvis_propagation_matrix = [[0]]
        self.dithering(array, width, length, jarvis_propagation_matrix)

    # Antiques filters

    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        # falta aumentar nn y rowsOfSquares una para residuos
        for n in range(width):
            self.update_string.set(str(int((n/width)*100)) + '/100%')

            for m in range(length):
                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
        self.update_string.set('100/100')
        
    # optimizable al guardar r+g...
    def toGrayPromiddle(self, array, width, length):
        fourTupleFunction = lambda r, g, b: ((r+g+b)//3,(r+g+b)//3,(r+g+b)//3,255)
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)



class Aplicacion(Frame):

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

        self.button_tosepia_filter = Button(
        self.tool_bar, text="Sepia", command=self.applySepia)
        self.button_tosepia_filter.grid(row=5, column=0, padx=5, pady=3, ipadx=10)
        
        self.button_toAtandt_filter = Button(
        self.tool_bar, text="At&t", command=self.applyAtandt)
        self.button_toAtandt_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)
        
        self.button_toBlackAndWhite_filter = Button(
        self.tool_bar, text="BlackAndWhite", command=self.applyBlackAndWhite)
        self.button_toBlackAndWhite_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)

        self.button_gray_filter = Button(
            self.tool_bar, text="ToGray", command=self.applyToGray)
        self.button_gray_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

            # 6th row
        self.att_wave_width_label = Label(self.tool_bar, text="Att wave width:")
        self.att_wave_width_label.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        self.att_wave_width_box = Entry(self.tool_bar, width = 4)
        self.att_wave_width_box.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

        self.att_wave_spacing_label = Label(self.tool_bar, text="Att wave spacing:")
        self.att_wave_spacing_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.att_wave_spacing_box = Entry(self.tool_bar, width = 4)
        self.att_wave_spacing_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)
        
    def reselect_image(self):
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
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        return fp

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
    
    def autorefresh_mini_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    
    def setUpdate(self, a=None,b=None,c=None):
        self.program_state.config(text = self.update.get())
        self.parent.update_idletasks()
        self.parent.after(0, self.setUpdate)

    def applyAtandt(self):
        self.revertChanges()
        try:
            self.filters.toGrayPromiddle(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                )

            self.update.set("gray finished")

            self.filters.blackAndWhite(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                )
            self.update.set("black/white finished")
            
            self.filters.atandt(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    ,int(self.att_wave_width_box.get())
                                    ,int(self.att_wave_spacing_box.get()))
            self.update.set("at&t finished")
            

        except ValueError as error:
            showerror(title='Error', message=error)

    def applySepia(self):
        self.revertChanges()
        try:
            
            self.filters.sepia(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
            

        except ValueError as error:
            showerror(title='Error', message=error)

    def applyBlackAndWhite(self):
        try:
            
            self.filters.blackAndWhite(

                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
            

        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyToGray(self):
        try:
            self.filters.toGrayPromiddle(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)




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
    
    


root = Tk()  # create root window
root.title("P9")  # title of the GUI window
root.maxsize(1920,1080)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()




