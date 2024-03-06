from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import *
# quitar updates en filtros
# quitar threadings

class Filters:
    def __init__(self, update_string):
        self.update_string = update_string

    def convolution_kernel_filter(self,array, width, length, kernel_matrix):
        # falta probar que kernel tenga sentido
        radio = len(kernel_matrix)//2

        for x in range(width):
            
            self.update_string.set(str(int((x/width)*100)) + '/100%')
            
            # Refreshes the square size each column iteration
            

            for y in range(length):
                
                pixel_buffer = [0,0,0]
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

                

                for i in range(x_range):
                    for j in range(y_range):
                        
                        pixel_buffer[0] += int((array[(start_matrix_coordinate[0]+i),(start_matrix_coordinate[1]+j)][0]) 
                                                * (kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)]))
                        pixel_buffer[1] += int((array[(start_matrix_coordinate[0]+i), (start_matrix_coordinate[1]+j)][1])
                                            *kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                        pixel_buffer[2] += int((array[(start_matrix_coordinate[0]+i), (start_matrix_coordinate[1]+j)][2])
                                            *kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                
                array[x,y] = (pixel_buffer[0],pixel_buffer[1], pixel_buffer[2])

        self.update_string.set('100/100')
        
    
    def blur(self,array, width, length):
        div = 1/5

        blur_convolution_matrix = [[0,div,0],[div,div,div], [0,div,0]]
        self.convolution_kernel_filter(array, width, length, blur_convolution_matrix)
    
    def motion_blur(self,array, width, length):
        div = 1/9

        motion_blur_convolution_matrix = [
                                    [div,0,0,0,0,0,0,0,0]
                                    ,[0,div,0,0,0,0,0,0,0]
                                    ,[0,0,div,0,0,0,0,0,0]
                                    ,[0,0,0,div,0,0,0,0,0]
                                    ,[0,0,0,0,div,0,0,0,0]
                                    ,[0,0,0,0,0,div,0,0,0]
                                    ,[0,0,0,0,0,0,div,0,0]
                                    ,[0,0,0,0,0,0,0,div,0]
                                    ,[0,0,0,0,0,0,0,0,div]
                                  ]
        self.convolution_kernel_filter(array, width, length, motion_blur_convolution_matrix)
    
    def finde_edges(self,array, width, length):
        finde_edges_convolution_matrix = [
                                    [0,0,-1,0,0]
                                    ,[0,0,-1,0,0]
                                    ,[0,0,2,0,0]
                                    ,[0,0,0,0,0]
                                    ,[0,0,0,0,0]
                                  ]
        self.convolution_kernel_filter(array, width, length, finde_edges_convolution_matrix)

    def finde_edges(self,array, width, length):
        finde_edges_convolution_matrix = [
                                    [0,0,-1,0,0]
                                    ,[0,0,-1,0,0]
                                    ,[0,0,2,0,0]
                                    ,[0,0,0,0,0]
                                    ,[0,0,0,0,0]
                                  ]
        self.convolution_kernel_filter(array, width, length, finde_edges_convolution_matrix)

    def sharpen(self,array, width, length):

        sharpen_convolution_matrix = [
                                     [-1,-1,-1]
                                    ,[-1,9,-1]
                                    ,[-1,-1,-1]
        ]
        self.convolution_kernel_filter(array, width, length, sharpen_convolution_matrix)

    def emboss(self,array, width, length):
        emboss_convolution_matrix = [
                                    [-1, -1,  0]
                                    ,[-1,  0,  1]
                                    ,[0,  1,  1]
                                    ]
        self.convolution_kernel_filter(array, width, length, emboss_convolution_matrix)

    def mean(self,array, width, length):
        div = 1/9

        mean_convolution_matrix = [
                                    [div,div,div]
                                    ,[div,div,div]
                                    ,[div,div,div]
                                  ]
        self.convolution_kernel_filter(array, width, length, mean_convolution_matrix)

        # Modifies the received array of pixels [(r,g,b,brightness),...]
    # to make it look like a chess table
    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        for n in range(width):
            self.update_string.set(     str(int((n/width)*100)) + '/100%')
            for m in range(length):

                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
        self.update_string.set('100/100%')
        
    
    def mica(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (int(rChannel * (r/255))
                                            ,int(bChannel * (b/255))
                                            ,int(gChannel * (g/255))
                                            ,255
                                            )
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
        self.refresh_mini_image()
        
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

        self.button_toBlur_filter = Button(
        self.tool_bar, text="Blur", command=self.applyBlur)
        self.button_toBlur_filter.grid(row=5, column=0, padx=5, pady=3, ipadx=10)

        self.button_toMotionBlur_filter = Button(
        self.tool_bar, text="Motion Blur", command=self.applyMotionBlur)
        self.button_toMotionBlur_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.button_toFindEdges_filter = Button(
        self.tool_bar, text="Find Edges", command=self.applyFindEdges)
        self.button_toFindEdges_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)
        
        self.button_toSharpen_filter = Button(
        self.tool_bar, text="Sharpen", command=self.applySharpen)
        self.button_toSharpen_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

        self.button_toEmboss_filter = Button(
        self.tool_bar, text="Emboss", command=self.applyEmboss)
        self.button_toEmboss_filter.grid(row=5, column=4, padx=5, pady=3, ipadx=10)

        self.button_toMean_filter = Button(
        self.tool_bar, text="Mean", command=self.applyMean)
        self.button_toMean_filter.grid(row=5, column=5, padx=5, pady=3, ipadx=10)
            
            # 6th row
        self.red_channel_label = Label(self.tool_bar, text="Mica: red component (0-255):")
        self.red_channel_label.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        self.red_channel_box = Entry(self.tool_bar, width = 4)
        self.red_channel_box.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

            # 7th row
    
        self.green_channel_label = Label(self.tool_bar, text="Mica: green component (0-255):")
        self.green_channel_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.green_channel_box = Entry(self.tool_bar, width = 4)
        self.green_channel_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)
        
            # 8th row
        self.blue_channel_label = Label(self.tool_bar, text="Mica: blue component (0-255):")
        self.blue_channel_label.grid(row=8, column=0, padx=5, pady=3, ipadx=10)

        self.blue_channel_box = Entry(self.tool_bar, width = 4)
        self.blue_channel_box.grid(row=8, column=1, padx=5, pady=3, ipadx=10)
        
        self.button_mica_filter = Button(
        self.tool_bar, text="Mica", command=self.applyMica)
        self.button_mica_filter.grid(row=9, column=0, padx=5, pady=3, ipadx=10)
        

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
        self.main_image = Image.open(fp)
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)

        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image_resized)
        
        # Frames images labels
        self.main_image_label.config(image=self.main_image_tk)

        self.mini_image_label.config(image=self.main_image_resized_tk)

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
    
    def refresh_mini_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    
    def setUpdate(self, a=None,b=None,c=None):
        # error
        self.program_state.config(text = self.update.get())
        self.parent.update_idletasks()
        self.parent.after(0, self.setUpdate)

    def applyBlur(self):
        self.revertChanges()
        try:

            
            self.filters.blur(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
            

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyMotionBlur(self):
        self.revertChanges()
        try:
            self.filters.motion_blur(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)

    def applyFindEdges(self):
        self.revertChanges()
        try:
            self.filters.finde_edges(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applySharpen(self):
        self.revertChanges()
        try:
            self.filters.sharpen(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyEmboss(self):
        self.revertChanges()
        try:
            self.filters.emboss(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyMean(self):
        self.revertChanges()
        try:
            self.filters.motion_blur(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)

    def applyMica(self):
        self.revertChanges()
        try:
            print()
            self.filters.mica(
                                    (self.main_image.load())
                                    ,int(self.red_channel_box.get())
                                    ,int(self.green_channel_box.get())
                                    ,int(self.blue_channel_box.get())
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
root.title("P2")  # title of the GUI window
root.maxsize(1920,1080)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()