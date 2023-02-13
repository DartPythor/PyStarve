class GameError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MapFormatError(GameError):
    def __init__(self, *args):
        super().__init__(*args)
