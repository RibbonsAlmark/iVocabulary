import os
import enchant
from utils.input_utils import input_setting, input_setting_with_default, input_yes_or_no
from utils.print_utils import bounder, bounder2, soft_banner, print_help_text
from utils.read_config import read_config
from functions.read_words import read_vocabulary
from functions.vocabulary_randomization import vocabulary_reorder
from functions.find_word import find_word
from functions.add_words import add_words
from functions.vocabulary_remark import remark
from functions.download_resources import download_resources


def get_vocabulary_list_text(vocabulary_file_root):
    vfl_msg = 'vocabulary lists: \n\n'
    for vocabulary_fn in os.listdir(vocabulary_file_root):
        vfl_msg += f"        {vocabulary_fn.replace('.txt', '')}\n"
    return vfl_msg


def print_banner(vocabulary_file_root):
    vlt = get_vocabulary_list_text(vocabulary_file_root)

    bt = f"{bounder}{soft_banner}\n\n\n{vlt}\n{bounder}"

    print(bt)
    return


def print_vocabulary_cover(vocabulary_name, new_vocabulary):
    if new_vocabulary:vocabulary_name += ' [NEW]'
    c00 = " __________________ \n"
    c01 = "|                  |\n"
    c02 = "|                  |\n"
    c03 = "|  %-16s|\n"%vocabulary_name
    c04 = "|                  |\n"
    c05 = "|                  |\n"
    c06 = "|                  |\n"
    c07 = "|                  |\n"
    c08 = "|                  |\n"
    c09 = "|                  |\n"
    c10 = "|__________________|\n"

    cl = [c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10]

    ct = ''
    for c in cl:ct += c

    print(ct)
    return


"""
TODO:
    1. trans .txt source file to .md file, use footnote to accomplish hide meanings info and show when mouse hover
    2. mix vocabularies
    3. remark
    4. mark after read a word
    5. move to previous word after read a word
    6. assimilate Oxford thief in this project
    -- 7. add back to forward function to remark operation
    -- 8. add only remark marked words option to remark operation
    9. make operations as object, generate hel text automatically
    10.merge multipul  vocabularies as one big list and do operation
    11.util for settings
"""
if __name__ == "__main__":
    # Settings
    vocabulary_file_root = read_config("basic", "vocabulary_file_root")

    # Initialize
    if not os.path.exists(vocabulary_file_root):os.makedirs(vocabulary_file_root)

    # Print banner
    print_banner(vocabulary_file_root)

    # Print operation help
    help_text = print_help_text()

    # Start work
    while True:
        # Choose operation
        op = input("input operation code: ").lower()

        if op == 'h':
            print(f"\n{help_text}")
        elif op == 'a':
            add_words(vocabulary_file_root)
        elif op == 'ro':
            vocabulary_reorder(vocabulary_file_root)
        elif op == 'f':
            find_word(vocabulary_file_root)
        elif op == 'r':
            read_vocabulary(vocabulary_file_root)
        elif op == 'rmk':
            remark(vocabulary_file_root)
        elif op == 'dl':
            download_resources()
        elif op == 'mg':
            from functions.merge_new_vocabulary import merge_new_vocabulary
            merge_new_vocabulary(vocabulary_file_root)
        elif op == 'q':
            print("\nQUIT\n")
            break
        else:
            print("[WARNING] invalid operation code")
            continue

        print(bounder)

