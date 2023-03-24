import turtle
import math
import random
import numpy as np
import settings


class Organism:
    """Represents a single organism and its genome."""

    def __init__(self, screen, identifier, position, destination, attributes):

        # setup turtle data members
        self._sprite = turtle.RawTurtle(screen)
        self._identifier = identifier  # can set with child class once they're ready
        self._position = position
        self._destination = destination
        self._direction = self.__update_direction()  # set initial direction automatically

        # set attributes
        self._vision = attributes["vision"] + (random.uniform(-1.0, 1.0) * attributes["mutation_rate"])
        self._peripheral = attributes["peripheral"] + (random.uniform(-1.0, 1.0) * attributes["mutation_rate"])
        self._speed = attributes["speed"] + (random.uniform(-1.0, 1.0) * attributes["mutation_rate"])
        self._damage = attributes["damage"] + (random.uniform(-1.0, 1.0) * attributes["mutation_rate"])
        self._separation_weight = attributes["separation_weight"]
        self._birth_rate = attributes["birth_rate"]
        self._mutation_rate = attributes["mutation_rate"]
        self._generation = attributes["generation"]
        self._lifespan = attributes["lifespan"]
        self._age = 0
        self._health = attributes["health"]
        self._energy = 0
        if self._identifier == 0:
            self._energy = self._health

        self._genome = self.get_attributes()  # currently not in use

    def get_health(self):
        """Return current health"""
        return self._health

    def decrement_health(self, damage):
        """Decrement current health"""
        self._health -= damage

    def get_identifier(self):
        """Return organism identifier"""
        return self._identifier

    def get_pos(self):
        """Return current position"""
        return self._position

    def get_offspring_pos(self):
        """Return position near current position"""
        return [self._position[0] + random.uniform(-10.0, 10.0), self._position[0] + random.uniform(-10.0, 10.0)]

    def get_dest(self):
        """Return current destination"""
        return self._destination

    def get_direction(self):
        """Return current direction"""
        return self._direction

    def get_generation(self):
        """Return generation number"""
        return self._generation

    def get_lifespan(self):
        """Return lifespan"""
        return self._lifespan

    def rand_dest(self, fast_forward) -> list:
        """Returns a random [x, y] coordinate destination within visual field"""
        vision_min = self._direction - self._peripheral
        vision_max = self._direction + self._peripheral
        self._direction = random.uniform(vision_min, vision_max)
        x = math.cos(self._direction) * self._vision * (math.log(fast_forward, 10) + 1)
        y = math.sin(self._direction) * self._vision * (math.log(fast_forward, 10) + 1)
        return [x, y]

    def set_dest(self, organisms, fast_forward):
        """Set new destination and update direction"""
        neighbors = self.__nearest_neighbors(organisms, self._vision)
        if not neighbors:
            # set random destination
            vector = self.rand_dest(fast_forward)
            self._destination[0] = self._position[0] + vector[0]
            self._destination[1] = self._position[1] + vector[1]
        else:
            vector = self.__apply_behaviors(neighbors)
            # set new destination
            self._destination[0] = self._position[0] + vector[0]
            self._destination[1] = self._position[1] + vector[1]
        self._direction = self.__update_direction()

    def battle(self, organisms, fast_forward):
        """For neighbors of the opposing type, attack, reducing health by the damage value"""
        neighbors = self.__nearest_neighbors(organisms, 5)
        for neighbor in neighbors:
            if self._identifier != neighbor.get_identifier():
                neighbor.decrement_health(self._damage)
                if self._identifier == 1:
                    if self._energy < self._health:
                        self._energy += (self._damage * (math.log(fast_forward, 10) + 1))

    def is_dead(self):
        """If the organism has been killed or if they have died of old age, returns True, otherwise False"""
        if self._lifespan < self._age or self._health <= 0:
            return True
        else:
            return False

    def is_fertile(self, fast_forward, prey_population):
        """If the organism happens to be fertile (probability based on birth rate) returns True, otherwise False"""
        if self._identifier == 1:
            if random.uniform(0, 1) < (self._birth_rate * (math.log(fast_forward, 10) + 1)) and self._energy > \
                    self._damage * (math.log(fast_forward, 10) + 1):
                # energy cost scaled down with faster speeds as consumption/attack rate doesn't increase
                self._energy -= (self._damage * (math.log(fast_forward, 10) + 1))
                return True
            else:
                return False
        else:
            if random.uniform(0, 1) < (self._birth_rate * (math.log(fast_forward, 10) + 1)) / (prey_population/100):
                return True
            else:
                return False

    def get_attributes(self):
        """Returns a dictionary of attributes for use in creation of offspring organisms"""
        attributes = {"generation": self._generation + 1,  # offspring's generation is always + 1
                      "identifier": self._identifier,
                      "lifespan": self._lifespan,
                      "health": self._health,
                      "vision": self._vision,
                      "peripheral": self._peripheral,
                      "speed": self._speed,
                      "damage": self._damage,
                      "separation_weight": self._separation_weight,
                      "birth_rate": self._birth_rate,
                      "mutation_rate": self._mutation_rate
                      }
        return attributes

    def increment_age(self, fast_forward):
        """Increments the age of the organism"""
        self._age += 0.01 * (math.log(fast_forward, 10) + 1)
        if self._identifier == 1 and self._energy == 0:
            self._health -= random.uniform(0, 0.1) * (math.log(fast_forward, 10) + 1)  # simulated starvation

    def proximity_check(self, distance_to_check):
        """Returns True if Organism is within the given distance of the target destination"""
        # find the cartesian distance to target from current position
        distance = math.dist(self._position, self._destination)
        # return True if less than distance_to_check
        if distance < distance_to_check:
            return True
        else:
            return False

    def __apply_behaviors(self, neighbors):
        """A private method that returns the resultant movement vector based on behaviors"""
        vector = np.array([0, 0])
        for neighbor in neighbors:
            if self._identifier == 1 and neighbor.get_identifier() == 0:
                vector = np.add(vector, self.__hunt(neighbor))
            elif self._identifier == 0 and neighbor.get_identifier() == 0:
                vector = np.add(vector, self.__flock(neighbor))
            elif self._identifier == 0 and neighbor.get_identifier() == 1:
                vector = np.add(vector, self.__flee(neighbor))
            else:
                vector = np.add(vector, self.__separate(neighbor))
        return vector

    def __hunt(self, other):
        """Predators move toward neighboring prey"""
        direction = self.__direction_towards(other)
        return np.array([math.cos(direction) * self._speed, math.sin(direction) * self._speed])

    def __flock(self, other):
        """Prey move toward neighboring prey keeping separation"""
        if math.dist(other.get_pos(), self._position) > self._speed * self._separation_weight:
            direction = self.__direction_towards(other)
            return np.array([math.sin(direction) * self._speed, math.cos(direction) * self._speed])
        else:
            return np.array([0, 0])

    def __flee(self, other):
        """Prey move away from neighboring predators"""
        direction = self.__direction_towards(other) + math.pi
        return np.array([math.cos(direction) * self._speed, math.sin(direction) * self._speed])

    def __separate(self, other):
        """Predators keep minimum distance away from neighboring predators"""
        if math.dist(other.get_pos(), self._position) < self._speed * self._separation_weight:
            direction = self.__direction_towards(other) + math.pi
            return np.array([math.cos(direction) * self._speed, math.sin(direction) * self._speed])
        else:
            return np.array([0, 0])

    def __direction_towards(self, other):
        """Private method that returns a direction given CURRENT position and destination"""
        # atan2(destination y - current y, destination x - current x)
        return math.atan2(other.get_pos()[1] - self._position[1],
                          other.get_pos()[0] - self._position[0])

    def __update_direction(self):
        """Private method that returns a direction given CURRENT position and destination"""
        # atan2(destination y - current y, destination x - current x)
        return math.atan2(self._destination[1] - self._position[1],
                          self._destination[0] - self._position[0])

    def __wrap_around(self, screen_size):
        if self._position[0] > screen_size / 2:
            self._position[0] = self._position[0] % (-screen_size / 2)
            self._destination[0] = self._destination[0] % (-screen_size / 2)
        elif self._position[0] < -screen_size / 2:
            self._position[0] = self._position[0] % screen_size / 2
            self._destination[0] = self._destination[0] % screen_size / 2
        if self._position[1] > screen_size / 2:
            self._position[1] = self._position[1] % (-screen_size / 2)
            self._destination[1] = self._destination[1] % (-screen_size / 2)
        elif self._position[1] < -screen_size / 2:
            self._position[1] = self._position[1] % screen_size / 2
            self._destination[1] = self._destination[1] % screen_size / 2
        self.__update_direction()

    def __nearest_neighbors(self, organisms, distance):
        """Private method that returns a list of neighbors that are within vision"""
        neighbors = []
        vision_min = self._direction - self._peripheral
        vision_max = self._direction + self._peripheral
        for organism in organisms:
            if self is not organism and vision_min < self.__direction_towards(organism) < vision_max:
                if math.dist(self.get_pos(), organism.get_pos()) < distance:
                    neighbors.append(organism)
        return neighbors

    # ---------------------------------
    # Turtle commands
    # ---------------------------------

    def delete_sprite(self):
        """Remove turtle sprite from the Organism object"""
        self._sprite = None

    def init_sprite(self, speed, diameter, screen=None):
        """Initialize the turtle sprite on screen"""
        # update sprite attribute with new turtle if screen provided
        if screen is not None:
            self._sprite = turtle.RawTurtle(screen)

        self.hide_default()  # hide default arrow
        self.speed(speed)
        self.up()  # don't draw line

        # set color for predator
        if self._identifier == 1:
            self.set_color(settings.pred_color)  # red

        # set color for prey
        else:
            self.set_color(settings.prey_color)  # green

        # set turtle location and draw
        self.move()
        self.draw_dot(diameter)

    def hide_default(self):
        """Hide default turtle arrow"""
        self._sprite.hideturtle()

    def speed(self, num):
        """Set turtle speed"""
        self._sprite.speed(num)  # animation speed 1-10 (0 means no animation)

    def up(self):
        """No lines are drawn when turtle moves"""
        self._sprite.up()

    def clear(self):
        """Clear shape"""
        self._sprite.clear()

    def draw_dot(self, diameter):
        """Draw circle on position given diameter"""
        self._sprite.dot(diameter)

    def set_color(self, color):
        """Set turtle color to the given string.
        Accepts color names ("red", "blue", etc.) or RGB hex values ("#FFFFFF")"""
        self._sprite.color(color)

    def update_pos(self, screen_size, slow_factor):
        """Increment current position towards destination"""
        # slow_factor reduces distance moved and makes the animation smoother
        self._position[0] += self._speed / slow_factor * math.cos(self._direction)
        self._position[1] += self._speed / slow_factor * math.sin(self._direction)

        # prevent organisms from going off-screen (only applicable at very high speeds)
        if self._position[0] > screen_size / 2 or self._position[0] < -screen_size / 2 \
                or self._position[1] > screen_size / 2 or self._position[1] < -screen_size / 2:
            self.__wrap_around(screen_size)

    def move(self):
        """Move sprite to current position"""
        self._sprite.goto(self._position[0], self._position[1])


class Predator(Organism):
    pass


class Prey(Organism):
    pass
