from Location import *


class Component:
    """Container for different ship components"""

    def __init__(self, name):
        self.name = name


class Frame:
    """Container for different ship configuration"""

    def __init__(self, name, configuration={}):
        self.name = name
        self.configuration = configuration

    def compatable(self, comp):
        """Check if a component will fit into the frames configuration"""
        for cls in self.configuration:
            if isinstance(comp, cls):
                return True
        return False

    def available_slots(self, comp):
        """Check if a component will fit into the frames configuration"""
        slots = []
        for cls in self.configuration:
            if isinstance(comp, cls):
                slots.append(cls)
        return slots


class HardwareManager:
    """Manager for slotting equipment into a frame"""

    def __init__(self, frame):
        self.frame = frame
        self.hardware = {}
        self.configuration = frame.configuration

    def compatable(self, comp):
        """Check if a component will fit into the frames configuration"""
        return self.frame.compatable(comp)

    def add(self, comp):
        if self.compatable(comp):
            if comp.type in self.hardware:
                slots = self.hardware[comp.type]
                if len(slots) < len(self.configuration[comp.type]):
                    slots.append(comp)
                    return True
            else:
                self.hardware[comp.type] = [comp]
                return True
        return False

    def swap(self, comp, index):
        if comp.type in self.hardware:
            n = len(self.hardware[comp.type])
            if index < n - 1:
                self.hardware[comp.type][index] = comp
                return True
            else:
                return False
        return False


class Ship:
    """Container for a frame, hardware setup, software, and location"""

    def __init__(self, location, frame):
        self.hwm = HardwareManager(frame)
        self.location = location

    def add_component(self, comp):
        return self.hwm.add(comp)

    def swap_component(self, comp, index):
        return self.hwm.swap(comp, index)

    def distance(self, other):
        if isinstance(other, Ship):
            return self.location.distance(other.location)
        elif isinstance(other, Location) or isinstance(other, _Location):
            return self.location.distance(other)


if __name__ == '__main__':
    print('you meant to run another file .... . .. . ..')
