# coding=utf-8
import sys

'''

@:param
line: 目标代码

@:return
true:  第line行目标代码包含 print() 函数
false: 第line行目标代码不包含 print() 函数

'''


def standard1(line):
    standard1 = "print"
    if line.find("#") != -1:
        return "NULL"
    if line.find(standard1) != -1:
        return line
    else:
        return "NULL"


'''

@:param
standard1Recorder: 目标代码每一行是否包含print()函数标记

@:return
true: 断言面向用例
false: 断言非面向用例

'''


def standard1Judge(standard1Recorder):
    illegalPrintFreq = 0
    printFreq = 0
    for i in range(standard1Recorder.__len__()):
        if standard1Recorder[i] == "NULL":
            continue
        else:
            printFreq += 1
            lineList = list(standard1Recorder[i])
            start = standard1Recorder[i].find("(")
            end = standard1Recorder[i].find(")")
            # 撷取 print函数 '()' 之间的打印信息
            printedContextlist = lineList[start + 1: end]
            printedContext = ''.join(printedContextlist)
            if (printedContext.isnumeric()):
                illegalPrintFreq += 1

    if printFreq > 2:
        return True
    else:
        if illegalPrintFreq != 0:
            return True
        else:
            return False


'''

@:param
line: 目标代码

@:type
syntaxTypefreq: list

standard2 index:
0 for
1 if
2 elif
3 else
4 while
5 do
6 def

@:var
standard2: 代码语句结构
syntaxTypefreq: 记录目标代码包含结构各出现频率

@:return
syntaxTypefreq: 第line行代码包含结构各出现频率 

'''

syntax = ["for", "if", "elif", "else", "while", "do", "def"]


def standard2(line):
    syntaxTypefreq = [0 for _ in range(syntax.__len__())]
    for i in range(syntax.__len__()):
        if line.find(syntax[i]) >= 0:
            if i == 2 and syntaxTypefreq[1] != 0:
                syntaxTypefreq[1] = 0
                syntaxTypefreq[2] += 1
            else:
                syntaxTypefreq[i] += 1
    return syntaxTypefreq


'''

@:param
standard2Recorder: 目标代码每一行所包含语法结构，1 表示包含，0 表示不包含

@:return
true: 断言面向用例
false: 断言非面向用例

'''


def standard2Judge(standard2Recorder):
    syntaxJudge = [0 for _ in range(syntax.__len__())]
    for i in range(syntaxJudge.__len__()):
        for j in range(standard2Recorder.__len__()):
            syntaxJudge[i] += standard2Recorder[j][i]
        # print(syntax[i], end=" ")
        # print(syntaxJudge[i])
    # print(syntaxJudge)
    syntaxKinds = 0
    for i in range(syntaxJudge.__len__()):
        if syntaxJudge[i] == 0:
            continue
        else:
            if i == 1:
                syntaxKinds += 1
            elif i != 1 and (i == 2 or i == 3):
                continue
            else:
                syntaxKinds += 1
    return syntaxKinds == 1


''''

@:param
firstLine: 目标代码第一行

@:return
true: 断言面向用例
false: 认定目标代码import其他python库，断言非面向用例

'''


def standard3Judge(firstLine):
    standard3 = "import"
    return firstLine.find(standard3) == -1


'''
check_Orientcase.py 主要对外接口

代码是否面向用例评判标准:
standard1
standard2
standard3

@:param
targetCodepath: 目标代码相对路径

@:return
true: 断言面向用例
false: 断言非面向用例

'''


def checkOrientCase(targetCodepath):
    # 起初都先假设目标代码为非面向用例
    assertCodeIsOrientCase = False
    with open(targetCodepath, "r", encoding="utf-8") as f:
        standard1Recorder = []
        standard2Recorder = []
        # 目标代码每一行，将存储为 list[] 的数据结构
        data = f.readlines()
        # 目标代码第一行
        firstLine = data[0]

        for i in range(data.__len__()):
            standard1Recorder.append(standard1(data[i]))
            standard2Recorder.append(standard2(data[i]))

        assertCodeIsOrientCase = standard1Judge(standard1Recorder) and \
                                 standard2Judge(standard2Recorder) and \
                                 standard3Judge(firstLine)

        return assertCodeIsOrientCase



#本地测试main函数

if __name__ == '__main__':
    assertCodeIsOrientCase = False
    with open("D:\數據科學基礎\\best-partner\\test\\plagiarize_case.py", "r", encoding="utf-8") as f:
        standard1Recorder = []
        standard2Recorder = []
        data = f.readlines()
        firstLine = data[0]
        #print(data)
        #print(firstLine)
        for i in range(data.__len__()):
            standard1Recorder.append(standard1(data[i]))
            standard2Recorder.append(standard2(data[i]))
        # print(standard1Recorder)
        # print(standard2Recorder)
        # print(standard1Judge(standard1Recorder))
        # print(standard2Judge(standard2Recorder))
        # print(standard3Judge(firstLine))
        assertCodeIsOrientCase = standard1Judge(standard1Recorder) and \
                                 standard2Judge(standard2Recorder) and \
                                 standard3Judge(firstLine)
        print(assertCodeIsOrientCase)


