import requests;
from bs4 import BeautifulSoup;

from colorama import init, Fore, Back, Style
init();

XIVData = {};

status_symbol = '\u25cf'
character_symbol = '\u25c6'

def requestXIVData(callback):
    worlds = requests.get('https://eu.finalfantasyxiv.com/lodestone/worldstatus/');
    if (worlds):
        html = worlds.text;
        soup = BeautifulSoup(html, 'lxml');
        for tag in soup.find_all('div', attrs={'data-region': True}):
            region = tag.attrs['data-region'];
            XIVData[region] = {};

            groups = tag.find_all('li', attrs={'class': 'world-dcgroup__item'})
            for group in groups:
                XIVData[region][group.h2.text] = {}

                for child in group.ul.find_all('div', attrs={'class': 'world-list__item'}):
                    if child != '\n':
                        child__worldname = child.find('div', attrs={'class': 'world-list__world_name'}).p.text;
                        child__status = child.find('div', attrs={'class': 'world-list__status_icon'}).i.attrs['data-tooltip'].strip()
                        child__character = child.find('div', attrs={'class': 'world-list__create_character'}).i.attrs['data-tooltip'].strip()
                        
                        XIVData[region][group.h2.text][child__worldname] = {
                            "status": child__status,
                            "character": child__character
                        }

        if callback: callback(True, XIVData);
    else:
        if callback: callback(False, 'smth gone wrong');

def XIVPrint(text):
    print(Back.CYAN + '[XIVStatus]' + Back.RESET + Fore.WHITE + " " + text + Fore.RESET);  

def requestCallback(ok, data):
    if ok:
        XIVPrint('Loaded ' + Fore.BLUE + str(len(data)) + Fore.WHITE + ' data centers.');
    else:
        XIVPrint(data);


if __name__ == '__main__':
    XIVPrint('Hello! Requesting server statuses.')
    requestXIVData(requestCallback);
