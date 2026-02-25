class WallChecker:

    @staticmethod
    def north_wall(cell: int) -> bool:
        return (cell & 1) > 0

    @staticmethod
    def east_wall(cell: int) -> bool:
        return (cell & 2) > 0

    @staticmethod
    def south_wall(cell: int) -> bool:
        return (cell & 4) > 0

    @staticmethod
    def west_wall(cell: int) -> bool:
        return (cell & 8) > 0
