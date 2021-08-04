from typing import List


class Config:
    def __init__(self, Selections: List[str] = [], All: bool = False, Extract: bool = False, Search: bool = False, Bulk: bool = False):
        self.Selections = Selections
        self.All = All
        self.Extract = Extract
        self.Search = Search
        self.Bulk = Bulk


class ROM():
    def __init__(self, Name: str, URI: str):
        self.Name = Name
        self.URI = URI


class SectionofROMs:
    def __init__(self, Section: str, ROMS: List[ROM]):
        self.Section = Section
        self.ROMS = ROMS


class SearchSelection:
    def __init__(self, System: str = '', Query: str = ''):
        self.System = System
        self.Query = Query


class BulkSystemROMS:
    def __init__(self, Sections: List[SectionofROMs], System: str):
        self.System = System
        self.Sections = Sections
