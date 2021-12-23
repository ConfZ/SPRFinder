import os
import time
import re
import subprocess
import pandas as pd
import settings
import utils
from Case import Case


class check_commits:
    def __init__(self, cmt_cases, tooltype):
        self.cmt_cases = cmt_cases
        self.tooltype = tooltype
        self.path = settings.path[tooltype]
        self.casepath = settings.casepath[tooltype]
        self.cmd = settings.cmd[tooltype]
    def run(self):
        utils.goto_path(settings.path)



        # if tooltype == 'cvc4':
        #     global cvc4_versions
        #     for row in df.itertuples():
        #         if getattr(row, 'CVC4-1.6') < getattr(row, 'CVC4-1.7'):
        #              commits = commit(os.path.join(casepath, getattr(row, 'bencharmks')),
        #                                                                  path,
        #                                                                  tooltype = 'cvc4',
        #                                                                  head=cvc4_versions['cvc4-1.7'],
        #                                                                  tail=cvc4_versions['cvc4-1.6'])
        #              commit.init_run()
        #
        #              if commit.reg() is False:
        #                 continue
        #              self.commits[getattr(row, 'benchmarks')] = commit
        #         elif getattr(row, )
