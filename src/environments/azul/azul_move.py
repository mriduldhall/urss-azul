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
