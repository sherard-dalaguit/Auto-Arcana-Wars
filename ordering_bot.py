from utils import BaseCharacter
from bot_utils import BaseBot


class HeadOnBot(BaseBot):
    """
    The HeadOnBot class inherits from the BaseBot class, designed to head-on confront the
    opponent's high damage-dealing characters with our equivalent ones.

    Attributes:
        opponent_damage_dealers: List of tuples (character_index, damage_dealt) in the opponent team
        team_damage_dealers: List of tuples (character_index, damage_dealt) in our team

    Methods:
        make_assignment(): Determines the position and items of each character in your team.
        process_previous_round_stats(): Processes the results of the previous round to inform the next assignments.
    """
    def __init__(self) -> None:
        """
		Initializes an instance of the HeadOnBot class,
		sets lists of damage dealers for both opponent and our team to empty.
		"""
        self.opponent_damage_dealers = []
        self.team_damage_dealers = []
    
    def make_assignment(self) -> list[dict]:
        """
		Creates an assignment of characters and items based on damage dealt.

		This strategy places characters in such a way that our characters that dealt the most damage
		in the previous round face the characters from the opponent team that did the same. All items
		go to the highest damage dealer from the opposing team.

		Returns:
			list[dict]: A list of dictionaries, each representing an assignment for a character.
		"""
        
        assignment = self.previous_character_ordering
        highest_damage_char_idx = 0
        
        if self.team_damage_dealers:
            previous_order = self.previous_character_ordering
            self.team_damage_dealers.sort(key = lambda x: x[1])
            self.opponent_damage_dealers.sort(key = lambda x: x[1])
            for damage_dealer_idx in range(len(self.team_damage_dealers)):
                team_char_idx, _ = self.team_damage_dealers[damage_dealer_idx]
                placement_idx, _ = self.opponent_damage_dealers[damage_dealer_idx]
                assignment[placement_idx] = previous_order[team_char_idx]
            highest_damage_char_idx, _ = self.opponent_damage_dealers[-1] 
        
        assignment[highest_damage_char_idx]["items"] = self.items
            
        return assignment
    
    def process_previous_round_stats(self,
                                     is_your_win: bool, 
                                     your_team: list[BaseCharacter], 
                                     opponent_team: list[BaseCharacter]) -> None:
        """
		Updates lists of damage dealers for both teams based on the results of a previous round.

		Args:
			is_your_win (bool): True if our team won in the last round, False otherwise
			your_team (list[BaseCharacter]): List of our characters after the last round
			opponent_team (list[BaseCharacter]): List of opponent characters after the last round
		"""
        
        self.opponent_damage_dealers = [(char_idx, char.damage_stats.damage_dealt)
                                        for char_idx, char in enumerate(opponent_team)]
        self.team_damage_dealers = [(char_idx, char.damage_stats.damage_dealt)
                                        for char_idx, char in enumerate(your_team)]
    
    
        
        