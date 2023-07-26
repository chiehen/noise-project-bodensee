import subprocess

from typer import Typer, Argument

from noiseTool.modules.Module import Module

app = Typer()


class ConstantRequestModule(Module):
    """SendRequestModule is a module that uses the send_request program to stress network with dummy requests."""
    # Save the parameters for the send_request tool
    params: str

    def __init__(self, params: str, **kwargs):
        """Initializes the SendRequestModule"""
        super().__init__(**kwargs)
        self.params = params

    def start(self):
        """Starts the send-requests tool as a subprocess and passes the parameters to it"""
        print(f"Starting send_request with parameters {self.params}")
        subprocess.Popen(f"python3 /SendRequest.py {self.params}", shell=True)

    def stop(self):
        """Stops the send_request tool by killing the process"""
        terminate_command = "pkill -f SendRequest"
        subprocess.Popen(terminate_command, shell=True)

    @staticmethod
    def get_name():
        """Returns the name of the module"""
        return "send_request"

    def add(self):
        """Adds the module to the list of modules"""
        print(f"Send_request is added with parameters {self.params}")
        self.save("params", self.params)


@app.command(help="Adds the send_request module to the list of modules. You can pass the parameters directly to send_request",
             name="add")
def add_send_request(params: str = Argument(..., help="The parameters for the stress-ng tool. Replace the params -- with "
                                                      "^ (e.g. --cpu 2 becomes ^cpu 2)")):
    """Adds the send_request module to the list of modules"""
    ConstantRequestModule(params.replace("^", "-")).add()
