import os
import pymysql
from utils.audio_utils import trans_mp3_to_wav, play_wav_audio
from utils.read_config import read_config, get_config_obj
from utils.theft_word_info import steal_word_info


def load_vocabulary_dict(vocabulary_file_root):
    vocabulary_dict = {}

    for vocabulary_fn in os.listdir(vocabulary_file_root):
        with open(os.path.join(vocabulary_file_root, vocabulary_fn), 'r', encoding='utf-8') as f:
            for ori_line in f.readlines():
                line = ori_line.replace(' ', '').replace('!', '').replace('\n', '')
                info_list = line.split('|')

                word = info_list[0]
                phonetic = info_list[1]
                meanings_info = info_list[2]
                vocabulary = vocabulary_fn.replace(".txt", '')

                vocabulary_dict[word] = {
                "phonetic": phonetic, 
                "meanings": meanings_info, 
                "vocabulary": vocabulary,
                "record_text": ori_line
            }

    return vocabulary_dict


def read_word(word, repeat_times = 1, repeat_interval = 1):
    ph_audio_root = read_config("basic", "ph_audio_root")
    ph_audio_folder = os.path.join(ph_audio_root, word[0].upper(), word)
    
    tmp_files_root = read_config("basic", "tmp_files_root")
    tmp_audio_folder = os.path.join(tmp_files_root, "tmp_audio")
    tmp_audio_path = os.path.join(tmp_audio_folder, "tmp_audio.wav")
    
    if not os.path.exists(tmp_audio_folder): os.makedirs(tmp_audio_folder)
    
    for ph_type in ["am", "tts", "en"]:
        
        mp3_file_name = f"{word}_ph_{ph_type}_mp3.mp3"
        mp3_file_path = os.path.join(ph_audio_folder, mp3_file_name).replace('\\', '/')

        if not os.path.exists(mp3_file_path):continue

        try:
            trans_mp3_to_wav(mp3_file_path, tmp_audio_path)
            play_wav_audio(tmp_audio_path, repeat_times, repeat_interval)
        except Exception as e:
            print(f"[WARNING] faied to play audio file {mp3_file_path}, {str(e)}")
            continue

        break

    return


# TODO: make my own ORM
def get_eg_info_from_db(word):# Get db config
    cfg = get_config_obj()
    host = cfg.get("database", "host")
    port = int(cfg.get("database", "port"))
    db = cfg.get("database", "db")
    user = cfg.get("database", "user")
    password = cfg.get("database", "password")

    # Connect to db
    db_conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password, charset='utf8')
    cursor = db_conn.cursor(pymysql.cursors.DictCursor)

    # Get word
    sql = f"""SELECT eg FROM dictionary WHERE word='{word}'"""
    cursor.execute(sql)
    results = cursor.fetchall()

    eg_text = results[0]["eg"]

    # Parse eg text
    eg_info = []
    raw_info_list = eg_text.split('\n')
    for i, raw_info in enumerate(raw_info_list):
        if raw_info == '':continue
        if i % 2 == 1:continue

        tmp_eg_info_dict = {
            "en": raw_info.replace("e.g. ", ''),
            "cn": raw_info_list[i + 1]
        }

        eg_info.append(tmp_eg_info_dict)

    # Disconnect db
    db_conn.close()
    cursor.close()
    return eg_info