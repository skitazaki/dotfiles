#!/bin/sh
#/ Usage: setup.sh

set -eu

BASEDIR=$(cd $(dirname $0) && pwd)
BINDIR=$HOME/bin

# Install "oh-my-zsh".
if [ ! -d ~/.oh-my-zsh ]
then
    curl -L http://install.ohmyz.sh | sh || :
    rm ~/.zshrc  # Replace this later.
fi

# Install "dotvim" and "Vundle.vim".
if [ ! -d ~/.vim ]
then
    git clone --recursive git://github.com/dotphiles/dotvim.git ~/.vim
    rm -fr ~/.vim/plugin/settings
fi

[ -f ~/.zshrc ]     || ln -s $BASEDIR/zshrc     ~/.zshrc
[ -f ~/.vimrc ]     || ln -s $BASEDIR/vimrc     ~/.vimrc
[ -f ~/.tmux.conf ] || ln -s $BASEDIR/tmux.conf ~/.tmux.conf
[ -f ~/.psqlrc ]    || ln -s $BASEDIR/psqlrc    ~/.psqlrc
[ -f ~/.gitconfig ] || sed 's:$HOME:'$HOME':' $BASEDIR/gitconfig > ~/.gitconfig
[ -f ~/.git-excludes ] || ln -s $BASEDIR/git-excludes ~/.git-excludes

# Put startup file.
# TODO: Change directory by Linux or MacOSX
# IPYTHON_DIR=$HOME/.ipython
# IPYTHON_STARTUP_DIR=$IPYTHON_DIR/profile_default/startup
# [ -d $IPYTHON_STARTUP_DIR ] || mkdir -p $IPYTHON_STARTUP_DIR
# cp -p $BASEDIR/ipythonstartup $IPYTHON_STARTUP_DIR/00-first.py

#
# Install basic command line binary packages.
#
[ -d $BINDIR ] || mkdir $BINDIR

tool_install () {
    url=$1
    program=$2
    dst=$BINDIR/$program
    curl -o $dst -L $url
    chmod +x $dst
}

# Install direnv
# https://github.com/direnv/direnv/blob/master/docs/installation.md
#curl -sfL https://direnv.net/install.sh | bash

#if [ `uname -s` = "Linux" ]; then
#    tool_install "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64" jq
#elif [ `uname -s` = "Darwin" ]; then
#    tool_install "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-osx-amd64" jq
#    tool_install "https://github.com/harelba/packages-for-q/raw/master/single-binary/Darwin/2.0.9/q" q
#fi
