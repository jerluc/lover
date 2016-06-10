lover
=====

A simple [LOVE](https://love2d.org/) game development CLI, for those of us who prefer CLIs over drag-and-drop :)

### Installation

```
go get github.com/jerluc/lover
```

### Usage

```
Usage:
  lover [command]

Available Commands:
  init        Creates a new project in the current directory
   run         Runs the current project

Flags:
  -c, --config string   Configuration file
  -h, --help            help for lover

Use "lover [command] --help" for more information about a command.
```

### Commands

#### `init`

Initializes a brand new LOVE-based project by downloading and extracting the latest LOVE distribution for your platform (or using the specific platforms and versions specified in your [.lover.yaml](#configuration-file)), and creating a simple "Hello, world" `main.lua`.

#### `run`

Runs your current project using your platform-specific LOVE distribution

#### Configuration file

For now, the configuration file (by default this is located in the root of your project directory as `.lover.yaml`) contains the following properties:

* `name` Your project name
* `description` A human-readable description of your project
* `author` Your name
* `license` Source licensing (currently unused, but defaults to "Apache"
* `loveVersion` The version of LOVE required for your project (defaults to "0.10.1")
* `targetPlatforms` A list of each platforms you want to target (must be one of `win32`, `win64`, `osx`, or `linux`)

### Supported platforms

At the moment, lover only supports OS X for automating project setup, but can still be used for actually running your project during development.

### Coming soon

* `init` support for more platforms!
* Prompting for lover configuration inputs (project name, description, etc)
* Autogeneration of a templated `config.lua` file
* Automated distribution/packaging for multiple platforms
* Auto-reloading project on file change
