import requests
from bs4 import BeautifulSoup
import sys
selections = [
    {0: 'NES'},
    {1: 'Genesis'},
    {2: 'SNES'},
    {3: 'Saturn'},
    {4: 'Playstation'},
    {5: 'N64'},
    {6: 'Dreamcast'},
    {7: 'Playstation 2'},
    {8: 'Xbox'},
    {9: 'Gamecube'},
    {10: 'Playstation 3'},
    {11: 'Wii'},
    {12: 'WiiWare'},
    {13: 'Game Boy'},
    {14: 'Game Boy Color'},
    {15: 'Game Boy Advanced'},
    {16: 'Nintendo DS'},
    {17: 'PSP'},
]

print('Welcome to the Vimm\'s Layer Download Script')
print('Please use responsibily, I am not liable for any damages, or legal issues caused by using this script')
print('Press Enter to download all of Vimm\'s roms or select from the following of what systems you would like')
print('Enter q when finished')

for x in range(0, 9):
    print(
        f'{x:5d} ==> {selections[x][x]:15} | {x+9:5d} ==> {selections[x+9][x+9]:10}')

inputs = []
while True:
    userinput = sys.stdin.readline()
    if(userinput == '\n' and len(inputs) == 0):
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


def GetROMDownloadURL(url: str):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        result = soup.find(id='download_form')
        result = result.find(attrs={'name': 'mediaId'})
        result = result['value']
        return result
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)


def GetIdvROMHomeURL(system: str):
    romurls = []
    sectionurls = [f'?p=list&system={system}&section=number', f'{system}/a', f'{system}/b', f'{system}/c', f'{system}/d', f'{system}/e', f'{system}/f', f'{system}/g', f'{system}/h', f'{system}/i', f'{system}/j', f'{system}/k', f'{system}/l',
                   f'{system}/m', f'{system}/n', f'{system}/o', f'{system}/p', f'{system}/q', f'{system}/r', f'{system}/s', f'{system}/t', f'{system}/u', f'{system}/v', f'{system}/w', f'{system}/x', f'{system}/y', f'{system}/z']
    for x in sectionurls:
        print('')


GetROMDownloadURL('https://vimm.net/vault/6')
