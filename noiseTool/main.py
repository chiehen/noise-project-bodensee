import json
import os
import tempfile
import time

from typer import Typer

import noiseTool.utils as utils
from noiseTool.modules.DummyNoise import DummyNoise

app = Typer()
noise_map = {
    "dummynoise": DummyNoise
}


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
    DummyNoise().save("test", {"test": "test"})


@app.command()
def activate():
    """Activate all registered noises"""
    tmp_dir = tempfile.gettempdir()
    tmp_filename = f"{tmp_dir}/noiseToolModules.json"
    content = "{}"
    if os.path.exists(tmp_filename):
        with open(tmp_filename, "r") as f:
            content = f.read()

    # load the current settings
    current = json.loads(content)

    for noise_name, noise_settings in current.items():
        noise = __create_class_instance(noise_name, noise_settings)
        noise.start()


@app.command()
def deactivate():
    """Deactivate all registered noises"""
    tmp_dir = tempfile.gettempdir()
    tmp_filename = f"{tmp_dir}/noiseToolModules.json"
    content = "{}"
    if os.path.exists(tmp_filename):
        with open(tmp_filename, "r") as f:
            content = f.read()

    # load the current settings
    current = json.loads(content)

    for noise_name, noise_settings in current.items():
        noise = __create_class_instance(noise_name, noise_settings)
        noise.stop()


def __create_class_instance(class_name, noise_settings):
    if class_name in noise_map:
        class_obj = noise_map[class_name]
        instance = class_obj(**noise_settings)
        return instance
    else:
        raise ValueError(f"Invalid class name: {class_name}")


if __name__ == "__main__":
    app()
