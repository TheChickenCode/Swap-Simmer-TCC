from random import choices
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk

import swap_framework as sf
from swap_game_data import *

#debug_variables

class SwapGame(tk.Tk):
    def __init__(self, title:str, size:tuple):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])

        #Handling style creating for many widgets
        self.style = ttk.Style()
        self.style.configure('playspace.TFrame', background='#2B3E50')
        self.style.configure('sidebar.TFrame', background='#424242')

        self.player_amount = tk.IntVar()
        self.player_amount.set(1)

        #For returning to main menu
        self.create_mainMenu()

        self.mainloop()
    
    def create_mainMenu(self):
        '''Only to be used internally by __init__ and on_return'''
        self.menu = BootMenu(self)

    def on_new_game(self):
        self.menu.pack_forget()
        self.ng = NGMenu(self, 0.25)

    def on_load_game(self):
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
        info_icon = Image.open(PATH_INFO_BUTTON_ICON)
        info_icon = ImageOps.fit(info_icon, (25, 25))
        self.info_icon = ImageTk.PhotoImage(master=info_frame ,image=info_icon)

        #Main Buttons
        button_new_game = ttk.Button(boot_buttons_frame_meta, command=self.master.on_new_game, text='New Game', width=20)
        button_load_game = ttk.Button(boot_buttons_frame_meta, command=self.master.on_load_game, text='Load Game', width=20)
        button_settings = ttk.Button(boot_buttons_frame_meta, command=self.master.on_settings, text='Settings', width=20)
        button_info = ttk.Button(info_frame, command=self.master.on_info, image=self.info_icon)

        #Packing Buttons
        button_new_game.pack()
        button_load_game.pack()
        button_settings.pack()
        button_info.pack(side=tk.RIGHT, anchor='s', padx=5, pady=5)

class NGMenu(ttk.Frame):
    def __init__(self, master, rel_width):
        super().__init__(master)
        self.rel_width = rel_width
        self.pc_amount = tk.IntVar(value = 1)
        self.playercards:list[PlayerCards] = []
        self.card_amount:int = 1
        
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
        self.player_number_cbox = ttk.Spinbox(self.grid1_frame, from_=1, to=8, wrap=True, textvariable=self.pc_amount, justify='center',
            command=self.place_player_cards, state='readonly')

        #Grid 3 Widgets
        self.grid3_frame = ttk.Frame(self.sidebar)
        self.return_to_main = ttk.Button(self.grid3_frame, text='Return', command=self.master.on_return)

        #Placements
        self.grid1_frame.grid(row=0)
        self.player_number_cbox.pack(anchor='center')

        self.grid3_frame.grid(row=2)
        self.return_to_main.pack(anchor='center')

    def create_playspace(self):
        self.playspace = ttk.Frame(self, borderwidth=10, style='playspace.TFrame', relief='raised')
        self.playercards.append(PlayerCards(self.playspace, 'Tango'))
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
                self.playercards.append(PlayerCards(self.playspace, 'Tango'))
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

class PlayerCards(ttk.Labelframe):
    def __init__(self, master, pl_name:str):
        super().__init__(master, text=pl_name)

        self.mind = ttk.Labelframe(self, text='Mind')
        self.body = ttk.Labelframe(self, text='Body')

        self.mind.pack()
        self.body.pack()


game = SwapGame('The Swap "Game"', (1000,700))