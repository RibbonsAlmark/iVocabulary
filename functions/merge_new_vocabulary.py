import os
from utils.input_utils import input_setting, input_setting_with_default, input_yes_or_no


# TODO:make static function for hint text at home page
class MergeNewVocabulary:
    def __init__(self, vocabulary_file_root):
        self.vocabularies_list = []
        self.word_info_lines = []
        self.vocabulary_file_root = vocabulary_file_root
        return

    def __load_vocabularies__(self):
        for vocabulary_name in self.vocabularies_list:
            vocabulary_path = os.path.join(self.vocabulary_file_root, f"{vocabulary_name}.txt")
            with open(vocabulary_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.word_info_lines += lines
        return

    def __get_vocabularies_list___(self):
        hint_text = "input name of vocabularies which will add to merged vocabulary (split with ',') : "
        vocabularies_list_str = input_setting(hint_text)
        self.vocabularies_list = vocabularies_list_str.replace(' ', '').split(',')
        return

    def merge(self, target_vocabulart_name="tmp"):
        self.__get_vocabularies_list___()
        self.__load_vocabularies__()
        target_vocabulary_path = os.path.join(self.vocabulary_file_root, f"{target_vocabulart_name}.txt")
        with open(target_vocabulary_path, 'w', encoding='utf-8') as f:
            f.writelines(self.word_info_lines)
        return


def merge_new_vocabulary(vocabulary_file_root):
    worker = MergeNewVocabulary(vocabulary_file_root)
    worker.merge()
    print("\nFNISHED\n")
    return