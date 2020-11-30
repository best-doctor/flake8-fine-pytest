class TestClass:
    def test_one(self, caplog, capsys):
        assert caplog

    @classmethod
    def test_two(cls, caplog):
        assert caplog

    def three(self, caplog):
        pass

    # this method's signature is broken on purpose.
    def four():
        pass
