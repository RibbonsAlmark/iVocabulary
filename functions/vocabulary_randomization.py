import os
import random
from utils.input_utils import input_setting


# class vocabularyOrderMaker:
#     def __init__(self, vocabulary_file_root):
#         self.vf_root = vocabulary_file_root
#         self.vf_path = None
#         self.v_name = None

#     def __get_vf_path__(self):
#         vocabulary_name = input_setting("input vocabulary name: ")
#         self.vf_path = os.path.join(self.vf_root, f"{vocabulary_name}.txt")
#         self.v_name = vocabulary_name
#         return vf_path

#     def randomization(self):
#         while True:
#             self.__get_vf_path__()
#             if os.path.exists(self.vf_path): break
#             else: print(f"[WARNING] can not find vocabulary [{self.v_name}] at {self.vf_root}")

#         with open(self.vf_path, 'r', encoding='utf-8') as f: lines = f.readlines()
#         random.shuffle(lines)
#         with open(self.vf_path, 'w', encoding='utf-8') as f: f.writelines(lines)

#         print(f"words in vocabulary [{self.v_name}] has been reordered")
#         return

#     def focus_on_marked(self):
#         while True:
#             self.__get_vf_path__()
#             if os.path.exists(self.vf_path): break
#             else: print(f"[WARNING] can not find vocabulary [{self.v_name}] at {self.vf_root}")

#         with open(self.vf_path, 'r', encoding='utf-8') as f: lines = f.readlines()
        
#         for line in lines:
#             if line[0] == '!': marked_list.append(line)
#             else: unmark_list.append(line)

#         ret_lines = marked_list + unmark_list
#         with open(self.vf_path, 'w', encoding='utf-8') as f: f.writelines(ret_lines)

#         print(f"words in vocabulary [{self.v_name}] has been reordered")
#         return



def vocabulary_reorder(vocabulary_file_root):
    # Initialize
    vocabulary_name = input_setting("input vocabulary name: ")
    vocabulary_path = os.path.join(vocabulary_file_root, f"{vocabulary_name}.txt")

    # TODO:
    randomization(vocabulary_path)
    # focus_on_marked(vocabulary_path)
    return


def randomization(vocabulary_path):
    if not os.path.exists(vocabulary_path):
        print(f"[WARNING] can not find vocabulary [{vocabulary_name}] at {vocabulary_file_root}")
        return

    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    random.shuffle(lines)
    
    with open(vocabulary_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    # print("\nFNISHED\n")
    print(f"words in vocabulary [{vocabulary_path}] has been reordered")
    return


def focus_on_marked(vocabulary_path):
    marked_list = []
    unmark_list = []

    if not os.path.exists(vocabulary_path):
        print(f"[WARNING] can not find vocabulary [{vocabulary_name}] at {vocabulary_file_root}")
        return

    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line[0] == '!':
            marked_list.append(line)
        else:
            unmark_list.append(line)

    ret_lines = marked_list + unmark_list

    with open(vocabulary_path, 'w', encoding='utf-8') as f:
        f.writelines(ret_lines)

    return