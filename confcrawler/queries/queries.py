"""Class to represent a conference. Consists only of conf dict and methods for queries."""

__author__ = "Lars Meister"

from dateutil import parser as dateparser

class Conference:
    """Provides methods for querying a conference."""

    paper_attributes = ["paper_title", "paper_link", "paper_authors", "paper_type", "paper_time",
                        "paper_keywords"]
    tutorial_attributes = ["tutorial_name", "tutorial_link", "tutorial_author", "tutorial_abstract",
                           "tutorial_time", "tutorial_location"]
    keynote_attributes = ["keynote_title", "keynote_speaker", "keynote_speaker_bio", "keynote_abstract",
                           "keynote_time", "keynote_location", "keynote_link"]
    workshop_attributes = ["workshop_name", "workshop_organizer", "workshop_description",
                          "workshop_day", "keynote_time", "workshop_location", "workshop_link"]

    conf_domains = ["submission_deadlines", "papers", "workshops", "tutorials", "keynotes"]

    def __init__(self, conference):
        """
        constructor.
        :param conference: dictionary needs to have structure as defined in template json.
        """
        self.conference = conference

    def location(self):
        """Returns the location."""
        return self.conference["location"]

    def datetime(self):
        """Returns the datetime."""
        return self.conference["datetime"]

    def deadlines(self):
        """Returns the deadlines."""
        return self.conference["submission_deadlines"]

    def topics(self):
        """Returns the topics."""
        return self.conference["topics"]

    def organizers(self):
        """Returns the organizers."""
        return self.conference["organizers"]

    def papers(self):
        """Returns all the papers with all available information."""
        return self.conference["papers"]

    def paper_search(self, search_value, search_key, show=None):
        """
        Return papers where given search_value matches information
        specified in search_key attribute in a paper.
        :param search_value: String
        :param search_key: see paper_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a paper
        :return: list of matching papers
        """
        papers = [paper for paper in self.conference["papers"] if search_value in paper[search_key]]
        if not papers:
            return None
        if show is None or show not in self.paper_attributes:
            return papers
        return [paper[show] for paper in papers]

    def keynotes(self):
        """Returns all the keynotes with all available information."""
        return self.conference["keynotes"]

    def keynote_search(self, search_value, search_key, show=None):
        """
        Return keynotes where given search_value matches information
        specified in search_key attribute in a keynote.
        :param search_value: String
        :param search_key: see keynote_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a keynote
        :return: list of matching keynotes
        """
        keynotes = [keynote for keynote in self.conference["keynotes"] if search_value in keynote[
            search_key]]
        if not keynotes:
            return None
        if show is None or show not in self.keynote_attributes:
            return keynotes
        return [keynote[show] for keynote in keynotes]

    def workshops(self):
        """Returns all the workshops with all available information."""
        return self.conference["workshops"]

    def workshop_search(self, search_value, search_key, show=None):
        """
        Return workshops where given search_value matches information
        specified in search_key attribute in a workshop.
        :param search_value: String
        :param search_key: see workshop_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a workshop
        :return: list of matching workshops
        """
        workshops = [workshop for workshop in self.conference["workshops"] if search_value in
                     workshop[search_key]]
        if not workshops:
            return None
        if show is None or show not in self.workshop_attributes:
            return workshops
        return [workshop[show] for workshop in workshops]

    def tutorials(self):
        """Returns all the tutorials with all available information."""
        return self.conference["tutorials"]

    def tutorial_search(self, search_value, search_key, show=None):
        """
        Return tutorials where given search_value matches information
        specified in search_key attribute in a tutorial.
        :param search_value: String
        :param search_key: see tutorial_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a tutorial
        :return: list of matching tutorials
        """
        tutorials = [tutorial for tutorial in self.conference["tutorials"] if search_value in
                     tutorial[search_key]]
        if not tutorials:
            return None
        if show is None or show not in self.tutorial_attributes:
            return tutorials
        return [tutorial[show] for tutorial in tutorials]

    def get_Sessions_by_date(self, search_date, search_domain, show=None):
        """
        Returns all items of a given search_domain (papers, workshops, tutorials,
        submission_deadlines, keynotes) which take place at given search_date.
        :param search_date: String of date in english format (11/04/2019 or 4 November 2019 etc.)
        :param search_domain: see conf_domains for available choices
        :param show: optional, allows to only show the specified attribute of a item
        :return: list of matching items
        """
        if search_domain not in self.conf_domains:
            print("Not a valid search domain, must be one of: ", self.conf_domains)
            return None
        search_date = dateparser.parse(search_date)
        items = []
        for item in self.conference[search_domain]:
            try:
                found_datetime = dateparser.parse(','.join(item["datetime"].split(',')[:-1]))
            except:
                continue
            if search_date == found_datetime:
                items.append(item)

        if not items:
            return None

        if show is None:
            return items

        if search_domain == "papers" and show not in self.paper_attributes:
            print("Specified show attribute not valid for papers. Must be one of: ",
                  self.paper_attributes)
            return items

        if search_domain != "papers" and show not in self.other_attributes:
            print("Specified show attribute not valid for " + search_domain + ". Must be one of: ",
                  self.other_attributes)
            return items

        return [item[show] for item in items]





