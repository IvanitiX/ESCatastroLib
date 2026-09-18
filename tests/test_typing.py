from escatastrolib.parsers.typing import to_str, to_int, to_float, to_bool, to_dict


class TestToStr:
    def test_none_returns_none(self):
        assert to_str(None) is None

    def test_empty_string_returns_none(self):
        assert to_str("") is None

    def test_whitespace_only_returns_none(self):
        assert to_str("   ") is None

    def test_strips_whitespace(self):
        assert to_str("  hola  ") == "hola"

    def test_no_strip(self):
        assert to_str("  hola  ", strip=False) == "  hola  "

    def test_int_to_str(self):
        assert to_str(42) == "42"

    def test_float_to_str(self):
        assert to_str(3.14) == "3.14"


class TestToInt:
    def test_none_returns_none(self):
        assert to_int(None) is None

    def test_empty_string_returns_none(self):
        assert to_int("") is None

    def test_valid_int(self):
        assert to_int("42") == 42

    def test_float_string(self):
        assert to_int("3.14") == 3

    def test_invalid_string_returns_none(self):
        assert to_int("abc") is None

    def test_bool_returns_int(self):
        assert to_int(True) == 1
        assert to_int(False) == 0

    def test_int_passthrough(self):
        assert to_int(42) == 42


class TestToFloat:
    def test_none_returns_none(self):
        assert to_float(None) is None

    def test_empty_string_returns_none(self):
        assert to_float("") is None

    def test_valid_float(self):
        assert to_float("3.14") == 3.14

    def test_comma_decimal(self):
        assert to_float("3,14") == 3.14

    def test_int_string(self):
        assert to_float("42") == 42.0

    def test_invalid_returns_none(self):
        assert to_float("abc") is None

    def test_float_passthrough(self):
        assert to_float(3.14) == 3.14


class TestToBool:
    def test_none_returns_default(self):
        assert to_bool(None) is False

    def test_none_with_custom_default(self):
        assert to_bool(None, default=True) is True

    def test_empty_returns_default(self):
        assert to_bool("") is False

    def test_true_strings(self):
        for val in ["true", "1", "yes", "y", "si", "sí", "s", "True", "YES"]:
            assert to_bool(val) is True

    def test_false_strings(self):
        for val in ["false", "0", "no", "n", "False", "NO"]:
            assert to_bool(val) is False

    def test_int_zero(self):
        assert to_bool(0) is False

    def test_int_nonzero(self):
        assert to_bool(1) is True
        assert to_bool(42) is True

    def test_bool_passthrough(self):
        assert to_bool(True) is True
        assert to_bool(False) is False


class TestToDict:
    def test_none_returns_none(self):
        assert to_dict(None) is None

    def test_string_returns_none(self):
        assert to_dict("hello") is None

    def test_list_returns_none(self):
        assert to_dict([1, 2, 3]) is None

    def test_dict_returns_dict(self):
        d = {"a": 1, "b": 2}
        assert to_dict(d) == d

    def test_returns_new_dict(self):
        d = {"a": 1}
        result = to_dict(d)
        result["b"] = 2
        assert "b" not in d
