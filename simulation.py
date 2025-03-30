"""Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

Copyright and Usage Information
===============================

All rights reserved. You may not use, modify, or distribute this code without written permission from the author.

This file is Copyright (c) 2025 Vriti Dahiya
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event (initial location, no previous command)
        first_location = self._game.get_location()
        first_event = Event(first_location.id_num, first_location.brief_description, None)
        self._events.add_event(first_event)

        # Generate the remaining events based on the commands and initial location
        self.generate_events(commands)

    def generate_events(self, commands: list[str]) -> None:
        """Generate all events in this simulation, handling both movement and non-movement commands."""
        current_location = self._game.get_location()
        visited_locations = set()

        for command in commands:
            # Check if command results in location change
            if command in current_location.available_commands:
                next_loc_id = current_location.available_commands[command]
                new_location = self._game.get_location(next_loc_id)

                # Update visited status and description
                if next_loc_id not in visited_locations:
                    description = new_location.long_description
                    visited_locations.add(next_loc_id)
                else:
                    description = new_location.brief_description

                current_location = new_location
            else:
                # For non-movement commands, use current location's description
                description = current_location.brief_description
                next_loc_id = current_location.id_num

            # Create and add event
            new_event = Event(
                next_loc_id,
                description,
                command,
                None,
                self._events.last
            )
            self._events.add_event(new_event)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim1 = AdventureGameSimulation('game_data.json', 1, ["go north"])
        >>> sim1.get_id_log()
        [1, 2]

        >>> sim2 = AdventureGameSimulation('game_data.json', 1, ["go north", "go east", "go north"])
        >>> sim2.get_id_log()
        [1, 2, 3, 6]
        """
        # Note: We have completed this method for you. Do NOT modify it for ex1.
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    #  A walkthrough of commands needed to win and lose the game
    win_walkthrough = ["go north", "go east", "look", "pick up", "laptop charger", "go west", "go north", "look",
                       "pick up", "lucky uoft mug", "go east", "go east", "look", "pick up", "large rock", "go north",
                       "drop", "large rock", "drop", "laptop charger", "go west", "go west", "look", "pick up",
                       "line 1 sign", "go east", "go east", "drop", "line 1 sign", "look", "pick up", "usb drive",
                       "pick up", "laptop charger", "go south", "go east", "drop", "laptop charger", "drop",
                       "lucky uoft mug", "drop", "usb drive", "chirly"]
    # chirly is the 'cheat code' to instantly finish the final sliding tile puzzle - since it's randomized each time,
    # we can't give a walkthrough for this portion
    expected_log = [1, 2, 3, 3, 3, 3, 2, 5, 5, 5, 5, 6, 7, 7, 7, 7, 11, 11, 11, 11, 11, 10, 9, 9, 9, 9, 10, 11, 11, 11,
                    11, 11, 11, 11, 11, 7, 8, 8, 8, 8, 8, 8, 8, 8]
    # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your walkthrough
    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_log == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go north", "go south"] * 16
    expected_log = [1, 2] * 16 + [1]
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()

    inventory_demo = ["look", "pick up", "toonie", "inventory"]
    expected_log = [1, 1, 1, 1, 1]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == sim.get_id_log()

    scores_demo = ["look", "pick up", "toonie", "score"]
    expected_log = [1, 1, 1, 1, 1]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == sim.get_id_log()

    # Note: You can add more code below for your own testing purposes
