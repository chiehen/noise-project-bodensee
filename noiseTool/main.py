import time
import noiseTool.utils as utils

from typer import Typer

app = Typer()


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


if __name__ == "__main__":
    app()
