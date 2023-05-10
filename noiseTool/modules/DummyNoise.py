from modules.Module import Module

class DummyNoise(Module):
    def __init(self, **kwargs):
        print("dummy noise init.")

    def start(self):
        print("dummy noise starts.")

    def stop(self):
        print("dummy noise starts.")

    def get_name(self):
        pass
