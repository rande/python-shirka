Shirka @ Ekino
--------------

Shirka is a bot written in python, the main usage is to react to command send on different channels. A channel can be a flowdock, a irc chan or anything where input text can be posted.

Setup
-----
 
    # create a new virtualenv
    virtualenv shirka 
    cd shirka
    source bin/activate

    # retrieve code source
    git clone git@git.myserver.com:repository.git src

    # install dependencies under the shirka virtual env
    cd src
    pip install -r pip_requirements.txt --upgrade

    python start.py shirka:start


Monitoring
----------

it is better to run the bot under a process management control like supervisord.

    apt-get install supervisord

    vim /etc/supervisor/conf.d/shirka.conf

    # add the following line into the /etc/supervisor/conf.d/shirka.conf file:

        [program:shirka]
        command=/home/MYUSER/shirka/bin/python /home/MYUSER/shirka/src/start.py -e odysseus
        process_name=%(program_name)s
        numprocs=1
        directory=/home/MYUSER/shirka/src
        autostart=true
        autorestart=true
        startsecs=10
        startretries=3
        user=MYUSER

    /etc/init.d/supervisord stop
    /etc/init.d/supervisord start

    # please not the restart command does not work

Reference
---------

- Shirka: https://github.com/rande/python-shirka