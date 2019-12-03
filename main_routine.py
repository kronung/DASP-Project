"""Main entry point."""

import util
from Queries.queries import Conference

if __name__ == "__main__":
    conf_dict = util.build_conference_dict("EMNLP_2019/output/emnlp2019_data.json", "EMNLP2019")
    emnlp = Conference(conf_dict)
    print(emnlp.get_Sessions_by_date("11/5/2019", "papers", "title"))
