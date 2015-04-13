from observable import *
import unittest

class Tests(unittest.TestCase):

    def test_get(self):
        o = Observable(0)
        self.assertTrue(o.get_value() == 0)

    def test_set_no_callback(self):
        o = Observable(0)
        o.set_value(1)
        self.assertTrue(o.get_value() == 1)

    def test_one_callback(self):
        o = Observable(0)
        l = []
        def callback(value):
            l.append(value)
        o.add_callback(callback)
        o.set_value(1)
        self.assertTrue(o.get_value() == 1)
        self.assertTrue(l == [1])

    def test_three_callbacks(self):
        o = Observable(0)
        l = []
        def callback0(value):
            l.append(value)
        def callback1(value):
            l.append(value * 2)
        def callback2(value):
            l.append(value * 3)
        o.add_callback(callback0)
        o.add_callback(callback1)
        o.add_callback(callback2)
        o.set_value(5)
        self.assertTrue(o.get_value() == 5)
        self.assertTrue(l == [5, 10, 15])

if __name__ == '__main__':
    unittest.main()