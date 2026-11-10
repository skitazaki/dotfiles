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

- [VS Code](https://code.visualstudio.com/) via Homebrew Cask in Bundle, with machine-wide settings linked from the repo under `vscode/User/`
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) via Homebrew Cask in Bundle
- [iTerm2](https://iterm2.com/) via Homebrew Cask in Bundle
- [ripgrep](https://github.com/BurntSushi/ripgrep) via Homebrew Bundle for fast recursive search with `rg`
- [Task](https://taskfile.dev/) via Homebrew Bundle for running tasks from [Taskfile.yml](Taskfile.yml)
- `zsh-syntax-highlighting` via Homebrew Bundle
- [GitHub Copilot CLI](https://github.com/github/copilot-cli) via Homebrew Cask in Bundle
- [Codex](https://developers.openai.com/codex/) via Homebrew Cask in Bundle
- [Claude Code](https://www.anthropic.com/claude-code) via Homebrew Cask in Bundle
- [Pi Coding Agent](https://pi.dev/) via Homebrew Bundle
- [Ollama](https://ollama.ai/) via Homebrew Bundle for running large language models locally
- Git via Xcode Command Line Tools

Homebrew-managed software is defined in [Brewfile](Brewfile) and installed with:

```sh
brew bundle --file=Brewfile
```

Common project commands are defined in [Taskfile.yml](Taskfile.yml) and run with `task`.

## Launch Agents through Ollama

After setup, you can launch Claude Code and Pi coding agents with Ollama integration:

### Claude Code

Launch Claude Code with Ollama with interactive model selection:

```sh
ollama launch claude
```

Or launch with a specific model in non-interactive mode (useful for scripts/CI):

```sh
ollama launch claude --model qwen3.5:cloud --yes -- -p "your prompt here"
```

See [Claude Code integration docs](https://docs.ollama.com/integrations/claude-code) for more options including web search and scheduled tasks.

### Pi Coding Agent

Launch Pi coding agent with Ollama:

```sh
ollama launch pi
```

Or launch Pi with a specific model:

```sh
ollama launch pi --model qwen3.5:cloud
```

Configure Ollama without launching:

```sh
ollama launch pi --config
```

See [Pi integration docs](https://docs.ollama.com/integrations/pi) for more features like extensions and autoresearch.

## Maintenance

Update Homebrew-managed software with:

```sh
brew bundle --file=Brewfile
```

Export currently installed formulae/casks:

```sh
brew bundle dump --force --file=Brewfile
```

Uninstall packages not listed in Brewfile:

```sh
brew bundle cleanup --file=Brewfile --force
```

Search for TODOs in the repository:

```sh
rg "TODO" .
```
