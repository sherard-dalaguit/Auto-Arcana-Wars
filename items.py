from utils import BaseItem, Stats

class EnchantedSword(BaseItem):
    @property
    def name(self) -> str:
        """Returns the name of the item."""
        return "Enchanted Sword"
    
    @property
    def passive_name(self) -> str:
        """Returns the name of the item and its special ability."""
        return ("Unique Passive: Lucky strike. Adds 5%(+25% of base Special "
                "Trigger Chance) to Special Trigger chance.")
        
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Calculates the effective stats after equipping the item.

        The new stats will be based on the base character stats and
        the passive ability effects if the passive is active.

        Args:
        	character_stats (Stats): The basic character stats before equipping the item

        Returns:
        	Stats: The new character stats after equipping the item.
        """
        if self.is_passive_active:
            passive_special_chance = 5 + (.25 * character_stats.special_trigger_chance)
        else:
            passive_special_chance = 0
        passive_stats = Stats(special_trigger_chance = passive_special_chance)
        return self.base_item_stats.add_stat_changes(passive_stats)
        
        
class ShinyStaff(BaseItem):
    @property
    def name(self) -> str:
        """Returns the name of the item."""
        return "Shiny Staff"
    
    @property
    def passive_name(self) -> str:
        """Returns the name of the item and its special ability."""
        return ("Passive: Blessings of Echo. Adds 1(+50% of base Magic Power)"
                " to Magic Power.")
        
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Calculates the effective stats after equipping the item.

        The new stats will be based on the base character stats and
        the passive ability effects if the passive is active.

        Args:
        	character_stats (Stats): The basic character stats before equipping the item

        Returns:
        	Stats: The new character stats after equipping the item.
        """
        added_magic_power = 1 + .5 * character_stats.magic_power
        passive_stats = Stats(magic_power = added_magic_power)
        return self.base_item_stats.add_stat_changes(passive_stats)
    
    
class MagicCauldron(BaseItem):
    @property
    def name(self) -> str:
        """Returns the name of the item."""
        return "A magic cauldron"
    
    @property
    def passive_name(self) -> str:
        """Returns the name of the item and its special ability."""
        return ("Unique Passive: Potion of life. Adds 10(+30% of base HP) to HP")
    
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Calculates the effective stats after equipping the item.

        The new stats will be based on the base character stats and
        the passive ability effects if the passive is active.

        Args:
        	character_stats (Stats): The basic character stats before equipping the item

        Returns:
        	Stats: The new character stats after equipping the item.
        """
        if self.is_passive_active:
            passive_hp = 10 + .3 * character_stats.total_hp
        else:
            passive_hp = 0
        passive_stats = Stats(current_hp=passive_hp, total_hp=passive_hp)
        return self.base_item_stats.add_stat_changes(passive_stats)
    
class Pole(BaseItem):
    @property
    def name(self) -> str:
        """Returns the name of the item."""
        return "A Pole"
    
    @property
    def passive_name(self) -> str:
        """Returns the name of the item and its special ability."""
        return ""
     
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Calculates the effective stats after equipping the item.

        The new stats will be based on the base character stats and
        the passive ability effects if the passive is active.

        Args:
        	character_stats (Stats): The basic character stats before equipping the item

        Returns:
        	Stats: The new character stats after equipping the item.
        """
        return self.base_item_stats
    
    
class SolidRock(BaseItem):
    @property
    def name(self) -> str:
        """Returns the name of the item."""
        return "A solid rock"
    
    @property
    def passive_name(self) -> str:
        """Returns the name of the item and its special ability."""
        return ""
    
    def calculate_effective_stats(self, character_stats: Stats) -> Stats:
        """
        Calculates the effective stats after equipping the item.

        The new stats will be based on the base character stats and
        the passive ability effects if the passive is active.

        Args:
        	character_stats (Stats): The basic character stats before equipping the item

        Returns:
        	Stats: The new character stats after equipping the item.
        """
        return self.base_item_stats
