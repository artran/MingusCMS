#!/bin/sh

PID_DIR=/tmp
RUNSERVER_PID=$PID_DIR/runserver.pid
CMSSERVER_PID=$PID_DIR/cmsserver.pid

kill -TERM `cat $RUNSERVER_PID`
kill -TERM `cat $CMSSERVER_PID`

rm $RUNSERVER_PID
rm $CMSSERVER_PID
