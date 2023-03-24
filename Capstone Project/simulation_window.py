import parameters_window
import settings
import organism
import simulation_steps
import statistics
import speed_control
import turtle
import random
import tkinter
import tkinter.filedialog as filemanager
import os
import pickle
import tktooltip

interrupt = False
pause_simulation = False
show_results = True


def create_organism(organisms, screen, identifier, position, destination, attributes, session_stats):
    """Create a new Organism class object with the given parameters and add it to organisms list"""
    organisms.append(organism.Organism(screen, identifier, position, destination, attributes))

    index = len(organisms) - 1

    session_stats.add_organism(organisms[index].get_attributes())
    organisms[index].init_sprite(settings.general["speed"], settings.general["diameter"])


def rand_coords():
    """Returns a list containing random [x, y] coordinates"""
    return [random.uniform(-settings.screen_size/2, settings.screen_size/2),
            random.uniform(-settings.screen_size/2, settings.screen_size/2)]


def initialize_organisms(organisms, screen, prey_attributes, pred_attributes, session_stats):
    """Generate starting Organism objects for prey and predators"""
    # generate initial predator population
    for i in range(pred_attributes["population"]):
        create_organism(organisms, screen, 1, rand_coords(), rand_coords(), pred_attributes, session_stats)

    # initial prey population
    for i in range(prey_attributes["population"]):
        create_organism(organisms, screen, 0, rand_coords(), rand_coords(), prey_attributes, session_stats)


def initialize_organisms_from_save(organisms, sim_screen):
    """Load Organisms from a saved list"""
    for organism_object in organisms:
        organism_object.init_sprite(settings.general["speed"], settings.general["diameter"], sim_screen)


def steps(organisms, session_stats, screen, speed_factors):
    """Run the turn steps for each organism"""
    # auto-update slow_factor
    speed_factors.auto_adjust(session_stats.get_pred_stats()["population"] +
                              session_stats.get_prey_stats()["population"])

    # run all steps for each organism in the list
    i = 0
    while i < len(organisms):

        # step 1
        simulation_steps.set_target(i, organisms, speed_factors)

        # step 2
        simulation_steps.move(i, organisms, speed_factors)

        # step 3
        simulation_steps.battle(i, organisms, speed_factors)

        # step 4
        if simulation_steps.conclude_turn(i, organisms, session_stats, screen, speed_factors):  # if organism hasn't died
            i += 1
    session_stats.next_turn()


def plus_one(one_element_list):
    """Add one to the first element in the list. Great for lazy programmers :-)"""
    one_element_list[0] += 1
    return one_element_list[0]


def change_to_simulation(root, organisms, prey_attributes, pred_attributes, save_data=None):
    """Build simulation screen and run the simulation"""
    global interrupt, pause_simulation, show_results
    interrupt = False
    pause_simulation = False
    current_row = [0]

    # remove any existing widgets
    for child in root.winfo_children():
        child.destroy()

    # track new session statistics
    if save_data is None:
        session_stats = statistics.Statistics(pred_attributes, prey_attributes)
    # otherwise load saved session statistics
    else:
        session_stats = save_data[1]
        session_stats.reset_start_time()  # reset stopwatch

    # track speed factors
    speed_factors = speed_control.SpeedControl(settings.general)

    # -----------------------------------------------------------------------------
    # HELP menu
    # -----------------------------------------------------------------------------
    menu = tkinter.Menu(root)
    help_menu = tkinter.Menu(menu, tearoff=0)
    root.config(pady=0, width=settings.screen_size*2, menu=menu)

    def show_general_help():
        """Displays general help popup"""
        parameters_window.popup(root, "Welcome to A-Life Challenge Help!\n\n"
                                      "SIMULATION WINDOW\n"
                                      "Hover over any part of the window/button to\n"
                                      "view tooltip help.\n\n"
                                      "ANIMATION SCREEN\n"
                                      "Organism activity is shown in the animation screen.\n"
                                      "Green dots represent PREY. Red dots represent\n"
                                      "PREDATORS.\n\n"
                                      "SESSION STATISTICS\n"
                                      "Current statistics of the simulation are shown in the\n"
                                      "Session Statistics frame. Hover over this frame to\n"
                                      "see a detailed breakdown of each statistic.")

    def show_button_help():
        """Displays button help popup"""
        parameters_window.popup(root, "Welcome to A-Life Challenge Help!\n\n"
                                      "SIMULATION SPEED\n"
                                      "To increase simulation speed, move slider to\n"
                                      "the right. Note: this feature emulates increased\n"
                                      "speeds, but may not result in the same outcome.\n\n"
                                      "PAUSE\n"
                                      "Press the pause button to pause/unpause the\n"
                                      "simulation.\n\n"
                                      "SAVE\n"
                                      "To save the current state of the simulation, press\n"
                                      "the save button. The simulation will pause while\n"
                                      "the save file is being created.\n\n"
                                      "LOAD\n"
                                      "Loads a new simulation from save file. The current\n"
                                      "simulation will not be saved. Simulation paused until\n"
                                      "a file is loaded.\n\n"
                                      "GRAPH RESULTS\n"
                                      "To view plots of the organism population and mutations\n"
                                      "over time, check the \"Show graph results\" box.")

    # ------------------------------
    # help label
    # ------------------------------
    help_menu.add_command(label="General Help", command=show_general_help)
    help_menu.add_command(label="Button Help", command=show_button_help)
    menu.add_cascade(menu=help_menu, label="Help")

    # -----------------------------------------------------------------------------
    # control buttons frame
    # -----------------------------------------------------------------------------
    button_frame = tkinter.Frame(root,
                                 width=settings.screen_size,
                                 height=settings.button_height,
                                 pady=settings.y_pad)
    button_frame.pack(side="bottom", anchor="sw")

    # -------------------------------
    # animation speed slider
    # -------------------------------
    def update_speed(num):
        """Update the simulation speed to reflect slider value"""
        speed_factors.set_fast_forward(int(num))
        print("Speed set to: " + num + ".")

    # speed slider
    speed_slider = tkinter.Scale(button_frame,
                                 command=update_speed,
                                 from_=1,
                                 to=10,
                                 label="Simulation Speed",
                                 showvalue=False,  # turn off current value display
                                 orient="horizontal",
                                 length=200,  # horizontal length of slider in pixels
                                 width=15)  # slider height in pixels
    speed_slider.pack(side="left", padx=(10, 100))
    tktooltip.ToolTip(speed_slider,
                      msg=settings.tooltip["fast_forward"],
                      delay=settings.delay_long)

    # -------------------------------
    # pause button
    # -------------------------------
    def pause():
        """Pause simulation"""
        global pause_simulation

        # toggle pause
        if not pause_simulation:
            pause_simulation = True
        else:
            pause_simulation = False

        # toggle button text
        if pause_text.get() == "Pause":
            pause_text.set("Resume")
        else:
            session_stats.reset_start_time()  # restart stopwatch from current time
            pause_text.set("Pause")

    # create pause button in button frame
    pause_text = tkinter.StringVar()
    pause_button = tkinter.Button(button_frame,
                                  textvariable=pause_text,
                                  command=pause,
                                  height=settings.button_height,
                                  width=settings.button_width)
    pause_button.pack(side="left")
    pause_text.set("Pause")
    tktooltip.ToolTip(pause_button,
                      msg=settings.tooltip["pause_button"],
                      delay=settings.delay_long)

    # -------------------------------
    # save button
    # -------------------------------
    def save():
        """Save current simulation"""
        # open save as filename dialog and save the file name
        # returns empty string on cancel
        file_name = filemanager.asksaveasfilename(initialfile='a_life_save',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[('Pickle File', '*.pkl')],
                                                  defaultextension='.pkl')
        # open the file and pickle the data IF user selected a file name
        if file_name:
            # temporarily clear turtle sprites from Organism objects to prep for pickling
            # can't use copy.deepcopy here since it also employs pickle
            for organism_object in organisms:
                organism_object.clear()
                organism_object.delete_sprite()

            # save current organisms and statistics
            pickle_data = [organisms, session_stats]

            # 'with' automatically error checks and closes file after nested code
            with open(file_name, 'wb') as save_file:
                pickle.dump(pickle_data, save_file, pickle.HIGHEST_PROTOCOL)

            # reinitialize sprites
            for organism_object in organisms:
                organism_object.init_sprite(settings.general["speed"],
                                            settings.general["diameter"],
                                            sim_screen)

        session_stats.reset_start_time()  # restart stopwatch from current time

    # create save button
    save_button = tkinter.Button(button_frame,
                                 text="Save",
                                 command=save,
                                 height=settings.button_height,
                                 width=settings.button_width)
    save_button.pack(side="left")
    tktooltip.ToolTip(save_button,
                      msg=settings.tooltip["save_button"],
                      delay=settings.delay_long)

    # -------------------------------
    # load button
    # -------------------------------
    def load():
        """Load simulation from save file"""
        global interrupt

        # get file to load
        file_name = filemanager.askopenfilename(initialfile='a_life_save',
                                                initialdir=os.getcwd(),
                                                filetypes=[('Pickle File', '*.pkl')],
                                                defaultextension='.pkl')
        # if file selected, load data and restart simulation
        if file_name:
            with open(file_name, 'rb') as load_file:
                try:
                    pickle_data = pickle.load(load_file)
                except (pickle.UnpicklingError, AttributeError, EOFError, IndexError):
                    parameters_window.popup(root, "Bad file. Please try again.")
                    return
                except ImportError:
                    parameters_window.popup(root, "Error importing module associated with file."
                                                  "\n\nPlease try again.")
                    return
                except Exception:
                    parameters_window.popup(root, "Unknown error occurred. Please try again.")
                    return

            # stop running simulation steps and reset variables
            interrupt = True
            sim_screen.resetscreen()
            organisms.clear()

            # restart simulation window
            change_to_simulation(root,
                                 organisms,
                                 settings.prey_attributes,
                                 settings.pred_attributes,
                                 pickle_data)

        # load aborted, restart stopwatch from current time
        else:
            session_stats.reset_start_time()

    # add load button to button frame
    load_button = tkinter.Button(button_frame,
                                 text="Load",
                                 command=load,
                                 height=settings.button_height,
                                 width=settings.button_width)
    load_button.pack(side="left")
    tktooltip.ToolTip(load_button,
                      msg=settings.tooltip["load_button"],
                      delay=settings.delay_long)

    # -------------------------------
    # stop button
    # -------------------------------
    def quit_simulation():
        """Stop turtle animation and simulation turns, then switch to parameters window"""
        global interrupt, show_results

        # stop running simulation steps and reset variables
        # may need to check interrupt in each turn step (if steps are executed after next line of code, returns errors)
        interrupt = True
        sim_screen.resetscreen()  # DO NOT USE bye() - cannot restart turtle graphics after bye()
        organisms.clear()
        if show_results:
            session_stats.log_population()

        # swap back to parameters window
        parameters_window.change_to_parameters(root,
                                               organisms,
                                               settings.prey_attributes,
                                               settings.pred_attributes)

    # add stop button to button frame
    stop_button = tkinter.Button(button_frame,
                                 text="Stop",
                                 command=quit_simulation,
                                 height=settings.button_height,
                                 width=settings.button_width)
    stop_button.pack(side="left", anchor="e", padx=(50, 0))
    tktooltip.ToolTip(stop_button,
                      msg=settings.tooltip["stop_button"],
                      delay=settings.delay_long)

    # -------------------------------
    # show session results check box
    # -------------------------------
    def show_graph():
        """Toggles the show_results global variable:
        when True, graph displayed after stop button is pressed,
        when False, graph is not displayed"""
        global show_results

        # toggle show results
        if graph_checkbox_var.get():
            show_results = True
        else:
            show_results = False

    # add checkbox to button_frame
    graph_checkbox_var = tkinter.BooleanVar()
    graph_checkbox = tkinter.Checkbutton(button_frame,
                                         text="Show graph results",
                                         command=show_graph,
                                         variable=graph_checkbox_var,
                                         onvalue=True,
                                         offvalue=False)
    graph_checkbox.pack(side="left", anchor="e", padx=settings.x_pad_left)
    # auto check button when show_results is True
    if show_results:
        graph_checkbox.select()

    tktooltip.ToolTip(graph_checkbox,
                      msg=settings.tooltip["graph_checkbox"],
                      delay=settings.delay_short)

    # -----------------------------------------------------------------------------
    # sim screen frame
    # -----------------------------------------------------------------------------
    # basic canvas for screen
    sim_canvas = tkinter.Canvas(root,
                                width=settings.screen_size,
                                height=settings.screen_size,
                                highlightbackground="black",
                                highlightthickness=1)
    sim_canvas.pack(side="left", anchor="ne", padx=settings.x_pad//4, pady=settings.y_pad//3)

    # setup turtle screen
    sim_screen = turtle.TurtleScreen(sim_canvas)
    sim_screen.tracer(0, 0)  # requires update method to be called on screen
    tktooltip.ToolTip(sim_canvas,
                      msg=settings.tooltip["sim_screen"],
                      delay=settings.delay_short)

    # initialize list of organisms - must happen before stats frame is populated
    if save_data is None:
        initialize_organisms(organisms, sim_screen, prey_attributes, pred_attributes, session_stats)
    else:
        organisms = save_data[0]
        initialize_organisms_from_save(organisms, sim_screen)

    # -----------------------------------------------------------------------------
    # live stats frame
    # -----------------------------------------------------------------------------
    side_frame = tkinter.Frame(root,
                               width=settings.screen_size//2,
                               highlightbackground="black",
                               highlightthickness=1)
    side_frame.pack(side="left", anchor="nw", padx=settings.x_pad//4, pady=settings.y_pad//3)
    tktooltip.ToolTip(side_frame,
                      msg=settings.tooltip["stats_frame"],
                      delay=settings.delay_long)

    # -------------------------------
    # get starting statistics
    # -------------------------------
    pred_stats = session_stats.get_pred_stats()
    prey_stats = session_stats.get_prey_stats()
    general_stats = session_stats.get_general_stats()

    # -------------------------------
    # window title
    # -------------------------------
    elapsed_time_label = tkinter.Label(side_frame,
                                       text="Session Statistics",
                                       font='Calibri 12 underline',
                                       height=2)
    elapsed_time_label.grid(row=plus_one(current_row),
                            column=0,
                            padx=settings.x_pad_right)

    # -------------------------------
    # total population
    # -------------------------------
    # population label
    tot_pop_label = tkinter.Label(side_frame, text="Total Population:")
    tot_pop_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show total population
    tot_pop_text = tkinter.StringVar(value=str(prey_stats["population"] + pred_stats["population"]))
    tot_pop = tkinter.Label(side_frame, textvariable=tot_pop_text)
    tot_pop.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # turn number
    # -------------------------------
    # label
    turn_number_label = tkinter.Label(side_frame, text="Turn Number:")
    turn_number_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show turn number
    turn_number_text = tkinter.StringVar(value=general_stats["turn"])
    turn_number = tkinter.Label(side_frame, textvariable=turn_number_text)
    turn_number.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # elapsed time
    # -------------------------------
    # label
    elapsed_time_label = tkinter.Label(side_frame, text="Time Elapsed:")
    elapsed_time_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # display time using Statistics class method
    elapsed_time_text = tkinter.StringVar(value=session_stats.get_time_str())
    elapsed_time = tkinter.Label(side_frame, textvariable=elapsed_time_text)
    elapsed_time.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # prey label
    # -------------------------------
    # prey label
    prey_label = tkinter.Label(side_frame, text="Prey", font='Calibri 11 underline', fg='green')
    prey_label.grid(row=plus_one(current_row), column=0, sticky="w", pady=settings.y_pad_top)

    # -------------------------------
    # prey population
    # -------------------------------
    # prey population label
    prey_pop_label = tkinter.Label(side_frame, text="Population:")
    prey_pop_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show prey population
    prey_pop_text = tkinter.StringVar(value=prey_stats["population"])
    prey_pop = tkinter.Label(side_frame, textvariable=prey_pop_text)
    prey_pop.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # prey generation
    # -------------------------------
    # prey generation label
    prey_gen_label = tkinter.Label(side_frame, text="Generation:")
    prey_gen_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show prey generation
    prey_gen_text = tkinter.StringVar(value=prey_stats["generation"])
    prey_gen = tkinter.Label(side_frame, textvariable=prey_gen_text)
    prey_gen.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # prey births
    # -------------------------------
    # prey births label
    prey_births_label = tkinter.Label(side_frame, text="Births:")
    prey_births_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show prey births
    prey_births_text = tkinter.StringVar(value=prey_stats["births"])
    prey_births = tkinter.Label(side_frame, textvariable=prey_births_text)
    prey_births.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # prey deaths
    # -------------------------------
    # prey deaths label
    prey_deaths_label = tkinter.Label(side_frame, text="Deaths:")
    prey_deaths_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show prey deaths
    prey_deaths_text = tkinter.StringVar(value=prey_stats["deaths"])
    prey_deaths = tkinter.Label(side_frame, textvariable=prey_deaths_text)
    prey_deaths.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # predator label
    # -------------------------------
    # predator label
    pred_label = tkinter.Label(side_frame, text="Predators", font='Calibri 11 underline', fg='firebrick')
    pred_label.grid(row=plus_one(current_row), column=0, sticky="w", pady=settings.y_pad_top)

    # -------------------------------
    # predator population
    # -------------------------------
    # predator population label
    pred_pop_label = tkinter.Label(side_frame, text="Population:")
    pred_pop_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show prey population
    pred_pop_text = tkinter.StringVar(value=pred_stats["population"])
    pred_pop = tkinter.Label(side_frame, textvariable=pred_pop_text)
    pred_pop.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # pred generation
    # -------------------------------
    # pred generation label
    pred_gen_label = tkinter.Label(side_frame, text="Generation:")
    pred_gen_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show pred generation
    pred_gen_text = tkinter.StringVar(value=pred_stats["generation"])
    pred_gen = tkinter.Label(side_frame, textvariable=pred_gen_text)
    pred_gen.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # pred births
    # -------------------------------
    # predator births label
    pred_births_label = tkinter.Label(side_frame, text="Births:")
    pred_births_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show pred births
    pred_births_text = tkinter.StringVar(value=pred_stats["births"])
    pred_births = tkinter.Label(side_frame, textvariable=pred_births_text)
    pred_births.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # pred deaths
    # -------------------------------
    # predator deaths label
    pred_deaths_label = tkinter.Label(side_frame, text="Deaths:")
    pred_deaths_label.grid(row=plus_one(current_row), column=0, sticky="w")

    # show pred deaths
    pred_deaths_text = tkinter.StringVar(value=pred_stats["deaths"])
    pred_deaths = tkinter.Label(side_frame, textvariable=pred_deaths_text)
    pred_deaths.grid(row=current_row[0], column=1, sticky="w")

    # -------------------------------
    # blank row
    # -------------------------------
    # blank
    blank_row_label = tkinter.Label(side_frame, text="")
    blank_row_label.grid(row=plus_one(current_row), column=1, sticky="w", padx=settings.x_pad_right_super)

    def update_stats_frame(stats_object):
        """Update the values in the statistics frame"""
        cur_pred_stats = stats_object.get_pred_stats()
        cur_prey_stats = stats_object.get_prey_stats()
        cur_general_stats = stats_object.get_general_stats()

        # update total population
        tot_pop_text.set(str(cur_prey_stats["population"] + cur_pred_stats["population"]))

        # update turn number
        turn_number_text.set(str(cur_general_stats["turn"]))

        # update elapsed time
        elapsed_time_text.set(session_stats.get_time_str())

        # update prey stats
        prey_pop_text.set(str(cur_prey_stats["population"]))
        prey_gen_text.set(str(cur_prey_stats["generation"]))
        prey_births_text.set(str(cur_prey_stats["births"]))
        prey_deaths_text.set(str(cur_prey_stats["deaths"]))

        # update predator stats
        pred_pop_text.set(str(cur_pred_stats["population"]))
        pred_gen_text.set(str(cur_pred_stats["generation"]))
        pred_births_text.set(str(cur_pred_stats["births"]))
        pred_deaths_text.set(str(cur_pred_stats["deaths"]))

    # -----------------------------------------------------------------------------
    # run simulation
    # -----------------------------------------------------------------------------
    # run simulation indefinitely
    while True:
        # exit simulation when stop button pressed
        if interrupt:
            break

        # unless paused, run steps
        if not pause_simulation:

            steps(organisms, session_stats, sim_screen, speed_factors)
            update_stats_frame(session_stats)

        # still need to update the screen even if paused
        # otherwise, program locks up
        sim_screen.update()
