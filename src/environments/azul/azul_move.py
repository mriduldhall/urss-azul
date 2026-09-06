from enum import Enum

class SourceType(Enum):
    FACTORY = 1
    CENTER = 2

class DestinationType(Enum):
    PATTERN_LINE = 1
    FLOOR_LINE = 2

class AzulMove:
    def __init__(self, source_type, source_index, tile, destination_type, destination_index):
        self.source_type = source_type
        self.source_index = source_index
        self.tile = tile
        self.destination_type = destination_type
        self.destination_index = destination_index

    def __eq__(self, other):
        if isinstance(other, AzulMove):
            return (self.source_type is other.source_type and
                    self.source_index == other.source_index and
                    self.tile is other.tile and
                    self.destination_type is other.destination_type and
                    self.destination_index == other.destination_index)
        return object.__eq__(self, other)
