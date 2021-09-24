import os
import random
from utils.input_utils import input_setting, input_yes_or_no, input_setting_with_default
from utils.ivocabulary_utils import read_word


def remark(vocabulary_file_root):
    # Input settings
    v_n = input_setting("input vocabulary name: ")
    marked_only = input_yes_or_no("only remark words marked (y/n): ")
    show_meaning = input_yes_or_no("dispaly meanings (y/n): ")
    read = input_yes_or_no("read during marking (y/n): ")
    reorder = input_yes_or_no("reorder vocabulary before remark (y/n): ")

    # Initialize
    v_pth = os.path.join(vocabulary_file_root, f"{v_n}.txt")

    # Validation
    if not os.path.exists(v_pth):
        print(f"[WARNING] can not find vocabulary [{v_n}] at {vocabulary_file_root}")
        return

    # Load vocabulary
    with open(v_pth, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Reorder
    if reorder:random.shuffle(lines)

    # Process marked only
    lines_for_rmk = []
    ignored_lines = []
    if marked_only:
        for line in lines:
            if line[0] == '!': lines_for_rmk.append(line)
            else: ignored_lines.append(line)
    else:
        lines_for_rmk = lines

    # Remark
    i = 0
    word_num = len(lines_for_rmk)
    while i < word_num:
        line = lines_for_rmk[i]
        # display word info
        if show_meaning:
            display_text = line[2:]
        else:
            tmp = line[2:].split('|')
            display_text = f"{tmp[0]}{tmp[1]}\n"
        # read word    
        if read:
            word = line[2:].split('|')[0].replace(' ', '')
            read_word(word)
        # mark, unmark or back to last one
        op = None
        hint_text = f"{display_text}[({i + 1}/{word_num}) enter 'm' for mark, enter 'b' back to last one ] >>> "
        while not op in ['m', 'b', 'n']: op = input_setting_with_default(hint_text, default_value = 'n')
        if op == 'm': # mark
            lines_for_rmk[i] = f"{'!'}{line[1:]}"
        elif op == 'b': # back
            i = max(i - 1, 0)
            continue
        else: # unmark
            lines_for_rmk[i] = f"{' '}{line[1:]}"
        # next i
        i += 1

    # Write vocabulary
    res_lines = lines_for_rmk + ignored_lines
    save = input_yes_or_no("save mark res (y/n): ")
    if save:
        with open(v_pth, 'w', encoding='utf-8') as f:
            f.writelines(res_lines)

    print("\nFNISHED\n")
    return
    