import math

general = {"diameter": 10,  # turtle diameter
           "speed": 10,  # animation speed
           "slow_factor": 30,  # controls movement speed of turtles
           "timer": int(1000 // 30),  # ontimer() turtle delay timer
           "fast_forward": 1,  # fast-forward modifier, base 1
           "proximity": 10,  # proximity check in simulation steps
           }

# turtle screen
screen_size = 600

# tkinter frame parameters
button_height = 2
button_width = 7
button_frame_height = 35

# tkinter widget padding
x_pad = 20
y_pad = 15
x_pad_left = (x_pad, 0)
x_pad_left_super = (x_pad*10, 0)
x_pad_right = (0, x_pad)
x_pad_right_super = (0, x_pad*10)
x_pad_both = (x_pad, x_pad)
y_pad_top = (y_pad, 0)
y_pad_bot = (0, y_pad)
y_pad_both = (y_pad, y_pad)

# prey and predator colors
prey_color = "#68ed53"
pred_color = "#de3f3c"

# prey and predator general attributes
# *NOTE: these initial values show up as the DEFAULT in the parameters screen
prey_attributes = {"population": 100,
                   "generation": 0,
                   "lifespan": 8,
                   "health": 1,
                   "vision": 10,
                   "peripheral": math.pi / 4,
                   "speed": 10,
                   "damage": 0,
                   "separation_weight": 1,
                   "birth_rate": 0.005,
                   "mutation_rate": 0.25
                   }

pred_attributes = {"population": 20,
                   "generation": 0,
                   "lifespan": 10,
                   "health": 10,
                   "vision": 30,
                   "peripheral": math.pi / 2,
                   "speed": 20,
                   "damage": 1,
                   "separation_weight": 1,
                   "birth_rate": 0.005,
                   "mutation_rate": 0.25
                   }

tooltip = {"prey_main": "Enter starting values for PREY.",
           "prey_population": "Starting population for PREY.\nMust be an integer >= 0.",
           "prey_health": "Starting health pool for PREY.\n"
                          "Increases the amount of damage the organism may receive before dying.\n"
                          "Must be an integer > 0.",
           "prey_speed": "Starting speed for PREY.\n"
                         "Increases distance moved per turn.\n"
                         "Must be an integer >= 0.",
           "prey_damage": "Starting damage value for PREY.\n"
                          "PREY deal damage only to PREDATORS.\n"
                          "Must be an integer >= 0.",
           "prey_birth_rate": "Starting birth rate for PREY.\n"
                              "Denotes probability that the organism will give birth each turn.\n"
                              "Must be a float value between (0, 0.01].",
           "prey_mutation_rate": "Starting mutation rate for PREY.\n"
                                 "Improves the chance of genome mutations.\n"
                                 "May be any value > 0.",
           "pred_main": "Enter starting values for PREDATORS.",
           "pred_population": "Starting population for PREDATORS.\nMust be an integer >= 0.",
           "pred_health": "Starting health pool for PREDATORS.\n"
                          "Increases the amount of damage the organism may receive before dying.\n"
                          "Must be an integer > 0.",
           "pred_speed": "Starting speed for PREDATORS.\n"
                         "Increases distance moved per turn.\n"
                         "Must be an integer >= 0.",
           "pred_damage": "Starting damage value for PREDATORS.\n"
                          "PREDATORS deal damage only to PREY.\n"
                          "Must be an integer >= 0.",
           "pred_birth_rate": "Starting birth rate for PREDATORS.\n"
                              "Denotes probability that the organism will give birth each turn.\n"
                              "Must be a float value between (0, 0.01].",
           "pred_mutation_rate": "Starting mutation rate for PREDATORS.\n"
                                 "Improves the chance of genome mutations.\n"
                                 "May be any value > 0.",
           "start_button": "Start the simulation with the current parameters.",
           "load_button": "Load a saved simulation from a save (.pkl) file.",
           "sim_screen": "Predators are RED dots.\nPrey are GREEN dots.",
           "stats_frame": "Live statistics of the simulation.\n\n"
                          "Population: current population of the organisms. Also broken\n"
                          "down by organism type.\n\n"
                          "Turn Number: current turn of the simulation. A turn consists of\n"
                          "setting destination, moving, fighting, and reproducing.\n\n"
                          "Time Elapsed: time since the simulation began.\n\n"
                          "Generation: current youngest generation. Initial 0. Each time a\n"
                          "child is born, their generation is 1 higher than the parent.\n\n"
                          "Births: number of births, broken down by organism type, since\n"
                          "the simulation began.\n\n"
                          "Deaths: number of deaths, broken down by organism type, since\n"
                          "the simulation began.",
           "fast_forward": "Fast-forward the simulation by up to 10x.",
           "pause_button": "Pause or unpause the simulation.",
           "save_button": "Save the current state of the simulation.\nSimulation paused during save.",
           "stop_button": "Stop the simulation and return to parameters window.",
           "graph_checkbox": "Shows population and mutation graphs when stop button is pressed.",
           }

delay_short = 0.30
delay_long = 1.0
