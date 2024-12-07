import os

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

class FolderAnalyzer:
    def __init__(self, paths: list):
        """
        Class that gives all the files without folders in a selection of folders
        :param paths: path of one or many folders
        """
        if not paths:
            print(RED + "No files or directories were provided." + RESET)
            input(RED + "\nProcess Failed, press enter to exit." + RESET)
            self.exists = False
        else:
            self.exists = True

        self.folder = []

        list_paths = []
        for element in paths:
            if os.path.isdir(element):
                self.folder.append(element)
                if element in list_paths:
                    list_paths.remove(element)
                for root_dir, _, files in os.walk(element):
                    for file in files:
                        list_paths.append(os.path.join(root_dir, file))
            else:
                list_paths = paths

            self.file_list = list_paths

            for sub_element in list_paths:
                self.final_file = sub_element
