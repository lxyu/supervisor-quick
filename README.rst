Supervisor-Quick
================

Bypass supervisor's nasty callbacks stack and make it quick!


Usage
-----

.. code:: bash

    $ pip install supervisor-quick

And add the following config to `supervisord.conf`.

.. code:: ini

    [ctlplugin:quick]
    supervisor.ctl_factory = supervisor_quick:make_quick_controllerplugin

Then start `supervisorctl` and use `quickstart`, `quickstop` and
`quickrestart` to start/stop/restart processes.

.. code::

    > quickstart app:0
    > quickstart app:
    > quickstart ap*
    > quickstart all

    > quickstop app:1
    > quickstop app:
    > quickstop ap*
    > quickstop all

    > quickrestart app:2
    > quickrestart app:
    > quickrestart ap*
    > quickrestart all

It effects `supervisorctl`, so you don't have to restart the whole
supervisord to make it work.


Why
---

I write this plugin because supervisor is just tooooo slow in
start/stop/restart app server in our prod servers.

And I checked the source code and found it is because of the
nasty callbacks stack, and this is a quote from source code
`supervisor/rpcinterface.py`::

    # XXX the above implementation has a weakness inasmuch as the
    # first call into each individual process callback will always
    # return NOT_DONE_YET, so they need to be called twice. The
    # symptom of this is that calling this method causes the
    # client to block for much longer than it actually requires to
    # kill all of the running processes. After the first call to
    # the killit callback, the process is actually dead, but the
    # above killall method processes the callbacks one at a time
    # during the select loop, which, because there is no output
    # from child processes after e.g. stopAllProcesses is called,
    # is not busy, so hits the timeout for each callback. I
    # attempted to make this better, but the only way to make it
    # better assumes totally synchronous reaping of child
    # processes, which requires infrastructure changes to
    # supervisord that are scary at the moment as it could take a
    # while to pin down all of the platform differences and might
    # require a C extension to the Python signal module to allow
    # the setting of ignore flags to signals.

And this plugin will do a `quick` start/stop/restart action that bypass
all the callback checks, making it lightning fast.

It also have wildcard concurrent execution support, keeping it fast
regardless of processes amount. (This function is inspired by
`supervisor-wildcards <https://github.com/aleszoulek/supervisor-wildcards>`_)


Example
-------

An example time demo for a app server with numprocs set to 32 to show how quick
supervisor can be with `quick` command.

.. code:: bash

    $ supervisorctl status
    app:0                            STOPPED
    app:1                            STOPPED
    app:10                           STOPPED
    ......
    app:7                            STOPPED
    app:8                            STOPPED
    app:9                            STOPPED

    $ time supervisorctl start app:
    24: started
    25: started
    26: started
    ......
    18: started
    31: started
    30: started
    supervisorctl start app:  0.06s user 0.02s system 0% cpu 48.442 total

    $ time supervisorctl stop app:
    24: stopped
    25: stopped
    26: stopped
    ......
    18: stopped
    31: stopped
    30: stopped
    supervisorctl stop app:  0.06s user 0.03s system 0% cpu 36.278 total

    $ time supervisorctl quickstart app:
    app:25: started
    app:24: started
    app:27: started
    ......
    app:1: started
    app:8: started
    app:9: started
    supervisorctl quickstart app:  0.09s user 0.03s system 19% cpu 0.618 total

    $ time supervisorctl quickstop app:
    app:26: stoped
    app:27: stoped
    app:22: stoped
    ......
    app:0: stoped
    app:9: stoped
    app:8: stoped
    supervisorctl quickstop app:  0.09s user 0.04s system 68% cpu 0.196 total
