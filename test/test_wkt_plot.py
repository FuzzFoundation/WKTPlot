from wktplot import wkt_plot

MOCK_SAVE_DIR = '/tmp/mock_me_up_scotty'

def setup_tests():
    test_obj = wkt_plot.WKTPLOT(MOCK_SAVE_DIR)
    return test_obj

def test_to_appease_pipeline():
    test_obj = setup_tests()
    assert MOCK_SAVE_DIR in test_obj.save_dir
