from core.twin.hub.twin_hub import TwinHub


class Twin:
    def __init__(self):
        pass

    @staticmethod
    def start():
        th = TwinHub()
        th.start()


if __name__ == "__main__":
    Twin.start()
