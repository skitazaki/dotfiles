# .bashrc

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific aliases and functions
[ -f ~/.bash_aliases ] && . ~/.bash_aliases
[ -f /etc/bash_completion ] && . /etc/bash_completion

alias ls="ls -FG"
alias ll="ls -l"
alias la="ls -A"
alias man="man -a"
alias grep="grep --color"
alias df="df -H"

alias p="pushd"
alias po="popd"

export LANG="en_US.UTF-8"
export SVN_EDITOR="vim"
export GIT_EDITOR="vim"

# http://www.ibm.com/developerworks/aix/library/au-spunixpower.html
#export LESS='--LINE-NUMBERS --quit-if-one-screen --quit-on-intr'
export HISTCONTROL=ignoreboth
export HISTIGNORE="&:ls:ll:la:l.:pwd:exit:clear"
shopt -s histappend
shopt -s cdspell

# since bash 4.x
#shopt -s autocd

# Python specific settings
[ -f $HOME/.pythonstartup ] && export PYTHONSTARTUP=$HOME/.pythonstartup
export VIRTUALENV_USE_DISTRIBUTE="true"

# Put these files on your own.
GIT_PROMPT=/usr/local/etc/bash_completion.d/git-prompt.sh
GIT_COMPLETION=/usr/local/etc/bash_completion.d/git-completion.bash

if [ -f $GIT_PROMPT -a -f $GIT_COMPLETION ]
then
    source $GIT_PROMPT
    source $GIT_COMPLETION
    PS1="\n\e[1;4;33m\u \w\e[m\e[1;2;31m\$(__git_ps1)\e[m [\#] @\h\n\$ "
else
    PS1="\n\e[1;4;33m\u \w\e[m [\#] @\h\n\$ "
fi

PS2="\e[31m> \e[m"

# SSH passphrase manager, thanks github help.
# http://help.github.com/working-with-key-passphrases/
SSH_ENV="$HOME/.ssh/environment"

# http://dev.mysql.com/doc/refman/5.1/en/mysql-commands.html
export MYSQL_PS1="mysql://\u@\h:/\d - \R:\m:\s > "

# start the ssh-agent
function start_agent {
    echo "Initializing new SSH agent..."
    # spawn ssh-agent
    ssh-agent | sed 's/^echo/#echo/' > "$SSH_ENV"
    echo succeeded
    chmod 600 "$SSH_ENV"
    . "$SSH_ENV" > /dev/null
    ssh-add
}

# test for identities
function test_identities {
    # test whether standard identities have been added to the agent already
    ssh-add -l | grep "The agent has no identities" > /dev/null
    if [ $? -eq 0 ]; then
        ssh-add
        # $SSH_AUTH_SOCK broken so we start a new proper agent
        if [ $? -eq 2 ];then
            start_agent
        fi
    fi
}

# check for running ssh-agent with proper $SSH_AGENT_PID
if [ -n "$SSH_AGENT_PID" ]; then
    ps -ef | grep "$SSH_AGENT_PID" | grep ssh-agent > /dev/null
    if [ $? -eq 0 ]; then
    test_identities
    fi
# if $SSH_AGENT_PID is not properly set, we might be able to load one from
# $SSH_ENV
else
    if [ -f "$SSH_ENV" ]; then
    . "$SSH_ENV" > /dev/null
    fi
   ps -ef | grep "$SSH_AGENT_PID" | grep ssh-agent > /dev/null
    if [ $? -eq 0 ]; then
        test_identities
    else
        start_agent
    fi
fi

# misc pipeline procedure
alias order="sort |uniq -c |sort -nr"
alias historder="history |cut -c8- |cut -d\" \" -f1 |order"
alias itemize="sed 's/^/ - /'"

# misc procedure with several argument

function search()
{
    ignore_list="svn swp tags o lo a exe git"
    if [ -n "$@" ]; then
        arg="-type f -wholename *~ -prune"
        for item in $ignore_list; do
            arg=$arg" -o -wholename *."$item" -prune"
        done
        find . $arg -o -print |xargs grep $@
    else
        echo "Usage: search search_word"
    fi
}
export search

ex () {
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1        ;;
      *.tar.gz)    tar xzf $1     ;;
      *.bz2)       bunzip2 $1       ;;
      *.rar)       rar x $1     ;;
      *.gz)        gunzip $1     ;;
      *.tar)       tar xf $1        ;;
      *.tbz2)      tar xjf $1      ;;
      *.tgz)       tar xzf $1       ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1  ;;
      *.7z)        7z x $1    ;;
      *)           echo "'$1' cannot be extracted via extract()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}
export ex

function cleanup()
{
    if [ -f ~/Makefile ]
    then
        make -f ~/Makefile clean
    else
        rm -f *~ *.pyc
    fi
}
export cleanup

# added by travis gem
[ -f /Users/shigeru/.travis/travis.sh ] && source /Users/shigeru/.travis/travis.sh
eval "$(direnv hook $0)"

