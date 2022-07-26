from sys import argv
from testutil import run_tests, test

@test
def it_should_pass_the_test():
    assert True

@test
def it_should_not_pass_the_test():
    assert False

if __name__ == '__main__':
    assert len(argv) > 1, 'command not specified'
    if argv[1] == 'test':
        run_tests('-t' in argv or '--traceback' in argv)
        exit()
    print(argv)
