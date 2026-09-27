import json

class TabQLCheckpointStore:
    @staticmethod
    def save(filename, checkpoint):
        data = checkpoint.to_data()
        with open(filename, 'w') as file:
            json.dump(data, file)
