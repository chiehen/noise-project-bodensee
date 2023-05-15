import os
from abc import abstractmethod
import tempfile
import json


class Module:
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def save(self, key: str, settings: dict):
        try:
            tmp_dir = tempfile.gettempdir()
            tmp_filename = f"{tmp_dir}/noiseToolModules.json"
            content = "{}"

            if os.path.exists(tmp_filename):
                with open(tmp_filename, "r") as f:
                    content = f.read()

            # load the current settings
            current = json.loads(content)
            current.update({self.get_name(): {key: settings}})

            # save the settings
            with open(tmp_filename, "w") as f:
                f.write(json.dumps(current))

        except Exception as e:
            print(f"Could not save settings for module {key}.")
            raise e
