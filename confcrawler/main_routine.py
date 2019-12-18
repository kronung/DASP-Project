"""Main entry point."""

from confcrawler.util import util
from confcrawler.queries import queries

if __name__ == "__main__":
    conf_dict = util.load_conference("emnlp2019/output/emnlp2019_data.json", "EMNLP2019")
    emnlp = queries.Conference(conf_dict)
    print(emnlp.get_Sessions_by_date("11/5/2019", "papers", "title"))
