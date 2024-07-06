from pathlib import Path
from random import choices
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk
from pywinstyles import set_opacity

import swap_framework as sf
from swap_game_data import *

#if not work try tk.update() --> Try anywhere i'm stuck
#debug_variables

class SwapGame(tk.Tk):
    def __init__(self, title:str, size:tuple):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])

        #Handling style creating for many widgets
        style = ttk.Style()
        style.configure('playspace.TFrame', background='#2B3E50') #Playspace
        style.configure('sidebar.TFrame', background='#424242') #Sidebar
        style.configure('return.TButton', background='#424242')
        style.configure('smallbar.TSeparator', background='#2B3E50') #Player card picture separator
        style.configure('playerimage.TLabel', background='#556573') #Player image
        style.configure('nameentry.TEntry', foreground='#A4A7AB') #Name entry with no name
        style.configure('transp.TButton', background='#010101') #Use this color for transparency

        self.player_amount = tk.IntVar()
        self.player_amount.set(1)

        #For returning to main menu
        self.create_mainMenu()

        self.mainloop()
    
    def create_mainMenu(self):
        '''Only to be used internally by __init__ and on_return'''
        self.menu = BootMenu(self)

    def on_new(self):
        self.menu.pack_forget()
        self.ng = NGMenu(self, 0.25)

    def on_load(self):
        pass

    def on_settings(self):
        pass

    def on_info(self):
        pass

    def on_return(self):
        for i in self.winfo_children():
            i.destroy()
        self.create_mainMenu()

class BootMenu(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(expand=True, fill='both', side=tk.TOP)
        self.create_widgets()

    def create_widgets(self):
        #Main buttons frame and frame inside frame, just to use place and pack together
        boot_buttons_frame = ttk.Frame(self)
        boot_buttons_frame.pack(expand=True, fill='both')
        boot_buttons_frame_meta = ttk.Frame(boot_buttons_frame)
        boot_buttons_frame_meta.place(relx=0.5, rely=0.5, anchor='center')

        #Info buttons frame
        info_frame = ttk.Frame(self)
        info_frame.pack(anchor='se')

        #Resizing and transforming image to be used by info button
        info_icon = Image.open(f'{PATH_IMAGE_FOLDER}info.png')
        info_icon = ImageOps.fit(info_icon, (25, 25))
        self.info_icon = ImageTk.PhotoImage(master=info_frame ,image=info_icon)

        #Main Buttons
        button_new = ttk.Button(boot_buttons_frame_meta, command=self.master.on_new, text='New Game', width=20)
        button_load = ttk.Button(boot_buttons_frame_meta, command=self.master.on_load, text='Load Game', width=20)
        button_settings = ttk.Button(boot_buttons_frame_meta, command=self.master.on_settings, text='Settings', width=20)
        button_info = ttk.Button(info_frame, command=self.master.on_info, image=self.info_icon)

        #Packing Buttons
        button_new.pack()
        button_load.pack()
        button_settings.pack()
        button_info.pack(side=tk.RIGHT, anchor='s', padx=5, pady=5)

class NGMenu(ttk.Frame):
    def __init__(self, master, rel_width):
        super().__init__(master)
        self.rel_width = rel_width
        self.pc_amount = tk.IntVar(value = 1)
        self.playercards:list[PlayerCardsTemplate] = []
        self.card_amount:int = 1

        #Sets up picture options
        self.pic_options = self.set_picture_options()

        
        self.pack(expand=True, fill='both')
        
        self.create_widgets()
        
    def create_widgets(self):
        self.create_playspace()
        self.create_sidebar()

        #Placing both frames based on the side_bar relative width
        self.sidebar.place(x=0, y=0, relwidth=self.rel_width, relheight=1)
        self.playspace.place(relx=self.rel_width, y=0, relwidth=(1-self.rel_width), relheight=1)

    def create_sidebar(self):
        self.sidebar = ttk.Frame(self, borderwidth=10, style='sidebar.TFrame', relief='raised')
        self.sidebar.rowconfigure((0,1,2), weight=1)
        self.sidebar.columnconfigure(0, weight=1)

        #Grid 1 Widgets
        self.grid1_frame = ttk.Labelframe(self.sidebar, text='Number of Players', style='sidebar.TFrame', labelanchor='n')
        self.player_number_cbox = ttk.Spinbox(
            self.grid1_frame, from_=1, to=8, wrap=True, textvariable=self.pc_amount, justify='center', 
            command=self.place_player_cards, state='readonly')

        #Grid 3 Widgets
        self.grid3_frame = ttk.Frame(self.sidebar)
        self.return_to_main = ttk.Button(self.grid3_frame, text='Return', command=self.master.on_return)
        self.return_to_main.configure(style='return.TButton')

        #Placements
        self.grid1_frame.grid(row=0)
        self.player_number_cbox.pack(anchor='center')

        self.grid3_frame.grid(row=2)
        self.return_to_main.pack(anchor='center')

    def create_playspace(self):
        self.playspace = ttk.Frame(self, borderwidth=10, style='playspace.TFrame', relief='raised')

        #Creates first player card
        #BUG: Whenever removed, when switching from 1 to 8 players, it sets to 7 players
        self.playercards.append(PlayerCardsTemplate(self.playspace, self.pic_options))
        self.playercards[0].grid(row=0, column=0, sticky='nswe', padx=10, pady=10)

        self.playspace.rowconfigure((0,1), weight=1, uniform='a')
        self.playspace.columnconfigure((0,1,2,3), weight=1, uniform='a')

        self.place_player_cards()

    def place_player_cards(self):
        b = self.pc_amount.get() #Target Amount
        c = len(self.playspace.winfo_children()) #Current Amount
      
        #Adds or removes ('b' - 'c') frames until 'c' is the same as 'b'
        if self.pc_amount.get() > len(self.playspace.winfo_children()):
            while True:
                if c == b: break
                self.playercards.append(PlayerCardsTemplate(self.playspace, self.pic_options))
                self.playercards[-1].grid(row=0 if (c) <= 3 else 1, column=(c) % 4, sticky='nswe', padx=10, pady=10)
                c += 1
        elif self.pc_amount.get() < len(self.playspace.winfo_children()):
            while True:
                if c == b: break
                self.playercards[-1].destroy()
                self.playercards.pop()
                c -= 1
        else:
            pass

    def set_picture_options(self) -> dict[str:str]:
        #Sets up dict with all files in portrait folder
        #BUG: Will get any file wether it is a picture or not
        return {pic.stem: str(pic) for pic in Path(PATH_IMG_PRESETS).iterdir()}

class PlayerCardsTemplate(ttk.Frame):
    def __init__(self, master, pic_dict:dict):
        super().__init__(master)
        self.pic_dict = pic_dict
        self.pic_options = list(pic_dict.keys())

        #Register command for age digit check
        self.age_cmd = (self.register(self.digit_check))

        #Creating canvas for background
        self.canvasl = tk.Canvas(self, borderwidth=0, highlightthickness=0)

        #Setting background
        pc_bg = Image.open(PATH_PLAYER_BG)
        pc_bg = ImageOps.fit(pc_bg, size=(500,1000))
        self.pc_bg = ImageTk.PhotoImage(master=self ,image=pc_bg)
        self.canvasl.create_image(0, 0, image=self.pc_bg)

        #Placeholder image
        placeholder_avatar = Image.open(PATH_PLACEHOLDER_AVATAR)
        placeholder_avatar = ImageOps.fit(placeholder_avatar, (PLAYER_IMAGE_WIDTH, PLAYER_IMAGE_HEIGHT))
        self.placeholder_avatar = ImageTk.PhotoImage(master=self ,image=placeholder_avatar)

        #Interface widgets
        self.picture_choice = ttk.Combobox(self, state='readonly', values=list(self.pic_dict.keys()))
        self.picture = ttk.Label(self, image=self.placeholder_avatar, style='playerimage.TLabel', relief='ridge') #Needs to be tk.Label for no border, use highlightthickness and borderwidth
        smallbar = ttk.Separator(self, orient='horizontal', style='smallbar.TSeparator')
        self.entry_name = ttk.Entry(self, style='nameentry.TEntry')
        self.age_sex_frame = ttk.Frame(self)
        self.sex_gender = ttk.Combobox(self.age_sex_frame, state='readonly', values=['Male', 'Female'], width=7)
        self.how_old = ttk.Entry(self.age_sex_frame, style='nameentry.TEntry')
        self.ethnicity_cbox = ttk.Combobox(self, values=['White', 'Black', 'Hispanic', 'Asian'])
        self.use_preset = ttk.Button(self, text='Use a Preset', command=self.get_player_info)
 
        #Picture combobox
        self.picture_choice.bind('<<ComboboxSelected>>', lambda _: self.picture_change(self.picture_choice.get()))
        self.picture_choice.set('Select Picture')

        #Name entry
        self.name_touched:bool = False
        self.entry_name.insert(0, 'Name')
        self.entry_name.bind('<FocusIn>', lambda _: self.clear_entry(self.entry_name))

        #Gender combobox
        self.sex_gender.set('Gender')

        #Age entry
        self.age_touched:bool = False
        self.how_old.insert(0, 'Age')
        self.how_old.bind('<FocusIn>', lambda _: self.clear_entry(self.how_old))

        #Ethnicity combobox
        self.ethnicity_cbox.set('Ethnicity')

        #Preset button | It took downloading a package to have transparency actually exists, this should be part of tkinter???????
        self.use_preset.configure(style='transp.TButton')
        set_opacity(self.use_preset.winfo_id(), color="#010101") #Needs to be called for every widget
        
        #Placements
        self.canvasl.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.picture_choice.pack(padx=30, pady=5)
        self.picture.pack()
        smallbar.pack(padx=15, pady=5, fill='x')
        self.entry_name.pack()
        self.age_sex_frame.pack(padx=18, pady=5)
        self.sex_gender.pack(side=tk.LEFT)
        self.how_old.pack()
        self.ethnicity_cbox.pack(padx=18)
        self.use_preset.pack(padx=18, pady=5, side=tk.BOTTOM, fill='x')

        ######ADD FRAME TO CONTAIN SEX AND AGE SO THEY SHARE A ROW#######

    def picture_change(self, pic_key):
        image1 = Image.open(self.pic_dict[pic_key])
        image1 = ImageOps.fit(image1, (PLAYER_IMAGE_WIDTH, PLAYER_IMAGE_HEIGHT))
        self.image2 = ImageTk.PhotoImage(master=self ,image=image1)

        self.picture.configure(image=self.image2)

    def clear_entry(self, widget):
        if widget is self.entry_name and not self.name_touched:
            self.clear_entry_meta(widget)
            self.name_touched = True
        elif widget is self.how_old and not self.age_touched:
            self.clear_entry_meta(widget)
            self.age_touched = True

            #Starts digit validation when focused
            self.how_old.configure(validate='key', validatecommand=(self.age_cmd, '%P'))

    def clear_entry_meta(self, widget):
        widget.delete(0, tk.END)
        widget.configure(style='TEntry')
        widget.bind('<FocusOut>', lambda _: self.remap_entry(widget))

    def remap_entry(self, widget):
        if widget is self.entry_name and self.entry_name.get() == '':
            self.restore_placeholder(widget, 'Name')
            self.name_touched = False
        elif widget is self.how_old and self.how_old.get() == '':
            #Remove digit validation after losing focus
            self.how_old.configure(validate='none', validatecommand='')

            self.restore_placeholder(widget, 'Age')
            self.age_touched = False

    def restore_placeholder(self, widget, text):
        widget.configure(style='nameentry.TEntry')
        widget.insert(0, text)
        widget.bind('<FocusIn>', lambda _: self.clear_entry(widget))

    def digit_check(self, P) -> bool:
        if str.isdigit(P) or P == '': return True
        else: return False

    def on_use_preset(self):
        pass

    def create_card(self, player_params:dict = {None:None}): #Creating generic player card widgets, will accept optional argumets for when using presets
        pass #dict individual PlayerObject attributes as keys

    def get_player_info(self, attribute:str = '') -> dict: #Using match,case to fetch specific player data, may not be needed (vars(), __getattr__<abstract function)
        p_info = {
            'pic' : { #Needs actual logic
                'object' : self.testpicture,
                'path' : ''
                },
            'name' : self.entry_name.get() if self.entry_name.get() != 'Name' else None, #Sends empty if no name set
            'gender' : self.sex_gender.get() if self.sex_gender.get() != 'Gender' else None, #Sends empty if not selected gender
            'age' : int(self.how_old.get()) if self.how_old.get() != 'Age' and int(self.how_old.get()) >= 18 else None, #Temporary age logic, needs to happen when start button is pressed
            'ethnicity' : self.ethnicity_cbox.get() if self.ethnicity_cbox.get() != 'Ethnicity' else None #Sends empty if not set ethnicity
        }
        print(p_info)
        return p_info


game = SwapGame('The Swap "Game"', (1000,700))