import os
import enchant
from utils.input_utils import input_setting_with_default, input_setting, input_yes_or_no
from utils.print_utils import bounder2, print_vocabulary_cover
from utils.ivocabulary_utils import load_vocabulary_dict
from utils.theft_word_info import steal_word_info


def input_word_info(word_info=''):
    while word_info == '':word_info = input("input word info: ")

    # Initialize
    word_info_list = word_info.replace('  ', ' ').split(' ')
    word = word_info_list[0]

    if len(word_info_list) == 1:
        phonetic = input_setting_with_default("input the phonetic: ", str, '')
        meaning = input_setting("input the meaning: ")
    elif len(word_info_list) == 2:
        phonetic = ''
        meaning = word_info_list[1]
    elif len(word_info_list) == 3:
        phonetic = word_info_list[1]
        meaning = word_info_list[2]
    else:
        raise Exception("wrong word info format")

    phonetic_text = f"/{phonetic}/"

    return word, phonetic_info, meaning


def write_vocabulary(f_obj, word, phonetic_type='us', auto=True):
    # Get word info
    if auto:
        word, phonetic_info, phonetic_audios_info, meanings_info, eg_info, exam_info = steal_word_info(word)
        ph_en = phonetic_info["en"]
        ph_us = phonetic_info["us"]
        if phonetic_type == 'en':
            phonetic_text = f"en: /{ph_en}/"
        elif phonetic_type == 'us':
            phonetic_text = f"us: /{ph_us}/"
        else:
            phonetic_info = f"en: /{ph_en}/   us: /{ph_us}/"
    else:
        word, phonetic_text, meanings_info = get_word_info(word)

    # Write record
    record_text = "  %-30s | %-50s | %s\n" %(word, f"{phonetic_text}", meanings_info)
    f_obj.write(record_text)

    # Print hint
    eg_text = ''
    if auto:
        counter = 0
        eg_num = 5 # get 5 example sentences
        for eg in eg_info:
            if not word in eg["en"].lower():continue
            counter += 1
            if counter > eg_num:break
            eg_text += "\ne.g. {}\n{}\n".format(eg["en"], eg["cn"])

    # record to vocabulary dict
    word_detail = {
        "phonetic": phonetic_text, 
        "meanings": meanings_info, 
        "record_text": record_text
    }
    return word_detail, eg_text


def add_words(vocabulary_file_root):
    # Input settings
    vocabulary_name = input_setting("input vocabulary name: ")
    allow_empty_phonetic = input_yes_or_no("allow empty phonetic (y/n): ")
    auto = input_yes_or_no("get phonetic and meanings information automatically (y/n): ")

    # Initialize
    vocabulary_path = os.path.join(vocabulary_file_root, f"{vocabulary_name}.txt")
    vocabulary_dict = load_vocabulary_dict(vocabulary_file_root)
    if not os.path.exists(vocabulary_file_root):os.makedirs(vocabulary_file_root)

    # Print layout
    print_vocabulary_cover(vocabulary_name, not os.path.exists(vocabulary_path))
    print(f"start record\n{bounder2}")

    d = enchant.Dict("en_US")

    with open(vocabulary_path, 'a', encoding='utf-8') as f:
        while True:
            word = input_setting("input the word(input q for quit, add '!' infront for skip spell check): ").lower()
            
            # Quit
            if word == 'q':break

            # Validation
            if '!' in word:
                word = word.replace('!', '')
            elif not d.check(word.split(' ')[0]):
                print(f"[WARNING] '{word}' not a word")
                continue
            
            if word in vocabulary_dict:
                tmp = vocabulary_dict[word]["vocabulary"]
                print(f"{bounder2}\nword '{word}' is already exist in vocabulary <{tmp}>\n{'-' * 50}")
                continue

            # Add word to vocabulary
            word_detail, eg_text = write_vocabulary(f, word, 'us', auto)
            word_detail["vocabulary"] = vocabulary_name
            vocabulary_dict[word] = word_detail

            # Print hint
            hint_text = f"record to vocabulary < {vocabulary_name} >:"
            hint_text += f"word:'{word}', "
            hint_text += f"phonetic:'{word_detail['phonetic'].replace(' ', '')}', "
            hint_text += f"meaning:'{word_detail['meanings'].replace(' ', '')}'"
            hint_text += f"\n{eg_text}"
            print(hint_text)
            print(bounder2)

    print("\nEXITED\n")
    return