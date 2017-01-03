Padawan.sublime
===============

**No plans for Windows support**

Padawan.sublime is a Sublime Text 3 plugin for [padawan.php server
](https://github.com/mkusher/padawan.php), a smart PHP code
completion server for Composer projects.

This plugin includes:
- Completion
- Commands for index generation and index saving
- Commands for starting, stopping and restarting the server

# Installation

1. Make sure you've installed [padawan.php server](
https://github.com/mkusher/padawan.php#how-to-use)
2. Install this plugin via [Package control](https://packagecontrol.io)
or clone this repo to `/path/to/your/sublime-text-3/Packages/`

# Demo video

Click the image below to watch a short video on what
Padawan.sublime can already do.

[![ScreenShot](http://i1.ytimg.com/vi/qpLJD24DYcU/maxresdefault.jpg)
](https://www.youtube.com/watch?v=qpLJD24DYcU)

# Requirements

Padawan.php requires PHP 5.5+

# Running

To get smart autocompletion all you need to do is the following easy steps:

1. Open your php composer project
2. Run the `Padawan: Generate Index` from the command palette
3. Run the `Padawan: Start Server` from the command palette after index
generation has stopped
4. Enjoy smart completion

# Plugins(Extensions)

You can extend Padawan.php by installing plugins.
See [Plugins List](https://github.com/mkusher/padawan.php/wiki/Plugins-list)
for more info.

## Installing

Use `Padawan: Add plugin` and type plugin name, for example `mkusher/padawan-di`

## Removing

Use `Padawan: Remove plugin` and choose one of the installed plugin from
the list.
