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

    def __post_init__(self):
        if self.delay < 0 or self.delay > 100000:
            raise ValueError('Delay must be between 0 and 100000ms')
        elif self.jitter < 0 or self.jitter > 100000 or (self.delay == 0 and self.jitter > 0):
            raise ValueError('Jitter must be between 0 and 100000, and delay > 0')
        elif self.loss < 0 or self.loss > 100:
            raise ValueError('Packet loss must be between 0 and 100')
        elif self.bandwidth is not None and self.bandwidth <= 0:
            raise ValueError('Bandwidth must be greater than 0')
        elif (self.delay + self.jitter + self.loss) == 0 and (self.bandwidth is None):
            raise ValueError('No network noise is imposed')


class NetworkControl(Module):
    """Configure the Linux kernel packet scheduler"""
    def __init__(self, **kwargs):
        if kwargs:
            self.setting = NetworkSetting(**kwargs["setting"])

    def start(self):
        cmd = ["tcset", "eth0"]
        if self.setting.bandwidth:
            cmd += ["--rate", f"{self.setting.bandwidth}Kbps"]
        cmd += ["--delay", f"{self.setting.delay}",
                "--delay-distro", f"{self.setting.jitter}", "--loss", f"{self.setting.loss}%", "--overwrite"]

        print(f"NetworkControl: Running command{cmd}")
        subprocess.run(cmd)

    def stop(self):
        cmd = ["tcdel", "eth0", "--all"]
        subprocess.run(cmd)

    def get_name(self):
        return self.__class__.__name__
