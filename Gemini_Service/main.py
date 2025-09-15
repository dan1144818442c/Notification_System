from manager import Manager
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

manager = Manager()

if __name__ == '__main__':
    manager.run()