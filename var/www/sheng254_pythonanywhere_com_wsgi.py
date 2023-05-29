import sys
from app import Quantron

sys.path.insert(0, '/home/Sheng254/mysite')

application = Quantron().app

if __name__ == '__main__':
    application.run()
