# Game of Nim Strategy Analysis 🎲

## What is the Game of Nim? 🤔

The Game of Nim is a classic mathematical strategy game involving two players and a number of objects (such as stones or sticks) arranged in rows. Players take turns removing one or more objects from a single row. The game can end under two main rule sets: the traditional version, where the player forced to take the last object loses, and the variant used in this project, where the last player to move wins.

## Project Structure 📂

This project is structured to offer a deep dive into AI-driven strategies for playing Nim. Inside the `agent/` folder, you'll find implementations of multiple AI agents, each employing a unique strategy to conquer the game:

- **NimSumAgent**: Utilizes the mathematical Nim-sum strategy, aiming to leave the opponent in a position where the Nim-sum of all piles is zero.
- **RLAgent**: Employs Q-learning, a form of reinforcement learning, to learn optimal moves through experience.
- **RandomAgent**: Makes moves at random, serving as a baseline for performance comparison.

## Getting Started 🚀

Before you start playing against the agents or evaluating them, you need to set up your environment. This project is written in Python and requires the installation of the `tqdm` library for progress bars during evaluation and training sessions. You can install `tqdm` using pip:

```bash
pip install tqdm
```

## Scripts 📜

Two main scripts are provided to interact with the game and the agents:

- **Evaluation Script (`evaluation.py`)**: This script conducts automated matches between the agents across different game configurations. It's an excellent way to benchmark the agents' performance and understand the strengths and weaknesses of their strategies.

- **Play Script (`play.py`)**: Fancy testing your strategic prowess against our AI agents? The `play.py` script allows you to do just that. You will be prompted to choose the game configuration (number of piles and max pile size) and select an agent to play against. It's a fun way to see how you stack up against the fruits of modern AI research in the realm of game theory!

## How to Use 🖥️

To start an evaluation of the agents, simply run:

```bash
python evaluation.py
```

When you're ready to challenge one of the agents to a game, execute:

```bash
python play.py
```

and follow the on-screen instructions to set up your game and select your opponent.

## Special Thanks 🙏

A huge thanks to [@Fatiepie](https://github.com/Fatiepie/) for the inspiration behind the RL agent implementation.

## Remarks 🤝

This project was made as the final course project for DSAI3203 - Fundementals of AI, given by Dr. Somaiyeh MahmoudZadeh

Thank you for exploring the Game of Nim AI Challenge 🎉
