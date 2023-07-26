import json
import os
import tempfile
from dataclasses import asdict

import typer
from typer import Typer

from noiseTool.modules.DummyNoise import DummyNoise
from noiseTool.modules.NetworkControl import NetworkControl, NetworkSetting
from noiseTool.modules.StessNGModule import StressNGModule, app as stress_ng_app
from noiseTool.modules.ConstantRequestModule import ConstantRequestModule, app as send_request


app = Typer()
app.add_typer(stress_ng_app, name="stress-ng", help="Module using Stress NG to stress the CPU, memory, etc.")
app.add_typer(send_request, name="send_request", help="Module to stress the server with dummy HTTP requests.")

noise_map = {
    DummyNoise.__name__: DummyNoise,
    NetworkControl.get_name(): NetworkControl,
    StressNGModule.get_name(): StressNGModule,
    ConstantRequestModule.get_name(): ConstantRequestModule,
}


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
def addConstantRequest():
    """Register constant request module.
    """
    setting = {}
    print("set network configuration", asdict(setting))
    ConstantRequestModule().save("setting", asdict(setting))


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
