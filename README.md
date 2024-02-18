## 💡 Idea

Train a Reinforcement Learning agent to play a simple dodging game. The game consists of a top-view grid, where the agent can move up, down, left or right. Enemies enter from each side and will cross the field. The agent will die when it is touched by one of the enemies. The amount of time the agent stays alive is equal to the score (reward) of the agent.

## Requirements

## Development

### Set up git hooks

Install [pre-commit tool](https://pre-commit.com/) and [mypy](https://github.com/python/mypy) to enable automatic checks and linting upon each commit:

```
pip install pre-commit mypy
pre-commit install
```

### Set up conda environment

Set up a conda environment with the requirements of this project:

```
conda create --name <environment_name> --file requirements.txt python=3.10
```

## 👩‍💻 Installation
