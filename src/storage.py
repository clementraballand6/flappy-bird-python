class S:
    ASSETS_PATH = "assets/"
    WINDOW_SIZE = (432, 768)

    @staticmethod
    def save_sprite(name, image):
        name = name.upper()
        if not hasattr(S, name):
            setattr(S, name, image)
            setattr(S, name + "_RECT", image.get_rect())
