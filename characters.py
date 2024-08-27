from utils import BaseCharacter, Stats, Damage, Attack

class Ninja(BaseCharacter):
    @property
    def name(self) -> str:
        """Returns the name of the character."""
        return "Ninja"
    
    @property
    def special_attack_name(self) -> str:
        """Returns the name of the character's special attack."""
        return (
            "Special Attack: A precise poisoned dagger shot designed to "
            "incapacitate most opponents"
        )
        
    @property
    def special_attack(self) -> Attack:
        """
        Performs the Ninja's special attack: A poisoned dagger shot.

        This attack deals 40 base damage, plus additional damage equal
        to 50% of the Ninja's physical power and magic power.

        Returns:
        	Attack: An instance of the Attack class, encapsulating
        	the damage and a description of the attack
        """
        damage = Damage(physical = 
            40 + .5 * self.effective_stats.physical_power +
                .5 * self.effective_stats.magic_power
            )
        description = (f"{self.name} performed {self.special_attack_name},"
                        f" dealing {damage.physical} Physical Damage.")
        return Attack(damage = damage, description = description)
        
class Mage(BaseCharacter):
    @property
    def name(self) -> str:
        """Returns the name of the character."""
        return "Mage"
    
    @property
    def special_attack_name(self) -> str:
        """Returns the name of the character's special attack."""
        return "Special Attack: A lullaby to deep sleep"
    
    @property
    def special_attack(self) -> Attack:
        """
        Performs the Mage's special attack: A lullaby to deep sleep.

        This attack deals 1 base damage, plus additional damage equal
        to 125% of the Mage's magic power.

        Returns:
        	 Attack: An instance of the Attack class, encapsulating
        	 the damage and a description of the attack
        """
        damage = Damage(magic = 1 + 1.25 * self.effective_stats.magic_power)
        description = (f"{self.name} performed {self.special_attack_name},"
                       f" dealing {damage.magic} Magic Damage.")
        return Attack(damage = damage, description = description)


class Warrior(BaseCharacter):
    @property
    def name(self) -> str:
        """Returns the name of the character."""
        return "Warrior"
    
    @property
    def special_attack_name(self) -> str:
        """Returns the name of the character's special attack."""
        return "Special Attack: A call to the shield hero"
    
    @property
    def special_attack(self) -> Attack:
        """
        Performs the Warrior's special attack: A call to the shield hero.

        This 'attack' heals 50 base hp, plus additional hp equal
        to 75% of the Warrior's physical power and 300% of the Warrior's
        magic power.

        Returns:
        	Attack: An instance of the Attack class, encapsulating
        	the stat updates to self and a description of the attack
        """
        healing_done = (50 + .75 * self.effective_stats.physical_power +
                        3 * self.effective_stats.magic_power)
        description = (f"{self.name} performed {self.special_attack_name},"
                       f" healing {healing_done} HP.")
        return Attack(stat_updates_to_self = Stats(current_hp = healing_done),  
                      description = description)
    