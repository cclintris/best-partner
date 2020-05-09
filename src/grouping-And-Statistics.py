# coding = utf-8
from collections import defaultdict

# 所有问题的类型
question_type = ["字符串", "数组", "数字操作", "树结构", "图结构", "排序算法", "线性表", "查找算法"]


def deal_with_data(student_score_list: dict, question_type_list: dict) -> list:
    """
    处理数据
    :param student_score_list:所有学生分数的字典
    :param question_type_list:所有问题类型的字典
    :return: 按加权总分分组的小组列表
    """
    # 获取按加权总分排序的小组列表
    students_list = list(student_score_list.keys())
    students_type_score = get_type_score_of_students(student_score_list, question_type_list)
    question_score_rate = get_type_score_rate_of_questions(students_type_score)
    students_total_score = get_weighted_score_of_students(students_type_score, question_score_rate)
    students_list.sort(key=lambda x: students_total_score[x])

    # 以5分为间距获取不少于5人不多于20人的小组，可能出现小组极差大于5分的情况
    group_list = group_by(students_list, students_total_score, 5, 20, 5)

    return group_list


def get_type_score_of_students(student_score_list: dict, question_type_list: dict) -> dict:
    """
    获取学生每种题型的总分
    :param student_score_list: 所有学生所有题目的分数
    :param question_type_list: 所有题目的类型字典
    :return: 每一学生每一类型题目总分的字典
    """
    student_score_list_group_by_question_type = defaultdict(dict)
    for studentId in student_score_list:
        # 构建每一个学生的分数字典
        student_score_list_group_by_question_type[studentId] = defaultdict(int)
        for questionId in student_score_list[studentId]:
            # 为每一个学生的分数字典增加每个同类型题目的分数
            student_score_list_group_by_question_type[studentId][question_type_list[questionId]] += \
                student_score_list[studentId][questionId]
    return student_score_list_group_by_question_type


def get_type_score_rate_of_questions(students_type_score: dict) -> dict:
    """
    获取每种题型的总体得分权值
    :param students_type_score: 每一学生每一类型题目的总分
    :return:每种题型的得分权值(权值公式：总得分/基准值)(此处定为20000/8*学生人数，并且权值越低权重越高)
    """
    questions_score_rate = defaultdict(int)
    base = 2500 * len(students_type_score)
    for _type in question_type:
        for studentId in students_type_score:
            # 将每个学生该类型的分数加入列表的对应项
            questions_score_rate[_type] += (students_type_score[studentId][_type])
        questions_score_rate[_type] /= base
    return questions_score_rate


def get_weighted_score_of_students(students_type_score: dict, questions_score_rate: dict) -> dict:
    """
    获取学生的加权总分
    :param students_type_score: 每一学生每一类型题目的总分
    :param questions_score_rate: 每一类型题目的总体得分权值
    :return:题型加权总分的字典(总分公式：求和(总分/总体得分权值))
    """
    students_total_score = defaultdict(int)
    for studentId in students_type_score:
        for _type in questions_score_rate:
            students_total_score[studentId] += (students_type_score[_type]) / (questions_score_rate[_type])
    return students_total_score


def group_by(student_list: list, student_total_score: dict, least: int, maximal: int, gap: int) -> list:
    """
    获得按水平分组的学生小组列表
    :param student_list:加权分从低到高的学生ID列表
    :param student_total_score: 学生的分数字典
    :param least: 每组学生的最少数目
    :param maximal: 每组学生的最多数目
    :param gap:分组的间隔
    :return:按水平分组的小组列表，列表的每一项是学生ID
    """
    # 初始化
    student_group_list = []
    count = 0
    # 从最低分的学生开始计算
    start = student_total_score[student_list[0]]
    # 计数器小于学生人数时
    while count < len(student_list):
        group = []
        # 人数必须不小于最小值，否则与下一组合并
        while len(group) < least:
            if len(student_list) <= count:
                break
            score = student_total_score[student_list[count]]
            # 总分在现区间内则加入小组，否则切换到下一个区间
            if start <= score < start + gap:
                group.append(student_list[count])
                count += 1
                if maximal < len(group):
                    break
            else:
                start += gap
                continue
        # 将小组值的拷贝添加到小组列表中
        student_group_list.append(group.copy())
    return student_group_list
