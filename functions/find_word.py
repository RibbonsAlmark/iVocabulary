from utils.input_utils import input_setting
from utils.ivocabulary_utils import load_vocabulary_dict
from utils.print_utils import bounder2


def find_word(vocabulary_file_root):
    vocabulary_dict = load_vocabulary_dict(vocabulary_file_root)

    while True:
        key_word = input_setting("input key word(input !q for quit, !rl for reload vocabulary dict): ")

        if key_word == '!q':break

        if key_word == '!rl':
            vocabulary_dict = load_vocabulary_dict(vocabulary_file_root)
            print(f"\nVOCABULARY DICT RELOADED\n{bounder2}")
            continue

        res_text = ''
        res_num = 0

        for word in vocabulary_dict:
            record_text = vocabulary_dict[word]["record_text"]
            vocabulary = vocabulary_dict[word]["vocabulary"]
            if key_word in record_text:
                res_text += record_text.replace('\n', f"   <{vocabulary}>\n")
                res_num += 1

        print(f"\n{res_num} WORDS HAS BEEN FOUND :\n\n{res_text}{bounder2}")

    return