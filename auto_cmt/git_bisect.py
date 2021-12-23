import utils
import settings
from settings import flag
from math import ceil
import os
from executor import run_command


def goto_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    print('move to path:', path)


def find_dir(path, name):
    for f in os.listdir(path):
        print(f)
        if str(f) == name:
            return True
    return False


class Bisect:
    def __init__(self, cmt_pair):
        # self.pair = cmt_pair
        self.bisect_fault = False
        all_cmts = list(settings.commit_log.keys())
        if cmt_pair[0] not in settings.commits:
            i = all_cmts.index(cmt_pair[0])
            while settings.commit_log[all_cmts[i]] == -1 or all_cmts[i] not in settings.commits:
                i += 1
                if all_cmts[i] == cmt_pair[1]:
                    self.bisect_fault = True
                    break
            cmt_pair[0] = all_cmts[i]
        if cmt_pair[1] not in settings.commits:
            j = all_cmts.index(cmt_pair[1])
            while settings.commit_log[all_cmts[j]] == -1 or all_cmts[j] not in settings.commits:
                j -= 1
                if all_cmts[j] == cmt_pair[0]:
                    self.bisect_fault = True
                    break
            cmt_pair[1] = all_cmts[j]
        self.commits = utils.cut_list_between_items(settings.commits, cmt_pair[0], cmt_pair[1])
        # self.commits = cmt_pair
        # self.former_flag = None
        # self.flag = None
        self.current = None
        self.is_find = False

    # def get_mid(self, pre, post):
    def get_mid(self):
        return ceil((0 + len(self.commits) - 1) / 2), self.commits[ceil((0 + len(self.commits) - 1) / 2)]

    def reset(self, cmt=None):
        os.chdir(settings.init_path)
        if cmt is None:
            cmt = self.current
        rout, rerr, rtime = run_command('git reset --hard {}'.format(cmt))
        print(rout)

        assert rout.find(cmt) != -1, 'the commit crashed! ' + rerr

    def build(self):
        os.chdir(settings.init_path)
        if find_dir(settings.init_path, 'CMakeLists.txt'):
            goto_path(os.path.join(settings.init_path, 'build'))
            out1, err1, _ = run_command('cmake ..')
            out2, err2, _ = run_command('make -j6')
        elif find_dir(settings.init_path, 'configure'):
            out1, err1, _ = run_command('./configure')
            out2, err2, _ = run_command('make -j6')
            goto_path(os.path.join(settings.init_path, 'build'))
        elif find_dir(settings.init_path, 'autogen.sh'):
            os.system('./autogen.sh')
            out1, err1, _ = run_command('./configure')
            out2, err2, _ = run_command('make -j6')
            goto_path(os.path.join(settings.init_path, 'builds'))
        else:
            raise Exception('cannot deal with this version')
        if str(out2).lower().find('error') != -1 or str(err2).lower().find('error') != -1:
            # print('build error:', err2)
            print('build failed!')
            return False
        else:
            print('build success!')
            return True

    def propagate(self):
        pair = [self.commits[0], self.commits[-1]]
        _, self.current = self.get_mid()
        if self.current in pair:
            self.is_find = True
            print('have found the commits!', self.current)
        self.reset()

        print('{} commits left!'.format(str(len(self.commits))))

    def mark(self, flag):
        ind, mid = self.get_mid()
        if flag == flag.good:
            print('marked good')
            self.commits = self.commits[ind:]
        elif flag == flag.bad:
            print('marked bad')
            self.commits = self.commits[:ind + 1]

    def pre_cmt(self, cmt):
        ind = self.commits.index(cmt)
        assert ind - 1 > 0, 'pre ind out of range'
        return self.commits[ind - 1]

    def post_cmt(self, cmt):
        ind = self.commits.index(cmt)
        assert ind + 1 < len(self.commits), 'post ind out of range'
        return self.commits[ind + 1]

    #完犊子，这个方法用不了，暂时舍弃
    def deal_with_run_error(self, case):
        negative_cmt = []
        negative_cmt.append(self.current)
        # 先向后挪动一位
        case.commit = self.post_cmt(self.current)

        ahead = False
        while case.ahead:
            ahead = True
            self.reset(case.commit)
            case.run()
            if case.flag == flag.run_error:
                case.ahead = True
                negative_cmt.append(case.commit)
            else:
                case.ahead = False
            case.commit = self.post_cmt(case.commit)
        if case.flag == flag.good and ahead == True:
            return
        elif case.flag == flag.mid:
            return
        case.commit = self.pre_cmt(self.current)
        while not case.ahead:
            self.reset(case.commit)
            if case.flag == flag.run_error:
                case.ahead = False
                negative_cmt.append(case.commit)
            else:
                case.ahead = True
            case.commit = self.pre_cmt(case.commit)
        return

    def deal_with_build_error(self):
        cmt = self.current
        post = self.post_cmt(cmt)
        settings.commits.remove(self.current)
        self.commits.remove(self.current)
        settings.commit_log[self.current] = -1
        self.current = post
        # is_success = False
        while True:
            cmt = post
            if cmt != self.commits[-1]:
                post = self.post_cmt(post)
            else:
                return
            self.reset(cmt)
            is_success = self.build()
            if is_success:
                break
            else:
                settings.commits.remove(cmt)
                self.commits.remove(cmt)
                settings.commit_log[cmt] = -1

        settings.commit_log[cmt] = 0
        self.current = cmt
