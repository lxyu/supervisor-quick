import fnmatch

from supervisor.supervisorctl import ControllerPluginBase


class QuickControllerPlugin(ControllerPluginBase):
    name = "quick"

    def __init__(self, controller, **config):
        self.ctl = controller

    def _quick_do(self, arg, command):
        assert command in ("start", "stop", "restart")

        supervisor = self.ctl.get_supervisor()
        do = getattr(supervisor, "{}Process".format(command))

        patterns = arg.strip().split()
        if not patterns:
            return self.ctl.output('No process matched given expression.')

        # compatible with group
        patterns = [p + '*' if p.endswith(':') else p for p in patterns]

        # if 'all' pattern exists, match all.
        if "all" in patterns or '*' in patterns:
            patterns = ['*']

        processes = set()
        for p in supervisor.getAllProcessInfo():
            p_name = "{}:{}".format(p["group"], p["name"])
            for pattern in patterns:
                if fnmatch.fnmatch(p_name, pattern):
                    processes.add(p_name)
                    break

        for p in processes:
            # set wait to False to do it quick
            do(p, False)

        # TODO recheck result to make sure it started
        return self.ctl.output("{} quick{}ed".format(arg, command))

    def do_quickstop(self, arg):
        self._quick_do(arg, command='stop')

    def do_quickstart(self, arg):
        self._quick_do(arg, command='start')

    def do_quickrestart(self, arg):
        pass


def make_quick_controllerplugin(controller, **config):
    return QuickControllerPlugin(controller, **config)
