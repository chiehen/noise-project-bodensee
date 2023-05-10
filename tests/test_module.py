from noiseTool.modules.Module import Module


def test_save_exists():
    func = getattr(Module, "save")
    assert callable(func)
