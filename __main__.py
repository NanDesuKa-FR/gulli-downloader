import os
from requests_html import HTMLSession
session = HTMLSession()
import subprocess
from sys import platform

def clean_text(name):
	return name.replace('|', ' ').replace('>', ' ').replace('<', ' ').replace('"', ' ').replace('?', ' ').replace('?',' ').replace('*', ' ').replace(':', ' ').replace('/', ' ').replace('\\', ' ')

def Logo():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
        
    print()                                                                                       
    print("       ..####...##..##..##......##......######..........##...##...####...##..##.")
    print("       .##......##..##..##......##........##............###.###..##..##...####..")
    print("       .##.###..##..##..##......##........##............##.#.##..######....##...")
    print("       .##..##..##..##..##......##........##............##...##..##..##...####..")
    print("       ..####....####...######..######..######..........##...##..##..##..##..##.")
    print("       ..............................By NanDesuKa?..............................")

def menu():
    print("\n\n  Make a choice:\n  ------------------------------------\n  1) Download with link\n  2) Download in Batch\n  ------------------------------------")

def Downloader(link):
    r = session.get(link)
    
    json = ((r.text).split("tc_vars = {")[1]).split('};')[0]
    title = (((json.split(r"'label': '")[1]).split("',")[0]).capitalize()).encode().decode('unicode-escape')
    infos = ((r.text).split("'content_level_3': '")[1]).split("'")[0]
    name = clean_text(title + " - " + infos.upper())
    id_dl = link.split('-vod')[1]
    type_demande = link.split("/")[3]
    if link.find("https://svod.gulli.fr/") != -1:
        type_demande = "svod"
    else:
        type_demande = "replay"
    
    test1080 = session.get("https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_1080.m3u8")
    if test1080.status_code == 200:
        print("  M3U8: https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_1080.m3u8")
        m3u8 = "https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_1080.m3u8"
        dimention = "1080p"
    else:
        test720 = session.get("https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_720.m3u8")
        if test720.status_code == 200:
            print("  M3U8: https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_720.m3u8")
            m3u8 = "https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_720.m3u8"
            dimention = "720p"
        else:
            test360 = session.get("https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_360.m3u8")
            if test360.status_code == 200:
                print("  M3U8: https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_360.m3u8")
                m3u8 = "https://d2l9m895ubsn89.cloudfront.net/" + type_demande + "/" + id_dl + ".ts/playlist_360.m3u8"
                dimention = "360p"
            else:
                print("  No M3U8 found.")
                exit()
                
    print("  Launching of the download... \n\n")
    command = 'N_m3u8DL-CLI_v2.9.0.exe {m3u8_url} --disableDateInfo --noProxy --enableDelAfterDone --workDir "./" --saveName "{name_out}"'.format(m3u8_url = m3u8, name_out = name + " [VF][" + dimention + "]")
    subprocess.call(command, shell=True)

def DownloadByLink():
    Logo()
    loop = True
    while loop == True:
        link = input("\n\n  Enter link: ")
        if link.find("https://svod.gulli.fr/") != -1 or link.find("https://replay.gulli.fr/") != -1 or link.find("-vod") != -1:
            loop = False
            Downloader(link)
        else:
            Logo()
            DownloadByLink()

def BatchDownloader():
    Logo()
    loop = True
    while loop == True:
        link = input("\n\n  Enter link: ")
        check_link = link.split("gulli.fr")[1]
        if link.find("https://svod.gulli.fr/") != -1 or link.find("https://replay.gulli.fr/") != -1:
            r = session.get(link)
            alllink = r.html.xpath('//a/@href')
            for element in alllink:
                if element.find(check_link) != -1 and element.startswith('//') == True:
                    Downloader(element.replace("//", "https://"))
            loop = False
        else:
            Logo()
            DownloadByLink()

if __name__ == "__main__":
    Logo()
    menu()
    loop = True
    while loop == True:
        reponse = input("  Choose 1 or 2: ")
        if reponse in ['1', '2']:
            Logo()
            loop = False
            if reponse == "1":
                DownloadByLink()
            elif reponse == "2":
                BatchDownloader()
        else:
            Logo()
            menu()