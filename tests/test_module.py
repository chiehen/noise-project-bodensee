import json
import os.path
import tempfile

from noiseTool.modules.Module import Module


def test_save_exists():
    func = getattr(Module, "save")
    assert callable(func)


class ModuleTests:
    def getTempFilePath(self):
        return f"{tempfile.gettempdir()}/noiseToolModules.json"

    def setUp(self):
        # check if the module file exists if yes -> delete it
        if os.path.exists(self.getTempFilePath()):
            os.remove(self.getTempFilePath())

    def test_save(self):
        class TestModule(Module):
            def __init__(self):
                pass

            def start(self):
                pass

            def stop(self):
                pass

            def get_name(self):
                return "test"

        module = TestModule()
        module.save("test", {"test": "test"})

        assert os.path.exists(self.getTempFilePath())

        with open(self.getTempFilePath(), "r") as f:
            content = f.read()

        self.assertEqual(json.loads(content), {"test": {"test": {"test": "test"}}})
