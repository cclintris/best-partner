import re
import os


def is_python(filepath):
    if os.path.getsize(filepath) == 0:
        return False
    file = open(filepath, 'r', encoding="utf-8")
    content = file.read()
    if content == "":
        return False
    if ("include" in content
            or "using namespace std" in content
            or "int main" in content):
        return False
    if ("static" in content
            or "void" in content
            or "String" in content
            or "args" in content):
        return False
    return True

