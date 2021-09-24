import time
from utils.theft_word_info import steal_word_info, eg_info_2_text
from utils.ivocabulary_utils import get_eg_info_from_db


bounder = "========================================================\n"
bounder2 = '-' * 50

soft_banner  = "      __     ___            ___                         \n"
soft_banner += "     |__|    \  \          /  /                         \n"
soft_banner += "      __      \  \        /  /                          \n"
soft_banner += "     |  |      \  \      /  /                           \n"
soft_banner += "     |  |       \  \    /  /                            \n"
soft_banner += "     |  |        \  \  /  /                             \n"
soft_banner += "     |  |         \  \/  /          Celestial-Being     \n"
soft_banner += "     |__|          \ __ /           Setsuna.F.Seiei     \n"

def print_count_down(wait_time):
    for i in range(wait_time):
        print(f"\r< {wait_time - i} >", end='')
        time.sleep(1)
    print('')
    return


def print_vocabulary_cover(vocabulary_name, new_vocabulary):
    if new_vocabulary:vocabulary_name += ' [NEW]'

    ct  = " __________________ \n"
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|  %-16s|\n"%vocabulary_name
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|                  |\n"
    ct += "|__________________|\n"
    
    print(ct)
    return


def print_eg(word, indentation = True, indentation_blank = "        "):
    if not indentation:
        indentation_blank = ''

    try:
        word, phonetic_info, phonetic_audios_info, meanings_info, eg_info, exam_info = steal_word_info(word)
    except Exception as e:
        eg_info = get_eg_info_from_db(word)

    # Parse eg_info
    eg_text = eg_info_2_text(word, eg_info)
    eg_text = eg_text.replace('\n', f"\n{indentation_blank}")
    eg_text = f"{indentation_blank}{eg_text}"

    print(eg_text)

    return eg_text
    
    
def print_help_text():
    help_text  = "operation codes: \n"
    help_text += "    h   : help \n"
    help_text += "    a   : add new words \n"
    help_text += "    ro  : vocabulary randomization \n"
    help_text += "    f   : find words by key word \n"
    help_text += "    r   : read words in vocabulary \n"
    help_text += "    rmk : remark words in vocabulary \n"
    help_text += "    dl  : download resources vocabularies need \n"
    help_text += "    q   : quit \n"

    print(help_text)
    
    return help_text
    