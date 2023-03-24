import matplotlib.pyplot as plt
import numpy as np
import time


class Statistics:
    """Track interesting statistics for the current simulation session."""
    def __init__(self, predator_attributes, prey_attributes):
        self._pred_init = predator_attributes
        self._prey_init = prey_attributes
        self._pred_avg = {
            "population": [],
            "vision": [0],
            "speed": [0],
            "damage": [0],
            "peripheral": [0]
        }
        self._prey_avg = {
            "population": [],
            "vision": [0],
            "speed": [0],
            "damage": [0],
            "peripheral": [0]
        }
        self._predator = {"population": 0,
                          "births": -1 * predator_attributes["population"],
                          "deaths": 0,
                          "generation": 0,
                          "vision": 0,
                          "peripheral": 0,
                          "speed": 0,
                          "damage": 0,
                          "lifespan": 0
                          }
        self._prey = {"population": 0,
                      "births": -1 * prey_attributes["population"],
                      "deaths": 0,
                      "generation": 0,
                      "vision": 0,
                      "peripheral": 0,
                      "speed": 0,
                      "damage": 0,
                      "lifespan": 0
                      }
        self._general = {"turn": 0,
                         "gen_length": 100,
                         "elapsed_time": 0.00,
                         }
        self._start_time = time.time()

    def get_pred_stats(self):
        return self._predator

    def get_prey_stats(self):
        return self._prey

    def get_prey_pop(self):
        return self._prey["population"]

    def get_general_stats(self):
        return self._general

    def get_generation(self, identifier):
        """Given an identifier, returns the corresponding organism's generation"""
        if identifier == 1:
            return self._predator["generation"]
        else:
            return self._prey["generation"]

    def set_generation(self, identifier, generation_num):
        """Given an identifier and generation, updates the corresponding organism's generation"""
        if identifier == 1:
            self._predator["generation"] = generation_num
        else:
            self._prey["generation"] = generation_num

    def __stopwatch(self):
        """Updates the current elapsed time since start_time"""
        self._general["elapsed_time"] = time.time() - self._start_time

    def get_time_str(self):
        """Return elapsed time as a string truncated to two decimal places"""
        self.__stopwatch()
        return "{:.2f}".format(self._general["elapsed_time"])

    def reset_start_time(self):
        """Resets start time to current time adjusted by elapsed time.
        Use when loading a saved Statistics object!"""
        self._start_time = time.time() - self._general["elapsed_time"]

    def __add_pred_avg(self, keys, data):
        """Recomputes average attribute values for newly added predator"""
        for attribute in keys:
            self._predator[attribute] = (((self._predator["population"] - 1) * self._predator[attribute]) +
                                         data[attribute]) / self._predator["population"]

    def __add_prey_avg(self, keys, data):
        """Recomputes average attribute values for newly added prey"""
        for attribute in keys:
            self._prey[attribute] = (((self._prey["population"] - 1) * self._prey[attribute]) +
                                     data[attribute]) / self._prey["population"]

    def __rm_pred_avg(self, keys, data):
        """Recomputes average attribute values for newly added predator"""
        if self._predator["population"] > 0:
            for attribute in keys:
                self._predator[attribute] = (((self._predator["population"] + 1) * self._predator[attribute]) -
                                             data[attribute]) / self._predator["population"]

    def __rm_prey_avg(self, keys, data):
        """Recomputes average attribute values for newly added prey"""
        if self._prey["population"] > 0:
            for attribute in keys:
                self._prey[attribute] = (((self._prey["population"] - 1) * self._prey[attribute]) +
                                         data[attribute]) / self._prey["population"]

    def add_organism(self, attributes):
        """Increments the population size of the organism type corresponding to the identifier"""
        if attributes["identifier"] == 1:
            self._predator["population"] += 1
            self._predator["births"] += 1  # increment births too
            self.__add_pred_avg(["vision", "speed", "damage", "peripheral"], attributes)
        else:
            self._prey["population"] += 1
            self._prey["births"] += 1
            self.__add_prey_avg(["vision", "speed", "damage", "peripheral"], attributes)

    def remove_organism(self, attributes):
        """Decrements the population size of the organism type corresponding to the identifier"""
        if attributes["identifier"] == 1:
            self._predator["population"] -= 1
            self._predator["deaths"] += 1  # increment deaths too
            self.__rm_pred_avg(["vision", "speed", "damage", "peripheral"], attributes)
        else:
            self._prey["population"] -= 1
            self._prey["deaths"] += 1
            self.__rm_prey_avg(["vision", "speed", "damage", "peripheral"], attributes)

    def next_turn(self):
        """Stores data for the current generation"""
        self._general["turn"] += 1
        if self._general["turn"] % self._general["gen_length"] == 0:
            self._pred_avg["population"].append(self._predator["population"])
            self._prey_avg["population"].append(self._prey["population"])
            attributes = ["vision", "speed", "damage", "peripheral"]
            for attribute in attributes:
                self._pred_avg[attribute].append(self._pred_init[attribute] - self._predator[attribute])
                self._prey_avg[attribute].append(self._prey_init[attribute] - self._prey[attribute])

    def log_population(self):
        """Generates a graph of population data"""
        pred_pop = np.array(self._pred_avg["population"])
        pred_vis = np.array(self._pred_avg["vision"])
        pred_spd = np.array(self._pred_avg["speed"])
        pred_dmg = np.array(self._pred_avg["damage"])
        pred_per = np.array(self._pred_avg["peripheral"])

        prey_pop = np.array(self._prey_avg["population"])
        prey_vis = np.array(self._prey_avg["vision"])
        prey_spd = np.array(self._prey_avg["speed"])
        prey_dmg = np.array(self._prey_avg["damage"])
        prey_per = np.array(self._prey_avg["peripheral"])

        fig, (pop, pred, prey) = plt.subplots(3)

        pop.plot(pred_pop, color='red', label='Predator')
        pop.plot(prey_pop, color='green', label='Prey')
        pop.set(ylabel="Population Size")

        pred.plot(pred_vis, color='red', linestyle='dashed', label='Vision')
        pred.plot(pred_spd, color='red', linestyle='solid', label='Speed')
        pred.plot(pred_dmg, color='red', linestyle='dashdot', label='Damage')
        pred.plot(pred_per, color='red', linestyle='dotted', label='Peripheral')
        pred.set(ylabel="Deviation")

        prey.plot(prey_vis, color='green', linestyle='dashed', label='Vision')
        prey.plot(prey_spd, color='green', linestyle='solid', label='Speed')
        prey.plot(prey_dmg, color='green', linestyle='dashdot', label='Damage')
        prey.plot(prey_per, color='green', linestyle='dotted', label='Peripheral')
        prey.set(xlabel="Time (100 turns)", ylabel="Deviation")

        pop.legend()
        pred.legend()
        prey.legend()
        plt.show()
