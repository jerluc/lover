lover
=====

lover is a simple [LÖVE](https://love2d.org/) game development CLI, for
those of us who prefer CLIs over drag-and-drop ;)

Furthermore, lover can be used to manage local development LÖVE binary
installations, and when it comes time to distribute your LÖVE project,
lover can be easily used for packaging your project with the right
version of LÖVE for the platform you are targeting.

### Installation

#### Using pip

```
pip install git+https://github.com/jerluc/lover.git
```

#### From source

```
git clone https://github.com/jerluc/lover.git
cd lover
python setup.py install
```

### Quick start

Once you've followed the [instructions on installing lover](#instructions),
you can create a brand-new "Hello, world!" LÖVE project by running:

```
lover new hello-lover
```

This will create a new LÖVE-based project in a directory called
`hello-lover` configured by the prompted options. Note: this step may
take a few minutes the very first time as it downloads the latest binary
version of LÖVE for your platform. Future invocations of `lover new`
will reuse this same cached binary, however.

Next, to run your new project, simply do:

```bash
# If you weren't already there
cd hello-lover
lover run
```

This should start the application in a new window and display a black
screen with "Hello, world!" written in white.

Lastly, if you just want to show off your cool project to your friends
and family, or if you need to package up your AAA game for release on
Steam, simply do (again within the `hello-lover` directory):

```
lover dist
```

This will create your distributable project files in a new directory
under `dist/{LOVE_VERSION}/{TARGET_PLATFORM}` (e.g.
`dist/0.10.1/darwin-64bit/hello-lover.app` on macOS).

And that's it! You're now ready to start developing your own games with
the LÖVE 2D framework!

### Full usage guide

```
Usage: lover [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  dist  Packages your project for distribution
  new   Creates a new LÖVE project
  run   Runs your project
```

### Commands

#### `new`

Initializes a brand new LÖVE-based project by downloading and extracting
the latest LÖVE distribution for your platform (or using the specific
platforms and versions specified in your
[.lover.yaml](#configuration-file)), and creating a simple "Hello,
world" `main.lua`.

#### `run`

Runs your current project using your platform-specific LÖVE distribution
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
* `loveVersion` The version of LÖVE required for your project (defaults
  to latest)
* `targets` A list of each platform you want to target (must be one of:
  `win-32bit`, `win-64bit`, `darwin-64bit`)

### Supported platforms

At the moment, lover only supports macOS and Windows for automating
project setup, but can still be used for actually running your project
during development.

### Coming soon

* Support for more platforms (see #5 for details)
* Automated distribution/packaging for multiple platforms
* Auto-reloading project on file change
