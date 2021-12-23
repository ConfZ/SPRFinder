import os
def roundedmap(val, precision=3):
    ret = "{"
    for key in val:
        ret += "\'" + key + "\'" + ' : ' + str(round(val[key], precision)) + ","
    ret = ret[0:len(ret) - 1]
    ret += "}"
    return ret
def generate_file(ast, path, name):
    if not os.path.exists(path):
        os.mkdir(path)
    file = open(os.path.join(path, name), 'w+')
    file.write(ast)
    file.close()