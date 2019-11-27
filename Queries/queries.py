"""Class to represent a conference. Consists only of conf dict and methods."""

__author__ = "Lars Meister"


class Conference:
    """Provides methods for querying a conference."""

    paper_attributes = ["title", "link", "authors", "type", "datetime", "topic"]
    other_attributes = ["title", "link", "authors", "abstract", "datetime", "location"]

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
        return self.conference["deadlines"]

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

    def keynote_search(self, search_name, search_by, show=None):
        """
        Return keynotes where given search_value matches information
        specified in search_key attribute in a keynote.
        :param search_value: String
        :param search_key: see other_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a keynote
        :return: list of matching keynotes
        """
        keynotes = [keynote for keynote in self.conference["keynotes"] if search_name in keynote[
            search_by]]
        if not keynotes:
            return None
        if show is None or show not in self.other_attributes:
            return keynotes
        return [keynote[show] for keynote in keynotes]

    def workshops(self):
        """Returns all the workshops with all available information."""
        return self.conference["workshops"]

    def workshop_search(self, search_name, search_by, show=None):
        """
        Return workshops where given search_value matches information
        specified in search_key attribute in a workshop.
        :param search_value: String
        :param search_key: see other_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a workshop
        :return: list of matching workshops
        """
        workshops = [workshop for workshop in self.conference["workshops"] if search_name in
                     workshop[
                         search_by]]
        if not workshops:
            return None
        if show is None or show not in self.other_attributes:
            return workshops
        return [workshop[show] for workshop in workshops]

    def tutorials(self):
        """Returns all the tutorials with all available information."""
        return self.conference["tutorials"]

    def tutorial_search(self, search_name, search_by, show=None):
        """
        Return tutorials where given search_value matches information
        specified in search_key attribute in a tutorial.
        :param search_value: String
        :param search_key: see other_attributes for available choices
        :param show: optional, allows to only show the specified attribute of a tutorial
        :return: list of matching tutorials
        """
        tutorials = [tutorial for tutorial in self.conference["tutorials"] if search_name in
                     tutorial[
                         search_by]]
        if not tutorials:
            return None
        if show is None or show not in self.other_attributes:
            return tutorials
        return [tutorial[show] for tutorial in tutorials]
