#!/bin/sh

BASEDIR=`cd $(dirname $0) && pwd`
FILES=(
    tmux.conf
    vimrc
    zshrc
)

for file in ${FILES[@]}
do
    [ -f ~/.$file ] || ln -s $BASEDIR/$file ~/.$file
done

# Install "oh-my-zsh".
[ -d ~/.oh-my-zsh ] || curl -L http://install.ohmyz.sh | sh

