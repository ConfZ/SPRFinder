#
# def self_adaptive(average_time, )
# if 20 < self.it <= 30:
#     if average_time > 15 and settings.max_str_len > settings.MinStr:
#
#         add = math.ceil(self.it /math.ceil(average_time))
#         if add > 20:
#             add = 20
#         settings.max_str_len -= add
#     elif settings.max_str_len < settings.MaxStr:
#         add = math.ceil(self.it / math.ceil(average_time))*5
#         if add > 30:
#             add = 30
#         settings.max_str_len += add
#     write = pd.DataFrame(
#         [settings.max_str_len,
#          settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
#     write.to_csv('./Parameter.csv', mode='a', header=False)
# if 30 <self.it < 40:
#
#     if settings.max_var_num < settings.GeneratorNumConst:
#         add = int(self.it/(math.ceil(average_time)*5))
#         if add > 5:
#             add = 5
#         settings.max_var_num += add
#     write = pd.DataFrame(
#         [settings.max_str_len,
#          settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
#     write.to_csv('./Parameter.csv', mode='a', header=False)
# elif 40 < self.it < 50:
#     if settings.max_assert_num < settings.NumAssert:
#         add = math.ceil(self.it / (math.ceil(average_time) * 100))
#         settings.max_assert_num += add
# elif 50 < self.it < 60:
#     if settings.max_depth < settings.GeneratorMaxDepth:
#         add = math.ceil(self.it / (math.ceil(average_time) * 100))
#         settings.max_depth += add
#     pop = []
#     write = pd.DataFrame(
#         [settings.max_str_len,
#          settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
#     write.to_csv('./Parameter.csv', mode='a', header=False)
#     for i in range(self.start_pop):
#         pop.append(self.gen_new_inst())