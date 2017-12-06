import os
import copy
import json
from sys import platform


class HaikuLoader:
    """
    A data access object wrapping our JSON files.
    Provides a convenient interface to our haiku data store.
    """

    _JSON_FILES = [
        'brady.json',
        'frogpond.json',
        'henderson.json',
        'museum_of_haiku.json',
        'virgilio.json',
        'reichhold.json'
    ]

    def __init__(self):
        """ Loads the data. """
        self._all_haiku = []

        data_dir = self._localized_data_dir()

        for filename in self._JSON_FILES:
            separator = self._localized_separator()
            filepath = separator.join([data_dir, filename])

            self._all_haiku.extend(self._load_haiku_from_file(filepath))

    def get_all(self):
        """ Returns a deep copy of all of the haiku. """
        all_haiku_copy = copy.deepcopy(self._all_haiku)

        return all_haiku_copy

    def get_all_lines(self):
        """ Returns a deep copy of all of the lines contained in all haiku. """
        all_lines = list(line for haiku in self._all_haiku for line in haiku)
        all_lines_copy = copy.deepcopy(all_lines)

        return all_lines_copy

    def _localized_data_dir(self):
        """ Returns the localized path to the data directory. """
        working_path = os.getcwd()
        separator = self._localized_separator()
        working_dir = working_path[:working_path.rfind(separator)]

        return separator.join([working_dir, 'data'])

    @staticmethod
    def _localized_separator():
        return '\\' if platform == 'win32' else '/'

    @staticmethod
    def _load_haiku_from_file(filepath):
        haiku_list = []

        with open(filepath, encoding="utf8") as file:
            for item in json.loads(file.read()):
                haiku_list.append(item['text'])

        return haiku_list
