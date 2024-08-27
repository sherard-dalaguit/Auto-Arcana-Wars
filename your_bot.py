from bot_utils import BaseBot
from utils import BaseCharacter


class YourBot(BaseBot):
	"""
	YourBot, a subclass of BaseBot, pits the character that has the highest survivability on your team
	against the character that deals the most damage on the opponent's team.

	Attributes:
		opponent_damage_dealers (list[tuple[int, int]]): A list of tuples where each tuple contains the character
														 index and the damage dealt by that character.
		team_survivability (list[tuple[int, int]]): A list of tuples where each tuple contains the character
													 index and the survivability score for that character
													 (calculated as current HP + armor).

	Methods:
		make_assignment(): Determines the position and items of each character in your team.
		process_previous_round_stats(): Processes the stats of the previous round to set up new battles.
	"""
	def __init__(self) -> None:
		"""
		Initializes an instance of YourBot, setting up lists for damage dealers and survivable characters.
		"""
		self.opponent_damage_dealers = []
		self.team_survivability = []

	def make_assignment(self) -> list[dict]:
		"""
		Creates assignments for each character on the team.

		This method sorts both the survivability of our own team and the damage dealers of the opponent's team.
		The characters are then assigned such that the character with the highest survivability on our team is
		pitted against the highest damage dealer on the opponent's team. Following this strategy, the rest of
		the characters are assigned.

		Returns:
			list[dict]: A list of dictionaries where each dictionary represents character assignments.
		"""

		assignment = self.previous_character_ordering

		if self.team_survivability:
			previous_order = self.previous_character_ordering
			self.team_survivability.sort(key=lambda x: x[1], reverse=True)
			self.opponent_damage_dealers.sort(key=lambda x: x[1])

			# Put the highest survivability character to combat against the highest damage dealer
			high_survivability_char_idx, _ = self.team_survivability[0]
			high_damage_oppo_char_idx, _ = self.opponent_damage_dealers[-1]
			assignment[high_damage_oppo_char_idx] = previous_order[high_survivability_char_idx]

			for i in range(1, len(self.team_survivability)):
				team_char_idx, _ = self.team_survivability[i]
				placement_idx, _ = self.opponent_damage_dealers[i - 1]
				assignment[placement_idx] = previous_order[team_char_idx]

			# Give the items to the character that holds position against the highest damage dealer
			assignment[high_damage_oppo_char_idx]["items"] = self.items

		return assignment

	def process_previous_round_stats(self,
									 is_your_win: bool,
									 your_team: list[BaseCharacter],
									 opponent_team: list[BaseCharacter]) -> None:
		"""
		Processes the results from the previous round.

		This method uses the stats from the previous round to prepare for the next round by determining who the damage
		dealers are for the opponent team, and calculating the survivability of our team.

		Args:
			is_your_win (bool): Whether or not you won the last round.
			your_team (list[BaseCharacter]): List of character objects representing your characters for the next round.
			opponent_team (list[BaseCharacter]): List of character objects representing your opponent's characters for
												 the next round.
		"""

		self.opponent_damage_dealers = [(char_idx, char.damage_stats.damage_dealt)
										for char_idx, char in enumerate(opponent_team)]
		self.team_survivability = [(char_idx, char.effective_stats.current_hp + char.effective_stats.armor)
								   for char_idx, char in enumerate(your_team)]
