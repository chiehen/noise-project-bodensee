import json
import os
import tempfile
import time
from dataclasses import asdict

import typer
from typer import Typer

import noiseTool.utils as utils
from noiseTool.modules.DummyNoise import DummyNoise
from noiseTool.modules.NetworkControl import NetworkControl, NetworkSetting

app = Typer()
noise_map = {
    DummyNoise.__name__: DummyNoise,
    NetworkControl.get_name(): NetworkControl
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
def network_control(
    delay: int = typer.Option(0, help="adds the chosen delay [ms] to the packets outgoing"),
    jitter: int = typer.Option(0, help="delay variation [ms]"),
    loss: int = typer.Option(0, help="packet loss rate [%]"),
    bandwidth: int = typer.Option(None, help="network bandwidth rate [Kbps]")
):
    """Register network control noise and parameter.
    """
    setting = NetworkSetting(delay=delay, jitter=jitter, loss=loss, bandwidth=bandwidth)

    print("set network configuration", asdict(setting))
    NetworkControl().save("setting", asdict(setting))


@app.command()
def activate():
    """Activate all registered noises"""
    settings = __read_noise_setting()

    for noise_name, noise_settings in settings.items():
        noise = __create_class_instance(noise_name, noise_settings)
        noise.start()


@app.command()
def deactivate():
    """Deactivate all registered noises"""
    settings = __read_noise_setting()

    for noise_name, noise_settings in settings.items():
        noise = __create_class_instance(noise_name, noise_settings)
        noise.stop()


def __read_noise_setting():
    content = "{}"

    tmp_dir = tempfile.gettempdir()
    tmp_filename = f"{tmp_dir}/noiseToolModules.json"
    if os.path.exists(tmp_filename):
        with open(tmp_filename, "r") as f:
            content = f.read()

    return json.loads(content)


def __create_class_instance(class_name, noise_settings):
    if class_name in noise_map:
        class_obj = noise_map[class_name]
        instance = class_obj(**noise_settings)
        return instance
    else:
        raise ValueError(f"Invalid class name: {class_name}")


if __name__ == "__main__":
    app()
