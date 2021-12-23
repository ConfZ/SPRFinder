import settings
import utils
import sys, os, pdb, glob, random, time
from instance import Instance
from gen import mk_gen
import settings
from thompson import Thompson
from instance import Instance
import pandas as pd
from dtw.dtw import dtw
import math
from numpy import mean
def get_time_similarity(times):
    return min([dtw(times, tl).distance for tl in settings.found_time_list])
class Fuzzer:
    def __init__(self, time0):
        self.init_time = time0
        self.time0 = time0
        self.it = 0
        self.find = False
        self.num_pop = settings.FuzzerPopulation
        self.num_keep = settings.FuzzerNumberOfHardestKept
        self.num_mutations = settings.FuzzerNumberOfMutations
        self.start_pop = settings.FuzzerNumberPopulationStart
        self.gen = mk_gen()
        self.mutator = Thompson(self.gen.ops)
        self.all_solved = set()
        self.last_mut_success = None

    def gen_new_inst(self):
        ret = self.gen.gen()
        while str(ret) in self.all_solved: ret = self.gen.gen()
        ret.solve()
        self.all_solved.add(ret)
        return ret

    def mutate_instance(self, inst, cap=5):
        banned_actions = []
        action = self.mutator.select_action()
        ret = self.gen.mutate(inst, action)
        it = 0
        while (ret == None or str(ret) in self.all_solved) and it < cap:
            banned_actions.append(action)
            action = self.mutator.select_action(banned_actions)

            ret = self.gen.mutate(inst, action)
            it += 1
        self.last_mut_success = (ret != None and str(ret) not in self.all_solved)
        if not self.last_mut_success:
            print("Warning, failed to mutate.")
        else:
            ret.solve()
        return ret if self.last_mut_success else self.gen_new_inst()

    def pick(self, pop):
        is_find = False
        for i in range(len(pop)):
            if pop[i].score() >= 10:
                is_find = True
                if not str(pop[i].primaries) in self.all_solved:
                    settings.reg_num += 1
                    utils.generate_file(pop[i].primaries,
                                        settings.reg_path, settings.file_name + str(settings.reg_num) + '.smt2')
                    settings.file_num += 1
                    print('find a case:', pop[i].primaries)
                    df1 = pd.DataFrame(
                        [settings.file_name + str(settings.reg_num) + '.smt2', pop[i].times[settings.solvers[0]],
                         pop[i].times[settings.solvers[1]], pop[i].times[settings.solvers[2]], pop[i].statistics[0], pop[i].statistics[1],
                    pop[i].statistics[2], pop[i].statistics[3]]).T
                    df1.to_csv('./Results.csv', mode='a', header=False)
                    pop[i] = self.gen_new_inst()
                    self.it = 0
                    settings.found_time_list.append(
                        [pop[i].times[settings.solvers[0]], pop[i].times[settings.solvers[1]],
                         pop[i].times[settings.solvers[2]]])
        pop.sort()
        return pop, is_find
    def select_mutate(self, p, keep_num):
        selected = []
        selected.append(p[-1])
        new = p[:-2]
        selected.extend(random.sample(new, keep_num - 1))
        return selected
    def run(self):
        print("Fuzzer Start")
        tried_instances = set()
        pop = []
        # GEN #0
        print("Gen #0", self.start_pop)
        for i in range(self.start_pop):
            pop.append(self.gen_new_inst())
            print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s Reward = %-3f Action = %-10s" % (
                i + 1, self.start_pop, "Initial Pop", utils.roundedmap(pop[i].times, 3), pop[i].score(),
                pop[i].results,
                float('nan'), "NA"))
            # r = self.pick(pop, i)
            # if r == 0:
            #     return
        pop.sort()

        # GEN LOOP
        igen = 0
        while True:
            igen += 1
            print("----------------------------------------------------------------------------------")
            print("Gen #" + str(igen))
            # keep best

            print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s Reward = %-3f Action = %-10s" % (
                1, self.num_pop, "Kept Pop", utils.roundedmap(pop[0].times, 3), pop[0].score(), pop[0].results,
                float('nan'),
                "NA"))
            print('the best:', pop[0].primaries)


            if time.time() - self.time0 > 900:
                df = pd.DataFrame([time.time() - self.init_time, settings.file_num, self.it]).T
                df.to_csv('./Statistics.csv', mode='a', header=False)
                self.time0 = time.time()
            if time.time() - self.init_time > 43200:
                print('finish the bandit')
            self.it += 1
            # mutate
            # for ibest in range(self.num_keep):
            # for imut in range(self.num_mutations):
            #     mutated = self.mutate_instance(pop[0])
            #     pop.append(self.mutate_instance(pop[0]))
            #
            #     if self.last_mut_success:
            #         self.mutator.reward(pop[-1].score() >= pop[0].score())
            #         self.mutator.time_reward(mutated.time_list)
            #     print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s Reward = %-3f Action = %-10s" % (
            #         len(pop), self.num_pop, "", utils.roundedmap(pop[-1].times, 3), pop[-1].score(),
            #         pop[-1].results,
            #         float('nan'), 'NA'))
            ready_to_mutate = self.select_mutate(pop, 2)
            print("ready_to_mutate:", ready_to_mutate)
            for case in ready_to_mutate:
                # for imut in range(self.num_mutations):
                mutated = self.mutate_instance(case)
                pop.append(mutated)
                if self.last_mut_success:
                    self.mutator.reward(mutated.score() >= case.score())
                    # time reward for DTW
                    self.mutator.time_reward(mutated.time_list)
                print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s Reward = %-3f Action = %-10s" % (
                    len(pop), self.num_pop, "", utils.roundedmap(pop[-1].times, 3), pop[-1].score(),
                    pop[-1].results,
                    float('nan'), 'NA'))
                # r = self.pick(pop, -1)
                # if r == 0:
                #     return
            # randomly fill
            pop.sort()
            pop = [pop[-1 - i] for i in range(self.num_keep)]
            while len(pop) < self.num_pop:
                pop.append(self.gen_new_inst())
                print("(%d/%-d)%-15sTimes = %-25s Score = %-7f IsSat = %-25s Reward = %-3f Action = %-10s" % (
                    len(pop), self.num_pop, "Rand", utils.roundedmap(pop[-1].times, 3), pop[-1].score(),
                    pop[-1].results,
                    float('nan'), "NA"))
                # self.pick(pop, -1)
                # r = self.pick(pop, -1)
                # if r == 0:
                #     return
            # if settings.BanditTrainingMode:
            # 	self.mutator.write_model()
            pop, is_find = self.pick(pop)
            if is_find:
                self.mutator.init_mutation()
                settings.op_dict = {}
            # average_time = mean(settings.all_run_time)
            average_time = settings.average_time[0]
            if 20 < self.it <= 30:
                if average_time > 15 and settings.max_str_len > settings.MinStr:

                    settings.max_str_len -= add
                elif settings.max_str_len < settings.MaxStr:
                    add = math.ceil(self.it / math.ceil(average_time))*5
                    if add > 30:
                        add = 30
                    settings.max_str_len += add
                write = pd.DataFrame(
                    [settings.max_str_len,
                     settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
                write.to_csv('./Parameter.csv', mode='a', header=False)
            if 30 <self.it < 40:

                if settings.max_var_num < settings.GeneratorNumConst:
                    add = int(self.it/(math.ceil(average_time)*5))
                    if add > 5:
                        add = 5
                    settings.max_var_num += add
                write = pd.DataFrame(
                    [settings.max_str_len,
                     settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
                write.to_csv('./Parameter.csv', mode='a', header=False)
            elif 40 < self.it < 50:
                if settings.max_assert_num < settings.NumAssert:
                    add = math.ceil(self.it / (math.ceil(average_time) * 100))
                    settings.max_assert_num += add
            elif 50 < self.it < 60:
                if settings.max_depth < settings.GeneratorMaxDepth:
                    add = math.ceil(self.it / (math.ceil(average_time) * 100))
                    settings.max_depth += add
                pop = []
                write = pd.DataFrame(
                    [settings.max_str_len,
                     settings.max_var_num, settings.max_assert_num, settings.max_depth]).T
                write.to_csv('./Parameter.csv', mode='a', header=False)
                for i in range(self.start_pop):
                    pop.append(self.gen_new_inst())




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
                # self.it = 0
