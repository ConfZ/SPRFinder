import settings
import math
import pandas as pd
import time
import random
STRING = 'string'
VARNUM = 'varnum'
ASSERT = 'assert'
DEPTH = 'depth'
def update_parameter(para_type, up_type):
    if para_type == 'string':
        if up_type == 'random':
            add = random.randint(20, 50)
        else:
            add = math.ceil(settings.it / math.ceil(1 if settings.average_time[0] == 0 else settings.average_time[0])) * 5
            add =  30 if add > 30 else add
        if settings.average_time[0] < 15:
            if settings.max_str_len < settings.MaxStr:
                settings.max_str_len += add
            else:
                settings.max_str_len = settings.MaxStr
        elif settings.average_time[0] >= 15 and settings.max_str_len > settings.MinStr:
            if settings.max_str_len > settings.MinStr:
                settings.max_str_len -= add
            else:
                settings.max_str_len = settings.MinStr

    elif para_type == 'varnum':
        if up_type == 'random':
            add = random.randint(1, 5)
        else:
            add = math.ceil(
                settings.it / (math.ceil(1 if settings.average_time[0] == 0 else settings.average_time[0]) * 5))
            add = 5 if add > 5 else add
        if settings.average_time[0] < 15:
            if settings.max_var_num < settings.MaxVarNum:
                settings.max_var_num += add
            else:
                settings.max_str_len = settings.MaxVarNum
        elif settings.average_time[0] >= 15:
            if settings.max_var_num > settings.MinVarNum:
                settings.max_var_num -= add
            else:
                settings.max_var_num = settings.MinVarNum
    elif para_type == 'assert':
        if up_type == 'random':
            add = random.randint(1, 3)
        else:
            add = math.ceil(settings.it / math.ceil((1 if settings.average_time[0] == 0 else settings.average_time[0]) * 100))
            add = 3 if add > 3 else add
        if settings.average_time[0] < 15:
            if settings.max_assert_num < settings.MaxAssertNum:
                settings.max_assert_num += add
            else:
                settings.max_assert_num = settings.MaxAssertNum
        elif settings.average_time[0] >= 15:
            if settings.max_assert_num > settings.MinAssertNum:
                settings.max_assert_num -= add
            else:
                settings.max_assert_num = settings.MinAssertNum

    elif para_type == 'depth':
        add = 1
        if settings.average_time[0] < 15:
            if settings.max_assert_num < settings.MaxDepth:
                settings.max_depth += add
            else:
                settings.max_depth = settings.MaxDepth
        elif settings.average_time[0] >= 15:
            if settings.max_depth > settings.MinDepth:
                settings.max_depth -= add
            else:
                settings.max_depth = settings.MinDepth
    else:
        raise ValueError("Wrong parameter type in self-adaptive!")

def self_adaptive(interval, update_by = 'time', update_value = 'random', t = 300):
    # ret = False
    if update_by == 'time':
        if t <= interval < 2*t:
            update_type = STRING
        elif 2*t <= interval < 3*t:
            update_type = VARNUM
        elif 4*t <= interval < 5*t:
            update_type = ASSERT
        elif 5*t <= interval < 6*t:
            update_type = DEPTH
        else:
            update_type = ''
    else:
        update_type = ''
    if len(update_type) != 0:
        update_parameter(update_type, update_value)
        return True
    else:
        return False



    # if update_by == 'round':
    #     if 20 < it <= 30:
    #         if settings.average_time[0] > 15 and settings.max_str_len > settings.MinStr:
    #
    #             add = math.ceil(it /math.ceil(settings.average_time[0]))
    #             if add > 20:
    #                 add = 20
    #             settings.max_str_len -= add
    #         elif settings.max_str_len < settings.MaxStr:
    #             add = math.ceil(it / math.ceil(settings.average_time[0]))*5
    #             if add > 30:
    #                 add = 30
    #             settings.max_str_len += add
    #         # write = pd.DataFrame(
    #         #     [settings.max_str_len,
    #         #      settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
    #         # write.to_csv('./Parameter.csv', mode='a', header=False)
    #     if 30 <it < 40:
    #
    #         if settings.max_var_num < settings.GeneratorNumConst:
    #             add = int(it/(math.ceil(settings.average_time[0])*5))
    #             if add > 5:
    #                 add = 5
    #             settings.max_var_num += add
    #         write = pd.DataFrame(
    #             [settings.max_str_len,
    #              settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
    #         write.to_csv('./Parameter.csv', mode='a', header=False)
    #     elif 40 < it < 50:
    #         if settings.max_assert_num < settings.NumAssert:
    #             add = math.ceil(it / (math.ceil(settings.average_time[0]) * 100))
    #             settings.max_assert_num += add
    #     elif 50 < it < 60:
    #         if settings.max_depth < settings.GeneratorMaxDepth:
    #             add = math.ceil(it / (math.ceil(settings.average_time[0]) * 100))
    #             settings.max_depth += add
    #
    #         write = pd.DataFrame(
    #             [settings.max_str_len,
    #              settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
    #         write.to_csv('./Parameter.csv', mode='a', header=False)
    #     else:
    #         ret = False


    # return ret