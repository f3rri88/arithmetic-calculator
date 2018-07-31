import timeit
import unittest
# from server import Server
from server.calculation.precedence_climbing import compute


class ServerTest(unittest.TestCase):
    '''Server TestCase'''

    def test_anotherthing(self):
        self.assertTrue(True)


class ArithmeticsTest(unittest.TestCase):
    '''Arithmetics TestCase'''

    def test_evaluation(self):
        self.assertEqual(
            compute('38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77'),
            eval('38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77'))
        self.assertEqual(
            compute('21 * 52 + 82 * 4'),
            eval('21 * 52 + 82 * 4'))
        self.assertEqual(
            compute('90 / 92 + 2 + 8 / 54 - 42 - 65 - 37 - 40 + 95'),
            eval('90 / 92 + 2 + 8 / 54 - 42 - 65 - 37 - 40 + 95'))
        self.assertEqual(
            compute('66 - 66 * 55 / 20 * 75'),
            eval('66 - 66 * 55 / 20 * 75'))
        self.assertEqual(
            compute('79 + 45 - 92 + 17 + 13 - 98 + 41 - 46 - 49'),
            eval('79 + 45 - 92 + 17 + 13 - 98 + 41 - 46 - 49'))
        self.assertEqual(
            compute('30 / 35 - 64 - 62 - 85 - 75 + 2 + 95 / 30 + 65'),
            eval('30 / 35 - 64 - 62 - 85 - 75 + 2 + 95 / 30 + 65'))
        self.assertEqual(
            compute('15 + 22 / 34 / 76 - 100 - 82'),
            eval('15 + 22 / 34 / 76 - 100 - 82'))
        self.assertEqual(
            compute('98 - 64 - 95 * 26'),
            eval('98 - 64 - 95 * 26'))

    def test_timing(self):
        SETUP_CODE = '''
from server.calculation.precedence_climbing import compute
'''
        TEST_CODE = '''
compute('38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77')
'''
        # timeit.repeat statement
        times = timeit.repeat(
            setup=SETUP_CODE,
            stmt=TEST_CODE,
            repeat=3,
            number=1)

        print('Time taken to evaluate one operation: {}'.format(times))

        SETUP_CODE = '''
from server.calculation.precedence_climbing import compute
f = open("files/testops.txt", 'r')
'''
        TEST_CODE = '''
for line in f:
    try:
        compute(line)
    except:
        continue
'''

        # timeit.repeat statement
        times = timeit.repeat(
            setup=SETUP_CODE,
            stmt=TEST_CODE,
            repeat=3,
            number=1)

        print('Time taken to evaluate test operations: {}'.format(times))

        SETUP_CODE = '''
from server.calculation.precedence_climbing import compute
f = open("files/operations.txt", "r")
'''
        TEST_CODE = '''
for line in f:
    try:
        compute(line)
    except:
        continue
'''

        # timeit.repeat statement
        times = timeit.repeat(
            setup=SETUP_CODE,
            stmt=TEST_CODE,
            repeat=3,
            number=1)

        print('Time taken to evaluate all operations: {}'.format(times))
