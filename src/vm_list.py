import commands
import sys
from time import gmtime, strftime
from collections import namedtuple
from workflow import Workflow

parallels_available = commands.getstatusoutput('which prlctl')[1]

try:
    from vboxapi import VirtualBoxManager
    from vboxapi.VirtualBox_constants import VirtualBoxReflectionInfo
    mgr = VirtualBoxManager(None, None)
    vbox = mgr.vbox
    constants = VirtualBoxReflectionInfo(False)
    vbox_available = True
except ImportError:
    vbox_available = False

VMDetails = namedtuple('VMDetails', ['name', 'id', 'state', 'type'])


def complete(wf):
    vm_name = ' '.join(wf.args)

    vm_list = get_vm_list()
    if any(x.name == vm_name for x in vm_list):
        vm_details = None
        for vm in vm_list:
            if vm.name == vm_name:
                vm_details = vm
                break

        if vm_details:
            vm_name = '"' + vm_name + '"'
            # Parallels
            if vm_details.state == "stopped":
                wf.add_item(
                    'Start', arg='start ' + vm_name,
                    uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            elif vm_details.state == "paused":
                for action in ['Resume', 'Stop', 'Pause', 'Reset', 'Suspend']:
                    wf.add_item(
                        action, arg=action.lower() + ' ' + vm_name,
                        uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            elif vm_details.state == "suspended":
                for action in ['Resume']:
                    wf.add_item(
                        action, arg=action.lower() + ' ' + vm_name,
                        uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            elif vm_details.state == "running":
                for action in ['Stop', 'Pause', 'Reset', 'Suspend', 'Restart']:
                    wf.add_item(
                        action, arg=action.lower() + ' ' + vm_name,
                        uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

                filename = "Screenshot\ " + \
                    strftime("%Y-%m-%d\ %H.%M.%S\ %p", gmtime()) + ".png"
                wf.add_item(
                    "Capture screenshot", "Saves a screenshot to Desktop", arg='capture ' + vm_name + ' --file ~/Desktop/' + filename,
                    uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            # Virtual Box
            elif vm_details.state in ["PoweredOff", "Saved"]:
                wf.add_item(
                    'Start', arg=vm_name + ' start',
                    uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            elif vm_details.state == "Paused":
                for action in ['Resume', 'PowerOff', 'SaveState']:
                    wf.add_item(
                        action, arg=vm_name + ' ' + action.lower(),
                        uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

            elif vm_details.state == "Running":
                for action in ['PowerOff', 'Pause', 'Reset', 'SaveState', 'ACPIPowerButton', 'ACPISleepButton']:
                    wf.add_item(
                        action, arg=vm_name + ' ' + action.lower(),
                        uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')

                filename = "Screenshot\ " + \
                    strftime("%Y-%m-%d\ %H.%M.%S\ %p", gmtime()) + ".png"
                wf.add_item(
                    "Capture screenshot", "Saves a screenshot to Desktop", arg=vm_name + ' screenshotpng ~/Desktop/' + filename,
                    uid=vm_name, valid=True, icon=vm_details.type, icontype='fileicon')
    else:
        for vm in vm_list:
            wf.add_item(vm.name, vm.state, uid=vm.id,
                        autocomplete=vm.name, valid=False, icon=vm.type, icontype='fileicon')

    wf.send_feedback()


def get_vm_list():
    output = []

    if parallels_available:
        for line in commands.getstatusoutput('prlctl list -a --no-header')[1].split('\n'):
            vm_details = line.split()
            status = vm_details[1]
            vm_id = vm_details[0]
            name = ' '.join(vm_details[3:])
            output.append(
                VMDetails(name, vm_id, status, '/Applications/Parallels Desktop.app'))

    if vbox_available:
        for m in mgr.getArray(vbox, 'machines'):
            output.append(VMDetails(
                m.name, m.id, get_vm_state(m.state), '/Applications/VirtualBox.app'))

    return output


def get_vm_state(state_const):
    for state, constant in constants.all_values('MachineState').iteritems():
        if constant == state_const:
            return state
    return None

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(complete))
