import sys
import os
import time
from workflow import Workflow


def execute(wf):
    query = ' '.join(wf.args)
    if query != "":
        if query[0] == '"':
            # Virtual Box
            command = query.split('"')[2].split(' ')[1]
            if query[-5:] == "start":
                os.popen('/usr/local/bin/VBoxManage startvm %s' % query[:-6])
            elif command in ['poweroff', 'pause', 'reset', 'suspend', 'savestate', 'acpipowerbutton', 'acpisleepbutton', 'screenshotpng']:
                if command in ['poweroff', 'reset', 'suspend']:
                    wf.clear_cache()
                os.popen('/usr/local/bin/VBoxManage controlvm %s' % query)
        elif len(query.split()) > 1:
            # Parallels
            command = query.split()[0]
            if command in ['stop', 'reset', 'suspend']:
                wf.clear_cache()
            os.popen('/usr/local/bin/prlctl %s' % query)

            if command in ['start', 'resume']:
                os.popen(
                    """ osascript -e 'activate application "/Applications/Parallels Desktop.app"' """)
                return

            # wait and then quit Parallels if possible
            time.sleep(2)
            if len(os.popen('/usr/local/bin/prlctl list --no-header').readlines()) == 0:
                os.popen(
                    """ osascript -e 'tell application "Parallels Desktop" to quit' """)


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(execute))
