#!/bin/sh

# The MIT License (MIT)
#
# Copyright (c) 2015 Shigeru Kitazaki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#/ Usage: boilterplate.sh
#/
#/ TODO: Write descritption on your own.

set -eu

###############################################################################
### Utility functions

# Thanks to:
# https://github.com/github/backup-utils

# Function to print usage embedded in a script's opening doc comments.
print_usage () {
    grep '^#/' <"$0" | cut -c 4-
    exit ${1:-1}
}

# Check for a "--help" arg and show usage
for a in "$@"; do
    if [ "$a" = "--help" ]; then
        print_usage
    fi
done

###############################################################################
### Configuration

BASEDIR=$(cd $(dirname $0) && pwd)
WORKING_DIR=`pwd`
APPNAME=`basename $0 | cut -d. -f1`
VERSION="0.1.0"
DRIVER=$APPNAME.py
LOG_FILE=$APPNAME-`date +"%Y%m%d%H%M%S"`.log

log () {
    level=$1
    shift
    message=$*
    echo `date +"%Y-%m-%d %H:%M:%S"` "[$level]" $message | tee -a $LOG_FILE
}

cat << EOT | tee -a $LOG_FILE
----------------------------------------------------------------------
Runtime Configuration:
  Base directory     : $BASEDIR
  Working directory  : $WORKING_DIR
  Application        : $APPNAME ($VERSION)
  Log file name      : $LOG_FILE
----------------------------------------------------------------------
EOT

###############################################################################
### Run tasks

log "INFO" Start tasks
log "INFO" Finish tasks

