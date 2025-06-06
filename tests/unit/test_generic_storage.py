import unittest
from dataclasses import dataclass

from pyiron_workflow.api import NOT_DATA

from pyiron_database.generic_storage import HDF5Storage, JSONStorage, PickleStorage


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rectangle:
    upper_left_corner: Point
    lower_right_corner: Point


class TestDataIO(unittest.TestCase):
    def store(self, group) -> None:
        group["int"] = 1
        group["float"] = 1.2
        group["string"] = "1"
        group["None"] = None
        group["NOT_DATA"] = NOT_DATA
        rect = Rectangle(Point(1, 2), Point(3, 4))
        group["rect"] = rect
        group["list"] = [1, 2, 3]
        import numpy as np

        group["np"] = np.array([1, 2, 3])

    def check(self, group) -> None:
        self.assertEqual(group["int"], 1)
        self.assertAlmostEqual(group["float"], 1.2)
        self.assertEqual(group["string"], "1")
        self.assertEqual(group["None"], None)
        self.assertEqual(group["NOT_DATA"], NOT_DATA)
        rect = group["rect"]
        self.assertEqual(rect.upper_left_corner.x, 1)
        self.assertEqual(rect.upper_left_corner.y, 2)
        self.assertEqual(rect.lower_right_corner.x, 3)
        self.assertEqual(rect.lower_right_corner.y, 4)
        self.assertListEqual(group["list"], [1, 2, 3])
        self.assertListEqual(group["np"].tolist(), [1, 2, 3])

    def test_json_io(self) -> None:
        with JSONStorage("dummy.json", "w") as group:
            self.store(group)
        with JSONStorage("dummy.json", "r") as group:
            self.check(group)

    def test_hdf5_io(self) -> None:
        with HDF5Storage("dummy.hdf5", "w") as group:
            self.store(group)
        with HDF5Storage("dummy.hdf5", "r") as group:
            self.check(group)

    def test_pickle_io(self) -> None:
        with PickleStorage("dummy.pickle", "wb") as group:
            self.store(group)
        with PickleStorage("dummy.pickle", "rb") as group:
            self.check(group)


if __name__ == "__main__":
    unittest.main()
