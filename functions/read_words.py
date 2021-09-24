import os
import random
import time
from utils.input_utils import input_setting, input_setting_with_default, input_yes_or_no
from utils.print_utils import print_count_down, print_eg
from utils.ivocabulary_utils import read_word


learning_mode_settings = (
    4, # reading_interval
    3, # repeat_times
    2, # repeat_interval
    True, # only_marked
    False, # pause after read a word
    None # reorder
)


quick_check_mode_settings = (
    2, # reading_interval
    1, # repeat_times
    0, # repeat_interval
    True, # only_marked
    False, # pause after read a word
    None # reorder
)


word_by_word_mode_settings = (
    0, # reading_interval
    3, # repeat_times
    1, # repeat_interval
    True, # only_marked
    True, # pause after read a word
    None # reorder
)


slow_review_mode_settings = (
    20, # reading_interval
    3, # repeat_times
    1, # repeat_interval
    True, # only_marked
    False, # pause after read a word
    True # reorder
)


none_settings = (
    None, # reading_interval
    None, # repeat_times
    None, # repeat_interval
    None, # only_marked
    None, # pause after read a word
    None # reorder
)


def custom_settings(
    reading_interval = None, 
    repeat_times = None, 
    repeat_interval = None, 
    only_marked = None, 
    pause = None, 
    reorder = None
):
    # Set default settings
    default_rdi = 4
    default_rpt = 3
    default_rpi = 2

    # Input settings
    if reading_interval == None:
        reading_interval = input_setting_with_default(f"input reading interval ({default_rdi} seconds by default): ", float, default_rdi)
    if repeat_times == None:
        repeat_times = input_setting_with_default(f"input repeat times ({default_rpt} times by default): ", int, default_rpt)
    if repeat_interval == None:
        repeat_interval = input_setting_with_default(f"input repeat interval ({default_rpi} seconds by default): ", float, default_rpi)
    if only_marked == None:
        only_marked = input_yes_or_no("only read marked words (y/n): ") 
    if pause == None:
        pause = not input_yes_or_no("pause after read a word (y/n , 'n' by default): ", negative_key = 'y', positive_key = 'n') 
    if reorder == None:
        reorder = not input_yes_or_no("reorder vocabulary in each round (y/n , 'n' by default): ", negative_key = 'y', positive_key = 'n')

    return reading_interval, repeat_times, repeat_interval, only_marked, pause, reorder


def input_reading_configs():
    hint_text = """select setting mode : 
    1 : learning
    2 : quick check
    3 : word by word
    4 : slow review
    5 : custom\n>>> """

    config_getting_mode = None
    while not config_getting_mode in [1, 2, 3, 4, 5]:
        config_getting_mode = input_setting_with_default(hint_text, int, 1)

    if config_getting_mode == 1: settings = learning_mode_settings
    elif config_getting_mode == 2: settings = quick_check_mode_settings
    elif config_getting_mode == 3: settings = word_by_word_mode_settings
    elif config_getting_mode == 4: settings = slow_review_mode_settings
    else: settings = none_settings

    settings = custom_settings(*settings)
    # settings = (return reading_interval, repeat_times, repeat_interval, only_marked, pause, reorder)

    return settings


def load_vocabulary_lines(vocabulary_path, only_marked = True):
    # Get reading settings
    with open(vocabulary_path, 'r', encoding='utf-8') as f:lines = f.readlines() # Load vocabulary

    # Get lines for read
    if only_marked:
        lines_for_read = []
        for line in lines:
            if line[0] == ' ':continue
            lines_for_read.append(line)
    else:
        lines_for_read = lines

    return lines_for_read


def read_vocabulary(vocabulary_file_root):
    # Input settings
    while True:
        vocabulary_name = input_setting("input vocabulary name: ")
        vocabulary_path = os.path.join(vocabulary_file_root, f"{vocabulary_name}.txt")
        if os.path.exists(vocabulary_path):break
        print(f"[WARNING] can not find vocabulary [{vocabulary_name}] at {vocabulary_file_root}")

    # Get reading settings
    reading_interval, repeat_times, repeat_interval, only_marked, pause, reorder = input_reading_configs()

    # Get lines for read
    lines_for_read = load_vocabulary_lines(vocabulary_path, only_marked)
    word_num = len(lines_for_read)

    # Start to read
    while True:

        # Reorder if reorder setting is on
        if reorder:random.shuffle(lines_for_read)

        # Count down for start
        print_count_down(5)

        print(f"READING VOCABULARY < {vocabulary_name} > ... ")

        for i, line in enumerate(lines_for_read):
            word_info = line.split('|')[0]
            marked = word_info[0] != ' '
            word = word_info.replace(' ', '').replace('!', '')
            
            print("%-7s %s %s" % (f"({i + 1}/{word_num})", "★" if marked else ' ', line[2:].replace('\n', '')))
            try:
                print_eg(word, indentation_blank = ' ' * 95)
            except Exception as e:
                print("    Sorry, can not print eg right now")
            
            read_word(word, repeat_times, repeat_interval)
            
            if pause:
                ht = "PAUSING ... ( input 'q' to quit this round, 's' to reset settings ) >>> "
                pause_input = input(ht)
                if pause_input == 'q':
                    break
                elif pause_input == 's':
                    reading_interval, repeat_times, repeat_interval, only_marked, pause, reorder = input_reading_configs(only_marked=only_marked)
            else:
                time.sleep(reading_interval)

        # Exit if not repeat
        action = ''
        ht = """a round finished, you want to :
        r : read again (default)
        q : exit reading mode
        s : reset settings and read again\n>>> """
        while not action in ['r', 'q', 's']:action = input_setting_with_default(ht, str, 'r')
        if action == 'q':
            break
        elif action == 's':
            reading_interval, repeat_times, repeat_interval, only_marked, pause, reorder = input_reading_configs()
            lines_for_read = load_vocabulary_lines(vocabulary_path, only_marked)
            word_num = len(lines_for_read)
        else:
            pass

    print("FINISHED")
            
    return