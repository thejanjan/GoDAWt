# 🎹 GoDAWt  
GoDAWt is a music engineer's toolkit for Godot 4+ to create easy music syncs and rhythm games.
Making components of your game react to the music can heavily improve the immersion and experience of your game. 

## Introduction

Making rhythm games and music syncs in games is deceptively difficult.
While it is already tedious to convert real-time music playback into events synced in-game,
it's also messy to demonstrate musical cues for rhythm games.
It is usually mandatory for game developers to create their own music mapping tools
to accomplish these tasks for larger projects.

**GoDAWt is designed to reduce the need for developers to create and design
their own rhythm and note editors by using the DAW as the editor.**   

This repository contains two tools for developers:
1. **🎛️️ Goise,** a Godot plugin which provides the tools to integrate Goise resources into game projects for music syncing and rhythm games
2. **🏜️ Renot,** a tool for processing Renoise project files into a Goise resources

---
## 🎛️ Goise

Goise is a Godot plugin which provides the tools to integrate Goise resources (music data processed into note data/timings) into game projects for music syncing and rhythm games.

### Installation

Goise is a regular editor plugin and can be installed the same way as any other.
Copy the `Goise` directory into your root project folder, and you should be able to activate it in your project settings.

### Documentation

todo

### Demos

todo

---
## 🏜 Renot

Renot is a tool for processing Renoise project files into a Godot resource for use in Goise.

Renoise is a music tracker with the features and functionality of a modern DAW.
**It is not mandatory to purchase it to use Renot,** as Renoise has an unlimited free trial that can do everything execpt export files to .wav.
However, Renot works best with the integration of music exports, so I do recommend purchasing it if you are interested in using it for your project's primary DAW. 

### Why Renoise?

Because it's my primary DAW.

And, unlike other DAWs, Renoise project files are extremely convenient for processing.
All Renoise projects can be extracted like a zip file, exposing its instrument and song data in a complete .xml format.

Renoise as a DAW also lends itself well to the production of video game music, especially for more retro styles.

### Installation

todo

### Documentation

todo

### Demos

todo

---
## Contributions

All contributions are appreciated!
I will be happy to look over and approve any PRs that I think are meaningful for the project.
I would be especially interested in seeing tools to create Goise resources with other DAWs. 
Renot is designed for my personal use and experience with Renoise as my primary DAW, but the integration of more mainstream DAWs would be greatly appreciated.

## License

All projects in this repository are under the MIT License.

Copyright (c) 2023-present, Micah Nichols (thejanjan)
