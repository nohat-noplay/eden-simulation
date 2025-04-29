# Eden Simulation 🦋🌸🌿
Year: 2023

✨ This was my first Python project, completed in 2023, marking the beginning of my journey into programming and the Python language.✨

## Project Overview
Eden Simulation is a dynamic garden ecosystem simulator where ants, butterflies, lizards, worms, flowers, and fossils interact with each other and react to changing weather events like rain. The simulation visualises animal behaviors and lifecycle stages across timesteps, with a day/night mode, rain events, and dynamic terrain updates.

## Features:
- Agent-Based Simulation: Modeled dynamic interactions between animals, food sources, and weather events across discrete timesteps.
- Object-Oriented Design: Built inheritance-based class hierachy for Animal, Food, and Event with state-driven behaviours (e.g., hunger, death, movement).
- Lifecycle Modeling: Simulated transformations (caterpillars → cocoons → butterflies) and aging processes (worms dying into fossils).
- Event-Driven Behaviour: Rain dynamically altered movement speed, food-seeking behaviour, and terrain state (flooding tunnels).
- Custom Visualisation: Animated matplotlib plots with custom SVG markers (svgpath2mpl, svgpathtools).
- Data-Driven Initialisation: Loaded world background and initial animal states from .csv files for flexible scenario setup.
- Robust User Input: Supported command-line arguments and validated interactive prompts for simulation configuration.
- Error Handling included

## Dependencies
Python 3.11+, matplotlib, numpy, svgpath2mpl, svgpathtools, random, sys

## How to Run
`python playEden.py`
You will be prompted to:
1. Enter the number of timesteps
2. Choose Day (D) or Night (N) mode

Alternatively, you can provide command-line arguments directly:
`python playEden.py 100 D`  (100 timesteps, Day mode)


## Important Notes for the User:
- SVG dependencies: The simulation uses hand-drawn SVG images. Ensure svgpath2mpl and svgpathtools are installed and critters folder located correctly

## Credits
Created by Saf Flatters
Artwork and SVG illustrations drawn by myself specifically for this project.

## Connect with Me
📫 [LinkedIn](https://www.linkedin.com/in/safflatters/)

## License and Usage
![Personal Use Only](https://img.shields.io/badge/Personal%20Use-Only-blueviolet?style=for-the-badge)

This project is intended for personal, educational, and portfolio purposes only.

You are welcome to view and learn from this work, but you may not copy, modify, or submit it as your own for academic, commercial, or credit purposes.

