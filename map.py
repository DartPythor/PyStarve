import load_functions
from errorsTypes import MapFormatError


class Map:
    def __init__(self, level: list, tiles_types: dict):
        self.level = level
        self.tiles_types = tiles_types
        self.array_tile = self._create_array_tile(level)

    def _create_array_tile(self, level: list) -> list:
        result = []

        for y, column in enumerate(level):
            column_result = []

            for x, item in enumerate(column):
                if item not in self.tiles_types:
                    raise MapFormatError(f"Invalid format map '{item}'")
                column_result.append(self.tiles_types[item])

            result.append(column_result)

        return result

    def update(self) -> None:
        ...


if __name__ == '__main__':
    map = Map(load_functions.load_level("test_map.txt"), {"#": 1, ".": 2, "p": 3})
    print(map.array_tile)

