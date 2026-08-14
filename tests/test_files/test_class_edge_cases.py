class TestEdgeCases:
    marker = 'not a test at all'

    def helper_method(self, capsys):
        return capsys

    def test_without_self_argument():
        pass

    @staticmethod
    def test_static_method_with_unused_fixture(caplog):
        assert True
