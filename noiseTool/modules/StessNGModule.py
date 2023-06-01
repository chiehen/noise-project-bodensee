import subprocess

from typer import Typer, Argument

from noiseTool.modules.Module import Module

app = Typer()


class StressNGModule(Module):
    """StressNGModule is a module that uses the stress-ng tool to stress the CPU, memory, IO, etc."""
    # Save the parameters for the stress-ng tool
    params: str

    def __init__(self, params: str, **kwargs):
        """Initializes the StressNGModule"""
        super().__init__(**kwargs)
        self.params = params

    def start(self):
        """Starts the stress-ng tool as a subprocess and passes the parameters to it"""
        print(f"Starting stress-ng with parameters {self.params}")
        subprocess.Popen(f"stress-ng {self.params}", shell=True)

    def stop(self):
        """Stops the stress-ng tool by killing the process"""
        terminate_command = "pkill -f stress-ng"
        subprocess.Popen(terminate_command, shell=True)

    @staticmethod
    def get_name():
        """Returns the name of the module"""
        return "stress_ng"

    def add(self):
        """Adds the module to the list of modules"""
        print(f"Stress-ng is added with parameters {self.params}")
        self.save("params", self.params)


@app.command(help="Adds the stress-ng module to the list of modules. You can pass the parameters directly to stress-ng",
             name="add")
def add_stress_ng(params: str = Argument(..., help="The parameters for the stress-ng tool. Replace the params -- with "
                                                   "^ (e.g. --cpu 2 becomes ^cpu 2)")):
    """Adds the stress-ng module to the list of modules"""
    StressNGModule(params.replace("^", "-")).add()
