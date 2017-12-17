import os

import sys

sys.path.append(os.path.abspath(os.path.join('../')))
from webscraper.app import app

if __name__ == "__main__":
    app.run()
