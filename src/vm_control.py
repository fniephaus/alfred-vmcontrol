import sys
import os
import subprocess
import commands
from workflow import Workflow


def execute(wf):
    query = ' '.join(wf.args)
    if query != "":
        if query[0] == '"':
            # Virtual Box
            command = query.split('"')[2].split(' ')[1]
            if query[-5:] == "start":
                os.system('VBoxManage startvm %s &' % query[:-6])
            elif command in ['poweroff', 'pause', 'reset', 'suspend', 'savestate', 'acpipowerbutton', 'acpisleepbutton', 'screenshotpng']:
                os.system('VBoxManage controlvm %s &' % query)
        elif len(query.split(' ')) > 1:
            # Parallels
            os.system('prlctl %s &' % query)


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(execute))
