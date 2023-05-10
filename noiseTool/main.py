import time
import noiseTool.utils as utils
from noiseTool.modules.DummyNoise import DummyNoise

from typer import Typer

app = Typer()
noises = []


@app.command()
def printNumbers(randomNumbers: bool = False):
    """This is just a dummy function. Feel free to delete everything.

    Args:
        randomNumbers (bool, optional): Indicates whether cool random numbers should be printed instead of a constant. Defaults to False.
    """
    while True:
        number = utils.get_cool_random_number() if randomNumbers else 25
        print(f"Your number is {number}. This number is{' not' if not utils.is_number_cool(number) else ''} cool.")
        time.sleep(1)


@app.command()
def addDummyNoise():
    """Dummy function for registering noise.
    Please delete it after real noise is implemented.
    """
    noises.append(DummyNoise())


@app.command()
def activate():
    """Activate all registered noises"""
    # load configuration from ???

    for noise in noises:
        noise.start()


@app.command()
def deactivate():
    """Deactivate all registered noises"""
    for noise in noises:
        noise.stop()


if __name__ == "__main__":
    app()
