"""Test SNEWS_PT installation"""

def test_import():
    try:
        import SNEWS_PT
    except Exception as exc:
        print('Could not import SNEWS_PT!\n')
        assert False, f"'import SNEWS_PT' raised an exception:\n {exc}"