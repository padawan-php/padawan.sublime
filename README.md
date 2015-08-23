Padawan.sublime
===============

Padawan.sublime is a Sublime Text 3 plugin for [padawan.php server
](https://github.com/mkusher/padawan.php), a smart PHP code
completion server for Composer projects.

This plugin includes:
- Completion
- Commands for index generation and index saving
- Commands for starting, stopping and restarting the server

# Demo video

Click the image below to watch a short video on what
Padawan.sublime can already do.

[![ScreenShot](http://i1.ytimg.com/vi/qpLJD24DYcU/maxresdefault.jpg)](https://www.youtube.com/watch?v=qpLJD24DYcU)

# Requirements

Padawan.php requires PHP 5.5+

# Installation

Clone this repo to `/path/to/your/sublime-text-3/Packages/`
and then run `sh install.sh`

# Running

To get smart autocompletion all you need to do is the following easy steps:
1. Install padawan.sublime plugin
2. Open your php composer project
3. Run the `Padawan: Generate Index` from the command palette
4. Run the `Padawan: Start Server` from the command palette after index
generation has stopped
5. Enjoy smart completion
