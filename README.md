---
title: OPEN-ENV
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.37.0"
python_version: "3.11"
app_file: server/app.py
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
