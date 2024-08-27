from utils import BaseCharacter
from bot_utils import BaseBot
import numpy as np


class RandomBot(BaseBot):
    """
    The RandomBot class inherits from the BaseBot class, designed to make random assignments.

    The logic of this bot is based on a random number generator, which is set with a defined seed value
    for predictable randomness.

    Attributes:
        rand: a random number generator object.

    Methods:
        make_assignment(): Determines the position and items of each character in your team.
        process_previous_round_stats(): Processes the results of the previous round to inform the next assignments.
        In this case it's a blank method since the strategy doesn't depend on it.
    """
    def __init__(self, seed: int = 16) -> None:
        """
		Initializes an instance of the RandomBot class, setting the seed for the random number generator.

		Args:
			seed (int): The seed for the random number generator. Defaults to 16.
		"""
        self.rand = np.random.default_rng(seed)
        
    def make_assignment(self) -> list[dict]:
        """
		Creates an assignment of characters and items.

		This method randomly shuffles the order of the characters and randomly assigns items to the characters.

		Returns:
			list[dict]: A list of dictionaries, each representing assignments for a character.
		"""
        assignment = self.previous_character_ordering
        self.rand.shuffle(assignment)
        item_assignments = self.rand.choice(len(assignment), size=(len(self.items),))
        for item_idx, char_idx in enumerate(item_assignments):
            if not "items" in assignment[char_idx]:
                assignment[char_idx]["items"] = []
            assignment[char_idx]["items"].append(self.items[item_idx])
        
        return assignment
    
    def process_previous_round_stats(self, 
                                     is_your_win: bool, 
                                     your_team: list[BaseCharacter], 
                                     opponent_team: list[BaseCharacter]) -> None:
        """
		Method to process the results of the previous round.

		This is a mandatory method for all bots, but it's not used by RandomBot, because the strategy
		doesn't depend on previous rounds' results.
		"""
        pass
