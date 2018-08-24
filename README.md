# Sequestrum
## Description
A dotfile manager for the masses. Now you may be wondering, why use this over Stow or Dotbot. Simple.
Well for starters, the name is better. Do you need any other reasons? Fine, fine.. some real reasons.
This is specifically made for dotfile management and provides features like modulatarity, proper symlink
error handling, dotfile repo setup, and more!

## Install Guide
1. git clone https://github.com/iiPlasma/sequestrum.git ~/Sequestrum
2. cd ~/Sequestrum
3. chmod +x Sequestrum
4. Add to $PATH

## User's Manual
First thing is first, your dotfiles need to be setup to work with Sequestrum. If you have used something like
stow or dotbot to manage your dotfiles, it's highly recommeneded testing this in a test directory before converting
your main dotfiles. You'll want to create a config file in your dotfiles so Sequestrum knows how to setup and install.
I've included an example below with all options available. 
```
options:
    base: &base
        dotfileDirectory: .dotfiles

    vimDirectory:
        <<: *base
        directoryName: vim
        commandsBefore:
            - ufetch
        links:
            - vimrc: .vimrc
        commandsAfter:
            - ls

    binDirectory:
        <<: *base
        directoryName: bin
        links:
            - bin: .scripts 
```

Note: All directory headers have to end in Directory (ex. vimDirectory, binDirectory). This is a W.I.P i can't write docs
so if anyone wants to help C:

## Feature Requests
- [X] Modularity
- [ ] Proper Guide (Yes this is a feature)
- [ ] Documentation
- [ ] Commands before and after symlink
- [ ] Uninstall
- [ ] Proper handling of when symlink fails because file already exists
