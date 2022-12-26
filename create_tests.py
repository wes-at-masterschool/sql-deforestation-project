# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:44:46 2021

@author: wes_c
"""

import json
import numpy as np
import numpy.random as random
import pandas as pd
from functools import reduce

def get_data(data_path):
    return json.load(open(data_path, 'r'))

def dict_to_df(dict_data, correct='Correct', figure='Figure'):
    reformat = []
    for question in dict_data:
        k = list(question.keys())[0]
        answers = question[k]
        reformat.append([k, answers.get('A'), answers.get('B'),
                         answers.get('C'), answers.get('D'),
                         answers.get(correct), answers.get(figure)])
    df = pd.DataFrame(reformat, columns=['Question', 'A', 'B',
                               'C', 'D', 'Correct', 'Figure'])
    return df

def make_quiz(content_key, data, n_questions=10, correct='Correct',
              figure='Figure', used=None):
    question_bank = data[content_key]
    q_numbers = range(len(question_bank))
    if used is not None:
        q_numbers = set(q_numbers) - set(used)
        if len(q_numbers) < n_questions:
            reused = random.choice(used, size=n_questions - len(q_numbers),
                                   replace=False)
            nums = np.concatenate((np.array(list(q_numbers)), reused))
        else:
            nums = random.choice(list(q_numbers),
                                 size=n_questions, replace=False)
    else:
        nums = random.choice(q_numbers, size=n_questions, replace=False)
    keys = [question_bank[num] for num in nums]
    df = dict_to_df(keys, correct=correct, figure=figure)
    return df, {content_key:nums}

def make_quizzes(data, content_keys=['Sheets', 'SQL', 'PythonData', 'Tableau'],
                 save_prefix='DataBootcamp',
                 correct='Correct', figure='Figure'):
    dicts = []
    #save DFs, later upload them to drive
    for key in content_keys:
        df, partial_dict = make_quiz(key, data, correct=correct, figure=figure)
        df.to_csv(save_prefix + key + 'Quiz.csv', index=False)
        dicts.append(partial_dict)
    used_questions = reduce(lambda x,y: {**x, **y}, dicts)
    return used_questions

def make_exam(data, used, 
              content_keys=['Sheets', 'SQL', 'PythonData', 'Tableau'],
              save_prefix='DataBootcamp', **kwargs):
    topic_questions = kwargs.get('questions_per_topic', 10)
    dfs = []
    for key in content_keys:
        df, _ = make_quiz(key, data, n_questions=topic_questions,
                          correct=kwargs.get('correct', 'Correct'),
                          figure=kwargs.get('figure', 'Figure'),
                          used=used.get(key))
        dfs.append(df)
    df = pd.concat(dfs, axis=0)
    df.to_csv(save_prefix + 'Exam.csv', index=False)
    return df

if __name__ == '__main__':
    data = get_data('test.json')
    used = make_quizzes(data)
    df = make_exam(data, used)
