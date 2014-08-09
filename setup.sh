#!/bin/sh

BASEDIR=`cd $(dirname $0) && pwd`
FILES=(
    tmux.conf
    vimrc
    zshrc
)

# Install "oh-my-zsh".
if [ ! -d ~/.oh-my-zsh ]
then
    curl -L http://install.ohmyz.sh | sh
    rm ~/.zshrc  # Replace this later.
fi

# Install "dotvim" and "Vundle.vim".
if [ ! -d ~/.vim ]
then
    git clone --recursive git://github.com/dotphiles/dotvim.git ~/.vim
    rm -fr ~/.vim/plugin/settings
fi

for file in ${FILES[@]}
do
    [ -f ~/.$file ] || ln -s $BASEDIR/$file ~/.$file
done

# Put startup file.
# TODO: Change directory by Linux or MacOSX
IPYTHON_DIR=$HOME/.ipython
IPYTHON_STARTUP_DIR=$IPYTHON_DIR/profile_default/startup
[ -d $IPYTHON_STARTUP_DIR ] || mkdir -p $IPYTHON_STARTUP_DIR
cp -p $BASEDIR/ipythonstartup $IPYTHON_STARTUP_DIR/00-first.py

