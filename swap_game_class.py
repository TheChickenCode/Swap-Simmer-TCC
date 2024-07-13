import tkinter as tk
from tkinter import ttk

from pathlib import Path
from typing import Callable
from random import choices
from PIL import Image, ImageTk, ImageOps
from pywinstyles import set_opacity

import swap_framework as sf
from swap_game_data import *

#if not work try tk.update() --> Try anywhere i'm stuck
#debug_variables

class SwapGame(tk.Tk):
    def __init__(self, title: str, size: tuple[int,int]) -> None:
        """
        Initialize the game window with a specified title and size.

        Args:
            title (str): The title to set for the application window.
            size (tuple[int, int]): A tuple specifying the width and height of the window.
                          Example: (width, height)
        """
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])

        #self.player_amount = tk.IntVar()
        #self.player_amount.set(1)

        self.setup_styles()
        self.create_main_menu()
        self.mainloop()

    def setup_styles(self) -> None:
        """
        Configures custom styles using ttk.Style for various widgets.
        """
        style = ttk.Style()
        style.configure('playspace.TFrame', background='#2B3E50') #Playspace
        style.configure('sidebar.TFrame', background='#424242') #Sidebar
        style.configure('return.TButton', background='#424242')
        style.configure('smallbar.TSeparator', background='#2B3E50') #Player card picture separator
        style.configure('playerimage.TLabel', background='#556573') #Player image
        style.configure('nameentry.TEntry', foreground='#A4A7AB') #Name entry with no name
        style.configure('transp.TButton', background='#010101') #Use this color for transparency

    def create_main_menu(self) -> None:
        '''
        Initializes the main menu using a BootMenu instance.
        '''
        self.menu = BootMenu(self)

    def on_new(self) -> None:
        '''
        Destroys the current menu and initializes a new game menu.
        '''
        self.menu.destroy()
        self.ng = NGMenu(self, 0.25)

    def on_load(self) -> None:
        pass

    def on_settings(self) -> None:
        pass

    def on_info(self) -> None:
        pass

    def on_return(self) -> None:
        """
        Clears all child widgets and creates the main menu.
        """        
        for i in self.winfo_children():
            i.destroy()
        self.create_main_menu()

class BootMenu(ttk.Frame):
    def __init__(self, master: ttk.Widget) -> None:
        """
        Initialize a frame for boot menu buttons and info.

        Args:
            master (ttk.Widget): The parent widget to place this frame into.
        """
        super().__init__(master)

        self.pack(expand=True, fill='both', side=tk.TOP)
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Sets up main buttons and an info button with their respective frames.

        - Creates main buttons ('New Game', 'Load Game', 'Settings') and configures them with commands.
        - Loads and resizes an info icon for the info button.
        - Places main buttons in a centered nested frame and info button in a separate frame.
        """
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
    def __init__(self, master: ttk.Widget, rel_width: float) -> None:
        """
        Initialize a player cards template frame.

        Args:
            master (ttk.Widget): The parent widget to place this frame into.
            rel_width (float): Relative width of the frame compared to its parent.

        Attributes:
            rel_width (float): Relative width of the frame.
            pc_amount (tk.IntVar): Number of player cards, initialized to 1.
            playercards (list): List to store instances of PlayerCardsTemplate.
            card_amount (int): Number of player cards, initialized to 1.
            pic_options (list): List of picture options for player avatars.
        """        
        super().__init__(master)
        self.rel_width = rel_width
        self.pc_amount = tk.IntVar(value = 1)
        self.playercards:list[PlayerCardsTemplate] = []
        self.card_amount:int = 1

        #Sets up picture options
        self.pic_options = self.set_picture_options()

        self.pack(expand=True, fill='both')   
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """
        Creates and places the main widgets for the application.

        - Calls `create_playspace()` to create and configure a playspace frame for player cards.
        - Calls `create_sidebar()` to create and configure a sidebar frame with player settings and game controls.
        - Places both frames (`self.sidebar` and `self.playspace`) within the main window using relative positioning.
        """        
        self.create_playspace()
        self.create_sidebar()

        #Placing both frames based on the side_bar relative width
        self.sidebar.place(x=0, y=0, relwidth=self.rel_width, relheight=1)
        self.playspace.place(relx=self.rel_width, y=0, relwidth=(1-self.rel_width), relheight=1)

    def create_sidebar(self) -> None:
        """
        Creates and configures a sidebar with widgets for player settings and game controls.

        - Creates a `ttk.Frame` (`self.sidebar`) with specific border width, style ('sidebar.TFrame'), and relief ('raised').
        - Configures rows and columns within `self.sidebar` for widget layout.
        
        Widgets:
        - Grid 1: Contains a label and a spinbox for selecting the number of players.
        - Grid 2: Includes buttons for saving and loading presets, and starting the game.
        - Grid 3: Holds a button to return to the main interface (`self.master.on_return`).
        """        
        self.sidebar = ttk.Frame(self, borderwidth=10, style='sidebar.TFrame', relief='raised')
        self.sidebar.rowconfigure((0,1,2), weight=1)
        self.sidebar.columnconfigure(0, weight=1)

        #Grid 1 Widgets
        grid1_frame = ttk.Frame(self.sidebar, style='sidebar.TFrame')
        grid1_label = ttk.Label(grid1_frame, text='Number of Players', background='#424242')
        player_number_cbox = ttk.Spinbox(
            grid1_frame, from_=1, to=8, wrap=True, textvariable=self.pc_amount, justify='center',
            command=self.place_pc_customizer, state='readonly'
        )

        #Grid 2 Widgets
        grid2_frame = ttk.Frame(self.sidebar, style='sidebar.TFrame')
        #TBI: save and load presets
        save_preset = ttk.Button(grid2_frame, text='Save as Starting Preset', style='return.TButton')
        load_preset = ttk.Button(grid2_frame, text='Load Starting Preset', style='return.TButton')
        start_game = ttk.Button(grid2_frame, text='Start Game', style='return.TButton', command=self.on_start)

        #Grid 3 Widgets
        grid3_frame = ttk.Frame(self.sidebar)
        return_to_main = ttk.Button(grid3_frame, text='Return', command=self.master.on_return)
        return_to_main.configure(style='return.TButton')

        #Placements
        grid1_frame.grid(row=0)
        grid1_label.pack(anchor='center')
        player_number_cbox.pack(anchor='center')

        grid2_frame.grid(row=1, sticky='we')
        save_preset.pack(anchor='center', fill='x', padx=10, pady=2.5)
        load_preset.pack(anchor='center', fill='x', padx=10, pady=2.5)
        start_game.pack(anchor='center', fill='x', padx=10, pady=2.5)

        grid3_frame.grid(row=2)
        return_to_main.pack(anchor='center')

    def create_playspace(self) -> None:
        """
        Creates and configures a playspace for player cards within the current widget.

        - Creates a ttk.Frame (`self.playspace`) with specific border width, style ('playspace.TFrame'), and relief ('raised').
        """
        self.playspace = ttk.Frame(self, borderwidth=10, style='playspace.TFrame', relief='raised')

        self.playspace.rowconfigure((0,1), weight=1, uniform='a')
        self.playspace.columnconfigure((0,1,2,3), weight=1, uniform='a')

        self.place_pc_customizer()

    def place_pc_customizer(self) -> None:
        """
        Adjusts the number of player card frames in the playspace to match the target amount.

        - Adds frames if the target amount (`self.pc_amount.get()`) is greater than the current amount.
        - Removes frames if the target amount is less than the current amount.
        - Arranges frames in a grid with a maximum of four frames per row.
        """
        b = self.pc_amount.get() #Target Amount
        c = len(self.playspace.winfo_children()) #Current Amount
      
        #Adds or removes ('b' - 'c') frames until 'c' is the same as 'b'
        if self.pc_amount.get() > len(self.playspace.winfo_children()):
            while True:
                if c == b: break
                self.playercards.append(PlayerCardsTemplate(self.playspace, self.pic_options))
                self.playercards[-1].grid(
                    row=0 if (c) <= 3 else 1,
                    column=(c) % 4,
                    sticky='nswe',
                    padx=10, pady=10
                )
                c += 1
        elif self.pc_amount.get() < len(self.playspace.winfo_children()):
            while True:
                if c == b: break
                self.playercards[-1].destroy()
                self.playercards.pop()
                c -= 1

    def set_picture_options(self) -> dict[str, str]:
        """
        Sets up a dictionary with all picture files in the portrait folder.
        
        Only includes files with common picture extensions.
        """
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        pic_choices: dict[str, str] = {pic.stem: str(pic) for pic in Path(PATH_IMG_PRESETS).iterdir() if pic.suffix.lower() in valid_extensions}
        return pic_choices
    
    def on_start(self) -> None:
        for i in self.playercards:
            p_info = i.get_player_info()
            self.cards = (i, p_info)
        print(self.cards)

class PlayerCardsTemplate(ttk.Frame):
    def __init__(self, master: ttk.Widget, pic_dict: dict) -> None:
        """
        Represents a template for player cards with customizable attributes.

        Args:
            master (tk.Widget): The parent widget to place this frame into.
            pic_dict (dict): A dictionary mapping picture options to their file paths.
        """        
        super().__init__(master)
        self.pic_dict = pic_dict
        self.pic_options = list(pic_dict.keys())
        self.image_avatar = None

        #Register command for age digit check
        self.age_cmd = self.register(self.digit_check)

        #Creating canvas for background
        canvasl = tk.Canvas(self, borderwidth=0, highlightthickness=0)

        #Setting background
        pc_bg = Image.open(PATH_PLAYER_BG)
        pc_bg = ImageOps.fit(pc_bg, size=(500,1000)) #random numbers
        self.pc_bg = ImageTk.PhotoImage(master=self, image=pc_bg)
        canvasl.create_image(0, 0, image=self.pc_bg)

        #Placeholder image
        placeholder_avatar = Image.open(PATH_PLACEHOLDER_AVATAR)
        placeholder_avatar = ImageOps.fit(placeholder_avatar, (PLAYER_IMAGE_WIDTH, PLAYER_IMAGE_HEIGHT))
        self.placeholder_avatar = ImageTk.PhotoImage(master=self ,image=placeholder_avatar)

        #Interface widgets
        self.picture_choice = ttk.Combobox(self, state='readonly', values=self.pic_options)
        'Needs to be tk.Label for no border, use highlightthickness and borderwidth'
        self.picture = ttk.Label(self, image=self.placeholder_avatar, style='playerimage.TLabel', relief='ridge')
        smallbar = ttk.Separator(self, orient='horizontal', style='smallbar.TSeparator')
        self.entry_name = ttk.Entry(self, style='nameentry.TEntry')
        self.age_sex_frame = ttk.Frame(self)
        self.sex_gender = ttk.Combobox(self.age_sex_frame, state='readonly', values=['Male', 'Female'], width=7)
        self.how_old = ttk.Entry(self.age_sex_frame, style='nameentry.TEntry')
        self.ethnicity_cbox = ttk.Combobox(self, values=['White', 'Black', 'Hispanic', 'Asian'])
        # Buttons that could be the same one
        self.use_preset = ttk.Button(self, text='Use a Preset', command=self.on_use_preset)
        self.create_custom = ttk.Button(self, text='Create Custom', command=self.on_create_custom)
        # ^Could probably just use one button

        #Picture combobox
        self.bind_choice_combobox(self.custom_picture_change, 'Select Picture')

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
        self.create_custom.configure(style='transp.TButton')
        set_opacity(self.create_custom.winfo_id(), color="#010101")
        
        #Placements
        canvasl.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.picture_choice.pack(padx=30, pady=5)
        self.picture.pack()
        smallbar.pack(padx=15, pady=5, fill='x')
        self.entry_name.pack()
        self.age_sex_frame.pack(padx=18, pady=5)
        self.sex_gender.pack(side=tk.LEFT)
        self.how_old.pack()
        self.ethnicity_cbox.pack(padx=18)
        self.use_preset.pack(padx=18, pady=5, side=tk.BOTTOM, fill='x')

    def bind_choice_combobox(self, command: Callable[[str], None], text: str) -> None:
        """
        Binds a command function to the picture choice combobox selection event.

        Used when starting a new player card instance or when switching from
        preset selection to customizing the player card.

        Args:
            command (Callable[[str], None]): The function to call when a selection is made.
            text (str): The default text to display in the combobox.
        """
        self.picture_choice.bind('<<ComboboxSelected>>', lambda _: command(self.picture_choice.get()))
        self.picture_choice.set(text)

    def custom_picture_change(self, pic_key: str) -> None:
        """
        Changes the displayed picture based on the selected custom picture key.

        Args:
            pic_key (str): The key representing the selected custom picture.
        """
        image1 = Image.open(self.pic_dict[pic_key])
        image1 = ImageOps.fit(image1, (PLAYER_IMAGE_WIDTH, PLAYER_IMAGE_HEIGHT))
        self.image_avatar = ImageTk.PhotoImage(master=self, image=image1)
        self.picture.configure(image=self.image_avatar)

    def preset_fill_data(self, choice_key: str) -> None:
        """
        Fills the player card with data from a selected preset.

        Args:
            choice_key (str): The key representing the selected preset.
        """        
        #Gets the preset tuple from the name
        preset_tuple: tuple[str,int,str,str,str] = presets[presets_dict.get(choice_key)]

        #Changing picture
        image1 = Image.open(preset_tuple[4])
        image1 = ImageOps.fit(image1, (PLAYER_IMAGE_WIDTH, PLAYER_IMAGE_HEIGHT))
        self.image_avatar = ImageTk.PhotoImage(master=self, image=image1)
        self.picture.configure(image=self.image_avatar)

        #Setting the rest of the info
        self.clear_entry(self.entry_name)
        self.clear_entry(self.how_old)
        self.entry_name.delete(0, tk.END) #Redundant but necessary for now      I don't want to do self.master.master.style.lookup
        self.how_old.delete(0, tk.END) #Redundant but necessary for now         ^^
        self.entry_name.insert(0, preset_tuple[0])
        self.how_old.insert(0, preset_tuple[1])
        self.sex_gender.set(preset_tuple[2])
        self.ethnicity_cbox.set(preset_tuple[3])

    def clear_entry(self, widget: ttk.Widget) -> None:
        """
        Clears and initializes an entry widget.

        Args:
            widget (tk.Widget): The entry widget to clear.
        """        
        if widget is self.entry_name and not self.name_touched:
            self.clear_entry_meta(widget)
            self.name_touched = True
        elif widget is self.how_old and not self.age_touched:
            self.clear_entry_meta(widget)
            self.age_touched = True

            #Starts digit validation when focused
            self.how_old.configure(validate='key', validatecommand=(self.age_cmd, '%P'))

    def clear_entry_meta(self, widget: ttk.Widget) -> None:
        """
        Clears and initializes an entry widget when focus is lost.

        Args:
            widget (tk.Widget): The entry widget to clear.
        """        
        widget.delete(0, tk.END)
        widget.configure(style='TEntry')
        widget.bind('<FocusOut>', lambda _: self.remap_entry(widget))

    def remap_entry(self, widget:ttk.Widget) -> None:
        """
        Restores placeholder text to an entry widget when focus is lost.

        Args:
            widget (tk.Widget): The entry widget to restore.
        """        
        if widget is self.entry_name and self.entry_name.get() == '':
            self.restore_placeholder(widget, 'Name')
            self.name_touched = False
        elif widget is self.how_old and self.how_old.get() == '':
            #Remove digit validation after losing focus
            self.how_old.configure(validate='none', validatecommand='')

            self.restore_placeholder(widget, 'Age')
            self.age_touched = False

    def restore_placeholder(self, widget: ttk.Widget, text: str) -> None:
        """
        Restores a placeholder text and style to an entry widget.

        Args:
            widget (tk.Widget): The entry widget to restore.
            text (str): The placeholder text to insert.
        """        
        widget.configure(style='nameentry.TEntry')
        widget.insert(0, text)
        widget.bind('<FocusIn>', lambda _: self.clear_entry(widget))

    def digit_check(self, p: str) -> bool:
        """
        Checks if a string consists of digits.

        Args:
            p (str): The string to check.

        Returns:
            bool: True if the string consists only of digits or is empty, False otherwise.
        """        
        return (str.isdigit(p) or p == '')

    def on_use_preset(self) -> None:
        """
        Prepares the player card for using a preset configuration.
        """        
        #Replaces button
        self.use_preset.pack_forget()
        self.create_custom.pack(padx=18, pady=5, side=tk.BOTTOM, fill='x') 

        #New values for pic choice
        self.picture_choice.configure(values=[x[0] for x in presets])
        self.bind_choice_combobox(self.preset_fill_data, 'Select Preset')

        self.reset_other_choices()

    def on_create_custom(self) -> None:
        """
        Prepares the player card for creating a custom configuration.
        """

        #Replaces button
        self.create_custom.pack_forget()
        self.use_preset.pack(padx=18, pady=5, side=tk.BOTTOM, fill='x')

        self.picture_choice.configure(values=self.pic_options)
        self.bind_choice_combobox(self.custom_picture_change, 'Select Picture')

        self.reset_other_choices()

    def reset_other_choices(self) -> None:
        """
        Resets other choices in the player card to default values.
        """

        #Reset picture
        self.picture.configure(image=self.placeholder_avatar)
        #Empty name
        self.entry_name.delete(0, tk.END)
        self.remap_entry(self.entry_name)
        #Empty gender
        self.sex_gender.set('Gender')
        #Empty age
        self.how_old.delete(0, tk.END)
        self.remap_entry(self.how_old)
        #Empty race
        self.ethnicity_cbox.set('Ethnicity')

    def get_player_info(self) -> dict:
        """
        Fetches player data and returns it as a dictionary.

        :return: Dictionary containing player information.
        """
        p_info = {
            'avatar' : {
                'object' : self.image_avatar if self.picture_choice.get() not in ('Select Picture', 'Select Preset') else self.placeholder_avatar,
                'path' : self.get_player_pic_path()
                },
            'name' : self.entry_name.get() if self.entry_name.get() != 'Name' else None, #Sends empty if no name set
            'gender' : self.sex_gender.get() if self.sex_gender.get() != 'Gender' else None, #Sends empty if not selected gender
            'age' : int(self.how_old.get()) if self.how_old.get() != 'Age' and int(self.how_old.get()) >= 18 else None, #Temporary age logic, needs to happen when start button is pressed
            'ethnicity' : self.ethnicity_cbox.get() if self.ethnicity_cbox.get() != 'Ethnicity' else None #Sends empty if not set ethnicity
        }
        return p_info

    def get_player_pic_path(self) -> str:
        """
        Retrieves the file path for the selected player picture choice.

        Returns:
            str: File path corresponding to the selected picture choice.
        """
        choice = self.picture_choice.get()
        pic_path = self.pic_dict.get(choice, presets_dict.get(choice, PATH_PLACEHOLDER_AVATAR))
        return pic_path

class IGPlayerCard(ttk.Frame):
    def __init__(self, master: tk.Widget, player_info: dict) -> None:
        super().__init__(master)

game = SwapGame('TC\'s Swap "Simmer"', (1000,700))
