"""Test snews_pt installation"""

def test_import():
    try:
        import snews_pt
    except Exception as exc:
        print('Could not import snews_pt!\n')
        assert False, f"'import snews_pt' raised an exception:\n {exc}"