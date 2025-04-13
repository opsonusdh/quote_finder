import requests
import os
import re
import time
import shutil
import sys
from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
from googlesearch import search



headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.89 Mobile Safari/537.36' 
}
col = {
        'black': '\033[30m',
        'purple':'\033[95m',
        'cyan':'\033[96m',
        'blue':'\033[94m',
        'green':'\033[92m',
        'yellow':'\033[93m',
        'red':'\033[91m',
        'bold':'\033[1m',
        'underline':'\033[4m',
        'end':'\033[0m',
}

def color(text,*args):
    
    txt = ''
    args = list(args)
    if 'end' in args:
        end = True
        args.remove('end')
    else:
        end = False
    for i in args:
        txt += col[i]
    if end:
        return txt+text+col['end']
    else:
        return txt+text

def logo(animation=False):
    text = "╭━━━╮╱╱╱╱╱╭╮╱╱╱╱╭━━━╮╱╱╱╱╱╭╮\n┃╭━╮┃╱╱╱╱╭╯╰╮╱╱╱┃╭━━╯╱╱╱╱╱┃┃\n┃┃╱┃┣╮╭┳━┻╮╭╋━━╮┃╰━━┳┳━╮╭━╯┣━━┳━╮\n┃┃╱┃┃┃┃┃╭╮┃┃┃┃━┫┃╭━━╋┫╭╮┫╭╮┃┃━┫╭╯\n┃╰━╯┃╰╯┃╰╯┃╰┫┃━┫┃┃╱╱┃┃┃┃┃╰╯┃┃━┫┃\n╰━━╮┣━━┻━━┻━┻━━╯╰╯╱╱╰┻╯╰┻━━┻━━┻╯\n╱╱╱╰╯                     By S.D.H. "
    if animation:
        for i in text.split("\n"):
            print(color(i,"green","end"))
            time.sleep(0.05)
    else:
        print(color(text,"green", "end"))

def translate(lang_code,text):
    translator = GoogleTranslator(source='auto',target=lang_code).translate
    translation = translator(text)
    translation = translation.replace('. ','। ')
    if translation[-1] == '.':
            fintr = list(str(translation))
            fintr[-1] = '।'
            translation = ''.join(fintr)
    return translation
    

def save_quote(quote,title):
    if "quote-translated" not in os.listdir():
        os.system("mkdir quote-translated")
    with open("quote-translated/"+title+".txt","w") as file:
        file.write(str(quote))


def get_details(link):
    html_text = requests.get(link+"?page=2",headers=headers).text
    soup = bs(html_text,'html.parser')
    title = soup.find("title").text
    total_page=int(title.split("of ")[-1].replace(")",""))
    title = title.split("(")[0]
    
    return title, total_page

def chunk(input_list, chunk_size):
    if not input_list:
        return []

    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

#google the name
def google(x):
    result = list(search(x+' quotes Goodreads'))
    for i in result:
        if "https://www.goodreads.com/work/quotes/" not in i:
            result.remove(i)
    return result[0]


def loading_bar(total, progress, time_st, time_end):
    terminal_width = shutil.get_terminal_size().columns
    bar_width = terminal_width - 30

    filled_width = int(round(bar_width * progress / float(total)))
    bar = '#' * filled_width + color('.',"black","end") * (bar_width - filled_width)
    
    total_time = time_end-time_st
        
    need_time = (total-progress-1)/(progress+1)*total_time
        
        
    if need_time < 60:
        need_time=str(round(need_time,2))+" s"
    else:
        need_time /= 60
        if need_time < 60:
            need_time=str(round(need_time,2))+" m"
        else:
            need_time /= 60
            need_time=str(round(need_time,2))+" h"
    
    percent = round(100.0 * progress / float(total), 1)
    sys.stdout.write(f'\r[{bar}] {percent}% ({progress}/{total})      {need_time}   ')
    sys.stdout.flush()
    
    
#get quotes
def retrive_quotes(link):
    logo()
    title, total_page = get_details(link)
    
    print("Title: "+title)
    print(f"Found {total_page} pages.")
    
    
    all_quote = []
    quote_num = 0
    
    start_time = time.time()
    os.system("clear")
    logo()
    print("Title: "+title)
    print("\nFetching pages...")
    for a in range(total_page):
        time_now = time.time()
        
        loading_bar(total_page,a+1,start_time,time_now)
            
            
        try:
            html_text = requests.get(link+"?page="+str(a+1),headers=headers).text
        except:
            print("\nInvalid Link or Network Connection Error")
            sys.exit()
        soup = bs(html_text,'html.parser')
        quotes = soup.find_all("blockquote",class_='quoteBody')
    
        for i in quotes:
            i = str(i)
            i = i.replace('<blockquote class="quoteBody">','')
            i = i.replace('</blockquote>','')
            i = i.replace('<br/>','\n')
            i = re.sub('<[^<]+?>', '', i)
            quote_num += 1
        
            all_quote.append(i)

    save_quote(all_quote,title)
    os.system("clear")
    
    logo()
    
    print(f"{quote_num} quotes saved in file {title}.txt")
    print("Open Saved Quotes to find it.")



#main code
os.system("clear")
logo(True)
print("\n\n")
print("Options:")
print("    1. Get Quotes")
print("    2. Saved Quotes")
print("    3. Exit")

inp = input("Enter Option: ")
if inp == "1":
    os.system("clear")
    logo()
    print()
    name = input("Enter The Name of the Novel: ")
    
    link = google(name)
    os.system("clear")
    
    retrive_quotes(link)

if inp == "2":
    quotes = os.listdir("quote-translated/")
    os.system("clear")
    print("Quote Finder\n")
    print("Title:")
    for i in enumerate(quotes):
        print(f"    {i[0]+1}. {'.txt'.join(i[1].split('.txt')[:-1])}")
    
    try:
        inp = int(input("Enter Option: "))
        if inp <= 0:
            raise ValueError
        quotes = quotes[inp-1]
        title = ".txt".join(quotes.split(".txt")[:-1])
        lang = input("Language-code to Translate(If no only press enter): ")
        if lang != "":
            try:
                translate(lang,"hello")
            except:
                print("""Please select on of the supported languages:
                    
afrikaans : af
albanian : sq
amharic : am
arabic : ar
armenian : hy
assamese : as
aymara : ay
azerbaijani : az
bambara : bm
basque : eu
belarusian : be
bengali : bn
bhojpuri : bho
bosnian : bs
bulgarian : bg
catalan : ca
cebuano : ceb
chichewa : ny
chinese (simplified) : zh-CN
chinese (traditional) : zh-TW
corsican : co
croatian : hr
czech : cs
danish : da
dhivehi : dv
dogri : doi
dutch : nl
english : en
esperanto : eo
estonian : et
ewe : ee
filipino : tl
finnish : fi
french : fr
frisian : fy
galician : gl
georgian : ka
german : de
greek : el
guarani : gn
gujarati : gu
haitian creole : ht
hausa : ha
hawaiian : haw
hebrew : iw
hindi : hi
hmong : hmn
hungarian : hu
icelandic : is
igbo : ig
ilocano : ilo
indonesian : id
irish : ga
italian : it
japanese : ja
javanese : jw
kannada : kn
kazakh : kk
khmer : km
kinyarwanda : rw
konkani : gom
korean : ko
krio : kri
kurdish (kurmanji) : ku
kurdish (sorani) : ckb
kyrgyz : ky
lao : lo
latin : la
latvian : lv
lingala : ln
lithuanian : lt
luganda : lg
luxembourgish : lb
macedonian : mk
maithili : mai
malagasy : mg
malay : ms
malayalam : ml
maltese : mt
maori : mi
marathi : mr
meiteilon (manipuri) : mni-Mtei
mizo : lus
mongolian : mn
myanmar : my
nepali : ne
norwegian : no
odia (oriya) : or
oromo : om
pashto : ps
persian : fa
polish : pl
portuguese : pt
punjabi : pa
quechua : qu
romanian : ro
russian : ru
samoan : sm
sanskrit : sa
scots gaelic : gd
sepedi : nso
serbian : sr
sesotho : st
shona : sn
sindhi : sd
sinhala : si
slovak : sk
slovenian : sl
somali : so
spanish : es
sundanese : su
swahili : sw
swedish : sv
tajik : tg
tamil : ta
tatar : tt
telugu : te
thai : th
tigrinya : ti
tsonga : ts
turkish : tr
turkmen : tk
twi : ak
ukrainian : uk
urdu : ur
uyghur : ug
uzbek : uz
vietnamese : vi
welsh : cy
xhosa : xh
yiddish : yi
yoruba : yo
zulu : zu
""")
                os.system("exit")
                raise ValueError
            tot = True
        else:
            tot = False
        
        with open("quote-translated/"+quotes) as file:
            quotes = eval(str(file.read()))
            quotes = chunk(quotes,15)
        print(len(quotes), "Pages Found.\n")
        input("Press Enter:")
        os.system("clear")
        logo()
        print()
        print("Title:",title)
        print()
        while True:
            inp = int(input("Enter page Number:"))
            if inp <= 0:
                raise ValueError
            os.system("clear")
            logo()
            print()
            print("Title:",title)
            print("Page:",inp)
            print()
            quote = quotes[inp-1]
            for i in enumerate(quote):
                print(f"{i[0]+1}) Quote: {i[1]}")
                if tot:
                    print("\nTranslation:",translate(lang,i[1]))
                print("~~~~~~~~~")
        
    except:
        print("Invalid Input.")
        os.system("exit")
