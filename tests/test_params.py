import unittest

from boxbotapi.params import Params


class TestParams(unittest.TestCase):
    def test_add_non_empty(self) -> None:
        params = Params()
        params.AddNonEmpty("value", "value")
        self.assertEqual(1, len(params))
        self.assertEqual("value", params["value"])

        params.AddNonEmpty("test", "")
        self.assertEqual(1, len(params))
        self.assertEqual("", params.get("test", ""))

    def test_add_non_zero(self) -> None:
        params = Params()
        params.AddNonZero("value", 1)
        self.assertEqual("1", params["value"])

        params.AddNonZero("test", 0)
        self.assertEqual("", params.get("test", ""))

    def test_add_non_zero_64(self) -> None:
        params = Params()
        params.AddNonZero64("value", "1")
        self.assertEqual("1", params["value"])

        params.AddNonZero64("test", "")
        self.assertEqual("", params.get("test", ""))

    def test_add_bool(self) -> None:
        params = Params()
        params.AddBool("value", True)
        self.assertEqual("true", params["value"])

        params.AddBool("test", False)
        self.assertEqual("", params.get("test", ""))

    def test_add_non_zero_float(self) -> None:
        params = Params()
        params.AddNonZeroFloat("value", 1)
        self.assertEqual("1.000000", params["value"])

        params.AddNonZeroFloat("test", 0)
        self.assertEqual("", params.get("test", ""))

    def test_add_interface(self) -> None:
        params = Params()
        params.AddInterface("value", {"name": "test"})
        self.assertEqual('{"name":"test"}', params["value"])

        params.AddInterface("test", None)
        self.assertEqual("", params.get("test", ""))

    def test_add_first_valid(self) -> None:
        params = Params()
        params.AddFirstValid("value", 0, "", "test")
        self.assertEqual("test", params["value"])

        params.AddFirstValid("value2", 3, "test")
        self.assertEqual("3", params["value2"])


if __name__ == "__main__":
    unittest.main()
