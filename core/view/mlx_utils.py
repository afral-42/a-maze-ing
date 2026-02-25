class MlxUtils:

    @staticmethod
    def get_color_value(r: int, g: int, b: int) -> int:
        color = b
        color |= g << 8
        color |= r << 16
        return color
