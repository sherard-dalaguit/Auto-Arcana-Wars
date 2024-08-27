from pathlib import Path
from utils import BaseCharacter
from bot_utils import BaseBot

STAT_TO_MAX = {
    "ninja": "physical_power",
    "mage": "magic_power",
    "warrior": "hp"
}


class MaxxerBot(BaseBot):
    """
	The MaxxerBot class inherits from the BaseBot class and customizes the assignment of characters and items with
	the aim of maximizing a specific stat for a specific character.

	Args:
		character_to_max (str): The name of the character whose specific stat we want to maximize.

	Methods:
		make_assignment(): Determines the position and items of each character in your team.
		process_previous_round_stats(): Processes the results of the previous round to inform the next assignments.
		In this case it's a blank method since the strategy doesn't depend on it.
	"""
    def __init__(self, character_to_max: str) -> None:
        """
		Initializes an instance of the MaxxerBot class, setting the character name to be maximized.

		Args:
			character_to_max (str): The name of the character whose specific stat we want to maximize.
		"""
        self.character_to_max = character_to_max

    def make_assignment(self) -> list[dict]:
        """
		Creates an assignment of characters and items.

		This strategy tries to put the specified character in the last position and assigns all
		items to this character. If the character is not in your team, the last character in your team gets all the items.

		Returns:
			list[dict]: A list of dictionaries, each representing an assignment for a character.
		"""
        assignment = self.previous_character_ordering
        
        candidates = [(char_idx, char) for char_idx, char 
                      in enumerate(assignment)
                      if char["character"]["name"] == self.character_to_max]
        if candidates:
            stat_to_maximize = STAT_TO_MAX[self.character_to_max]
            best_char_idx, best_char = max(
                candidates, key=lambda x: x[1]["character"]["stats"][stat_to_maximize])
        else:
            best_char_idx = 0  # no main characters found :(
        
        assignment.insert(-1, assignment.pop(best_char_idx))
        assignment[-1]["items"] = self.items
        
        return assignment
        
    def process_previous_round_stats(self, 
                                     is_your_win: bool, 
                                     your_team: list[BaseCharacter], 
                                     opponent_team: list[BaseCharacter]) -> None:
        """
		Method to process the results of the previous round.

		This is a mandatory method for all bots, but it's not used by MaxxerBot, because the strategy
		doesn't depend on the outcome of previous rounds.
		"""
        pass
            
    
    
    
        
        