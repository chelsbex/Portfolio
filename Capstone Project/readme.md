# A-Life Challenge: an artificial life simulator

#### Authors: Chelsey Beck and Christopher Felt

The A-Life Challenge is an artificial life simulation of a simple predator-prey paradigm. The organisms in this simulation boast a visual capability allowing them to chase, run away, or group together depending on behavioral tendencies. Each organism possesses a unique "genome" and, if they successfully reproduce, pass their unique capabilities down to their offspring. Survival of the fittest!

## <ins>Installation:</ins>

1. Extract contents of zip to the same directory on a machine with Python 3.11 or later.
2. Install required packages: **matplotlib**, **numpy**, and **tkinter-tooltip**. The following standard libraries are also required: math, os, pickle, random, time, tkinter, and turtle.
3. Run main.py

## <ins>How to use the program:<ins>

#### Parameters Window:

The program starts up by immediately displaying the parameters screen window, pictured in figure 1 below. In this window, you may adjust the starting input parameters for prey and predators, including population, health, speed, damage, birth rate, and mutation rate.

![figure 1](https://user-images.githubusercontent.com/54368648/225216415-f91b86ea-265f-48c4-9bc7-aa74480b3787.png)<br>
Figure 1 - Parameters screen. Arrows indicate input fields.

The input parameters are generally self explanatory, but we have supplied a detailed description of each below. Note: negative values are not allowed for any parameter. If a negative value is entered, the program will give the user a warning popup describing the error and will not proceed to the simulation window. Birth rates are additionally capped at 0.01, and speed is capped at 100.  

Input Parameters:
1. Population - controls the starting number of the corresponding organism type, prey or predators. Recommended range of values for total combined predator and prey population is 2 to 300. Population values higher than ~300 may result in slower animation speeds. Warning: total population values above 1000 may severely impact performance.  
2. Health - this attribute allows the organism to survive more hits.
3. Speed - controls how quickly the organism moves on the screen. 
4. Damage - when a prey and predator are adjacent, they reduce each other’s health by their corresponding damage value. Prey will never attack prey and predators will never attack predators.
5. Birth Rate - this parameter determines how often the organism will reproduce offspring. Higher values mean the organism is more likely to reproduce each turn.
6. Mutation Rate - determines the rate at which an organism’s attributes differ from its parent’s when it is born. Currently not implemented in organism behavior.

Once the desired parameters have been entered, click the “Start” button to begin the simulation. Alternatively, click the “Load” button to open a save file of a previous simulation saved state. The default directory for this feature is the current working directory, and only .pkl extension files will be visible. Upon loading a saved file, the program will automatically switch to the simulation window, and the simulation will pick up from where it left off in the save file.   

#### Simulation Window:

When the “Start” button is pressed or a saved file is loaded, the parameters screen will be replaced by the simulation screen, see figure 2 below. This window consists of three components: 

1. an animated screen representing the simulation. green dots represent prey and red dots represent predators.
2. a statistics frame with live updated statistics of the simulation.
3. a control panel with buttons that allow the user to make changes to the simulation.

![figure 2](https://user-images.githubusercontent.com/54368648/225217110-f4bf4722-39e4-4f1a-afd1-6692b48e2d6a.png)<br>
Figure 2 - Simulation screen with “animation screen”, “control panel”, and “statistics frame”.

The control panel consists of five buttons and one checkbox. Each is described in detail below. See figure 3 for the location of the corresponding button to each number.

1. “Pause”/”Resume” - freezes the simulation after the current turn finishes. The simulation will remain frozen until the “Resume” button is pressed. The name of this button changes appropriately when pressed. 
2. “Stop” - ends the simulation immediately. <br>
    a. If “Show graph results” is checked a plot charting the population of the prey and predators over time is shown upon closing. Note: no data will be shown until after turn #200.
3. “Load” - opens a dialog box that allows the user to load a previously saved simulation from a save file. The default directory is the current working directory. Only .pkl files will be visible. While the dialog box is open, the simulation is paused, and will resume if the load fails or is aborted.
4. “Save” - opens a dialog box that allows the user to save the current state of the simulation to a save file. The default directory opened is the current working directory and the default file name and extension for save files is a_life_save.pkl. The simulation is paused while the dialog box is open and will resume when the file is successfully saved, an error occurs, or the operation is aborted.
5. “Simulation Speed” (slider) - increases the speed of the simulation by a factor of between 1-10 times. Slide the slider to the right to increase speed, with the rightmost position resulting in 10 times speed and the leftmost position resulting in normal speed. Note: this fast-forward feature emulates a faster simulation, but may not result in the same outcome as if the slider were not used. The setting adjusts organism speed, birth-rate, energy, etc. proportionately to the speed value to achieve the fast-forward effect. Turns and time-elapsed proceed at a normal rate regardless of the speed. 
   
![figure 3](https://user-images.githubusercontent.com/54368648/225217863-7e78c56b-0059-4839-a604-65ff416c1224.png)<br>
Figure 3 - Simulation screen with pause and stop buttons highlighted.

When the population graph window is closed, or if the Stop button is pressed with the Show graph result checkbox unchecked, the simulation window will automatically revert to the parameters screen window. The simulation may be rerun with different parameters as many times as desired.
