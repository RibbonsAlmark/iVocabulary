import os
import pymysql
import random
import time
import requests
import json
from bs4 import BeautifulSoup
from utils.read_config import read_config


class icibaDictRat:
    def __init__(self) -> None:
        self.load_config()
        self.db_connection_flag = False
        self.URL = 'http://www.iciba.com/'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }

    def load_config(self):
        self.ph_audio_root = read_config("basic", "ph_audio_root")
        return

    def __db_connect__(self):
        if not self.db_connection_flag:
            host = read_config("database", "host")
            port = int(read_config("database", "port"))
            db = read_config("database", "db")
            user = read_config("database", "user")
            password = read_config("database", "password")

            self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password, charset='utf8')
            self.cursor = self.db_conn.cursor(pymysql.cursors.DictCursor)
            self.db_connection_flag = True
        return

    def __db_disconnnect__(self):
        if self.db_connection_flag:
            self.db_conn.close()
            self.cursor.close()
            self.db_connection_flag = False
        return

    def get_word_info(self, word):
        url = self.URL + word
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

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
        phonetic_info = {"en": symbols["ph_en"], "us": symbols["ph_am"]}

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
        return word, phonetic_info, phonetic_audios_info, meanings_info, eg_info, exam_info

    def __pharse_word_info__(self, phonetic_info, meanings_info, eg_info, exam_info):
        phonetic_text = "en: /{}/   us: /{}/".format(phonetic_info["en"], phonetic_info["us"])
        meanings_text = meanings_info
        eg_text = ''
        for eg in eg_info: eg_text += "e.g. {}\n{}\n".format(eg["en"], eg["cn"])
        eg_text = eg_text.replace('"', '')
        exam_text = exam_info
        return phonetic_text, meanings_text, eg_text, exam_text

    def __save_word_info__(self, word, phonetic_text, meanings_text, eg_text, exam_text, mark=None):
        if mark == None:
            sql = """INSERT INTO dictionary(word, phonetic, mean, eg) 
            VALUES 
            ("{}", "{}", "{}", "{}")""".format(word, phonetic_text, meanings_text, eg_text)
        else:
            sql = """INSERT INTO dictionary(word, phonetic, mean, eg, mark) 
            VALUES 
            ("{}", "{}", "{}", "{}", "{}")""".format(word, phonetic_text, meanings_text, eg_text, mark)
        self.cursor.execute(sql)
        self.db_conn.commit()
        return

    def __save_audio__(self, word, phonetic_audios_info):
        faild_list = []
        ph_audio_folder = os.path.join(self.ph_audio_root, word[0].upper(), word)
        if not os.path.exists(ph_audio_folder):os.makedirs(ph_audio_folder)

        for audio_name in phonetic_audios_info:
            mp3_name = f"{word}_{audio_name}"
            mp3_file_name = f"{mp3_name}.mp3"
            mp3_file_path = os.path.join(ph_audio_folder, mp3_file_name)
            mp3_url = phonetic_audios_info[audio_name]
            if os.path.exists(mp3_file_path):continue
            try:
                res = requests.get(mp3_url,stream=True)
            except:
                faild_list.append(mp3_name)
                continue
            with open(mp3_file_path, 'wb') as fd:
                for chunk in res.iter_content():fd.write(chunk)
        return faild_list

    def get_word(self, word, mark=None, phonetic_text=None, meanings_text=None, eg_text=None, exam_text=None):
        self.__db_connect__()

        if '(' in word:word = word.replace('(', '').replace(')', '')
        self.cursor.execute(f"""SELECT * FROM dictionary WHERE word='{word}'""")
        results = self.cursor.fetchall()
        if len(results) > 0:return

        word, phonetic_info, phonetic_audios_info, meanings_info, eg_info, exam_info = self.get_word_info(word)
        pharsed_word_info = self.__pharse_word_info__(phonetic_info, meanings_info, eg_info, exam_info)
        if phonetic_text == None: phonetic_text = pharsed_word_info[0]
        if meanings_text == None: phonetic_text = pharsed_word_info[1]
        if eg_text == None: phonetic_text = pharsed_word_info[2]
        if exam_text == None: phonetic_text = pharsed_word_info[3]

        self.__save_word_info__(word, phonetic_text, meanings_text, eg_text, exam_text, mark)
        self.__save_audio__(word, phonetic_audios_info)
        return

    def __del__(self):
        self.__db_disconnnect__()


def rat_look_vocabularies(vocabulary_path):
    failed_num = 0
    dict_rat = icibaDictRat()
    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_num = len(lines)
        for i, line in enumerate(lines):
            if '!' in line: mark = '!'
            else: mark = None

            line = line.replace(' ', '').replace('!', '').replace('\n', '')
            info_list = line.split('|')
            word = info_list[0]
            meanings_text = info_list[2]
            
            # try:
            #     dict_rat.get_word(word, meanings_text=meanings_text)
            # except Exception as e:
            #     print(e)
            #     failed_num += 1
            dict_rat.get_word(word, meanings_text=meanings_text)

            print(f"\rsaving words in <{vocabulary_path}> ... ({i + 1} / {line_num}) ", end='')
            # sleep_time = random.randint(5,20) / 10
            # time.sleep(sleep_time)
    print('')
    return failed_num, line_num


def download_resources():
    vocabulary_file_root = read_config("basic", "vocabulary_file_root")
    vocabularies_list = os.listdir(vocabulary_file_root)
    vocabulary_num = len(vocabularies_list)
    for i, vocabulary in enumerate(vocabularies_list):
        print("START TO PARSE VOCABULARY [{}] <{} / {}>".format(vocabulary.replace(".txt", ''), i + 1, vocabulary_num))
        vocabulary_path = os.path.join(vocabulary_file_root, vocabulary)
        failed_num, word_num = rat_look_vocabularies(vocabulary_path)
        print("VOCABULARY [{}] SAVING FINISHED, SUCCESS RATE: <{} / {}>".format(vocabulary.replace(".txt", ''), word_num - failed_num, word_num))
    return