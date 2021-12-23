import os
import re
import settings
# import math

FIND_CMT = re.compile(r'.*\[(?P<COMMIT>\w*)\].*')
FIND_TAR = re.compile(r'(?P<TAR>\w*) is the first bad commit')

def pair2key(pair):
    return  ','.join(pair)
def key2pair(key):
    return key.split(',')
def cut_list_between_items(orgin_list, pre, post):
    ind_pre = orgin_list.index(pre)
    ind_post = orgin_list.index(post)
    print(ind_pre, ind_post)
    return orgin_list[ind_pre: ind_post+1]


def iter_path(path):
    file_names = [os.path.join(fpath, fname)
                  for fpath, _, file_list in os.walk(path)
                  for fname in file_list if fname.endswith('.smt2')]
    return file_names
# def get_mid(pair):
#     cmt_index1 = settings.commits.index(pair[0])
#     cmt_index2 = settings.commits.index(pair[1])
#     return settings.commits[math.ceil((cmt_index1+cmt_index2)/2)]

def goto_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    print('move to path:', path)


def cmake_make(path):
    os.chdir(os.path.join(path, 'build'))
    os.system('cmake ..')
    os.system('make -j5')


def find_cmt(rst):
    try:
        target = re.search(FIND_CMT, rst).group('COMMIT')
    except AttributeError:
        target = None
    return target


def find_tar(rst):
    try:
        target = re.match(FIND_TAR, rst).group('TAR')
    except AttributeError:
        target = None
    return target
