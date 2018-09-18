# Sequestrum
## Description
A modern, lightweight dotfile manager for the masses. This README.md may look daunting, but trust me on this, it's easy as pie.
Promise. Now you may be wondering, why use this over Stow or Dotbot. Simple.Well for starters, the name is better. Do you need any
other reasons? Fine, fine.. some real reasons.This is specifically made for dotfile management and provides features like modulatarity, 
dotfile repository setup, and more!

## Install Guide
1. `sudo pip install sequestrum`
2. Leave a star on this repo
3. Enjoy!

## Usage
### Getting Started
First, you'll need a Sequestrum Config in your dotfiles so it knows how to properly handle files. A guide to writing 
your own custom config along with an exampe config are down included down below. After you're done writing your config,
you can come back to finish setup! 

**Note:** Your dotfiles should be empty of all config files to keep from having duplicate files unless for some reason you
would want that. Never edit your config when you have packages installed. Unlink then edit your config to prevent lost files.

Now they you're all setup with your config file, time for the fun to begin! If your configuration file is setup correctly, you
should be able to run `sequestrum --setup` (full list of commands below) to finish setting up your dotfiles. If something goes 
wrong, be sure to check your configuration file to make sure everything is correct. Run `-sequestrum --install` after to symlink 
your dotfiles to your system. Setup will delete all local system files and move them to the dotfile repository.

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

The name of your config file should be config.yaml, and should be placed within your dotfiles. In theory, the config file
could be placed anywhere as long as you get your dotfileDirectory correct, but for cleanliness, it's recommneded to be placed
within your dotfile repository.

### Config Guide
As you can notice, all config files have to begin with `options:`. After that, you need to add a base, just take the one off the
example configuration but change the name of the dotfileDirectory to wherever your dotfiles are located. For each set of files you
want to package you'll need a seperate package declaration (ex. vimPackage in the example).

#### Directories
As you'll notice the each set of links you want to group will need their own package. You can name these whatever you like as long 
as they end in "Package" (ex. vimPackage or binPackage). In each package, you must include the directory name and 
links. Directory name is whatever you'd like the directory holding all the links to be called, and the links are the files getting linked.
Each link is formatted like so: `dotfileFileName: localFilePath`. So in the example config, the file vimrc within my dotfiles would be 
linked to ~/.vimrc.

### Installing
Installing dotfiles onto your system is as easy as pie. Simple run sequestrum -i <package>. Make sure that the location on your system doesn't
exist yet or it'll toss you an error. You can use all to install all your dotfiles.

#### Additonal Options
On top of the two required includes (directoryName and links), you also have to option to add a commandsBefore and commandsAfter.
The names are pretty self explanatory, commandsBefore is a list of commands to run before the symlinking, and commandsAfter is a list 
of commands to run after the symlinking. More of custom options will be added in the future. If you have any ideas, just leave a feature
request. C:

### List of Commands
1. -s, --setup  : Setup your dotfile repository
2. -i, --install: Installs your dotfiles onto the system
3. -u, --unlink : Unlink a package from your system
4. -d, --delete : Delete a repository from your dotfiles
5. -r, --refresh: Refresh your dotfiles based on your config
6. -b, --backup : Backup your system and check your config

## TODOS
- [ ] Dual way safety checks for install and setup
- [ ] Safety checks before backup
- [ ] Fix Refresh
- [ ] Commands to modify config
- [ ] Add support for more directories than home

## Contributing
If you'd like to contribute, whether that'd be improving the comments or README (which could always use work), or adding functionality,
just fork this, add to it, then send a merge request. I'll try and get around to looking at it as soon as possible.

## License
Copyright (c) 2018-2018 Ivy Zhang. Released under the MIT License.
