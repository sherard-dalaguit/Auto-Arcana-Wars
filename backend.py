from pathlib import Path
from utils import BaseCharacter, Stats, Attack, Damage, RngEngine
from game import read_data

N_ROUNDS = 5
N_WINS = 3
DASHES = "-" * 20


def pretty_format_teams(your_team: list[BaseCharacter], 
                        opponent_team: list[BaseCharacter]) -> str:
    """Format the currently standing teams for printing

    Arguments:
        your_team -- the characters in your team still alive
        opponent_team -- the opponent team's characters still alive

    Returns:
        the pretty formatted string of the teams
    """
    your_team = [char.name for char in reversed(your_team)]
    opponent_team = [char.name for char in opponent_team]
    return f"\n\t{your_team} -----VS----- {opponent_team}"
    

def calculate_damage_taken(damage: Damage, character_stats: Stats) -> Stats:
    """
    Calculates the actual damage dealt to a character based on their stats
    and the incoming damage.

    Damage is reduced by the character's armor or magic resistance.

    Args:
        damage (Damage): The incoming damage, which can be physical and/or magical.
        character_stats (Stats): The stats of the character getting hit.

    Returns:
        Stats: A Stats object where the current_hp attribute is set to
        the negative of the actual damage dealt.
    """
    hp_lost = 0
    hp_lost += (damage.physical - damage.physical * character_stats.armor / 100)
    hp_lost += (damage.magic - damage.magic * character_stats.magic_resistance / 100)
    return Stats(current_hp=-hp_lost)


def calculate_miss_chance(damage: Damage, character_stats: Stats) -> float:
    """
    Calculates the chance that an attack will miss based on the character's
    stats and the type of incoming damage.

    For physical damage, the miss chance is proportional to the character's armor / 10.
    Similarly, for magical damage, it is proportional to the magic resistance / 10.
    If there is no incoming damage, the miss chance is 0.

    Args:
        damage (Damage): The incoming damage, which can be physical or magical
        character_stats (Stats): The stats of the character aiming to dodge the attack

    Returns:
        float: The calculated miss chance
    """
    if damage.magic > damage.physical:
        miss_chance = character_stats.magic_resistance / 10
    else:
        miss_chance = character_stats.armor / 10
    return miss_chance


def play_turn(your_character: BaseCharacter, 
              opponent_character: BaseCharacter, 
              is_your_turn: bool,
              rng_engine: RngEngine) -> str:
    """Take a turn in the game, updating the character's stats and returning 
        a description of what happened in the turn
        
    Raises:
        ValueError if any of the characters are already dead (0 current_hp)

    Arguments:
        your_character -- your character in the combat
        opponent_character -- the opponent's character
        is_your_move -- whether it is your move or not
        rng_engine -- the rng system handling the randomness in the game

    Returns:
        the description of what happened in the move
    """
    if any([char.effective_stats.current_hp <= 0 
            for char in [your_character, opponent_character]]):
        raise ValueError("One of the characters is already dead")
                
    attacking_char = your_character if is_your_turn else opponent_character
    attacking_player = "Your" if is_your_turn else "Opponent's"
    defending_char = opponent_character if is_your_turn else your_character
    defending_player = "Opponent's" if is_your_turn else "Your"
    
    special_chance = attacking_char.effective_stats.special_trigger_chance
    is_attack_special = rng_engine.rng(probability=special_chance)
    attack = (attacking_char.basic_attack if not is_attack_special 
              else attacking_char.special_attack)
        
    if attack.stat_updates_to_self is not None:
        attacking_char.effective_stats = \
            attacking_char.effective_stats.add_stat_changes(attack.stat_updates_to_self)
        extra_description = ""
    
    else:
        miss_chance = calculate_miss_chance(damage=attack.damage, 
                                            character_stats=defending_char.effective_stats)
        is_damage_missed = rng_engine.rng(probability=miss_chance)
        if is_damage_missed:
            extra_description = f"It missed {defending_player} {defending_char.name}."
        else:
            hp_update = calculate_damage_taken(damage=attack.damage, 
                                            character_stats=defending_char.effective_stats)
            defending_char.effective_stats = \
                defending_char.effective_stats.add_stat_changes(hp_update)
            extra_description = f"{defending_player} {defending_char.name} lost {-hp_update.current_hp:.3f} HP. "

            total_damage = attack.damage.physical + attack.damage.magic
            attacking_char.damage_stats.damage_dealt += total_damage
            defending_char.damage_stats.damage_taken += total_damage
            defending_char.damage_stats.damage_mitigated += (total_damage - abs(hp_update.current_hp))

            if defending_char.effective_stats.current_hp == 0:
                extra_description += f"It fainted."
                attacking_char.damage_stats.kills += 1
            
    return f"{attacking_player} {attack.description} {extra_description}"


def play_round(your_assignment: Path, 
               opponent_assignment: Path,
               is_your_turn_first: bool, 
               rng_engine: RngEngine) -> tuple[bool, list[str], tuple[list[BaseCharacter], list[BaseCharacter]]]:
    """Play the **round** out under the game engine.

    Arguments:
        your_assignment -- your team assignment for this round
        opponent_assignment -- the opponent's assignment for this round
        is_your_turn_first -- whether the first player to take turn is you
        rng_engine -- the rng system handling the randomness in the game

    Returns:
        a tuple of the outcome and a list of the **round** breakdown:
            - whether you won or not: True if you did, False otherwise
            - the turn-by-turn breakdown of what happened throughout
    """
    your_team = read_data(your_assignment)
    opponent_team = read_data(opponent_assignment)
    your_char_idx = opponent_char_idx = 0
    
    is_your_turn = is_your_turn_first
    
    pretty_format_hp = lambda char: f"[{char.effective_stats.current_hp:.1f}/{char.effective_stats.total_hp:.1f}]"
    
    play_by_play_description = [pretty_format_teams(your_team, opponent_team)]
    
    while your_char_idx < len(your_team) and opponent_char_idx < len(opponent_team):
        your_character = your_team[your_char_idx]
        opponent_character = opponent_team[opponent_char_idx]
        play_by_play_description.append(
            (f"\t{your_character.name} {pretty_format_hp(your_character)}"
             f" VS "
             f"{opponent_character.name} {pretty_format_hp(opponent_character)}"
             ))
        
        outcome = play_turn(your_character, opponent_character, is_your_turn, rng_engine)
        play_by_play_description.append(f"\t\t{outcome}")
        is_char_down = False
        if your_character.effective_stats.current_hp <= 0:
            your_char_idx += 1
            is_char_down = True
        if opponent_character.effective_stats.current_hp <= 0:
            opponent_char_idx += 1
            is_char_down = True
        if is_char_down and (your_char_idx < len(your_team) 
                             and opponent_char_idx < len(opponent_team)):
            play_by_play_description.append(
                pretty_format_teams(your_team[your_char_idx:], opponent_team[opponent_char_idx:]))  
            
        is_your_turn = not is_your_turn
    
    return your_char_idx < opponent_char_idx, play_by_play_description, (your_team, opponent_team)
        

def play_match(your_assignments: Path, 
               opponent_assignments: Path,
               rng_engine: RngEngine) -> tuple[bool, list[str]]:
    """Play the match out under the game engine. 

    Arguments:
        your_assignments -- your assignments for all rounds in the match
        opponent_assignments -- the opponent's assignments for all rounds in the match
        rng_engine -- the rng system handling the randomness in the game

    Returns:
        a tuple of the outcome and a list of the match breakdown:
            - whether you won or not: True if you did, False otherwise
            - the turn-by-turn breakdown of what happened throughout
    """
    
    is_your_turn_first = rng_engine.rng(probability=50)
    your_wins, opponent_wins = 0, 0
    play_by_play_description = []
    for round in range(1, N_ROUNDS + 1):        
        play_by_play_description.append(f"\n{DASHES} Round {round}. {DASHES}")
        is_round_your_win, round_description = play_round(
            your_assignment=your_assignments / f"{round}.json",
            opponent_assignment=opponent_assignments / f"{round}.json",
            is_your_turn_first=is_your_turn_first,
            rng_engine=rng_engine
        )
        round_description = [f"\t{turn_description}" for turn_description in round_description]
        play_by_play_description.extend(round_description)
        
        if is_round_your_win:
            your_wins += 1
            round_outcome = "WIN"
        else:
            opponent_wins += 1
            round_outcome = "LOSS"
        play_by_play_description.append(
            f"\nOutcome: {round_outcome}. Series Score: {your_wins}-{opponent_wins}.")
        is_your_turn_first = not is_your_turn_first
        
        is_match_over = your_wins == N_WINS or opponent_wins == N_WINS
        if is_match_over:
            play_by_play_description.append(
                f"\n{DASHES} {round_outcome} {your_wins}-{opponent_wins}. {DASHES}")
            break
        
    return your_wins > opponent_wins, play_by_play_description
    
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument("--your_assignments", 
                        type=str, 
                        help="The location of the team assignment file to read",
                        default="./your_assignments",
                        required=False)
    parser.add_argument("--opponent_assignments", 
                        type=str, 
                        help="The location of the team assignment file to read",
                        default="./opponent_assignments",
                        required=False)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    your_assignments = Path(args.your_assignments)
    opponent_assignments = Path(args.opponent_assignments)
    rng_engine = RngEngine()
    match_outcome, description = play_match(your_assignments=your_assignments, 
               opponent_assignments=opponent_assignments, 
               rng_engine=rng_engine)
    if args.out is not None:
        with open(args.out, "w") as f:
            print(*description, sep="\n", file=f)
    else:
        print(*description, sep="\n")
