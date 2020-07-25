import re
import requests

'''
缺陷：
1. 判断def之前有无空行时候，没有考虑def是否在class|def内
2. 检查引号简单的判断是否混用单双引号，没有考虑其他单双引号使用的标准
3. 判断=, !=等二元运算符时没有考虑他们本身是字符串的情况
4. 
'''


class Checker:
    # 翻译时使用的翻译接口
    url = "http://fanyi.youdao.com/translate"
    # 所有以下变量 True无问题 False有问题
    # 如果tab_or_space = 0，则说明这篇代码的缩进用的是space；如果tab_or_space = 1，则说明这篇代码的缩进用的是tab
    tab_or_space = -1
    is_indent_using_one = True
    is_space_nums_multiple_of_four = True
    is_within_len_range = True
    is_not_trailing_space = True
    is_space_around_operator = True
    is_not_space_around_operator_in_def = True
    # 必要时，可以使用两种引号
    is_using_one_quotation = True
    is_not_blank_line_beginning = True
    is_not_inline_comments = True
    is_space_after_pound = True
    is_blank_line_after_import = True
    is_blank_line_before_class = True
    is_blank_line_before_def = True
    is_not_diff_package_in_the_same_line = True
    is_import_before_from = True
    is_not_blank_between_import = True
    is_using_meaningful_name = True

    # 构造函数 传入需检查的代码路径
    def __init__(self, filepath: str):
        self.file = open(filepath, 'r', encoding="utf-8")
        self.check_indentation()
        self.check_length()
        self.check_names()
        self.check_spaces()
        self.check_blank_line()
        self.check_import()
        self.check_marks()
        self.check_annotation()

    # 检查tab和空格
    def check_indentation(self):
        is_space = ' +'
        is_tab = '\t+'
        for line in self.file:
            if re.match(is_space, line):
                space_num = 0
                index = 0
                # 检查空格是否是4的倍数
                while line[index] == ' ':
                    space_num = space_num + 1
                    index = index + 1
                    if index == len(line):
                        break
                if space_num % 4 != 0:
                    self.is_space_nums_multiple_of_four = False
                if self.tab_or_space == -1:
                    self.tab_or_space = 0
                elif self.tab_or_space == 1:
                    self.is_indent_using_one = False
            if re.match(is_tab, line):
                if self.tab_or_space == -1:
                    self.tab_or_space = 1
                elif self.tab_or_space == 0:
                    self.is_indent_using_one = False
        if self.tab_or_space == -1:
            self.tab_or_space = 0

    # 检查长度
    def check_length(self, max_length=120):
        for line in self.file:
            if len(line) >= max_length:
                self.is_within_len_range = False

    # 检查命名
    def check_names(self):
        name_list = []
        for_while_num = 0
        for line in self.file:
            name = ''
            if re.match('[^\'\"]*for', line) or re.match('[^\'\"]*while', line):
                for_while_num = for_while_num + 1
            if '=' in line:
                index = line.find('=') - 1
                if line[index] == ' ':
                    while line[index] == ' ':
                        index = index - 1
                    while line[index] != ' ' and line[index] != '\t' and index != 0:
                        name = line[index] + name
            if '[' not in name and '(' not in name and name != '':
                if name not in name_list:
                    name_list.append(name)
        meaningless_name = 0
        for name in name_list:
            data = {'doctype': 'json', 'type': 'AUTO', 'i': name}
            result = requests.get(self.url, params=data)
            translate_result = result.json()['translateResult'][0][0]['tgt']
            is_meaningful = False
            for i in translate_result:
                if u'\u4e00' <= i <= u'\u9fff':
                    is_meaningful = True
            if not is_meaningful:
                meaningless_name = meaningless_name + 1
        if meaningless_name > for_while_num:
            self.is_using_meaningful_name = False

    # 检查空格
    def check_spaces(self):
        for line in self.file:
            # 检查尾随空格
            if line[len(line)-1] == ' ':
                self.is_not_trailing_space = False
            # 检查赋值(=), 比较(==, <, >, !=, <=, >=)这些二元运算符放置空格
            # 不在def内
            if 'def' not in line:
                for i in range(len(line)):
                    # 判断 =
                    if line[i] == '=':
                        # 判断左边
                        if (line[i-1] != ' '
                                and line[i-1] != '!'
                                and line[i-1] != '>'
                                and line[i-1] != '<'
                                and line[i-1] != '+'
                                and line[i-1] != '-'):
                            self.is_space_around_operator = False
                        # 判断 ==
                        if line[i+1] == '=':
                            if line[i+2] != ' ':
                                self.is_space_around_operator = False
                        # 判断右边
                        elif line[i+1] != ' ':
                            self.is_space_around_operator = False
                    # 判断 >
                    elif line[i] == '>':
                        # 判断左边
                        if line[i - 1] != ' ':
                            self.is_space_around_operator = False
                        # 判断 >=
                        if line[i + 1] == '=':
                            if line[i + 2] != ' ':
                                self.is_space_around_operator = False
                        # 判断右边
                        elif line[i + 1] != ' ':
                            self.is_space_around_operator = False
                    # 判断 <
                    elif line[i] == '<':
                        # 判断左边
                        if line[i - 1] != ' ':
                            self.is_space_around_operator = False
                        # 判断 <=
                        if line[i + 1] == '=':
                            if line[i + 2] != ' ':
                                self.is_space_around_operator = False
                        # 判断右边
                        elif line[i + 1] != ' ':
                            self.is_space_around_operator = False
                    # 判断 !
                    elif line[i] == '!':
                        # 判断左边
                        if line[i - 1] != ' ':
                            self.is_space_around_operator = False
                        # 判断右边
                        if line[i + 2] != ' ':
                            self.is_space_around_operator = False
            # 在def内
            else:
                for i in range(len(line)):
                    # 判断 =
                    if line[i] == '=':
                        # 判断左边
                        if line[i-1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                        # 判断 ==
                        if line[i+1] == '=':
                            if line[i+2] == ' ':
                                self.is_not_space_around_operator_in_def = False
                        # 判断右边
                        elif line[i+1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                    # 判断 >
                    elif line[i] == '>':
                        # 判断左边
                        if line[i - 1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                        # 判断 >=
                        if line[i + 1] == '=':
                            if line[i + 2] == ' ':
                                self.is_not_space_around_operator_in_def = False
                        # 判断右边
                        elif line[i + 1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                    # 判断 <
                    elif line[i] == '<':
                        # 判断左边
                        if line[i - 1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                        # 判断 <=
                        if line[i + 1] == '=':
                            if line[i + 2] == ' ':
                                self.is_not_space_around_operator_in_def = False
                        # 判断右边
                        elif line[i + 1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                    # 判断 !
                    elif line[i] == '!':
                        # 判断左边
                        if line[i - 1] == ' ':
                            self.is_not_space_around_operator_in_def = False
                        # 判断右边
                        if line[i + 2] == ' ':
                            self.is_not_space_around_operator_in_def = False

    # 检查空行
    def check_blank_line(self):
        lines = self.file.readlines()
        for i in range(len(lines)):
            # 检查开头是否是空行
            if i == 0 and not re.match('\\S', lines[0]):
                self.is_not_blank_line_beginning = False
            # 检查import之后有无空行
            temp = i
            while re.match('[^\'\"]*import', lines[temp]):
                if temp == len(lines)-1:
                    self.is_blank_line_after_import = False
                else:
                    temp = temp + 1
            # 如果有import
            if temp != i:
                # 略过所有# 注释
                while re.match('\\s*#', lines[temp]):
                    if temp == len(lines) - 1:
                        self.is_blank_line_after_import = False
                    else:
                        temp = temp + 1
                # 略过所有'''注释
                if re.match("\\s*'''", lines[temp]):
                    if temp == len(lines) - 1:
                        self.is_blank_line_after_import = False
                    else:
                        temp = temp + 1
                    while not re.match("\\s*'''", lines[temp]):
                        if temp == len(lines) - 1:
                            self.is_blank_line_after_import = False
                        else:
                            temp = temp + 1
                    if temp == len(lines) - 1:
                        self.is_blank_line_after_import = False
                    else:
                        temp = temp + 1
                # 略过所有"""注释
                if re.match('\\s*"""', lines[temp]):
                    if temp == len(lines) - 1:
                        self.is_blank_line_after_import = False
                    else:
                        temp = temp + 1
                    while not re.match('\\s*"""', lines[temp]):
                        if temp == len(lines) - 1:
                            self.is_blank_line_after_import = False
                        else:
                            temp = temp + 1
                    if temp == len(lines) - 1:
                        self.is_blank_line_after_import = False
                    else:
                        temp = temp + 1
                if re.match('\\S', lines[temp]):
                    self.is_blank_line_after_import = False
            # 检查class之前有无空行
            if re.match('[^\'\"]*class', lines[i]) and i != 0:
                if temp == 0:
                    self.is_blank_line_before_class = False
                else:
                    temp = i - 1
                # 略过所有# 注释
                while re.match('\\s*#', lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_class = False
                    else:
                        temp = i - 1
                # 略过所有'''注释
                if re.match("\\s*'''", lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_class = False
                    else:
                        temp = i - 1
                    while not re.match("\\s*'''", lines[temp]):
                        if temp == 0:
                            self.is_blank_line_before_class = False
                        else:
                            temp = i - 1
                    if temp == 0:
                        self.is_blank_line_before_class = False
                    else:
                        temp = i - 1
                # 略过所有"""注释
                if re.match('\\s*"""', lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_class = False
                    else:
                        temp = i - 1
                    while not re.match('\\s*"""', lines[temp]):
                        if temp == 0:
                            self.is_blank_line_before_class = False
                        else:
                            temp = i - 1
                    if temp == 0:
                        self.is_blank_line_before_class = False
                    else:
                        temp = i - 1
                if re.match('\\S', lines[temp]) or re.match('\\S', lines[temp-1]):
                    self.is_blank_line_before_class = False
            # 检查def之前有无空行
            if re.match('[^\'\"]*def', lines[i]) and i != 0:
                if temp == 0:
                    self.is_blank_line_before_def = False
                else:
                    temp = i - 1
                # 略过所有# 注释
                while re.match('\\s*#', lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_def = False
                    else:
                        temp = i - 1
                # 略过所有'''注释
                if re.match("\\s*'''", lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_def = False
                    else:
                        temp = i - 1
                    while not re.match("\\s*'''", lines[temp]):
                        if temp == 0:
                            self.is_blank_line_before_def = False
                        else:
                            temp = i - 1
                    if temp == 0:
                        self.is_blank_line_before_def = False
                    else:
                        temp = i - 1
                # 略过所有"""注释
                if re.match('\\s*"""', lines[temp]):
                    if temp == 0:
                        self.is_blank_line_before_def = False
                    else:
                        temp = i - 1
                    while not re.match('\\s*"""', lines[temp]):
                        if temp == 0:
                            self.is_blank_line_before_def = False
                        else:
                            temp = i - 1
                    if temp == 0:
                        self.is_blank_line_before_def = False
                    else:
                        temp = i - 1
                if re.match('\\S', lines[temp]):
                    self.is_blank_line_before_def = False

    # 检查导入
    def check_import(self):
        lines = self.file.readlines()
        import_start = -1
        from_start = -1
        for i in range(len(lines)):
            if re.match('[^\'\"]*import', lines[i]):
                if import_start == -1 and not re.match('[^\'\"]*from[^\'\"]*import', lines[i]):
                    import_start = i
                if from_start == -1 and re.match('[^\'\"]*from[^\'\"]*import', lines[i]):
                    from_start = i
                # 检查同行中导入了两个相同的包
                if ',' in lines[i]:
                    if not re.match('[^\'\"]*from[^\'\"]*import', lines[i]):
                        self.is_not_diff_package_in_the_same_line = False
        # 检查import在from前
        if from_start <= import_start:
            if from_start == -1 and import_start == -1:
                self.is_import_before_from = True
            else:
                self.is_import_before_from = True
        # 检查import是否分离
        is_importing = -1
        for i in range(len(lines)):
            if re.match('[^\'\"]*import', lines[i]):
                if is_importing == -1:
                    is_importing = 1
                elif is_importing == 0:
                    self.is_not_blank_between_import = False
            elif not re.match('\\s*#', lines[i]):
                if is_importing == 1:
                    is_importing = 0

    # 检查引号
    def check_marks(self):
        # 如果flag = 0，则说明这篇代码用的是单引号；如果flag = 1，则说明这篇代码用的是双引号
        flag = -1
        for line in self.file:
            for i in range(len(line)):
                if line[i] == '\'':
                    if flag == -1:
                        flag = 0
                    elif flag == 1:
                        self.is_using_one_quotation = False
                if line[i] == '\"':
                    if flag == -1:
                        flag = 1
                    elif flag == 0:
                        self.is_using_one_quotation = False

    # 检查注释
    def check_annotation(self):
        for line in self.file:
            if re.match('[^#]+#', line):
                self.is_not_inline_comments = False
            if not re.match('\\s*#* +', line):
                self.is_space_after_pound = False

