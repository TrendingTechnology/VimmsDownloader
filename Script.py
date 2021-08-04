"""The Vimms-DL Tool"""
import zipfile
from threading import Thread
import re
import sys
import os
from typing import List
import py7zr
from requests.models import Response
from fake_useragent.fake import FakeUserAgent, UserAgent
import requests
from bs4 import BeautifulSoup
from src.helpers import models
from src import helpers


def GetROMDownloadURL(url: str):
    try:
        page = requests.get('https://vimm.net/' + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(id='download_form')
        result = result.find(attrs={'name': 'mediaId'})
        result: str = result['value']
        return result
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
    roms: List[models.ROM] = []
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
                if (odd is not None):
                    resultsoup = BeautifulSoup(str(odd.contents[0]),
                                               'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = models.ROM(name, result)
                    roms.append(rom)
                    odd = None
                if (even is not None):
                    resultsoup = BeautifulSoup(str(even.contents[0]),
                                               'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = models.ROM(name, result)
                    roms.append(rom)
                    even = None
        return roms
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)


def GetAllSystemROMS(system: str):
    sectionroms: List[models.SectionofROMs] = []
    sectionurls = [
        f'?p=list&system={system}&section=number', f'{system}/a',
        f'{system}/b', f'{system}/c', f'{system}/d', f'{system}/e',
        f'{system}/f', f'{system}/g', f'{system}/h', f'{system}/i',
        f'{system}/j', f'{system}/k', f'{system}/l', f'{system}/m',
        f'{system}/n', f'{system}/o', f'{system}/p', f'{system}/q',
        f'{system}/r', f'{system}/s', f'{system}/t', f'{system}/u',
        f'{system}/v', f'{system}/w', f'{system}/x', f'{system}/y',
        f'{system}/z'
    ]
    for x in sectionurls:
        roms: List[models.ROM] = GetSectionofROMS(x)
        section: models.SectionofROMs = models.SectionofROMs(x, roms)
        sectionroms.append(section)
    SystemROMS: models.BulkSystemROMS = models.BulkSystemROMS(
        sectionroms, system)
    return SystemROMS


def DownloadFile(pageurl: str, downloadurl: str, path: str):
    x = 0
    while True:
        agent: FakeUserAgent = UserAgent()
        headers: dict[str, str] = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'User-Agent': agent.random,
            'Referer': f'https://vimm.net/vault{pageurl}'
        }
        file: Response = requests.get(
            f'https://download2.vimm.net/download/?mediaId={downloadurl}',
            headers=headers,
            allow_redirects=True)
        if file.status_code == 200:
            filename: str = file.headers['Content-Disposition']
            filename: List[str] = re.findall(r'"([^"]*)"', filename)
            filename: str = filename[0]
            fullpath: str = os.path.join(path, filename)
            open(fullpath, 'wb').write(file.content)
            return filename
        if x == 4:
            print(f'5 Requests made to {downloadurl} and failed')
            break
        if file.status_code != 200:
            x += 1
            continue


def GetSearchSelection():
    searchselection: models.SearchSelection = models.SearchSelection()
    print('\nPlease select what system you want to search')
    helpers.PrintConsoleList()
    while True:
        userinput = sys.stdin.readline()
        try:
            if (not (int(userinput) > 17 or int(userinput) < 0)):
                searchselection.System = helpers.selections[int(userinput)][
                    int(userinput)]
                break
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue
    print('Input what rom you want to search for')
    searchselection.Query = sys.stdin.readline()
    return searchselection


def GetSearchSection(searchselection: models.SearchSelection):
    roms: List[models.ROM] = []
    try:
        page = requests.get(
            f'https://vimm.net/vault/?p=list&system={helpers.SelectionToUri(searchselection.System)}&q={searchselection.Query}'
        )
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(
            'table', {'class': 'rounded centered cellpadding1 hovertable'})
        for j in result.contents:
            if j != '\n':
                newsoup = BeautifulSoup(str(j), 'html.parser')
                odd = newsoup.find(attrs={'class': 'odd'})
                even = newsoup.find(attrs={'class': 'even'})
                if (odd is not None):
                    resultsoup = BeautifulSoup(str(odd.contents[0]),
                                               'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = models.ROM(name, result)
                    roms.append(rom)
                    odd = None
                if (even is not None):
                    resultsoup = BeautifulSoup(str(even.contents[0]),
                                               'html.parser')
                    result = resultsoup.find('a', href=True)
                    name = result.contents[0]
                    result = result['href']
                    rom = models.ROM(name, result)
                    roms.append(rom)
                    even = None
        return roms
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)


def PrintWelcome():
    print(r"""
     _   _ _                          _           _     ______                    _                 _
    | | | (_)                        | |         (_)    |  _  \                  | |               | |
    | | | |_ _ __ ___  _ __ ___  ___ | |     __ _ _ _ __| | | |_____      ___ __ | | ___   __ _  __| | ___ _ __
    | | | | | '_ ` _ \| '_ ` _ \/ __|| |    / _` | | '__| | | / _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
    \ \_/ / | | | | | | | | | | \__ \| |___| (_| | | |  | |/ / (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |
    \___/|_|_| |_| |_|_| |_| |_|___/\_____/\__,_|_|_|  |___/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|
        """)
    print('Welcome to the Vimm\'s Lair Download Script')
    print(
        'Please use responsibily, I am not liable for any damages, or legal issues caused by using this script'
    )


def GetProgramMode():
    config: models.Config = models.Config()
    print('\nWould you like to do bulk download or search for specific?')
    print('(B/S)')
    print('Default is \'B\'')
    while True:
        userinput = sys.stdin.readline()
        if (userinput == '\n'):
            config.Bulk = True
            break
        if (userinput.lower() == 'b\n'):
            config.Bulk = True
            break
        if (userinput.lower() == 's\n'):
            config.Search = True
            break
        else:
            print('Not a selection')
            print('Please Select B/s')
            continue
    return config


def GetBulkSelections(config: models.Config):
    print(
        'Press Enter to download all of Vimm\'s roms or select from the following of what systems you would like'
    )
    print('Enter \'q\' when finished if choosing specific consoles')
    helpers.PrintConsoleList()
    while True:
        userinput = sys.stdin.readline()
        if (userinput == '\n' and len(config.Selections) == 0):
            config.All = True
            break
        if (userinput == 'q\n'):
            break
        try:
            if (not (int(userinput) > 17 or int(userinput) < 0)):
                config.Selections.append(userinput)
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue
    return config


def GetExtractionStatus(config: models.Config):
    print(
        'Would you like to automatically extract and delete archives after download? (Y/n)'
    )
    print('Default is \'y\'')
    while True:
        userinput = sys.stdin.readline()
        if (userinput == '\n'):
            config.Extract = True
            break
        if (userinput.lower() == 'y\n'):
            config.Extract = True
            break
        if (userinput.lower() == 'n\n'):
            config.Extract = False
            break
        if ((userinput.lower() != 'n\n') and userinput.lower() != 'y\n'):
            print('Not a selection')
            print('Please Select Y/n')
            continue
    return config


def PrintSearchResults(roms: List[models.ROM]):
    count = 0
    print(
        '\nSelect which roms you would like to download and then enter \'d\'')
    for x in roms:
        print(f'{count:5d} ==> {x.Name:15}')
        count += 1


def GetSearchResultInput(roms: List[models.ROM]):
    downloadselroms: List[int] = []
    print(
        '\nSelect which roms you would like to download and then enter \'d\'')
    while True:
        userinput = sys.stdin.readline()
        if (userinput == '\n'):
            print('Please select a rom or press \'q\' to quit program')
            continue
        if (userinput == 'q\n'):
            exit()
        if (userinput == 'd\n'):
            return downloadselroms
        try:
            if (not (int(userinput) > len(roms) - 1 or int(userinput) < 0)):
                downloadselroms.append(int(userinput))
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue


def DownloadSearchResults(downloads: List[int], roms: List[models.ROM],
                          config: models.Config):
    threads = []
    for x in downloads:
        downloadname = DownloadFile(roms[x].URI,
                                    GetROMDownloadURL(roms[x].URI), '.')
        if config.Extract:
            t = Thread(target=ExtractandDeleteSearchResults,
                       args=(downloadname, ))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()


def ExtractFile(path: str, name: str):
    fullpath = os.path.join(path, name)
    basefilename = re.findall(r'(.+?)(\.[^.]*$|$)', name)
    basefilename = str(basefilename[0][0])
    filetype = re.findall(r'((?:zip|7z))', fullpath)
    try:
        if str(filetype[0]).lower() == 'zip':
            with (zipfile.ZipFile(fullpath, 'r')) as zip:
                dirpath: str = CreateDirectoryForROM(basefilename, path)
                zip.extractall(os.path.join(dirpath))
        if str(filetype[0]).lower() == '7z':
            with py7zr.SevenZipFile(fullpath, mode='r') as z:
                dirpath: str = CreateDirectoryForROM(basefilename, path)
                z.extractall(dirpath)
    except:
        pass


def DeleteFile(path: str, name: str):
    os.remove(os.path.join(path, name))


def CheckIfNeedToReSearch():
    search: bool = False
    print('\nDo you want to search again?(y/N)')
    while True:
        userinput = sys.stdin.readline()
        if (userinput == '\n'):
            break
        if (userinput.lower() == 'y\n'):
            search = True
            break
        if (userinput.lower() == 'n\n'):
            break
        if ((userinput.lower() != 'n\n') and userinput.lower() != 'y\n'):
            print('Not a selection')
            print('Please Select Y/n')
            continue
    return search


def CreateDirectoryForROM(name: str, path: str):
    newpath: str = os.path.join(path, name)
    os.mkdir(newpath)
    return newpath


def RunSearchLoop(config: models.Config):
    while True:
        selection: models.SearchSelection = GetSearchSelection()
        roms: List[models.ROM] = GetSearchSection(selection)
        PrintSearchResults(roms)
        restart: bool = CheckIfNeedToReSearch()
        if restart:
            continue
        downloads: List[int] = GetSearchResultInput(roms)
        DownloadSearchResults(downloads, roms, config)
        print('Done!')
        restart: bool = CheckIfNeedToReSearch()
        if restart:
            continue
        else:
            exit()


def ExtractandDeleteSearchResults(download: str):
    ExtractFile('.', download)
    DeleteFile('.', download)


def RunSelectedProgram(config: models.Config):
    if config.Bulk:
        config: models.Config = GetBulkSelections(config)
    if config.Search:
        RunSearchLoop(config)
    return config


def Main():
    PrintWelcome()
    config: models.Config = GetProgramMode()
    config: models.Config = GetExtractionStatus(config)
    RunSelectedProgram(config)


if __name__ == '__main__':
    Main()
