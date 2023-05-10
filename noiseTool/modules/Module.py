from abc import abstractmethod
import tempfile
import json


class Module:
    @abstractmethod
    def __init(self, **kwargs):
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

    def save(self, settings, key):
        try:
            # create a temporary file
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.name = "noiseToolModules.json"
            current_str = tmp.read()

            # load the current settings
            current = json.loads(current_str)
            current[self.get_name()][key] = settings

            # write the new settings
            tmp.write(json.dumps(current))
            tmp.close()
        except Exception as e:
            print(f"Could not save settings for module {key}.")
            raise e
