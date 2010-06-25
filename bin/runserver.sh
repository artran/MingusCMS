#! /bin/sh

PID_DIR=/tmp
RUNSERVER_PID=$PID_DIR/runserver.pid
CMSSERVER_PID=$PID_DIR/cmsserver.pid

if [ -z $VIRTUAL_ENV ];
    then {
        echo "You need to setup the virtual environment first"
        exit 1
    };
fi

if [ -f $RUNSERVER_PID ] || [ -f $CMSSERVER_PID ];
    then {
        echo "Already running"
        exit 2
    };
fi

django-admin.py runserver 127.0.0.1:8000 &
echo $! > $RUNSERVER_PID # This is the wrong PID - need the child PID.

TEST_SERVER=True django-admin.py runserver 127.0.0.1:8001 &
echo $! > $CMSSERVER_PID # This is the wrong PID - need the child PID.
