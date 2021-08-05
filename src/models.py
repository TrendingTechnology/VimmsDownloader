"""Data models for Vimms-DL"""

from typing import List


class ROM:
    """Used to hold a details about a single ROM"""
    def __init__(self, Name: str, URI: str):
        self.Name = Name
        self.URI = URI


# Sections are either a search query or #-A-Z subsections on vimms


class SectionofROMs:
    """Used to hold a details about multiple ROMs"""
    def __init__(self, Section: str, ROMS: List[ROM]):
        self.Section = Section
        self.ROMS = ROMS


class SearchSelection:
    """Used when in search mode to get the parameters for the search criteria"""
    def __init__(self, System: str = '', Query: str = ''):
        self.System = System
        self.Query = Query


class BulkSystemROMS:
    """Used hold all of a systems ROMS"""
    def __init__(self, Sections: List[SectionofROMs], System: str):
        self.System = System
        self.Sections = Sections


class Search:
    """Used in search mode to hold data for the type of search"""
    def __init__(self,
                 SearchSelections: SearchSelection,
                 General: bool = False):
        self.SearchSelections = SearchSelections
        self.General = General


class Config:
    """Config object created based on user input"""
    def __init__(self,
                 All: bool = False,
                 Extract: bool = False,
                 BulkMode: bool = False,
                 SearchMode: bool = False):
        self.Selections: List[str] = []
        self.All = All
        self.Extract = Extract
        self.SearchMode = SearchMode
        self.BulkMode = BulkMode
        self.__QuerySelection: SearchSelection = SearchSelection()
        self.Query: Search = Search(self.__QuerySelection)
