from os import system
from typing import List


class TestCase:
    def __init__(self, func, name: str) -> None:
        self.func = func
        self.name = name

    def run(self, verbose = False):
        try:
            self.func()
        except AssertionError as e:
            system('clear')
            print('❌ TEST FAILED ❌')
            print(f'Test: {self.name}')
            print(f"File: {self.func.__module__}")
            if verbose:
                raise e
            else:
                exit(1)

TESTS_TO_RUN: List[TestCase] = []

def test(func, name: str = None):
    global TESTS_TO_RUN
    id = name if name != None else func.__name__.replace('_', ' ', -1)
    TESTS_TO_RUN.append(TestCase(func, id))
    return func

def run_tests(verbose = False):
    global TESTS_TO_RUN
    for test in TESTS_TO_RUN:
        test.run(verbose)
    print(f'💪 {len(TESTS_TO_RUN)} TESTS PASSED 💪')

