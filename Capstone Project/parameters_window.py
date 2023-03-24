import settings
import simulation_window
import tkinter
import tkinter.filedialog as filemanager
import os
import pickle
import tktooltip


def popup(root, message):
    """Display a message as a popup notification above the root window"""
    popup_win = tkinter.Toplevel(root)

    display_message = tkinter.Label(popup_win, text=message)
    display_message.pack(padx=settings.x_pad_both, pady=settings.y_pad_both)
    close_win = tkinter.Button(popup_win,
                               text="OK",
                               command=popup_win.destroy,
                               height=settings.button_height,
                               width=settings.button_width)
    center_window(popup_win)  # center popup!
    close_win.pack()


def center_window(window):
    """Centers the given tkinter window on the screen"""
    # inspiration: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    window.update_idletasks()  # required to ensure winfo width and height queries return accurate values

    # calculate x, y coordinates for top left corner of centered window
    w_height = window.winfo_screenheight()
    x_coord = window.winfo_screenwidth() // 2 - window.winfo_width() // 2
    y_coord = w_height // 2 - window.winfo_height() // 2
    y_coord = y_coord - w_height // 6  # move window up slightly

    # geometry method: window.geometry(f'{width}x{height}+{x}+{y}')
    # where {width}x{height} is window height and width
    # and +{x}+{y} are the x and y coordinates of the window's top left corner
    window.geometry("+" + str(x_coord) + "+" + str(y_coord))


def change_to_parameters(root, organisms, prey_attributes, pred_attributes, initialize=False):
    """Build Parameters screen"""
    # remove any existing widgets
    for child in root.winfo_children():
        child.destroy()

    # -----------------------------------------------------------------------------
    # HELP menu
    # -----------------------------------------------------------------------------
    menu = tkinter.Menu(root)
    help_menu = tkinter.Menu(menu, tearoff=0)
    root.config(pady=settings.y_pad, menu=menu)

    def show_help():
        """Displays a popup when help menu is clicked"""
        popup(root, "Welcome to A-Life Challenge Help!\n\n"
                    "PARAMETER WINDOW\n"
                    "Hover over any label or field to see tooltips,\n"
                    "including minimum/maximum values.\n\n"
                    "START\n"
                    "When desired parameters are entered, \n"
                    "press start button to begin simulation.\n\n"
                    "LOAD\n"
                    "To start a simulation from a saved state, \n"
                    "press Load and select the save file.")

    # ------------------------------
    # help label
    # ------------------------------
    help_menu.add_command(label="Show Help", command=show_help)
    menu.add_cascade(menu=help_menu, label="Help")

    # -----------------------------------------------------------------------------
    # PREY frame
    # -----------------------------------------------------------------------------
    prey_frame = tkinter.Frame(root,
                               width=settings.screen_size,
                               height=settings.screen_size/2,
                               highlightbackground=settings.prey_color,
                               highlightthickness=2)
    prey_frame.pack(side="top", anchor="n")

    prey_main_label = tkinter.Label(prey_frame,
                                    text="Prey Parameters",
                                    font='Calibri 12 underline',
                                    height=2)
    prey_main_label.grid(row=0, column=0, sticky="w", padx=settings.x_pad_left)
    tktooltip.ToolTip(prey_main_label, msg=settings.tooltip["prey_main"], delay=settings.delay_short)

    # -------------------------------
    # labels for text entry boxes
    # -------------------------------
    # population
    prey_nostart_label = tkinter.Label(prey_frame, text="Population")
    prey_nostart_label.grid(row=1, column=0, sticky="w", padx=settings.x_pad_left)
    tktooltip.ToolTip(prey_nostart_label, msg=settings.tooltip["prey_population"], delay=settings.delay_short)

    # health
    prey_health_label = tkinter.Label(prey_frame, text="Health")
    prey_health_label.grid(row=1, column=1, sticky="w")
    tktooltip.ToolTip(prey_health_label, msg=settings.tooltip["prey_health"], delay=settings.delay_short)

    # speed
    prey_speed_label = tkinter.Label(prey_frame, text="Speed")
    prey_speed_label.grid(row=1, column=2, sticky="w")
    tktooltip.ToolTip(prey_speed_label, msg=settings.tooltip["prey_speed"], delay=settings.delay_short)

    # damage
    prey_damage_label = tkinter.Label(prey_frame, text="Damage")
    prey_damage_label.grid(row=3, column=0, sticky="w", padx=settings.x_pad_left, pady=settings.y_pad_top)
    tktooltip.ToolTip(prey_damage_label, msg=settings.tooltip["prey_damage"], delay=settings.delay_short)

    # birth rate
    prey_birth_rate_label = tkinter.Label(prey_frame, text="Birth Rate")
    prey_birth_rate_label.grid(row=3, column=1, sticky="w", pady=settings.y_pad_top)
    tktooltip.ToolTip(prey_birth_rate_label, msg=settings.tooltip["prey_birth_rate"], delay=settings.delay_short)

    # mutation rate
    prey_mutation_rate_label = tkinter.Label(prey_frame, text="Mutation Rate")
    prey_mutation_rate_label.grid(row=3, column=2, sticky="w", pady=settings.y_pad_top)
    tktooltip.ToolTip(prey_mutation_rate_label,
                      msg=settings.tooltip["prey_mutation_rate"], delay=settings.delay_short)

    # -------------------------------
    # text entry boxes
    # -------------------------------
    # population
    prey_population_entry = tkinter.Entry(prey_frame)
    prey_population_entry.insert(0, prey_attributes["population"])
    prey_population_entry.grid(row=2, column=0, padx=settings.x_pad_both)
    tktooltip.ToolTip(prey_population_entry, msg=settings.tooltip["prey_population"], delay=settings.delay_short)

    # health
    prey_health_entry = tkinter.Entry(prey_frame)
    prey_health_entry.insert(0, prey_attributes["health"])
    prey_health_entry.grid(row=2, column=1, padx=settings.x_pad_right)
    tktooltip.ToolTip(prey_health_entry, msg=settings.tooltip["prey_health"], delay=settings.delay_short)

    # speed
    prey_speed_entry = tkinter.Entry(prey_frame)
    prey_speed_entry.insert(0, prey_attributes["speed"])
    prey_speed_entry.grid(row=2, column=2, padx=settings.x_pad_right)
    tktooltip.ToolTip(prey_speed_entry, msg=settings.tooltip["prey_speed"], delay=settings.delay_short)

    # damage
    prey_damage_entry = tkinter.Entry(prey_frame)
    prey_damage_entry.insert(0, prey_attributes["damage"])
    prey_damage_entry.grid(row=4, column=0, padx=settings.x_pad_both, pady=settings.y_pad_bot)
    tktooltip.ToolTip(prey_damage_entry, msg=settings.tooltip["prey_damage"], delay=settings.delay_short)

    # birth rate
    prey_birth_rate_entry = tkinter.Entry(prey_frame)
    prey_birth_rate_entry.insert(0, prey_attributes["birth_rate"])
    prey_birth_rate_entry.grid(row=4, column=1, padx=settings.x_pad_right, pady=settings.y_pad_bot)
    tktooltip.ToolTip(prey_birth_rate_entry, msg=settings.tooltip["prey_birth_rate"], delay=settings.delay_short)

    # mutation rate
    prey_mutation_rate_entry = tkinter.Entry(prey_frame)
    prey_mutation_rate_entry.insert(0, prey_attributes["mutation_rate"])
    prey_mutation_rate_entry.grid(row=4, column=2, padx=settings.x_pad_right, pady=settings.y_pad_bot)
    tktooltip.ToolTip(prey_mutation_rate_entry,
                      msg=settings.tooltip["prey_mutation_rate"], delay=settings.delay_short)

    # -----------------------------------------------------------------------------
    # pad frame
    # -----------------------------------------------------------------------------
    pad_frame_1 = tkinter.Frame(root, height=settings.button_frame_height)
    pad_frame_1.pack(side="top")

    # -----------------------------------------------------------------------------
    # PREDATOR frame
    # -----------------------------------------------------------------------------
    pred_frame = tkinter.Frame(root,
                               width=settings.screen_size,
                               height=settings.screen_size / 2,
                               highlightbackground=settings.pred_color,
                               highlightthickness=2)
    pred_frame.pack(side="top", anchor="n")

    pred_main_label = tkinter.Label(pred_frame,
                                    text="Predator Parameters",
                                    font='Calibri 12 underline',
                                    height=2)
    pred_main_label.grid(row=0, column=0, sticky="w", padx=settings.x_pad_left)
    tktooltip.ToolTip(pred_main_label, msg=settings.tooltip["pred_main"], delay=settings.delay_short)

    # -------------------------------
    # labels for text entry boxes
    # -------------------------------
    # population
    pred_nostart_label = tkinter.Label(pred_frame, text="Population")
    pred_nostart_label.grid(row=1, column=0, sticky="w", padx=settings.x_pad_left)
    tktooltip.ToolTip(pred_nostart_label, msg=settings.tooltip["pred_population"], delay=settings.delay_short)

    # health
    pred_health_label = tkinter.Label(pred_frame, text="Health")
    pred_health_label.grid(row=1, column=1, sticky="w")
    tktooltip.ToolTip(pred_health_label, msg=settings.tooltip["pred_health"], delay=settings.delay_short)

    # speed
    pred_speed_label = tkinter.Label(pred_frame, text="Speed")
    pred_speed_label.grid(row=1, column=2, sticky="w")
    tktooltip.ToolTip(pred_speed_label, msg=settings.tooltip["pred_speed"], delay=settings.delay_short)

    # damage
    pred_damage_label = tkinter.Label(pred_frame, text="Damage")
    pred_damage_label.grid(row=3, column=0, sticky="w", padx=settings.x_pad_left, pady=settings.y_pad_top)
    tktooltip.ToolTip(pred_damage_label, msg=settings.tooltip["pred_damage"], delay=settings.delay_short)

    # birth rate
    pred_birth_rate_label = tkinter.Label(pred_frame, text="Birth Rate")
    pred_birth_rate_label.grid(row=3, column=1, sticky="w", pady=settings.y_pad_top)
    tktooltip.ToolTip(pred_birth_rate_label, msg=settings.tooltip["pred_birth_rate"], delay=settings.delay_short)

    # mutation rate
    pred_mutation_rate_label = tkinter.Label(pred_frame, text="Mutation Rate")
    pred_mutation_rate_label.grid(row=3, column=2, sticky="w", pady=settings.y_pad_top)
    tktooltip.ToolTip(pred_mutation_rate_label,
                      msg=settings.tooltip["pred_mutation_rate"], delay=settings.delay_short)

    # -------------------------------
    # text entry boxes
    # -------------------------------
    # population
    pred_population_entry = tkinter.Entry(pred_frame)
    pred_population_entry.insert(0, pred_attributes["population"])
    pred_population_entry.grid(row=2, column=0, padx=settings.x_pad_both)
    tktooltip.ToolTip(pred_population_entry, msg=settings.tooltip["pred_population"], delay=settings.delay_short)

    # health
    pred_health_entry = tkinter.Entry(pred_frame)
    pred_health_entry.insert(0, pred_attributes["health"])
    pred_health_entry.grid(row=2, column=1, padx=settings.x_pad_right)
    tktooltip.ToolTip(pred_health_entry, msg=settings.tooltip["pred_health"], delay=settings.delay_short)

    # speed
    pred_speed_entry = tkinter.Entry(pred_frame)
    pred_speed_entry.insert(0, pred_attributes["speed"])
    pred_speed_entry.grid(row=2, column=2, padx=settings.x_pad_right)
    tktooltip.ToolTip(pred_speed_entry, msg=settings.tooltip["pred_speed"], delay=settings.delay_short)

    # damage
    pred_damage_entry = tkinter.Entry(pred_frame)
    pred_damage_entry.insert(0, pred_attributes["damage"])
    pred_damage_entry.grid(row=4, column=0, padx=settings.x_pad_both, pady=settings.y_pad_bot)
    tktooltip.ToolTip(pred_damage_entry, msg=settings.tooltip["pred_damage"], delay=settings.delay_short)

    # birth rate
    pred_birth_rate_entry = tkinter.Entry(pred_frame)
    pred_birth_rate_entry.insert(0, pred_attributes["birth_rate"])
    pred_birth_rate_entry.grid(row=4, column=1, padx=settings.x_pad_right, pady=settings.y_pad_bot)
    tktooltip.ToolTip(pred_birth_rate_entry, msg=settings.tooltip["pred_birth_rate"], delay=settings.delay_short)

    # mutation rate
    pred_mutation_rate_entry = tkinter.Entry(pred_frame)
    pred_mutation_rate_entry.insert(0, pred_attributes["mutation_rate"])
    pred_mutation_rate_entry.grid(row=4, column=2, padx=settings.x_pad_right, pady=settings.y_pad_bot)
    tktooltip.ToolTip(pred_mutation_rate_entry,
                      msg=settings.tooltip["pred_mutation_rate"], delay=settings.delay_short)

    # -----------------------------------------------------------------------------
    # pad frame
    # -----------------------------------------------------------------------------
    pad_frame_1 = tkinter.Frame(root, height=settings.button_frame_height//2)
    pad_frame_1.pack(side="top", anchor="n")

    # -----------------------------------------------------------------------------
    # button frame
    # -----------------------------------------------------------------------------
    # create button frame
    button_frame = tkinter.Frame(root, width=settings.screen_size, height=settings.button_frame_height)
    button_frame.pack(side="top")

    # ------------------------------
    # start button
    # ------------------------------
    def start():
        """Get data from input fields and start simulation"""
        int_error = " error.\n\nPlease enter an integer."
        float_error = " error.\n\nPlease enter a float."

        # --------------------------------------
        # grab input from PREY entry fields
        # --------------------------------------
        # --------------------
        # population
        temp_population = prey_attributes["population"]
        try:
            prey_attributes["population"] = int(prey_population_entry.get())

        except ValueError:
            popup(root, "Prey population" + int_error)
            return

        # display popup warning for negative values
        if prey_attributes["population"] < 0:
            prey_attributes["population"] = temp_population  # reset value
            popup(root, "Error.\n\nPrey population must be a positive integer.")
            return

        # --------------------
        # health
        temp_health = prey_attributes["health"]
        try:
            prey_attributes["health"] = int(prey_health_entry.get())

        except ValueError:
            popup(root, "Prey health" + int_error)
            return

        # check for negative value
        if prey_attributes["health"] < 1:
            prey_attributes["health"] = temp_health
            popup(root, "Error.\n\nPrey health must be >= 1.")
            return

        # --------------------
        # speed
        temp_speed = prey_attributes["speed"]
        try:
            prey_attributes["speed"] = int(prey_speed_entry.get())

        except ValueError:
            popup(root, "Prey speed" + int_error)
            return

        # check for negative value
        if prey_attributes["speed"] < 0 or prey_attributes["speed"] > 100:
            prey_attributes["speed"] = temp_speed
            popup(root, "Error.\n\nPrey speed must be between [0, 100].")
            return

        # --------------------
        # damage
        temp_damage = prey_attributes["damage"]
        try:
            prey_attributes["damage"] = int(prey_damage_entry.get())

        except ValueError:
            popup(root, "Prey damage" + int_error)
            return

        # check for negative value
        if prey_attributes["damage"] < 0:
            prey_attributes["damage"] = temp_damage
            popup(root, "Error.\n\nPrey damage must be a positive integer.")
            return

        # --------------------
        # birth rate
        temp_birth_rate = prey_attributes["birth_rate"]
        try:
            prey_attributes["birth_rate"] = float(prey_birth_rate_entry.get())

        except ValueError:
            popup(root, "Prey birth rate" + float_error)
            return

        # check if birth rate is too high
        if prey_attributes["birth_rate"] > 0.01 or prey_attributes["birth_rate"] <= 0:
            prey_attributes["birth_rate"] = temp_birth_rate  # reset birth rate to previous
            popup(root, "Error.\n\nPrey birth rate must be between (0, 0.01].")
            return

        # --------------------
        # mutation rate
        temp_mutation_rate = prey_attributes["mutation_rate"]
        try:
            prey_attributes["mutation_rate"] = float(prey_mutation_rate_entry.get())

        except ValueError:
            popup(root, "Prey mutation rate" + float_error)
            return

        # check for negative value
        if prey_attributes["mutation_rate"] < 0:
            prey_attributes["mutation_rate"] = temp_mutation_rate
            popup(root, "Error.\n\nPrey mutation rate must be positive.")
            return

        # --------------------------------------
        # grab input from PREDATOR entry fields
        # --------------------------------------
        # --------------------
        # population
        temp_population = pred_attributes["population"]
        try:
            pred_attributes["population"] = int(pred_population_entry.get())

        except ValueError:
            popup(root, "Predator population" + int_error)
            return

        # check for negative value
        if pred_attributes["population"] < 0:
            pred_attributes["population"] = temp_population
            popup(root, "Error.\n\nPredator population must be a positive integer.")
            return

        # --------------------
        # health
        temp_health = pred_attributes["health"]
        try:
            pred_attributes["health"] = int(pred_health_entry.get())

        except ValueError:
            popup(root, "Predator health" + int_error)
            return

        # check for negative value
        if pred_attributes["health"] < 1:
            pred_attributes["health"] = temp_health
            popup(root, "Error.\n\nPredator health must be >= 1.")
            return

        # --------------------
        # speed
        temp_speed = pred_attributes["speed"]
        try:
            pred_attributes["speed"] = int(pred_speed_entry.get())

        except ValueError:
            popup(root, "Predator speed" + int_error)
            return

        # check for negative value
        if pred_attributes["speed"] < 0 or pred_attributes["speed"] > 100:
            pred_attributes["speed"] = temp_speed
            popup(root, "Error.\n\nPredator speed must be between [0, 100].")
            return

        # --------------------
        # damage
        temp_damage = pred_attributes["damage"]
        try:
            pred_attributes["damage"] = int(pred_damage_entry.get())

        except ValueError:
            popup(root, "Predator damage" + int_error)
            return

        # check for negative value
        if pred_attributes["damage"] < 0:
            pred_attributes["damage"] = temp_damage
            popup(root, "Error.\n\nPredator damage must be positive.")
            return

        # --------------------
        # birth rate
        temp_birth_rate = pred_attributes["birth_rate"]
        try:
            pred_attributes["birth_rate"] = float(pred_birth_rate_entry.get())

        except ValueError:
            popup(root, "Predator birth rate" + float_error)
            return

        # check if birth rate is too high
        if pred_attributes["birth_rate"] > 0.01 or pred_attributes["birth_rate"] <= 0:
            pred_attributes["birth_rate"] = temp_birth_rate  # reset birth rate to previous
            popup(root, "Error.\n\nPredator birth rate must be between (0, 0.01].")
            return

        # --------------------
        # mutation rate
        temp_mutation_rate = pred_attributes["mutation_rate"]
        try:
            pred_attributes["mutation_rate"] = float(pred_mutation_rate_entry.get())

        except ValueError:
            popup(root, "Predator mutation rate" + float_error)
            return

        # check for negative value
        if pred_attributes["mutation_rate"] < 0:
            pred_attributes["mutation_rate"] = temp_mutation_rate
            popup(root, "Error.\n\nPredator mutation rate must be a positive integer.")
            return

        # ------------------------------
        # change to simulation screen
        # ------------------------------
        simulation_window.change_to_simulation(root, organisms, prey_attributes, pred_attributes)

    start_button = tkinter.Button(button_frame,
                                  text="Start",
                                  command=start,
                                  height=settings.button_height,
                                  width=settings.button_width)
    start_button.pack(side="left")
    tktooltip.ToolTip(start_button,
                      msg=settings.tooltip["start_button"],
                      delay=settings.delay_long)

    # ------------------------------
    # load button
    # ------------------------------
    def load():
        """Load simulation from save file"""
        # get file to load
        file_name = filemanager.askopenfilename(initialfile='a_life_save',
                                                initialdir=os.getcwd(),
                                                filetypes=[('Pickle File', '*.pkl')],
                                                defaultextension='.pkl')
        # if file selected, load data and restart simulation
        if file_name:
            with open(file_name, 'rb') as load_file:
                # check for bad file
                try:
                    pickle_data = pickle.load(load_file)
                except (pickle.UnpicklingError, AttributeError, EOFError, IndexError):
                    popup(root, "Bad file. Please try again.")
                    return
                except ImportError:
                    popup(root, "Error importing module associated with file."
                                "\n\nPlease try again.")
                    return
                except Exception:
                    popup(root, "Unknown error occurred. Please try again.")
                    return

            # switch to simulation window with load data
            simulation_window.change_to_simulation(root,
                                                   organisms,
                                                   settings.prey_attributes,
                                                   settings.pred_attributes,
                                                   pickle_data)

    load_button = tkinter.Button(button_frame,
                                 text="Load",
                                 command=load,
                                 height=settings.button_height,
                                 width=settings.button_width)
    load_button.pack(side="left")
    tktooltip.ToolTip(load_button,
                      msg=settings.tooltip["load_button"],
                      delay=settings.delay_long)

    # -----------------------------------------------------------------------------
    # center tkinter window
    # -----------------------------------------------------------------------------
    if initialize:
        center_window(root)
