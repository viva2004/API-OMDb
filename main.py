from components.app import App
from tests.testcases import testcases_bucketlist
from tests.testcases import testcases_søkeresultat

def main():
    testcases_bucketlist()
    testcases_søkeresultat()
    min_app = App()
    min_app.kjør()

if __name__ == '__main__':
    main()