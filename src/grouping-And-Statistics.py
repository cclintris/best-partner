# coding = utf-8
from collections import defaultdict

# 所有问题的类型
question_type = ["字符串", "数组", "数字操作", "树结构", "图结构", "排序算法", "线性表", "查找算法"]


def deal_with_data(student_score_list: dict, question_type_list: dict):
    """
    处理数据
    :param student_score_list:所有学生分数的字典
    :param question_type_list:所有问题类型的字典
    :return: 按加权总分排序的学生列表
    """
    students_list = student_score_list.keys()
    students_type_score = get_type_score_of_students(student_score_list)
    question_score_rate = get_type_score_rate_of_questions(students_type_score)
    students_total_score = get_weighted_score_of_students(students_type_score, question_score_rate)
    students_list = sorted(students_list, key=lambda x: students_total_score[x])
    return students_list


def get_type_score_of_students(student_score_list: dict):
    """
    获取学生每种题型的总分
    :param student_score_list: 所有学生所有题目的分数
    :return: 每一学生每一类型题目总分的字典
    """
    student_score_list_group_by_question_type = defaultdict(dict)
    for studentId in student_score_list:
        # 构建每一个学生的分数字典
        student_score_list_group_by_question_type[studentId] = defaultdict(int)
        for questionId in student_score_list[studentId]:
            # 为每一个学生的分数字典增加每个同类型题目的分数
            student_score_list_group_by_question_type[studentId][question_type[questionId]] += \
                student_score_list[studentId][questionId]
    return student_score_list_group_by_question_type


def get_type_score_rate_of_questions(students_type_score: dict):
    """
    获取每种题型的总体得分率
    :param students_type_score: 每一学生每一类型题目的总分
    :return:每种题型的总得分率
    """
    questions_score_rate = defaultdict(int)
    for _type in question_type:
        for studentId in students_type_score:
            questions_score_rate[_type] += (students_type_score[studentId][_type])
        questions_score_rate[_type] /= 20000
    return questions_score_rate


def get_weighted_score_of_students(students_type_score: dict, questions_score_rate: dict):
    """
    获取学生的加权总分
    :param students_type_score: 每一学生每一类型题目的总分
    :param questions_score_rate: 每一类型题目的总体得分率
    :return:
    """
    students_total_score = defaultdict(int)
    for studentId in students_type_score:
        for _type in questions_score_rate:
            students_total_score[studentId] += (students_type_score[_type]) / (questions_score_rate[_type])
    return students_total_score
