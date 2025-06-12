# 🕵️‍♂️ Robbery Simulation AI Game
**COS30002 – Artificial Intelligence for Games**  
Custom Project by **Chathil Vithanage (104195065)**

A 2D AI simulation where a Thief agent attempts to steal a gem while avoiding a patrolling and reactive Guard. The Guard uses a Finite State Machine (FSM) to switch between patrol and chase behaviors, while the Thief supports both manual control and automatic navigation using pathfinding and basic steering behaviors.

---

## 🎮 Gameplay Overview

- The **Thief** must reach the **Gem** in the center of the maze.
- The **Guard** patrols and chases the Thief when detected.
- The Guard can **shoot** bullets that reduce the Thief's health.
- The game ends when:
  - 🟩 The Thief reaches the Gem — **YOU WIN**
  - 🟥 The Thief’s health reaches 0 — **YOU LOSE**

---

## 🧠 AI Techniques Used

| Agent  | Behavior Type        | Techniques |
|--------|----------------------|------------|
| Guard  | FSM (Finite State Machine) | Patrol, Chase, Shoot |
| Thief  | Behavior-Based (Manual & Auto) | Flee, Seek, Pathfinding |
|        | Planned (Future Work) | Reinforcement Learning |

---

## 🗺️ Features

- Grid-based map loaded from `map.txt`
- A* pathfinding algorithm for auto-navigation
- FSM logic for Guard (patrol and chase states)
- Bullet shooting and health system
- UI labels for health, FSM state, win/lose messages
- Toggle between **manual** and **auto** Thief control

---

## 🧩 Controls

| Key         | Action                        |
|-------------|-------------------------------|
| `Arrow Keys`| Move Thief (manual mode)      |
| `T`         | Toggle Auto Mode (pathfinding)|

---

## 🖥️ Setup & Running the Game

### 🔧 Requirements
- Python 3.9+
- Pyglet  
  Install via pip:
  ```bash
  pip install pyglet
