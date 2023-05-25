import json
import os
import tempfile
import time

from typer import Typer

import noiseTool.utils as utils
from noiseTool.modules.DummyNoise import DummyNoise
from noiseTool.modules.StessNGModule import StressNGModule, app as stress_ng_app

app = Typer()
app.add_typer(stress_ng_app, name="stress-ng", help="Module using Stress NG to stress the CPU, memory, etc.")

noise_map = {
    DummyNoise.__name__: DummyNoise,
    StressNGModule.get_name(): StressNGModule,
}


@app.command()
def addDummyNoise():
    """Dummy function for registering noise.
    Please delete it after real noise is implemented.
    """
    DummyNoise().save("test", {"test": "test"})


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
