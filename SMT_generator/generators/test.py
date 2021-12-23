import bin.myGenerators as my
import SMT_generator.ast as sast
import bin.globalVal as g
from bin.utils import check_lit_position
import bin.utils as u
def list_match(var1, var2):
    list1 = var1
    list2 = var2
    i = 0
    list3 = []
    index = []
    while i < len(list1):
        j = 0
        p = i
        while j < len(list2) and p < len(list1):
            tmp = []
            ind = []

            if list1[p] == list2[j]:
                ind = [p, j]
            while list1[p] == list2[j]:
                tmp.append(list1[p])
                p += 1
                j += 1
                if p >= len(list1) or j >= len(list2):
                    break
            if len(list3) < len(tmp):
                list3 = tmp
                index = ind
            j += 1
        i += 1
    return list3, index


def check_lit_position(lit, int_var):
    lit_len = [len(v) for v in lit]
    length = 0
    for i in range(len(lit_len)):
        length += lit_len[i]
        if length > int_var:
            return i
    return -1





if __name__ == "__main__":
    my.make_assemble_Str(3)
    # expr, model = my.index_termination()
    # print('expr:', expr)
    # print('del:', model)
    # a = {'Id<var0>': ['lit3', 'lit1'], 'Id<var1>': ['lit3', 'lit0', 'lit0'], 'Id<var2>': ['lit2'], 'Id<var3>': ['lit3', 'lit2', 'lit0', 'lit3'], 'Id<var4>': ['lit0', 'lit0'], 'Id<var5>': ['lit0'], 'Id<var7>': ['lit1', 'lit2', 'lit0', 'lit2'], 'Id<var8>': ['lit2'], 'Id<var9>': ['lit2'], 'Id<var10>': 'lit2', 'Id<var11>': ['lit1', 'lit1', 'lit0']}
    # c = my.make_var_pairs(1, sort=sast.STRING_SORT)
    # print(g.var_assem_dict)
    a = "iA61UZw0PITrx86EzhxXIe60HjsBhilfMF7ny8V7vI4Rz7EGswhp4WlW2bM80079eheA5ExtjSs10eJaPwHrVftpybaybg9RjhbnT1cP10f6WJUhLdN532vyjZBe82bXrT1ed7tPNm8BVWKzZ6R8Uk4yfenKi5MdZhFn7EAqL0BsF0W9X7hsLeyu75e4n1hyKrT1nDfR3jNDd2AgKbJuT9V08pd21UDmZ1zFFwPTBMsRY1M4q2F5tM09XcJpzxeyIOSaQNv6hXY4"
    print(len(a))
