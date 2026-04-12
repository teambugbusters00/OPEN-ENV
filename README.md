---
title: OPEN-ENV
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
python_version: "3.10"
app_file: Dockerfile
pinned: false
---

# OPEN-ENV

A trading environment for AI agents.

## Features

- Trading simulation environment
- Easy, medium, and hard difficulty levels
- Grading system for agent performance

## Usage

```python
from openenv import create_env

env = create_env()
obs, info = env.reset()
obs, reward, done, truncated, info = env.step(action)
```
