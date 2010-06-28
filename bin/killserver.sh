#!/bin/sh

PID_DIR=/tmp
RUNSERVER_PID_FILE=$PID_DIR/runserver.pid
CMSSERVER_PID_FILE=$PID_DIR/cmsserver.pid

RUNSERVER_PID=`cat $RUNSERVER_PID_FILE`
CMSSERVER_PID=`cat $CMSSERVER_PID_FILE`

for child in $(ps -o pid,ppid -ax | \
   awk "{ if ( \$2 == $RUNSERVER_PID || \$2 == $CMSSERVER_PID) { print \$1 }}")
do
  echo "Killing child process $child because ppid = $RUNSERVER_PID"
  kill $child
done

rm $RUNSERVER_PID_FILE
rm $CMSSERVER_PID_FILE
