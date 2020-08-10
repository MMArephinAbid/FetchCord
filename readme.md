<h1 align="center">FetchCord</h1>
</p>
<p align="center">
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img src="https://img.shields.io/badge/Compatible-MacOS%2FLinux-brightgreen?style=for-the-badge&logo=linux&logoColor=white">
    </a>
  <a href="https://www.python.org/downloads/">
       <img src="https://img.shields.io/badge/Python-version%3A%203.8-red?style=for-the-badge&logo=python&logoColor=white"">
    </a>
   <a href="https://discord.gg/P4h9kdV">
       <img src="https://img.shields.io/discord/742068289278312549?label=Discord&logo=discord&logoColor=white&style=for-the-badge">
    </a>
    <a href="https://img.shields.io/badge/Compatible-MacOS%2FWindows%2FLinux-brightgreen?style=for-the-badge&logo=discord">
       <img src="https://cdn.discordapp.com/attachments/695182849476657223/742064452421288077/FetchDis.png"
    </a>
  
  </a>
</p>

# Table of content
- [Features](#features)
- [To-Do](#to-do)
- [Installing](#installing-and-running)
     - [Install on (gnu/)linux](#installing-on-gnulinux)
        - [Running on (gnu/)linux](#run)
           - [Arguments](#arguments)
   - [Install on MacOS](#installing-on-macos)
       - [Running on MacOs](#run-1)
- [Examples](#examples)

### Features
***
  - [✓] Distribution detection

  - [✓] Distribution Version

  - [✓] Package detection

  - [✓] Kernel Detection

  - [✓] Uptime

  - [✓] Detecting Window Manager/Desktop Environment

  - [✓] Detecting GPU/CPU and display it in a cycle (thanks to Hyper-KVM)
  - [✓] Flatpak support

### To-Do
***
  - [✗] Add more distributions (If your distro is not supported open an issue)

  - [✗] Detect Window Manager/Desktop Environment version

  - [✗] Add Snap support

  - [✗] Add support for desktop icon use

  - [✗] More CPUs, ex. Pentium, Older AMD CPUs

  - [✗] More GPUs?

***

# Installing and Running

### Installing on (GNU/)Linux
> `#` the command should be ran as `sudo`

> `$` the command should be ran as user

_From download/cloned directory_

```sh
# ./install.sh
```
### Run

NOTE: you must have neofetch installed

To run the script simply run `fetchcord`, python 3.8 should have the `distro` module but if you get an error install it via pip,

```sh
$ pip3 install distro
```
#### Arguments
--distro, shows only distro and kernel version and package count.

--hardware, shows only CPU and GPU info.

--shell, shows only terminal and shell info.

--time, -t, set custom duration for cycles in seconds.

-h or --help, shows this information above.

## Installing on MacOS
> `#` the command should be ran as `sudo`

> `$` the command should be ran as user

_From download/cloned directory_

```sh
# ./macinstall.sh
```


### Run 

```sh
$ python3 run-rpc.py
```

## Examples

![Arch with awesome](Examples/arch_example.png) ![Debian with Cinnamon](Examples/debian_example.png) ![Fedora with xfce](Examples/fedora_example.png)

![manjaro with i3](Examples/manjaro%20example.png) ![mint with mate](Examples/mint_example.png) ![popos with kde](Examples/pop_example.png)

![void with dwm](Examples/void_example.png) ![endeabour with deepinde](Examples/end_example.png) ![centos with unity](Examples/centos_example.png)

![ubuntu with budgie](Examples/ubuntu_example.png) ![macos with a macbook](Examples/mac_example.png) ![OpenSUSE with gnome](Examples/suse_example.png)

![amd with nvidia](Examples/amd_example.png)
