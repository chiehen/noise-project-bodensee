import subprocess
from dataclasses import dataclass
from typing import Optional

from noiseTool.modules.Module import Module


@dataclass
class NetworkSetting:
    delay: int = 0 
    jitter: int = 0
    loss: int = 0
    bandwidth: Optional[int] = None


class NetworkControl(Module):
    """Configure the Linux kernel packet scheduler"""
    def __init__(self, **kwargs):
        self.setting = NetworkSetting(**kwargs)

    def start(self):
        cmd = ["tcset", "eth0"]
        if self.setting.bandwidth:
            cmd += ["--rate", f"{self.setting.bandwidth}Kbps"]
        cmd += ["--delay", f"{self.setting.delay}",
                "--delay-distro", f"{self.setting.jitter}", "--loss", f"{self.setting.loss}%", "--overwrite"]

        print(cmd)
        subprocess.run(cmd)

    def stop(self):
        cmd = ["tcdel", "eth0", "--all"]
        subprocess.run(cmd)

    def get_name(self):
        return self.__class__.__name__
