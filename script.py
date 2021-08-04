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


def get_rom_download_url(url: str):
    """Gets the Download ID for the a specific ROM from the ROMs page url"""
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


def get_sub_section_letter_from_str(subsection: str):
    """Returns the subsection letter to get the downloaded ROM to the\
            correct alphanumeric directory"""
    number = '&section=number'
    if number in subsection.lower():
        return 'number'
    else:
        return subsection[-1]


def get_section_of_roms(section: str):
    """Gets a section of ROM home page URIs from a system category"""
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


def get_all_system_roms(system: str):
    """Used in bulk mode to get the home page URI for every rom on a system"""
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
        roms: List[models.ROM] = get_section_of_roms(x)
        section: models.SectionofROMs = models.SectionofROMs(x, roms)
        sectionroms.append(section)
    SystemROMS: models.BulkSystemROMS = models.BulkSystemROMS(
        sectionroms, system)
    return SystemROMS


def download_file(pageurl: str, downloadurl: str, path: str):
    """Downloads one rom from the uri, downloadid\
            downloads to the path director"""
    x = 0
    while True:
        agent: FakeUserAgent = UserAgent()
        headers: dict[str, str] = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image' +
            '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Connection':
            'keep-alive',
            'User-Agent':
            agent.random,
            'Referer':
            f'https://vimm.net/vault{pageurl}'
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


def get_search_selection():
    """Gets search criteria for search mode"""
    searchselection: models.SearchSelection = models.SearchSelection()
    print('\nPlease select what system you want to search')
    helpers.print_console_list()
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


def get_search_section(searchselection: models.SearchSelection):
    """Gets a section of roms from the search selection"""
    roms: List[models.ROM] = []
    try:
        page = requests.get(
            'https://vimm.net/vault/?p=list&system=' +
            f'{helpers.selection_to_uri(searchselection.System)}' +
            f'&q={searchselection.Query}')
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


def get_program_mode():
    """Gets input from user to go into either (Bulk/Search) mode"""
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


def get_bulk_selections(config: models.Config):
    """Gets input in bulk mode if the user wants to only download specific consoles"""
    print('Press Enter to download all of Vimm\'s roms or select from the\
		 following of what systems you would like')
    print('Enter \'q\' when finished if choosing specific consoles')
    helpers.print_console_list()
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


def get_extraction_status(config: models.Config):
    """Used in Bulk and Search mode to check if user wants to \
            extract and delete downloaded ROM archives"""
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
        if ((userinput.lower() != 'n\n') and (userinput.lower() != 'y\n')):
            print('Not a selection')
            print('Please Select Y/n')
            continue
    return config


def print_search_results(roms: List[models.ROM]):
    """Prints the returned search results from the users query"""
    count = 0
    print(
        '\nSelect which roms you would like to download and then enter \'d\'')
    for x in roms:
        print(f'{count:5d} ==> {x.Name:15}')
        count += 1


def get_search_result_input(roms: List[models.ROM]):
    """Used to get input in search mode for what ROMs the user wants to download"""
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


def download_search_results(downloads: List[int], roms: List[models.ROM],
                            config: models.Config):
    """Downloads the users specified roms in search mode"""
    threads = []
    for x in downloads:
        downloadname = download_file(roms[x].URI,
                                     get_rom_download_url(roms[x].URI), '.')
        if config.Extract:
            t = Thread(target=extract_and_delete_search_results,
                       args=(downloadname, ))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()


def extract_file(path: str, name: str):
    """Extracts the downloaded archives"""
    fullpath = os.path.join(path, name)
    basefilename = re.findall(r'(.+?)(\.[^.]*$|$)', name)
    basefilename = str(basefilename[0][0])
    filetype = re.findall(r'((?:zip|7z))', fullpath)
    try:
        if str(filetype[0]).lower() == 'zip':
            with (zipfile.ZipFile(fullpath, 'r')) as zip:
                dirpath: str = create_directory_for_rom(basefilename, path)
                zip.extractall(os.path.join(dirpath))
        if str(filetype[0]).lower() == '7z':
            with py7zr.SevenZipFile(fullpath, mode='r') as z:
                dirpath: str = create_directory_for_rom(basefilename, path)
                z.extractall(dirpath)
    except:
        pass


def delete_file(path: str, name: str):
    """Deletes the archives"""
    os.remove(os.path.join(path, name))


def check_if_need_to_re_search():
    """Gets user input to research if query didn't return wanted results"""
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


def create_directory_for_rom(name: str, path: str):
    """Used to create the directory for the ROMs archived files to\
            be extracted to"""
    newpath: str = os.path.join(path, name)
    os.mkdir(newpath)
    return newpath


def run_search_loop(config: models.Config):
    """Main loop for the search program"""
    while True:
        selection: models.SearchSelection = get_search_selection()
        roms: List[models.ROM] = get_search_section(selection)
        print_search_results(roms)
        restart: bool = check_if_need_to_re_search()
        if restart:
            continue
        downloads: List[int] = get_search_result_input(roms)
        download_search_results(downloads, roms, config)
        print('Done!')
        restart: bool = check_if_need_to_re_search()
        if restart:
            continue
        else:
            exit()


def extract_and_delete_search_results(download: str):
    """Used to extract and delete the archives in search mode"""
    extract_file('.', download)
    delete_file('.', download)


def run_selected_program(config: models.Config):
    """Runs selected program"""
    if config.Bulk:
        config: models.Config = get_bulk_selections(config)
    if config.Search:
        run_search_loop(config)
    return config


def main():
    """Programs main method"""
    helpers.print_welcome()
    config: models.Config = get_program_mode()
    config: models.Config = get_extraction_status(config)
    run_selected_program(config)


if __name__ == '__main__':
    main()
