class AzulActionEncoder:
    @staticmethod
    def encode(move):
        encoded_action = ""
        encoded_action += str(move.source_type.value)
        encoded_action += str(move.source_index)
        encoded_action += move.tile.value
        encoded_action += str(move.destination_type.value)
        encoded_action += str(move.destination_index)
        return encoded_action

    @staticmethod
    def get_config():
        return "azul-action-encoder"
