# Generated by Creer at 10:54PM on October 16, 2015 UTC, git hash: '98604e3773d1933864742cb78acbf6ea0b4ecd7b'
# This is a simple class to represent the PoliceDepartment object in the game. You can extend it by adding utility functions here in this file.

from games.anarchy.building import Building

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add addtional import(s) here
# <<-- /Creer-Merge: imports -->>

class PoliceDepartment(Building):
    """ The class representing the PoliceDepartment in the Anarchy game.

    Used to keep cities under control and raid Warehouses.
    """

    def __init__(self):
        """ initializes a PoliceDepartment with basic logic as provided by the Creer code generator
        """
        Building.__init__(self)

        # private attributes to hold the properties so they appear read only




    def raid(self, warehouse):
        """ Bribe the police to raid a Warehouse, dealing damage equal based on the Warehouse's current exposure, and then resetting it to 0.

        Args:
            warehouse (Warehouse): The warehouse you want to raid.

        Returns:
            int: The amount of damage dealt to the warehouse, or -1 if there was an error.
        """
        return self._run_on_server('raid', warehouse=warehouse)


    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>
