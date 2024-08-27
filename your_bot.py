from bot_utils import BaseBot
from utils import BaseCharacter


class YourBot(BaseBot):
	def __init__(self) -> None:
		self.opponent_damage_dealers = []
		self.team_survivability = []

	def make_assignment(self) -> list[dict]:

		assignment = self.previous_character_ordering

		if self.team_survivability:
			previous_order = self.previous_character_ordering
			self.team_survivability.sort(key=lambda x: x[1], reverse=True)
			self.opponent_damage_dealers.sort(key=lambda x: x[1])

			# Put the highest survivability character to combat against highest damage dealer
			high_survivability_char_idx, _ = self.team_survivability[0]
			high_damage_oppo_char_idx, _ = self.opponent_damage_dealers[-1]
			assignment[high_damage_oppo_char_idx] = previous_order[high_survivability_char_idx]

			# For the rest, use the same strategy as before
			for i in range(1, len(self.team_survivability)):
				team_char_idx, _ = self.team_survivability[i]
				placement_idx, _ = self.opponent_damage_dealers[i - 1]
				assignment[placement_idx] = previous_order[team_char_idx]

		# Once again, give the items to the character that holds position against the highest damage dealer
			assignment[high_damage_oppo_char_idx]["items"] = self.items

		return assignment

	def process_previous_round_stats(self,
									 is_your_win: bool,
									 your_team: list[BaseCharacter],
									 opponent_team: list[BaseCharacter]) -> None:

		self.opponent_damage_dealers = [(char_idx, char.damage_stats.damage_dealt)
										for char_idx, char in enumerate(opponent_team)]
		self.team_survivability = [(char_idx, char.effective_stats.current_hp + char.effective_stats.armor)
								   for char_idx, char in enumerate(your_team)]
