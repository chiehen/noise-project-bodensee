from modules.Module import Module


class DummyNoise(Module):
    """Dummy Class just to test CLI interface. Please remove after inplement real noise."""
    def __init__(self, **kwargs):
        print(kwargs)
        print("dummy noise init.")

    def start(self):
        print("dummy noise starts.")

    def stop(self):
        print("dummy noise stops.")

    def get_name(self):
        return self.__class__.__name__
