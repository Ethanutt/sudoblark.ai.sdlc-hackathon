import dungeon


def test_package_imports_with_a_version():
    assert dungeon.__version__ == "0.1.0"
