lover
=====

A simple [LOVE](https://love2d.org/) game development CLI, for those of
us who prefer CLIs over drag-and-drop :)

### Installation

```
pip install git+git://github.com/jerluc/lover.git
```

### Usage

```
Usage: lover [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  dist  Packages your project for distribution
  new   Creates a new LOVE project
  run   Runs your project
```

### Commands

#### `new`

Initializes a brand new LOVE-based project by downloading and extracting
the latest LOVE distribution for your platform (or using the specific
platforms and versions specified in your
[.lover.yaml](#configuration-file)), and creating a simple "Hello,
world" `main.lua`.

#### `run`

Runs your current project using your platform-specific LOVE distribution
and the version configured in your [.lover.yaml](#configuration-file).

#### `dist`

Packages your current project into a distributable binary package for
the platforms specified in your [.lover.yaml](#configuration-file).

Note that this only supports macOS packaging at the moment.

#### Configuration file

For now, the configuration file (by default this is located in the root
of your project directory as `.lover.yaml`) contains the following
properties:

* `name` Your project name
* `description` A human-readable description of your project
* `author` Your name
* `loveVersion` The version of LOVE required for your project (defaults
  to latest)
* `targets` A list of each platform you want to target (must be one of:
  `win-32bit`, `win-64bit`, `darwin-64bit`)

### Supported platforms

At the moment, lover only supports macOS and Windows for automating
project setup, but can still be used for actually running your project
during development.

### Coming soon

* Support for more platforms (Linux!)
* Automated distribution/packaging for multiple platforms
* Auto-reloading project on file change
