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
- [ripgrep](https://github.com/BurntSushi/ripgrep) via Homebrew Bundle for fast recursive search with `rg`
- [Task](https://taskfile.dev/) via Homebrew Bundle for running tasks from [Taskfile.yml](Taskfile.yml)
- `zsh-syntax-highlighting` via Homebrew Bundle
- [GitHub Copilot CLI](https://github.com/github/copilot-cli) via Homebrew Cask in Bundle
- [Codex](https://developers.openai.com/codex/) via Homebrew Cask in Bundle
- Git via Xcode Command Line Tools

Homebrew-managed software is defined in [Brewfile](Brewfile) and installed with:

```sh
brew bundle --file=Brewfile
```

Common project commands are defined in [Taskfile.yml](Taskfile.yml) and run with `task`.

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

Useful local search command once the bundle is installed:

```sh
rg "TODO" .
```
