# dotfiles

Setup `zsh` using [Oh My Zsh](https://ohmyz.sh/) and put config files for `git`.

## Prerequisites

- macOS with [Xcode Command Line Tools](https://developer.apple.com/xcode/) for Git
- [Homebrew](https://brew.sh/)
- `curl`

## Setup

```sh
./setup.sh
```

This will install and configure:

### Programming Languages

- [Go](https://golang.org/) via Homebrew Bundle
- [Python](https://www.python.org/) via [uv](https://docs.astral.sh/uv/) in Homebrew Bundle
- [Node.js](https://nodejs.org/) via [fnm](https://github.com/Schniz/fnm) in Homebrew Bundle

### Developer Tools

- [VS Code](https://code.visualstudio.com/) via Homebrew Cask in Bundle
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) via Homebrew Cask in Bundle
- [iTerm2](https://iterm2.com/) via Homebrew Cask in Bundle
- `zsh-syntax-highlighting` via Homebrew Bundle
- [GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli) via `gh` extension
- Git via Xcode Command Line Tools

Homebrew-managed software is defined in [Brewfile](Brewfile) and installed with:

```sh
brew bundle --file=Brewfile
```

## Maintenance

Common commands for keeping your bundle up to date:

```sh
# Add or remove packages in Brewfile, then apply changes
brew bundle --file=Brewfile

# Export currently installed formulae/casks into Brewfile
brew bundle dump --force --file=Brewfile

# Uninstall packages not listed in Brewfile
brew bundle cleanup --file=Brewfile --force
```
