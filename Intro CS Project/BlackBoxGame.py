# Author: Chelsey Beck
# Date: 8/7/2020
# Description: 3 interacting classes that as a whole, represent a BlackBox game that is played by placing Atoms that
# each have a position and deflection points. Rays may be shot from positions around the black box. Rays have entry
# positions and interact with atoms and deflections. If no rays are struck, ray will have an exit point.
# BlackBoxGame contains a game board, has methods to add atoms to the board, and to shoot rays within the board.
# The class also keeps score and allows a user to guess the position of atoms within the board.


class Atom:
    """Represents an atom with a position in a row and column and 1-4 deflection points"""

    def __init__(self, row, column):                    # takes row column parameters
        self._position = (row, column)
        self._row = row
        self._column = column
        self._deflections = {}                          # creates empty dictionary to store deflections
        self._reflections = []
        self.add_deflections()                          # deflections will be identified using cartesian quadrants

    def add_deflections(self):
        """
        For a given atom object, adds to the deflections dictionary key-value pairs of the quadrant of the deflection
        if the atom was the origin and the position on the board of the deflection.
        Deflections will be stored for positions that may be in border positions outside of the black box.
        These cases will be handled when deflections are added to the board.
        Storing of deflections will allow for rays to interpret the directionality of a deflection
        when one is encountered.
        :return: none
        """
        self._deflections[1] = (self._row - 1, self._column + 1)        # add deflections for quadrant 4
        self._deflections[2] = (self._row - 1, self._column - 1)        # add deflections for quadrant 3
        self._deflections[3] = (self._row + 1, self._column - 1)        # add deflections for quadrant 2
        self._deflections[4] = (self._row + 1, self._column + 1)        # add deflections for quadrant 2

    def get_row(self):
        """
        :return: the row of the atom object
        """
        return self._row

    def get_column(self):
        """
        :return: the column of the atom object
        """
        return self._column

    def get_deflections(self):
        """
        :return: the dictionary of deflections for the the atom object
        """
        return self._deflections


class Ray:
    """
    Represents a ray with an entry point and an exit point if one occurs, and a result with corresponding point value.
    Results include a hit (1 point, no exit), a reflection (1 point and same exit as entry), a deflection (2 points)
    and a miss (2 points)
    """
    def __init__(self, row, column, board_object):
        self._row = row
        self._column = column
        self._board = board_object
        self._exit_point = self.route()
        if self._exit_point is None or self._exit_point == (self._row, self._column):   # if hit or reflection
            self._score = -1                                                            # negative 1 score
        else:                                                                           # if deflection or miss
            self._score = -2                                                            # negative 2 score

    def get_ray_result(self):
        """
        :return: the exit point of the ray as a tuple if an exit point exists (miss, deflection, reflection),
        None if a hit occurs, or False if the ray does not start from a border position
        """
        return self._exit_point

    def get_ray_score(self):
        """
        :return: The score value for the given ray; a negative integer
        """
        return self._score

    def route(self):
        """
        A method that calls one of four functions for moving a ray up, down, left, and right within
        a black box depending on the entry position of the ray.
        :return: the returned tuple of the exit point of the ray (or none if none occurs)
        """
        if self._row == 0:                              # if ray enters top of board
            return self.down(self._row, self._column)   # begin movement down from entry point
        elif self._row == 9:                            # if ray begins from bottom of board
            return self.up(self._row, self._column)     # begin movement up from entry point
        elif self._column == 0:                         # if ray begins from left side of board
            return self.right(self._row, self._column)  # begin movement right from entry point
        elif self._column == 9:                         # if ray begins from right side of board
            return self.left(self._row, self._column)   # begin movement left from entry point
        else:
            return False

    def down(self, row, column):
        """
        Advances a ray to the next downward position; calls functions to change the direction of the ray if a
        deflection or reflection occurs. Returns none in the case of a hit.
        :param row:
        :param column:
        :return: a tuple of the exit point of the ray (or none if none occurs)
        """
        step = self._board[row+1][column]
        if type(step) == str:                       # base case: if the ray reaches an edge/exit point
            return row + 1, column                  # returns the position of the exit point
        if step is None:                            # if no atoms/deflections/reflections encountered
            return self.down(row+1, column)         # continues in same direction
        elif step == 0 or step == 3 or step == 4:   # if a reflection is encountered
            return self.up(row+1, column)           # ray moves into next position then turns around
        elif step == 1:                             # if deflection is encountered to upper right of atom
            return self.right(row+1, column)        # ray moves into next position then turns right
        elif step == 2:                             # if deflection is encountered to upper left of atom
            return self.left(row+1, column)         # ray moves into next position then turns left
        else:                                       # only other outcome is an encountered atom (hit)
            return None                             # none = no exit point

    def up(self, row, column):
        """
        Advances a ray to the next upward position; calls functions to change the direction of the ray if a
        deflection or reflection occurs. Returns none in the case of a hit.
        :param row:
        :param column:
        :return: a tuple of the exit point of the ray (or none if none occurs)
        """
        step = self._board[row-1][column]
        if type(step) == str:                           # if the ray reaches an edge/exit point
            return row - 1, column                      # returns the position of the exit point
        if step is None:                                # if no atoms/deflections/reflections encountered
            return self.up(row-1, column)               # continues in same direction
        elif step == 0 or step == 1 or step == 2:       # if a reflection is encountered
            return self.down(row-1, column)             # ray moves into next position then turns around
        elif step == 3:                                 # if deflection is encountered to bottom left of atom
            return self.left(row-1, column)             # ray moves into next position then turns left
        elif step == 4:                                 # if deflection is encountered to bottom right of atom
            return self.right(row-1, column)            # ray moves into next position then turns right
        else:                                           # only other outcome is an encountered atom (hit)
            return None                                 # none = no exit point

    def right(self, row, column):
        """
        Advances a ray to the next right position; calls functions to change the direction of the ray if a
        deflection or reflection occurs. Returns none in the case of a hit.
        :param row:
        :param column:
        :return: a tuple of the exit point of the ray (or none if none occurs)
        """
        step = self._board[row][column+1]
        if type(step) == str:                       # if the ray reaches an edge/exit point
            return row, column + 1                  # returns the position of the exit point
        if step is None:                            # if no atoms/deflections/reflections encountered
            return self.right(row, column+1)        # continues in same direction
        elif step == 0 or step == 1 or step == 4:   # if a reflection is encountered
            return self.left(row, column+1)         # ray moves into next position then turns around
        elif step == 2:                             # if deflection is encountered to top left of atom
            return self.up(row, column+1)           # ray moves into next position then turns up
        elif step == 3:                             # if deflection is encountered to bottom left of atom
            return self.down(row, column+1)         # ray moves into next position then turns dowm
        else:                                       # only other outcome is an encountered atom (hit)
            return None                             # none = no exit point

    def left(self, row, column):
        """
        Advances a ray to the next left position; calls functions to change the direction of the ray if a
        deflection or reflection occurs. Returns none in the case of a hit.
        :param row:
        :param column:
        :return: a tuple of the exit point of the ray (or none if none occurs)
        """
        step = self._board[row][column-1]
        if type(step) == str:                       # if the ray reaches an edge/exit point
            return row, column - 1                  # returns the position of the exit point
        if step is None:                            # if no atoms/deflections/reflections encountered
            return self.left(row, column-1)         # continues in same direction
        elif step == 0 or step == 2 or step == 3:   # if a reflection is encountered
            return self.right(row, column-1)        # ray moves into next position then turns around
        elif step == 1:                             # if deflection is encountered to top right of atom
            return self.up(row, column-1)           # ray moves into next position then turns up
        elif step == 4:                             # if deflection is encountered to bottom right of atom
            return self.down(row, column-1)         # ray moves into next position then turns dowm
        else:                                       # only other outcome is an encountered atom (hit)
            return None                             # none = no exit point


class BlackBoxGame:
    """
    Represents the row and column positions of a 10x10 black box game
    Contains methods to initialize the board with each atom placed and a starting score of 25
    to allow guesser to shoot rays and update points accordingly,
    to allow the guesser to guess the position of an atom,
    to inform the guesser of how many atoms have not yet been guessed,
    and to notify the user of the current score.
    """

    def __init__(self, atoms_list):
        """
        :param atoms_list: a list of ordered pair tuples representing row and column positions of atoms (1-8)
        :returns: nothing
        Initializes the empty game board as a list of 10 rows, each a list with 10 column positions.
        Updates the game board to represent the placing of each atom by updating the value to 1.
        If the user passes a tuple that represents a position outside of the black box the board will not be updated.
        Also initializes private data members for the score (25)
        and the number of atoms that have not been guessed (the length of the passed list of tuple positions)
        and an empty list to store previous atom guesses
        """
        self._black_box = [['C', '', '', '', '', '', '', '', '', 'C'],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['', None, None, None, None, None, None, None, None, ''],
                           ['C', '', '', '', '', '', '', '', '', 'C']]
        self._atom_positions = atoms_list
        self._atoms = [self.add_atom(pos[0], pos[1]) for pos in atoms_list]     # for each position, add an atom
        self._score = 25
        self._atoms_left = len(atoms_list)
        self._atom_guesses = []                                                 # empty list to store guesses
        self.update_board()                                                     # places atoms/deflections on board

    def update_board(self):
        """
        Takes no parameters and updates the board to include deflections (represented by integer 1-4 depending on
        quadrant relative to atom) and reflections (occurring when two atoms are separated by one space, represented
        bu integer 0). Only assigns integer values if space not occupied by an atom and space is in the black box.
        Does not change border positions.
        :return: none
        """
        for atom in self._atoms:                                                # for each atom in the list of atoms
            self._black_box[atom.get_row()][atom.get_column()] = atom           # place atom object in the position
            deflections = atom.get_deflections()                                # pull out dict of deflections
            for quadrant in deflections:                                        # for each entry in the dict
                position = deflections[quadrant]                                # pull out the position value
                if self._black_box[position[0]][position[1]] in range(1, 5):    # if a deflection is already there
                    self._black_box[position[0]][position[1]] = 0               # double deflection - reflection
                elif self._black_box[position[0]][position[1]] is None:         # if no atom is in that location
                    self._black_box[position[0]][position[1]] = quadrant        # add quadrant value in deflection pos

    def add_atom(self, row, column):
        """
        :param row and column: values representing the position of the atom to be added
        :return: none
        Mutates the black box game board to represent atoms with the integer 2 and deflection points in positions
        diagonal to the atom as the integer 1. If an atom is already located in the position of a deflection
        point, the value remains 2.
        """
        value = self._black_box[row][column]                        # pulls out the value of the position
        if value is None or value in range(0, 5):                   # if the space is not occupied by an atom
            return Atom(row, column)                                # creates an atom object in that space

    def get_score(self):
        """
        A method named get_score that takes no parameters and returns the current score.
        """
        return self._score

    def shoot_ray(self, row, column):
        """
        :param row
        :param column: the border row and column from which the ray enters the black box
        :return: False, if row and column are corners or in the black box, None if hit, or tuple representing the exit
        A function that allows the guesser to shoot a ray from the specified entry point. If a hit occurs,
        returns None and 1 point is deducted. If a reflection occurs, returns the exit point and 1 point deducts.
        If a deflection or a miss occurs, returns the exit point and 2 points are deducted.
        """
        if self._black_box[row][column] == '':              # if no ray has been shot from the entry point
            ray = Ray(row, column, self._black_box)         # ray object is created
            self._score += ray.get_ray_score()              # the score is adjusted based on the outcome
            result = ray.get_ray_result()                   # the result (exit point or none) is created
            if result is None:                              # if there is not an exit point
                self._black_box[row][column] = 'H'          # the entry point is marked a hit
            elif result == (row, column):                   # if the exit point is the same as the entry
                self._black_box[row][column] = 'R'          # the entry point is marked a reflection
            else:                                           # if the exit point is not the entry point
                self._black_box[row][column] = 'D'          # the entry point is marked as a deflection
                self._black_box[result[0]][result[1]] = 'D' # also marks the exit point (entry/exit is reversible)
            return result

    def guess_atom(self, row, column):
        """
        :param row:
        :param column: the row and column positions of the atom guessed
        :returns: Boolean True if guess is correct, False if incorrect
        Takes as parameters a row and column (in that order).
        If there is an atom with that position is in the list of atoms, returns True, otherwise returns False.
        The guessing player's score will be adjusted down 5 points for an incorrect guess
        """
        if (row, column) not in self._atom_guesses:         # if the position has not already been guessed
            self._atom_guesses.append((row, column))        # add the position to the list of guesses
            if (row, column) in self._atom_positions:       # if the position is that of an atom
                self._atoms_left += -1                      # remove one from the # of atoms remaining
                return True
            else:
                self._score += -5                           # subtract 5 for wrong guess
                return False

    def atoms_left(self):
        """
        :param: none
        :returns self._atoms_left: the current number of unguessed atoms
        A method that takes no parameters and returns the number of atoms that haven't been guessed yet.
        """
        return self._atoms_left
