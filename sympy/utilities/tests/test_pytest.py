from sympy.utilities.pytest import raises

def test_raises_okay_if_expected_exception():
    def f():
        raise ValueError()
    raises(ValueError, f)
    raises(ValueError, "raise ValueError")

def test_not_okay_if_no_exception():
    try:
        raises(Exception, lambda: 1+1)
        assert False
    except Exception, e:
        assert str(e) == "DID NOT RAISE"

    try:
        raises(Exception, '1 + 1')
        assert False
    except Exception, e:
        assert str(e) == "DID NOT RAISE"

def test_not_okay_if_wrong_exception():
    def f():
        raise ValueError()
    try:
        raises(TypeError, f)
        assert False
    except ValueError:
        pass

    try:
        raises(TypeError, "raise ValueError")
        assert False
    except ValueError:
        pass

# Now we can use raises() instead of try/catch
# to test that a specific exception class is raised

def test_second_argument_should_be_callable_or_string():
    raises(TypeError, lambda: raises(Exception, 42))
