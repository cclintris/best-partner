import re
import os


def is_python(filepath):
    if os.path.getsize(filepath) == 0:
        return False
    file = open(filepath, 'r', encoding="utf-8")
    file_name = filepath.split("/")[3]
    content = eval(file.read())
    file.close()
    file = open("../code/res/" + file_name + "/main.py", 'r', encoding="utf-8")
    for line in file:
        if "print" in line:
            if "(" not in line:
                return False
    if content["lang"] == "Python3":
        return True
    else:
        return False
    # if content == "":
    #     return False
    # if ("include" in content
    #         or "using namespace std" in content
    #         or "int main" in content):
    #     return False
    # if ("static" in content
    #         or "void" in content
    #         or "String" in content
    #         or "args" in content):
    #     return False
    # return True
