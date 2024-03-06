from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import *

# USA
class Filters:
    def __init__(self, update_string):
        self.update_string = update_string

    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        for n in range(width):
            self.update_string.set(str(int((n/width)*100)) + '/100%')

            for m in range(length):
                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
        self.update_string.set('100/100')
        
    def mosaicHtmlTagger(self,sqOgWidth,sqOgLength, array, width, length, pixelTagFunction, header, footer):
        open("result.html", 'w').close()
        with open('result.html', 'a') as f:
            f.write(header)

        if (sqOgLength>width or sqOgWidth > length):
                return

        metric = lambda c1,c2: int(sqrt(
                            pow((c1[0]-c2[0]),2)
                            +pow((c1[1]-c2[1]),2)
                            +pow(abs(c1[2]-c2[2]),2))
                            )
                

        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]
        

        sqLength = sqOgLength
        for m in range(rowsOfSquares):
            # table break to separate squares lines
            with open('result.html', 'a') as f:
                f.write("<tr><td><nobr>")
                
            self.update_string.set("Filtro principal:"+str(int((m/rowsOfSquares)*100)) + '/100%')

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            
            sqWidth = sqOgWidth
            for n in range(columnsOfSquares):
                
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
            
                tag = pixelTagFunction(promiddleOfSquare[0], promiddleOfSquare[1], promiddleOfSquare[2])
                with open('result.html', 'a') as f:
                    f.write(tag)
            with open('result.html', 'a') as f:
                    f.write("</nobr></td></tr> \n")
        with open('result.html', 'a') as f:
                    f.write(footer)
        self.update_string.set('100/100')
    
    def mosaicHtmlTagger_with_context(self,sqOgWidth,sqOgLength, array, width, length, pixelTagFunction, header, footer):
        open("result.html", 'w').close()
        with open('result.html', 'a') as f:
            f.write(header)

        if (sqOgLength>width or sqOgWidth > length):
                return

        metric = lambda c1,c2: int(sqrt(
                            pow((c1[0]-c2[0]),2)
                            +pow((c1[1]-c2[1]),2)
                            +pow(abs(c1[2]-c2[2]),2))
                            )
                

        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]
        

        sqLength = sqOgLength

        for m in range(rowsOfSquares):
            with open('result.html', 'a') as f:
                f.write("<tr><td><nobr>")
            self.update_string.set("Main filter:"+str(int((m/rowsOfSquares)*100)) + '/100%')

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            sqWidth = sqOgWidth
            for n in range(columnsOfSquares):
                

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
            
                tag = pixelTagFunction(promiddleOfSquare[0], promiddleOfSquare[1], promiddleOfSquare[2],n,m,columnsOfSquares)
                with open('result.html', 'a') as f:
                    f.write(tag)
            with open('result.html', 'a') as f:
                    f.write("</nobr></td></tr> \n")
        with open('result.html', 'a') as f:
                    f.write(footer)
        self.update_string.set('100/100')
    
    def coloured_letters(self, array, width, length, repeat_letter):
        def tagger(r,g,b):
            return '<span style="color:#{:02x}{:02x}{:02x};">{rep_letter}</span>'.format(r, g, b, rep_letter=repeat_letter)
        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table></span>"
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)
    def gray_letters(self, array, width, length, repeat_letter):
        self.toGray(array,width, length)
        def tagger(r,g,b):
            return '<span style="color:#{:02x}{:02x}{:02x};">{rep_letter}</span>'.format(r, g, b, rep_letter= repeat_letter)
        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table></span>"
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)

    def dark_letters(self, array, width, length):
        self.toGray(array,width, length)
        def tagger(r,g,b):
            # chars_lighter_growing_list = ["/  
            chars_lighter_growing_list = ["M","N","H","r","#","Q","N","A","D","0","4","2","$","%","+",".","b","/"]      

            range = len(chars_lighter_growing_list)
            return chars_lighter_growing_list[int((r*range)/255)]

        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table><\span>"
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)
    def coloured_dark_letters(self, array, width, length):
        def tagger(r,g,b):
            chars_lighter_growing_list = ["M","N","H","r","#","Q","N","A","D","0","4","2","$","%","+",".","b","/"]      
            range = len(chars_lighter_growing_list)
            char = chars_lighter_growing_list[int((r*range)/255)]

            return '<span style="color:#{:02x}{:02x}{:02x};">{rep_letter}</span>'.format(r, g, b,rep_letter=char)
        
        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table><\span>"
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)
    def gray_dark_letters(self, array, width, length):
        self.toGray(array,width, length)
        def tagger(r,g,b):
            chars_lighter_growing_list = ["M","N","H","r","#","Q","N","A","D","0","4","2","$","%","+",".","b","/"]      

            range = len(chars_lighter_growing_list)
            char = chars_lighter_growing_list[int((r*range)/255)]

            return '<span style="color:#{:02x}{:02x}{:02x};">{rep_letter}</span>'.format(r, g, b,rep_letter=char)
        
        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table><\span>"
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)
    def coloured_text(self, array, width, length, text):
        self.toGray(array,width, length)
        def tagger(r,g,b, x,y, width):
            text_len = len(text)
            if (text_len==0):
                return "$"
            advance_in_text = (y*width)+x
            letter = text[advance_in_text%text_len]
            return '<span style="color:#{:02x}{:02x}{:02x};">{rep_letter}</span>'.format(r, g, b,rep_letter= letter)
        
        
        header = '<span style="font-family:Courier"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table></span>"
        self.mosaicHtmlTagger_with_context(3,3,array, width, length, tagger, header, footer)
    def dark_cards(self, array, width, length):
        self.toGray(array,width, length)
        def tagger(r,g,b):
            chars_lighter_growing_list = ["A","B","C","D","E","F","J"]

            range = len(chars_lighter_growing_list)
            return chars_lighter_growing_list[int((r*range)/255)]

        header = '<style>@font-face {font-family: card;src: url(cards.ttf);}</style><span style="font-family: card;"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table></span>"
        
                    
        self.mosaicHtmlTagger(3,3,array, width, length, tagger, header, footer)
    def dark_dominos(self, array, width, length):
        self.toGray(array,width, length)
        def tagger(r,g,b, x,y,width):
            left_domino_lighter_growing_list = ["0","1","2","3","4","5","6","7","8","9"]
            rigth_domino_lighter_growing_list = [")","!","@","#","$","%","^","&","*","("]
            
            if(len(left_domino_lighter_growing_list)<len(rigth_domino_lighter_growing_list)):
                range = len(left_domino_lighter_growing_list)
            else:
                range = len(rigth_domino_lighter_growing_list)

            if(x%2 == 0):
                char = left_domino_lighter_growing_list[int((r*range)/255)]
            else:
                char = rigth_domino_lighter_growing_list[int((r*range)/255)]
            return char

        header = '<style>@font-face {font-family: domino;src: url(domino.ttf);}</style><span style="font-family: domino;"><table border="0" cellspacing="0" cellpadding="0">'
        footer = "</table></span>"
                    
        self.mosaicHtmlTagger_with_context(3,3,array, width, length, tagger, header, footer)
    


    # optimizable al guardar r+g...
    def toGray(self, array, width, length):
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


        self.Coloured_letters_button = Button(
            self.tool_bar, text="ToColoured_letters", command=self.applyColoured_letters)
        self.Coloured_letters_button.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.Gray_letters_button = Button(
            self.tool_bar, text="ToGray_letters", command=self.applyGray_letters)
        self.Gray_letters_button.grid(row=5, column=2, padx=5, pady=3, ipadx=10)

        self.Dark_letter_button = Button(
            self.tool_bar, text="ToDark_letter", command=self.applyDark_letter)
        self.Dark_letter_button.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

        self.Coloured_dark_letters_button = Button(
            self.tool_bar, text="ToColoured_dark_letters", command=self.applyColoured_dark_letters)
        self.Coloured_dark_letters_button.grid(row=6, column=0, padx=5, pady=3, ipadx=10)
        
        self.Gray_dark_letters_button = Button(
            self.tool_bar, text="ToGray_dark_letters", command=self.applyGray_dark_letters)
        self.Gray_dark_letters_button.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

        self.Coloured_text_button = Button(
            self.tool_bar, text="ToColoured_text", command=self.applyColoured_text)
        self.Coloured_text_button.grid(row=6, column=2, padx=5, pady=3, ipadx=10)

        self.Dark_cards_button = Button(
            self.tool_bar, text="ToDark_cards", command=self.applyDark_cards)
        self.Dark_cards_button.grid(row=6, column=3, padx=5, pady=3, ipadx=10)

        self.Dark_dominos_button = Button(
            self.tool_bar, text="ToDark_dominos", command=self.applyDark_dominos)
        self.Dark_dominos_button.grid(row=6, column=4, padx=5, pady=3, ipadx=10)

        
        
        
        self.coloured_letters_char_label = Label(self.tool_bar, text="Coloured letters char:")
        self.coloured_letters_char_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.coloured_letters_char_box = Entry(self.tool_bar, width = 4)
        self.coloured_letters_char_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)

        # For 7th row entry
        self.gray_letters_char_label = Label(self.tool_bar, text="Gray letters char:")
        self.gray_letters_char_label.grid(row=8, column=0, padx=5, pady=3, ipadx=10)

        self.gray_letters_char_box = Entry(self.tool_bar, width = 4)
        self.gray_letters_char_box.grid(row=8, column=1, padx=5, pady=3, ipadx=10)

        self.coloured_text_label = Label(self.tool_bar, text="Coloured text filter text:")
        self.coloured_text_label.grid(row=9, column=0, padx=5, pady=3, ipadx=10)

        self.coloured_text_box = Entry(self.tool_bar, width = 4)
        self.coloured_text_box.grid(row=9, column=1, padx=5, pady=3, ipadx=10)

    def reselect_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            initialdir='~/Desktop/Practicas PDI/P1',
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
            initialdir='~/Desktop/Practicas PDI/P1',
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
            initialdir='~/Desktop/Practicas PDI/P1',
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

    def applyColoured_letters(self):
        try:
            self.filters.coloured_letters(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    , self.coloured_letters_char_box.get()
                                    )
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyGray_letters(self):
        try:
            self.filters.gray_letters(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    , (self.gray_letters_char_box.get())
                                    )
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyDark_letter(self):
        try:
            self.filters.dark_letters(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyColoured_dark_letters(self):
        try:
            self.filters.coloured_dark_letters(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyGray_dark_letters(self):
        try:
            self.filters.gray_dark_letters(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyColoured_text(self):
        try:
            self.filters.coloured_text(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    ,(self.coloured_text_box.get())
                                    )
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyDark_cards(self):
        try:
            self.filters.dark_cards(
                                    (self.main_image.load())
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1]))
        except ValueError as error:
            showerror(title='Error', message=error)
    def applyDark_dominos(self):
        try:
            self.filters.dark_dominos(
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
        self.main_image = Image.open(self.to_edit_image_fp)
        self.update_main_image()
    


root = Tk()  # create root window
root.title("P1")  # title of the GUI window
# root.maxsize(1920,1080)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()







# toGrayPromiddle(px,w,l)
# blackAndWhite(px,w,l)
# atandt(px,w,l,10,1)
# im.show()

# colores sin letras @, M
# tono de gris Q,M
# MNH#QNAD042$%+.b/
# (1)+(3)
# (2)+(3)
# colores con texto
# naipes
# dominós
