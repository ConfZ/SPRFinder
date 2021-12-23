import math
import settings

settings.NumAssert = 15
settings.MaxStr = 500
settings.MinStr = 10
settings.GeneratorNumConst = 20
if __name__ == '__main__':
    average_time = 5
    settings.max_var_num = 3
    settings.max_assert_num = 4
    settings.max_depth = 3
    settings.max_str_len = 10
    # it = 20
    add = 0
    for it in range(0, 100):
        if 20 < it <= 30:
            if average_time > 15 and settings.max_str_len > settings.MinStr:
                add = math.ceil(it / math.ceil(average_time))
                if add > 20:
                    add = 20
                settings.max_str_len -= add
            elif settings.max_str_len < settings.MaxStr:
                add = math.ceil(it / math.ceil(average_time)) * 5
                if add > 30:
                    add = 30
                settings.max_str_len += add
            # write = pd.DataFrame(
            #     [settings.max_str_len,
            #      settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
            # write.to_csv('./Parameter.csv', mode='a', header=False)
        if 30 < it < 40:
            if settings.max_var_num < settings.GeneratorNumConst:
                add = math.ceil(it / (math.ceil(average_time) * 5))
                if add > 5:
                    add = 5
                settings.max_var_num += add
            # write = pd.DataFrame(
            #     [settings.max_str_len,
            #      settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
            # write.to_csv('./Parameter.csv', mode='a', header=False)
        elif 40 < it < 50:
            if settings.max_assert_num < settings.NumAssert:
                add = math.ceil(it / (math.ceil(average_time) * 100))
                settings.max_assert_num += add
                if add > 3:
                    add = 3
                if settings.max_assert_num > settings.NumAssert:
                    settings.max_assert_num = settings.NumAssert
        elif 50 < it < 60:
            if settings.max_depth < settings.GeneratorMaxDepth:
                # add = math.ceil(it / (math.ceil(average_time) * 100))
                settings.max_depth += 1
            pop = []
        print('max_str_len:', settings.max_str_len, 'max_var_num:', settings.max_var_num,
              'max_assert_num:', settings.max_assert_num, 'max_depth:', settings.max_depth, 'add:', add)
            # write = pd.DataFrame(
            #     [settings.max_str_len,
            #      settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
            # write.to_csv('./Parameter.csv', mode='a', header=False)
            # for i in range(start_pop):
            #     pop.append(self.gen_new_inst())