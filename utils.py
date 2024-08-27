from typing import NamedTuple
import abc
import math
import numpy as np
from dataclasses import dataclass

N_ITEMS = 3


class RngEngine:
    def __init__(self, seed: int = 56) -> None:
        """Create the RNG backend for the game

        NOTE: DO NOT create an instance of this class. 
                It is already created where needed

        Keyword Arguments:
            seed -- the pseudo rng seed to use (default: {56})
        """
        self._rand = np.random.default_rng(seed=seed)

    def rng(self, probability: float) -> bool:
        """Roll a dice with the probability and see if the result is
            within that bet. 
            
            NOTE: DO NOT call this function. 
                It is already called where needed 

        Arguments:
            probability -- the probability of rolling the expected outcome, a number from [0-100]

        Returns:
            Whether or not the expected outcome was rolled. 
                True if it was, False otherwise
        """
        return self._rand.random() < (probability / 100)


class Stats(NamedTuple):
    current_hp: float = 0
    total_hp: float = 0
    armor: float = 0
    magic_resistance: float = 0
    physical_power: float = 0
    magic_power: float = 0
    special_trigger_chance: float = 0

    def add_stat_changes(self, changes: "Stats") -> "Stats":
        """
        Updates the stats based on the provided changes while ensuring
        that the values remain within their appropriate ranges.

        Args:
        	changes (Stats): The stat changes to be applied.

        Returns:
        	Stats: The updated stats after the changes have been applied.

        Note:
        	The current HP cannot exceed total HP and is ensured to be at least 0.
        	The special trigger chance is capped at 100.
        """
        new_stats = {}
        for stat_name, [min_val, max_val] in [
                ["total_hp", [0, math.inf]],
                ["current_hp", [0, "total_hp"]],
                ["armor", [0, math.inf]],
                ["magic_resistance", [0, math.inf]],
                ["physical_power", [0, math.inf]],
                ["magic_power", [0, math.inf]],
                ["special_trigger_chance", [0, 100]]]:
            new_stat = getattr(self, stat_name) + getattr(changes, stat_name)
            if max_val == "total_hp":
                max_val = new_stats["total_hp"]  # to cap current hp to new max hp
            normalized_stat = min(max_val, max(min_val, new_stat))
            new_stats[stat_name] = normalized_stat
        return Stats(**new_stats)

    def __str__(self) -> str:
        """
        Returns a formatted string providing detailed information about the object's attributes.
        """
        formatted_stats = [f"{formatted_name}: {stat:.1f}"
            for formatted_name, stat in [
                ["Current HP", self.current_hp],
                ["Total HP", self.total_hp],
                ["Armor", self.armor],
                ["Magic Resistance", self.magic_resistance],
                ["Physical Power", self.physical_power],
                ["Magic Power", self.magic_power],
                ["Special Trigger Chance", self.special_trigger_chance]
            ]
        ]
        return "\n".join(formatted_stats)


class Damage(NamedTuple):
    """
    A NamedTuple representing the amount of damage inflicted in an attack.

    Attributes:
    	physical (float): The amount of physical damage inflicted. Defaults to 0
    	magic (float): The amount of magic damage inflicted. Defaults to 0
    """
    physical: float = 0
    magic: float = 0


class Attack(NamedTuple):
    """
    A NamedTuple representing an attack in the game.

    Attributes:
    	damage (Damage): The damage inflicted by the attack. Defaults to None
    	stat_updates_to_self (Stats): The updates to the attacker's stats as
    	a result of the attack. Defaults to None.
    	description (str): A textual description of the attack. Defaults to None.
    """
    damage: Damage = None
    stat_updates_to_self: Stats = None
    description: str = None


@dataclass
class DamageStats:
    """
        The DamageStats class tracks and aggregates damage-related statistics for characters during a round.

        Each character will include this DamageStats class to provide an additional set of detailed statistics related
        to damage dealt, taken, mitigated, and number of kills.

        Attributes:
            damage_dealt: Total damage output, regardless of the HP lost by the opponent.
            damage_taken: Total damage taken, regardless of the HP lost by the character.
            damage_mitigated: Calculated as damage taken minus HP lost.
            kills: The number of opponent characters killed.

        Note that these attributes are adjusted during and after the game rounds. They are intended to provide an in-depth
        statistic that can inform strategies and character assignments in subsequent rounds.
    """
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    damage_mitigated: float = 0.0
    kills: int = 0


class BaseItem(abc.ABC):
    """
    BaseItem is an abstract base class the represents a generic
    item in a game. Specific items should inherit from this class
    and customize the 'name', 'passive_name', and 'calculate_effective_stats'
    methods to match their individual behaviors.

    The class serves as a contract for what each item should include
    """
    def __init__(self, base_item_stats: Stats,
                 is_passive_active: bool = True) -> None:
        """
        Initialize an instance of the BaseItem class

        Args:
        	base_item_stats (Stats): The base statistics associated with the item.
        	is_passive_active (bool): The state indicating if the passive is active.
        """
        super().__init__()
        self.base_item_stats = base_item_stats
        self.is_passive_active = is_passive_active

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Abstract method representing a 'name' property.

        This method is intended to be overridden in subclasses to
        return the name of the item as a string.

        Returns:
        	str: The name of the item
        """
        pass

    @property
    @abc.abstractmethod
    def passive_name(self) -> str:
        """
        Abstract method representing a 'passive_name' property

        This property is intended to be overridden in subclasses to
        return the passive name of the item as a string.

        Returns:
        	str: The name and passive effect of the item.
        """
        pass

    @abc.abstractmethod
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Abstract method to calculate effective statistics.

        This method should be overridden by subclasses to provide
        functionality that takes base character stats
        and calculates some effective stats.

        Args:
        	base_character_stats (Stats): The original statistics of a
        	character before applying the item effect.

        Returns:
        	Stats: The calculated statistics after applying the item effect.
        """
        pass

    def __eq__(self, value: object) -> bool:
        """
        Overrides the default implementation of the equality operator.
        Two objects of class BaseItem are considered equal if the 'name'
        properties are the same.

        Args:
        	other (Any): The other object that this BaseItem will be compared to.

        Returns:
        	bool: True if the other object is an instance of BaseItem and its
        	name property is the same as this BaseItem's. False otherwise
        """
        if not isinstance(value, BaseItem):
            return False
        else:
            return self.name == value.name

    def __str__(self) -> str:
        """
            Defines the string representation of a BaseItem object.

            This method returns a string that provides detailed information about the
            BaseItem object, including its type and any other relevant attributes.
            This string representation is primarily used for debugging and logging purposes.

            Returns:
                str: A string representation of the BaseItem object.
            """
        stats = str(self.base_item_stats).split("\n")
        useful_stats = []
        for stat in stats:
            _, stat_value = stat.split(":")
            stat_value = float(stat_value)
            if stat_value > 0:
                useful_stats.append(stat)
        if self.is_passive_active:
            useful_stats.append(self.passive_name)
        useful_stats = "\n".join(useful_stats)
        return f"{self.name}: \n{useful_stats}"


class BaseCharacter(abc.ABC):
    """
	BaseCharacter is an abstract base class for a character entity. It lays the
	foundation for how a character should be structured in the context of this application
	with methods for managing items, accessing character's name and their special attack.

	Attributes:
		base_stats (Stats): initial stats of the character;
		added_item_stats (Stats): stats gained from items;
		effective_stats (Stats): current stats after applying items;
		items (list[BaseItem]): items held by the character
	"""
    def __init__(self, base_stats: Stats) -> None:
        """
        Initialize BaseCharacter with base stats, added stats, effective stats and items.

        Args:
        	base_stats (Stats): initial stats of the character;
        """
        super().__init__()
        self.base_stats = base_stats
        self.added_item_stats = Stats()
        self.effective_stats = self.base_stats
        self.items = []
        self.damage_stats = DamageStats()

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
		Abstract property for the character's name.
		"""
        pass

    @property
    @abc.abstractmethod
    def special_attack_name(self) -> str:
        """
        Abstract property for the character's special attack name.
        """
        pass

    def add_item(self, item: BaseItem) -> None:
        """
        Adds an item to the character's inventory and updates the effective stats
        with the effective item stats. If the character already has 3 items or
        if the item has a unique passive which is already active, raises an exception.

        Args:
        	item (BaseItem): Item to be added which affects effective stats.

        Raises:
        	ValueError:
        		If character already has 3 items or if item's unique passive is already active.

        Notes:
        	This method modifies the character's added_item_stats to account for the effective
        	stats of the added item. This means the added_item_stats represent the cumulative
        	impact of all items so far added to the character, based on their effective stats.
        """
        if len(self.items) == N_ITEMS:
            raise ValueError("Attempted to add more items than allowed in game.")

        if "Unique Passive" in item.passive_name and item in self.items:
            item.is_passive_active = False

        self.items.append(item)
        self.added_item_stats = self.added_item_stats.add_stat_changes(
            item.calculate_effective_stats(self.base_stats))
        self.effective_stats = self.base_stats.add_stat_changes(
            self.added_item_stats)

    def __str__(self) -> str:
        """
            Defines the string representation of a BaseCharacter object.

            This method returns a string that gives detailed information about the
            BaseCharacter object, including its name, character type, health points,
            and any other relevant attributes. This string representation is primarily
            used for debugging and logging purposes.

            Returns:
                str: A string representation of the BaseCharacter object.
        """
        formatted_stats = str(self.effective_stats).replace("\n", "\n\t")
        item_stats = ""
        for item_idx, item in enumerate(self.items):
            formatted_item_info = str(item).replace("\n", "\n\t\t\t")
            item_stats += f"\n\t\t{(item_idx + 1)}: {formatted_item_info}"
        if item_stats:
            formatted_item_stats = f"\n\t  with items {item_stats}"
        else:
            formatted_item_stats = ""
        return (f"{self.name}: \n\t{formatted_stats}" 
                f"{formatted_item_stats}")

    @property
    def basic_attack(self) -> Attack:
        """
        Creates a Basic Attack instance based on teh character's effective stats.
        This represents a universal attack that every character can perform.

        The damage done is impacted by the character's physical power. The return Attack
        instance encapsulates the damage done as well as a textual description of the action.

        Returns:
        	Attack: An object representing the damage dealt by the attack
        	and a description of the attack itself.
        """
        damage = Damage(physical=self.effective_stats.physical_power)
        description = (f"{self.name} performed a Basic Attack, "
                       f"dealing {damage.physical} Physical Damage.")
        return Attack(damage=damage, description=description)

    @property
    @abc.abstractmethod
    def special_attack(self) -> Attack:
        """
        Abstract property for the character's special attack.
        """
        pass
