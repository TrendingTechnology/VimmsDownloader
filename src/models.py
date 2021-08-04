"""Data models for Vimms-DL"""
from typing import List


class Config:
    """Config object created based on user input"""
    def __init__(self,
                 Selections: List[str] = [],
                 All: bool = False,
                 Extract: bool = False,
                 Search: bool = False,
                 Bulk: bool = False):
        self.Selections = Selections
        self.All = All
        self.Extract = Extract
        self.Search = Search
        self.Bulk = Bulk


class ROM():
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
