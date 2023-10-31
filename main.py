from ghentUniversity import UGHENT
from UAlberta import UAlberta
from BaseCrawler import BaseCrawler

if __name__ == '__main__':
    base = BaseCrawler()
    alberta = UAlberta()
    alberta.handler()
    # ughent = UGHENT()
    # ughent.handler()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
