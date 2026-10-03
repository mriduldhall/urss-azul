from environments.azul.tiles import Tiles
from environments.azul.azul_move import AzulMove, SourceType, DestinationType

class AzulActionMapping:
    def __init__(self):
        self.mapping = []
        for source_index in range(5):
            for tile in Tiles:
                if tile == Tiles.STARTING:
                    continue
                for destination in DestinationType:
                    if destination == DestinationType.PATTERN_LINE:
                        for destination_index in range(5):
                            self.mapping.append(AzulMove(SourceType.FACTORY, source_index, tile, destination, destination_index))
                    else:
                        self.mapping.append(AzulMove(SourceType.FACTORY, source_index, tile, destination, 0))

        for tile in Tiles:
            if tile == Tiles.STARTING:
                continue
            for destination in DestinationType:
                if destination == DestinationType.PATTERN_LINE:
                    for destination_index in range(5):
                        self.mapping.append(
                            AzulMove(SourceType.CENTER, 0, tile, destination, destination_index))
                else:
                    self.mapping.append(AzulMove(SourceType.CENTER, 0, tile, destination, 0))

    def get_mapping(self, move):
        return self.mapping.index(move)

    @staticmethod
    def get_config():
        return "azul-action-mapping"
