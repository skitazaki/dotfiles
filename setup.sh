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

# Install Go
if ! command -v go > /dev/null 2>&1
then
    brew install go
fi

# Install Node via nvm
if [ ! -d "$HOME/.nvm" ]
then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
fi

# Install Python toolchain via uv
if ! command -v uv > /dev/null 2>&1
then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install GitHub CLI (for GitHub Copilot CLI)
if ! command -v gh > /dev/null 2>&1
then
    brew install gh
fi

# Install GitHub Copilot CLI extension
if command -v gh > /dev/null 2>&1
then
    if gh extension list 2>/dev/null | grep -q 'gh-copilot'
    then
        gh extension upgrade gh-copilot 2>/dev/null || true
    else
        gh extension install github/gh-copilot 2>/dev/null || true
    fi
fi

# Install VS Code
if [ "$(uname -s)" = "Darwin" ] && ! command -v code > /dev/null 2>&1
then
    brew install --cask visual-studio-code
fi

# Install Docker Desktop
if [ "$(uname -s)" = "Darwin" ] && ! command -v docker > /dev/null 2>&1
then
    brew install --cask docker
fi
