#!/bin/sh
#/ Usage: setup.sh

set -eu

BASEDIR=$(cd $(dirname $0) && pwd)

# Install "oh-my-zsh".
if [ ! -d ~/.oh-my-zsh ]
then
    curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | sh || :
    rm -f ~/.zshrc  # Replace this later.
fi

[ -f ~/.zshrc ]        || ln -s $BASEDIR/zshrc        ~/.zshrc
[ -f ~/.gitconfig ]    || sed 's:$HOME:'$HOME':' $BASEDIR/gitconfig > ~/.gitconfig
[ -f ~/.git-excludes ] || ln -s $BASEDIR/git-excludes ~/.git-excludes

#
# Install developer tools for the AI era.
#

# Install Homebrew (macOS package manager)
if ! command -v brew > /dev/null 2>&1
then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Git via Xcode Command Line Tools (macOS)
if [ "$(uname -s)" = "Darwin" ] && ! xcode-select -p > /dev/null 2>&1
then
    xcode-select --install
fi

# Install formulae and casks listed in Brewfile.
brew bundle --file="$BASEDIR/Brewfile"
