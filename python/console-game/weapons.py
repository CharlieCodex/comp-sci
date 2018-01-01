from ship import *
from enum import Enum
import numpy as np


class Damage:
    """Container for an unapplied typed damage amount
       (Used for handing 'armor' mechanics)"""

    def __init__(self, amount, type_name):
        self.amount = amount
        self.type_name = type_name


class EnergyDamage(Damage):
    """Container for an unapplied phased energy 'Damage'"""

    def __init__(self, amount, phase):
        super().__init__(amount, "Energy")
        self.phase = phase


class Weapon(Component):
    """General component from which all weapons extend,
       enforcing all inherit the attack member function"""

    def __init_subclass__(cls):
        if not cls.attack:
            assert TypeError("All weapons must"
                             " implement the attack member function")


class EnergyWeapon(Weapon):
    """Weapon component which allows for JIT creation of
       phased energy weapons"""

    def __init__(self, name, amplitude, phase=0):
        self.name = name
        self.amplitude = amplitude
        self.phase = phase

    def attack(self, ship, target):
        dist = ship.distance(target)
        damage = EnergyDamage(self.amplitude / np.sqrt(dist), self.phase)
        return damage


class Sheild(Component):
    """General component from which all sheilds extend,
       enforcing all inherit the mitigate member function"""

    def __init_subclass__(cls):
        if not cls.mitigate:
            assert TypeError("All sheilds must"
                             " implement the mitigate member function")


class EnergySheild(Sheild):
    """Sheild component which allows for JIT creation of
       phased energy sheilds"""

    def __init__(self, amplitude, phase=0):
        self.amplitude = amplitude
        self.phase = phase

    def mitigate(self, ship, damage):
        if isinstance(damage, EnergyDamage):
            phi = damage.phase - self.phase
            # ensure phi is in the correct range (0 <= x <= 1)
            x = abs(phi % (2 * np.pi) / (2 * np.pi))
            # just a pretty mitigation function equal
            # to one for values near 0 and 0 for values near 1
            mitigation = x ** 2 - 2 * x + 1
            damage.amount *= mitigation
        return damage
