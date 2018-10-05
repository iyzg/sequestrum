# Sequestrum
## Description
A modern, lightweight, easy to use dotfile manager for the masses that provides modularity, dotfile repository setup, and more.

## Install Guide
1. `sudo pip install (--user) sequestrum`
2. Leave a star on this repo
3. Enjoy!

## Usage
### Getting Started
You'll need to create a Sequestrum configuration in your dotfiles so that the program knows how to properly handle your dotfiles.
Refer to **Config Guide** to for information on configuration, or **Example Config** for an example of the configuration/

**Note:** Your dotfiles should be empty of configuration files to prevent duplicates, unless this is the intention. Never edit
your configuration when you have packages installed. Unlink before editing configuration files to prevent file loss.

Once your configuration file is setup correctly, run `sequestrum --setup` to finish setting up your dotfiles. If something goes
wrong, ensure that your configuration is correct. Run `sequestrum --install` afterwards to create symbolic links of your dotfiles
to your system. Setup will delete all local system files and move them to the dotfile repository.

### Example Config
Here is an example of a finished config file.

```
options:
    base: &base
        dotfileDirectory: .dotfiles
    
    vimPackage:
        directoryName: vim
        commandsBefore:
            - ufetch
        links:
            - vimrc: .vimrc
            - vim-plugins: .vim/plugins
        commandsAfter:
            - ls

```

### Config Guide
Configuration is done with YAML. If you are not familiar with YAML syntax, it would be in your best interest to get
at least a basic understanding of the syntax.

The name of your configuration file should be **config.yaml** and should be placed in your dotfiles, or anywhere as long as the
directory is specified in the `dotfileDirectory` variable in the configuration.

All configuration files begin with `options:`, which is a parent to `base`. For each set of files you wish to package you'll need a
separate package declaration (view **directories** for information on package declarations). Refer to the example configuration if needed.

#### Directories
Each set of links you want grouped require their own package. Packages can be named anything you would like so long as they're suffixed
with the word "Package" (e.g. vimPackage or binPackage). Each package must include the directory name and links. Links are all of the
files that will be linked to the package. Each link is listed in an array with the key as the link name, and the value being the path
to the link.

### Installing
To install dotfiles, simply run `sequestrem --install <package>`. Make sure that the directory specified by the package doesn't exist at
the time of running the installation command. You can use `all` as a keyword in place of the package name in the installation command
to install all dotfiles.

#### Additonal Options
In addition to the required options for packages, you may also use `commandsBefore` and `commandsAfter` keys, which specify a list
of commands that are to be run before and after (respectively )symbolic links are created.

Additional options will be added in the future, and suggestions for additional options are open (be sure to leave a feature request).

### List of Arguments

|Short|Long|Description|
|-|-|-|
|-s|--setup|Sets up your dotfile repository|
|-i|--install|Installs your dotfiles to the system|
|-i|--unlink|Unlinks a package from your system|
|-d|--delete|Deletes a repository|
|-r|--refresh|Refreshes dotfiles based on the loaded configuration|
|-b|--backup|Backs up your system configuration|

## TODOS
- [ ] Dual way safety checks for install and setup
- [ ] Add support for more directories than home
- [ ] Colors!!!
- [ ] Verbose Mode
- [ ] Pep8ify

## Contributing
If you'd like to contribute, whether that'd be improving the comments or README (which could always use work), or adding functionality,
just fork this, add to it, then send a merge request. I'll try and get around to looking at it as soon as possible.
Be sure to read [CONTRIBUTING.md](CONTRIBUTING.md) first though.

## License
Copyright (c) 2018-2018 Ivy Zhang. Released under the MIT License.
