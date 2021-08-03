from typing import List
import re
from fake_useragent.fake import FakeUserAgent, UserAgent
import requests
from bs4 import BeautifulSoup
import sys
import os
from requests.models import Response

selections: list[dict[int, str]] = [
    {0: 'NES'},
    {1: 'Genesis'},
    {2: 'SNES'},
    {3: 'Saturn'},
    {4: 'Playstation'},
    {5: 'N64'},
    {6: 'Dreamcast'},
    {7: 'Playstation-2'},
    {8: 'Xbox'},
    {9: 'Gamecube'},
    {10: 'Playstation-3'},
    {11: 'Wii'},
    {12: 'WiiWare'},
    {13: 'Game-Boy'},
    {14: 'Game-Boy-Color'},
    {15: 'Game-Boy-Advanced'},
    {16: 'Nintendo-DS'},
    {17: 'PSP'},
]


class Config:
    def __init__(self, Selections: List[str] = [], All: bool = False, Extract: bool = False):
        self.Selections = Selections
        self.All = All
        self.Extract = Extract


class ROM:
    def __init__(self, Name: str, URI: str):
        self.Name = Name
        self.URI = URI


class SectionofROMs:
    def __init__(self, Section: str, ROMS: List[ROM]):
        self.Section = Section
        self.ROMS = ROMS


class BulkSystemROMS:
    def __init__(self, Sections: List[SectionofROMs], System: str):
        self.System = System
        self.Sections = Sections


print('Welcome to the Vimm\'s Lair Download Script')
print('Please use responsibily, I am not liable for any damages, or legal issues caused by using this script')
print('Press Enter to download all of Vimm\'s roms or select from the following of what systems you would like')
print('Enter q when finished')

for x in range(0, 9):
    print(
        f'{x:5d} ==> {selections[x][x]:15} | {x+9:5d} ==> {selections[x+9][x+9]:10}')

inputs: List[str] = []
config: Config = Config()
while True:
    userinput = sys.stdin.readline()
    if(userinput == '\n' and len(inputs) == 0):
        config.All = True
        break
    if(userinput == 'q\n'):
        break
    try:
        if(not(int(userinput) > 17 or int(userinput) < 0)):
            inputs.append(userinput)
        else:
            print('Not a selection')
            print('Please select a value from the list')
    except ValueError:
        print('Please select a value from the list')
        continue
config.Selections = inputs

print('Would you like to automatically extract and delete archives after download? (Y/n)')
print('Default is \'y\'')
while True:
    userinput = sys.stdin.readline()
    if(userinput == '\n'):
        config.Extract = True
        break
    if(userinput.lower() == 'y\n'):
        config.Extract = True
        break
    if(userinput.lower() == 'n\n'):
        config.Extract = False
        break
    if((userinput.lower() != 'n\n') and userinput.lower() != 'y\n'):
        print('Not a selection')
        print('Please Select Y/n')
        continue


def GetROMDownloadURL(url: str):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(id='download_form')
        result = result.find(attrs={'name': 'mediaId'})
        result = result['value']
        test = {
            'url': result,
            'thecookie': page.cookies
        }
        return test
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)


def GetSubSectionLetterFromStr(subsection: str):
    number = '&section=number'
    if number in subsection.lower():
        return 'number'
    else:
        return subsection[-1]


def GetSectionofROMS(section: str):
    roms: List[ROM] = []
    try:
        page = requests.get('https://vimm.net/vault/' + section)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(
            'table', {'class': 'rounded centered cellpadding1 hovertable'})
        for j in result.contents:
            if j != '\n':
                newsoup = BeautifulSoup(str(j), 'html.parser')
                odd = newsoup.find(attrs={'class': 'odd'})
                even = newsoup.find(attrs={'class': 'even'})
                if(odd is not None):
                    resultsoup = BeautifulSoup(
                        str(odd.contents[0]), 'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = ROM(name, result)
                    roms.append(rom)
                    odd = None
                if(even is not None):
                    resultsoup = BeautifulSoup(
                        str(even.contents[0]), 'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = ROM(name, result)
                    roms.append(rom)
                    even = None
        return roms
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)


def GetAllSystemROMS(system: str):
    sectionroms: List[SectionofROMs] = []
    sectionurls = [f'?p=list&system={system}&section=number', f'{system}/a', f'{system}/b', f'{system}/c', f'{system}/d', f'{system}/e', f'{system}/f', f'{system}/g', f'{system}/h', f'{system}/i', f'{system}/j', f'{system}/k', f'{system}/l',
                   f'{system}/m', f'{system}/n', f'{system}/o', f'{system}/p', f'{system}/q', f'{system}/r', f'{system}/s', f'{system}/t', f'{system}/u', f'{system}/v', f'{system}/w', f'{system}/x', f'{system}/y', f'{system}/z']
    for x in sectionurls:
        roms: List[ROM] = GetSectionofROMS(x)
        section: SectionofROMs = SectionofROMs(x, roms)
        sectionroms.append(section)
    SystemROMS: BulkSystemROMS = BulkSystemROMS(sectionroms, system)
    return SystemROMS


def CreateAlphaNumStructure(path: str, system: str):
    dirnames: list[str] = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    try:
        for x in dirnames:
            os.mkdir(os.path.join(path, 'ROMS', system, x))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating AlphaNum Structure')
        print(e)


def CreateROMHomeDir(path: str):
    try:
        os.mkdir(os.path.join(path, 'ROMS'))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating Home Directory')
        print(e)


def CreateROMSystemDir(path: str, system: str):
    try:
        os.mkdir(os.path.join(path, 'ROMS', system))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating Home Directory')
        print(e)


def CheckIfHomeDirCreated(path: str):
    for x in os.listdir(path):
        if x == 'ROMS':
            return True


def CheckIfSystemDirCreated(path: str, system: str):
    for x in os.listdir(os.path.join(path, 'ROMS')):
        if x == system:
            return True


def CreateAllNoHome(path):
    for x in selections:
        for value in x:
            CreateROMHomeDir(path)
            CreateROMSystemDir(path, x[value])
            CreateAlphaNumStructure(path, x[value])


def CreateAllWHome(path):
    for x in selections:
        for value in x:
            CreateROMSystemDir(path, x[value])
            CreateAlphaNumStructure(path, x[value])


def CreateSelWHome(path):
    CreateROMSystemDir(path, selections[int(x)][int(x)])
    CreateAlphaNumStructure(path, selections[int(x)][int(x)])


def CreateSelNoHome(path):
    CreateROMSystemDir(path, selections[int(x)][int(x)])
    CreateAlphaNumStructure(path, selections[int(x)][int(x)])


# Fix this mess later
def CreateDirectoryStructure(Config: Config):
    path: str = os.getcwd()
    if config.All:
        if not CheckIfHomeDirCreated(path):
            CreateAllNoHome(path)
        if CheckIfHomeDirCreated(path):
            CreateAllWHome(path)
    if not Config.All:
        if CheckIfHomeDirCreated(path):
            CreateSelWHome(path)
        if not CheckIfHomeDirCreated(path):
            CreateSelNoHome(path)


def DownloadFile(pageurl: str, downloadurl: str, path: str):
    agent: FakeUserAgent = UserAgent()
    headers: dict[str, str] = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent': agent.random,
        'Referer': f'https://vimm.net/vault/{pageurl}'
    }
    file: Response = requests.get(
        downloadurl, headers=headers, allow_redirects=True)
    filename: str = file.headers['Content-Disposition']
    filename: List[str] = re.findall(r'"([^"]*)"', filename)
    filename: str = filename[0]
    fullpath:str = os.path.join(path, filename)
    open(fullpath, 'wb').write(file.content)
