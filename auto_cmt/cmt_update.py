import os
def update_git_log(path):
    os.chdir(path)
    os.system('git pull')
    os.system('git log --pretty=format:\'%h\' > ../log.log')

if __name__ == '__main__':
    update_git_log('./z3')