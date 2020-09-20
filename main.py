# Imports
import requests, json, threading, traceback, ctypes, os
from colorama import Fore,Back,Style, init
from bs4 import BeautifulSoup
init()
def clearscreen():
    os.system('cls')

# Get X-CSRF TOKEN -- SomethingElse
def getxcsrf(InputCookie):
    token_request = requests.session()
    token_request.cookies['.ROBLOSECURITY'] = InputCookie
    r = token_request.post('https://www.roblox.com/api/item.ashx?')
    try:
        return r.headers['X-CSRF-TOKEN']
    except:
        return False

# Vip Scraper -- Tvnyl
def vip_scraper():
    vip_url = 'https://freerobloxvipservers.com/'
    req = requests.get(vip_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    vip_finder = soup.find_all('p', class_='text-sm mb-0')
    vip_link = [i.a['href'] for i in vip_finder]
    discord_link = 'https://discord.gg/SdQ5u9x'
    if discord_link in vip_link:
        vip_link.remove(discord_link)
    with open("vip_links.txt", 'w') as f:
        for i in vip_link:
            f.write(f'{i}\n')



# Transfer bot
def transfer_bot(price):
    percent_30 = 30/100 * int(price)
    add_percent = percent_30 + int(price)
    print(add_percent)  

# Start Screen
def StartScreen():
    clearscreen()
    print(Fore.MAGENTA+"""
    ███████████████████████████████████████████████████████████████████████████████████████████████████████████""")
    print(Fore.LIGHTMAGENTA_EX+"""
    VVVVVVVV           VVVVVVVV  iiii                             tttt          lllllll                     
    V::::::V           V::::::V i::::i                         ttt:::t          l:::::l                     
    V::::::V           V::::::V  iiii                          t:::::t          l:::::l                     
    V::::::V           V::::::V                                t:::::t          l:::::l                     
     V:::::V           V:::::V iiiiiii nnnn  nnnnnnnn    ttttttt:::::ttttttt     l::::l     eeeeeeeeeeee    
      V:::::V         V:::::V  i:::::i n:::nn::::::::nn  t:::::::::::::::::t     l::::l   ee::::::::::::ee  
       V:::::V       V:::::V    i::::i n::::::::::::::nn t:::::::::::::::::t     l::::l  e::::::eeeee:::::ee
        V:::::V     V:::::V     i::::i nn:::::::::::::::ntttttt:::::::tttttt     l::::l e::::::e     e:::::e
         V:::::V   V:::::V      i::::i   n:::::nnnn:::::n      t:::::t           l::::l e:::::::eeeee::::::e
          V:::::V V:::::V       i::::i   n::::n    n::::n      t:::::t           l::::l e:::::::::::::::::e 
           V:::::V:::::V        i::::i   n::::n    n::::n      t:::::t           l::::l e::::::eeeeeeeeeee  
            V:::::::::V         i::::i   n::::n    n::::n      t:::::t    tttttt l::::l e:::::::e           
             V:::::::V         i::::::i  n::::n    n::::n      t::::::tttt:::::tl::::::le::::::::e          
              V:::::V          i::::::i  n::::n    n::::n      tt::::::::::::::tl::::::l e::::::::eeeeeeee  
               V:::V           i::::::i  n::::n    n::::n        tt:::::::::::ttl::::::l  ee:::::::::::::e  
                VVV            iiiiiiii  nnnnnn    nnnnnn          ttttttttttt  llllllll   eeeeeeeeeeeeee
                """)
    print(Fore.MAGENTA+"""
    ███████████████████████████████████████████████████████████████████████████████████████████████████████████""")
    
# dont Put the inputs in a function                                                             
                                                                                                        
StartScreen()
                                                                                                        
                                                                                                        
                                                                                                        
                                                                                                        
