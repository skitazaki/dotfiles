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

# Link machine-wide VS Code settings from the dotfiles repo.
link_or_replace() {
    src="$1"
    dst="$2"

    if [ -L "$dst" ]; then
        return 0
    fi

    if [ -e "$dst" ]; then
        mv "$dst" "$dst.bak"
    fi

    ln -s "$src" "$dst"
}

for vscode_user in "$HOME/Library/Application Support/Code/User" "$HOME/Library/Application Support/Code - Insiders/User"; do
    [ -d "$vscode_user" ] || mkdir -p "$vscode_user"
    link_or_replace "$BASEDIR/vscode/User/settings.json" "$vscode_user/settings.json"
    link_or_replace "$BASEDIR/vscode/User/github-copilot-worktree-policy.md" "$vscode_user/github-copilot-worktree-policy.md"
done

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
