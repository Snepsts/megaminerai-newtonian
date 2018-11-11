# This is where you build your AI for the Newtonian game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

from colorama import init, Fore, Back, Style

class AI(BaseAI):
    """ The AI you add and improve code inside to play Newtonian. """

    intern_plans = []

    @property
    def game(self):
        """The reference to the Game instance this AI is playing.

        :rtype: games.newtonian.game.Game
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self):
        """The reference to the Player this AI controls in the Game.

        :rtype: games.newtonian.player.Player
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
            player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "arrays_start_at_zero" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its player and
            game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic

        # Un-comment this line if you are using colorama for the debug map.
        # init()

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
            dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won
            or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        #self.display_map()
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        """
            Please note: This code is intentionally bad. You should try to optimize everything here. THe code here is 
            only to show you how to use the game's mechanics with the MegaMinerAI server framework.
        """
        # Goes through all the units that you own.
        for unit in self.player.units:
            # Only tries to do something if the unit actually exists.
            if unit is not None and unit.tile is not None:
                if unit.job.title == 'physicist':
                    self.phys_turn(unit)
                elif unit.job.title == 'intern':
                    self.intern_turn(unit)
                elif unit.job.title == 'manager':
                    self.manager_turn(unit)

        return True
        # <<-- /Creer-Merge: runTurn -->>

    def phys_turn(self, unit):
        # If the unit is a physicist, tries to work on machines that are ready, but if there are none,
        # it finds and attacks enemy managers.
        # Tries to find a workable machine for blueium ore.
        # Note: You need to get redium ore as well.
        target = None

        # Goes through all the machines in the game and picks one that is ready to process ore as its target.
        for machine in self.game.machines:
            if machine.tile.blueium_ore >= machine.refine_input:
                target = machine.tile
        if target is None:
            # Chases down enemy managers if there are no machines that are ready to be worked.
            for enemy in self.player.opponent.units:
                # Only does anything if the unit that we found is a manager and belongs to our opponent.
                if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'manager':
                    # Moves towards the manager.
                    while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                        # Moves until there are no moves left for the physicist.
                        if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                            break
                    if unit.tile in enemy.tile.get_neighbors():
                        if enemy.stun_time == 0 and enemy.stun_immune == 0:
                            # Stuns the enemy manager if they are not stunned and not immune.
                            unit.act(enemy.tile)
                        else:
                            # Attacks the manager otherwise.
                            unit.attack(enemy.tile)
                    break
        else:
            # Gets the tile of the targeted machine if adjacent to it.
            adjacent = False
            for tile in target.get_neighbors():
                if tile == unit.tile:
                    adjacent = True
            # If there is a machine that is waiting to be worked on, go to it.
            while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1 and not adjacent:
                if not unit.move(self.find_path(unit.tile, target)[0]):
                    break
            # Acts on the target machine to run it if the physicist is adjacent.
            if adjacent and not unit.acted:
                unit.act(target)


    def intern_turn(self, unit):
        print('Intern Turn:')
        if len(self.intern_plans) == 0:
            ore = self.get_closest_ore(unit)
            print(ore)
            unit_data = [unit, ore]
            self.intern_plans.append(unit_data)
        else:
            unit_data = [x for x in self.intern_plans if x[0] == unit]
            if len(unit_data) == 0:
                units_gathering_blue = [x for x in self.intern_plans if x[1] == 'blueium']
                units_gathering_red = [x for x in self.intern_plans if x[1] == 'redium']
                if len(units_gathering_blue) < len(units_gathering_red):
                    data = [unit, 'blueium']
                else:
                    data = [unit, 'redium']
                self.intern_plans.append(data)
                unit_data = data
            else:
                unit_data = unit_data[0]

        if unit_data[1] == 'blueium':
            if unit.blueium_ore < unit.job.carry_limit:
                print('\tblue inventory not full still gathering')
                target = self.get_closest_blueium_ore()
                self.gather(unit, 'blueium ore', target)
            else:
                self.deposit(unit, 'blueium')

        else:
            if unit.redium_ore < unit.job.carry_limit:
                print('\tred inventory not full still gathering')
                target = self.get_closest_redium_ore()
                self.gather(unit, 'redium ore', target)
            else:
                self.deposit(unit, 'redium')
        print('end of unit turn')


    def gather(self, unit, ore, target):
        # Moves towards our target until at the target or out of moves.
        if len(self.find_path(unit.tile, target)) > 0:
            while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 0:
                if not unit.move(self.find_path(unit.tile, target)[0]):
                    break
        # Picks up the appropriate resource once we reach our target's tile.
        if ore == 'blueium ore':
            if unit.tile == target and target.blueium_ore > 0:
                unit.pickup(target, 0, ore)
        else:
            if unit.tile == target and target.redium_ore > 0:
                unit.pickup(target, 0, ore)

    def deposit(self, unit, color):
        print('\tdepositing ' + color + '!')
        tile = self.get_closest_machine(unit, color)
        while unit.moves > 0 and len(self.find_path(unit.tile, tile)) > 1:
            print('\t'+ color + ' depositor moving!')
            if not unit.move(self.find_path(unit.tile, tile)[0]):
                break
        if len(self.find_path(unit.tile, tile)) <= 1:
            print('\tdropping ' + color)
            unit.drop(tile, 0, color)

    def get_closest_machine(self, unit, color):
        machines = []
        smallest = 999
        closest_tile = None

        for tile in self.game.tiles:
            if tile.machine is not None and tile.machine.ore_type == color:
                machines.append(tile)

        for tile in machines:
            path_length = len(self.find_path(unit.tile, tile))
            if path_length != 0 and path_length < smallest:
                smallest = path_length
                closest_tile = tile
        return closest_tile

    def get_closest_blueium_ore(self):
        target = None
        for tile in self.game.tiles:
            if tile.blueium_ore > 0 and tile.machine is None:
                target = tile
                break
        return target

    def get_closest_redium_ore(self):
        target = None
        for tile in self.game.tiles:
            if tile.redium_ore > 0 and tile.machine is None:
                target = tile
                break
        return target

    def get_closest_ore(self, unit):
        blue = self.get_closest_machine(unit, 'blueium')
        red = self.get_closest_machine(unit, 'redium')
        b_length = len(self.find_path(unit.tile, blue))
        print(b_length)
        r_length = len(self.find_path(unit.tile, red))
        print(r_length)
        if b_length < r_length:
            return 'blueium'
        else:
            return 'redium'


    def manager_turn(self, unit):
        # Finds enemy interns, stuns, and attacks them if there is no blueium to take to the generator.
        self.get_refined_material_tile()
        target = self.get_refined_material_tile()
        if target is None and not self.unit_carries_material(unit):
            for enemy in self.game.units:
                # Only does anything for an intern that is owned by your opponent.
                if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'intern':
                    # Moves towards the intern until reached or out of moves.
                    while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                        if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                            break
                    # Either stuns or attacks the intern if we are within range.
                    if unit.tile in enemy.tile.get_neighbors():
                        if enemy.stun_time == 0 and enemy.stun_immune == 0:
                            # Stuns the enemy intern if they are not stunned and not immune.
                            unit.act(enemy.tile)
                        else:
                            # Attacks the intern otherwise.
                            unit.attack(enemy.tile)
                    break
        elif target is not None:
            # Moves towards our target until at the target or out of moves.
            self.move_in_path(unit, self.find_path(unit.tile, target))
            # Picks up blueium once we reach our target's tile.
            if len(self.find_path(unit.tile, target)) <= 1:
                if target.blueium > 0:
                    unit.pickup(target, 0, 'blueium')
                elif target.redium > 0:
                    unit.pickup(target, 0, 'redium')
        elif target is None and self.unit_carries_material(unit):
            # Stores a tile that is part of your generator.
            gen_tile = self.player.generator_tiles[0]
            # Goes to your generator and drops blueium in.
            self.move_in_path(unit, self.find_path(unit.tile, target))
            # Deposits blueium in our generator if we have reached it.
            if len(self.find_path(unit.tile, gen_tile)) <= 1:
                if unit.blueium > 0:
                    unit.drop(gen_tile, 0, 'blueium')
                elif unit.redium > 0:
                    unit.drop(gen_tile, 0, 'redium')
    @staticmethod
    def move_in_path(self, unit, path):
        if len(path) <= 0:
            return

        while unit.moves > 0 and len(path) > 0:
            if unit.move(path[0]):
                del path[0]
            else:
                break

    def get_refined_material_tile(self):
        materials = []
        ret = None

        for tile in self.game.tiles:
            if self.get_material_count_of_tile(tile) > 1:
                materials.append(tile)

        if len(materials) > 0:
            ret = materials[0]
            for tile in materials:
                if self.get_material_count_of_tile(tile) > self.get_material_count_of_tile(ret): #TODO: Make this better
                    ret = tile
        else:
            ret = None

        return ret

    @staticmethod
    def unit_carries_material(unit):
        return unit.blueium > 0 or unit.redium > 0 or unit.blueium_ore > 0 or unit.redium_ore > 0

    @staticmethod
    def get_material_count_of_tile(tile):
        ret = 0

        ret += tile.redium
        ret += tile.blueium

        return ret

    def find_path(self, start, goal):
        """A very basic path finding algorithm (Breadth First Search) that when
            given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.newtonian.tile.Tile): the starting Tile
            goal (games.newtonian.tile.Tile): the goal Tile
        Returns:
            list[games.newtonian.tile.Tile]: A list of Tiles
            representing the path, the the first element being a valid adjacent
            Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    def display_map(self):
            # A function to display the current state of the map, mainly used for
            # debugging without the visualizer. Use this to see a live view of what
            # is happening during a game, but the visualizer should be much clearer
            # and more helpful. To use this, make sure to un-comment the import for
            # colorama and download it with pip.
        
        print('\033[0;0H', end='')
        for y in range(0, self.game.map_height):
            print(' ', end='')
            for x in range(0, self.game.map_width):
                t = self.game.tiles[y * self.game.map_width + x]
                if t.machine is not None:
                    if t.machine.ore_type == 'redium':
                        print(Back.RED, end='')
                    else:
                        print(Back.BLUE, end='')
                elif t.is_wall:
                    print(Back.BLACK, end='')
                else:
                    print(Back.WHITE, end='')
                foreground = ' '
                if t.machine is not None:
                    foreground = 'M'
                print(Fore.WHITE, end='')
                if t.unit is not None:
                    if t.unit.owner == self.player:
                        print(Fore.CYAN, end='')
                    else:
                        print(Fore.MAGENTA, end='')
                    foreground = t.unit.job.title[0].upper()

                elif t.blueium > 0 and t.blueium >= t.redium:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'R'

                elif t.redium > 0 and t.redium > t.blueium:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'R'
                elif t.blueium_ore > 0 and t.blueium_ore >= t.redium_ore:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.redium_ore > 0 and t.redium_ore > t.blueium_ore:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.owner is not None:
                    if t.type == 'spawn' or t.type == 'generator':
                        if t.owner == self.player:
                            print(Back.CYAN, end='')
                        else:
                            print(Back.MAGENTA, end='')
                print(foreground + Fore.RESET + Back.RESET, end='')
            if y < 10:
                print(' 0' + str(y))
            else:
                print(' ' + str(y))
        print('\nTurn: ' + str(self.game.current_turn) + ' / '
              + str(self.game.max_turns))
        print(Fore.CYAN + 'Heat: ' + str(self.player.heat)
              + '\tPressure: ' + str(self.player.pressure) + Fore.RESET)
        print(Fore.MAGENTA + 'Heat: ' + str(self.player.opponent.heat)
              + '\tPressure: ' + str(self.player.opponent.pressure) + Fore.RESET)
        return
    # <<-- /Creer-Merge: functions -->>
