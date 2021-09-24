import requests
from bs4 import BeautifulSoup
import json


def eg_info_2_text(word, eg_info, eg_num = 10):
    eg_text = ''
    counter = 0

    for eg in eg_info:
        if not word in eg["en"].lower():continue
        if counter >= eg_num:break
        eg_text += "e.g. {}\n{}\n".format(eg["en"], eg["cn"])
        counter += 1

    eg_text = eg_text.replace('"', '')

    return eg_text


def steal_word_info(word):
    URL = 'http://www.iciba.com/'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    url = URL + word
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Get source html
    '''  Old codes for get phonetic, meaning and e.g. info html

    phonetic_html = soup.findAll("ul",{"class":"Mean_symbols__1jA1O"})[0]
    meaning_html = soup.findAll("ul",{"class":"Mean_part__1Xi6p"})[0]
    eg_html = soup.findAll("div",{"class":"SceneSentence_scene__18VZD"})[0]
    
    '''
    exam_html = soup.findAll("p",{"class":"Mean_tag__2APAe"})
    props_html = soup.findAll("script",{"type":"application/json"})[0]

    # Get word props info
    props = props_html.contents[0]
    props = json.loads(props)["props"]
    pageProps = props["pageProps"]
    initialReduxState = pageProps["initialReduxState"]
    word_p = initialReduxState["word"]
    wordInfo = word_p["wordInfo"]
    # Get symbols info
    baesInfo = wordInfo["baesInfo"]
    symbols = baesInfo["symbols"][0]
    symbols_key_list = symbols.keys()
    # Get sentences info
    if "new_sentence" in wordInfo.keys():
        new_sentence = wordInfo["new_sentence"][0]
        sentences = new_sentence["sentences"]
    else:
        sentences = []

    # Get phonetic info by symbols info
    phonetic_info = {
        "en": symbols["ph_en"],
        "us": symbols["ph_am"]
    }

    # Get phonetic audios info
    phonetic_audios_info = {}
    for key in symbols_key_list:
        if "mp3" in key:
            phonetic_audios_info[key] = symbols[key]

    # Get meaning info by symbols info
    meanings_info = ''
    meaning_list = symbols["parts"]
    i_counter = len(meaning_list) - 1
    
    for i, meaning_detail in enumerate(meaning_list):
        part = meaning_detail["part"]
        means = meaning_detail["means"]
        j_counter = len(means) - 1
        
        meanings_info += part

        for j, meaning in enumerate(means):
            meanings_info += meaning
            if j < j_counter:meanings_info += "，"

        if i < i_counter: meanings_info += "   "
    meanings_info = meanings_info.replace('; ', ',').replace(',', '，')

    # Get e.g. info from wordInfo
    eg_info = sentences

    # Get exam info
    if len(exam_html) == 0:
        exam_info = ''
    else:
        exam_info = exam_html[0].text


    '''  Old codes for get phonetic, meaning and e.g. info

    # Get phonetic info
    phonetic_info = ''
    phonetic_list = phonetic_html.findAll("li")
    phonetic_type = phonetic_type.lower()

    if phonetic_type == 'us':
        for val in phonetic_list:
            text = val.text
            if "美" in text:phonetic_info = re.search(r"(?<=\[).*?(?=\])", text).group()
            else:continue
        phonetic_info = f"us: /{phonetic_info}/"
    elif phonetic_type == 'en':
        for val in phonetic_list:
            text = val.text
            if "英" in text:phonetic_info = re.search(r"(?<=\[).*?(?=\])", text).group()
            else:continue
        phonetic_info = f"en: /{phonetic_info}/"
    else:
        for val in phonetic_list:
            text = val.text
            tmp = re.search(r"(?<=\[).*?(?=\])", text).group()
            if "英" in text:tmp = f"en: /{tmp}/   "
            else:tmp = f"us: /{tmp}/   "
            phonetic_info += tmp
    
    # Get meaning info
    meanings_info = ''
    meaning_list = meaning_html.findAll("li")
    for val in meaning_list:
        meaning_type = val.findAll("i")[0].text
        meanings = val.findAll("div")[0].findAll("span")

        meanings_info += meaning_type
        for meaning in meanings:meanings_info += meaning.text

        meanings_info += "   "
    meanings_info = meanings_info.replace('; ', ',').replace(',', '，')

     # Get example sentences info
    eg_info = ''
    eg_list = eg_html.findAll("div")
    eg_num = 5 # get 5 example sentences
    for i, eg in enumerate(eg_list):
        if i >= eg_num:break
        # ignore example sentences which not contain required word
        if len(eg.findAll("b",{"class":"highlight"})) == 0:
            eg_num += 1
            continue
        eg_en = eg.findAll("span")[0].text
        eg_zh = eg.findAll("p",{"class":"NormalSentence_cn__27VpO"})[0].text
        eg_text = f"e.g. {eg_en}\n{eg_zh}\n"
        eg_info += eg_text

    '''

    return word, phonetic_info, phonetic_audios_info, meanings_info, eg_info, exam_info