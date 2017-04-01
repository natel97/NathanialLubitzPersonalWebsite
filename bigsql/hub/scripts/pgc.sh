#!/bin/bash

##################################################
####     Copyright (c) 2016-2017 BigSQL       ####
##################################################

start_dir="$PWD"

# resolve links - $0 may be a softlink
this="${BASH_SOURCE-$0}"
common_bin=$(cd -P -- "$(dirname -- "$this")" && pwd -P)
script="$(basename -- "$this")"
this="$common_bin/$script"
# convert relative path to absolute path
config_bin=`dirname "$this"`
script=`basename "$this"`
pgc_home=`cd "$config_bin"; pwd`

export PGC_HOME="$pgc_home"
export PGC_LOGS="$pgc_home/logs/pgcli_log.out"

cd "$PGC_HOME"

hub_new="$PGC_HOME/hub_new"
if [ -d "$hub_new" ];then
  `mv $PGC_HOME/hub_new $PGC_HOME/hub_upgrade`
  log_time=`date +"%Y-%m-%d %H:%M:%S"`
  echo "$log_time [INFO] : completing hub upgrade" >> $PGC_LOGS
  `mv $PGC_HOME/hub $PGC_HOME/hub_old`
  `cp -rf $PGC_HOME/hub_upgrade/* $PGC_HOME/`
  `rm -rf $PGC_HOME/hub_upgrade`
  `rm -rf $PGC_HOME/hub_old`
  log_time=`date +"%Y-%m-%d %H:%M:%S"`
  echo "$log_time [INFO] : hub upgrade completed" >> $PGC_LOGS
fi

declare -a array
array[0]="$PGC_HOME/hub/scripts"
array[1]="$PGC_HOME/hub/scripts/lib"

export PYTHONPATH=$(printf "%s:${PYTHONPATH}" ${array[@]})

pydir="$PGC_HOME/python2"
if [ -d "$pydir" ]; then
  export PATH="$pydir/bin:$PATH"
  if [ `uname` == "Darwin" ]; then
    export DYLD_LIBRARY_PATH="$pydir/lib/python2.7:$DYLD_LIBRARY_PATH"
  else
    export LD_LIBRARY_PATH="$pydir/lib/python2.7:$LD_LIBRARY_PATH"
  fi
fi

python -u "$PGC_HOME/hub/scripts/pgc.py" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9" 
