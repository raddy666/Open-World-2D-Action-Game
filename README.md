# 🕹️ 2D Open-World Action Game (Python / PgZero)

A **2D open-world action game** built in **Python using PgZero**, featuring real-time combat, vehicles, NPC AI, and multiple interconnected city zones.

This project implements a **gameplay systems built on PgZero and gameplay layer**, supporting **50+ concurrent entities**, modular systems, and scalable open-world simulation.

---

## 🎮 Gameplay

- Explore a multi-zone city world:
  - Residential
  - Industrial
  - Downtown
- Engage in melee and ranged combat
- Interact with NPCs, enemies, vehicles, and shops
- Hijack vehicles and navigate live city traffic
- Progress through increasing difficulty, including custom boss encounters

---

## ✨ Core Features

### 🌆 Open-World Systems
- Seamless gameplay across multiple environments
- Dynamic NPC spawning based on player position and progression
- Centralized game state management supporting high entity counts

### ⚔️ Combat System
- Object-oriented weapon hierarchy (melee / ranged)
- Player and enemy combat state management
- Proximity-based enemy engagement and targeting
- Custom boss fight mechanics with specialized behaviors

### 🤖 AI & NPCs
-  Enemy AI implemented with finite state machines
- Finite state machines for NPC and player logic
- Autonomous NPC movement and interaction
- Three levels of increasing difficulty ending in a boss fight

### 🚗 Vehicle System
- Player vehicle hijacking mechanics
- Physics-aware driving controls with collision handling
- Autonomous NPC traffic system with rule-based collision avoidance

---

## 🧠 Engine Design

The game runs on PgZero's update/draw loop with a tile-grid map for terrain checks.

### Engine vs Game Logic

- **Engine Layer:** entity system, event handling, AI framework, collision, world state
- **Game Layer:** weapons, enemies, vehicles, levels, progression, boss mechanics

Character sprites are generated using the  
**Universal LPC Spritesheet Generator**, ensuring consistent animation and character customization. For more information about credits See [below](##-💳-Credits)

---

## 🎮 Controls

| Key | Action |
|----|------|
| `W / A / S / D` | Player movement |
| `Mouse / Attack Key` | Attack |
| `1 / 2 / 3` | Switch weapons |
| `E` | Interact / enter vehicle |
| `Left Shift` | Run |
| `Esc` | Quit game |

Controls are configurable via the input mapping module and can be easily extended.

---

## ▶️ Setup & Run

### Requirements
- Python 3.x
- PgZero

### Option 1: pip (requirements.txt)

Install dependencies using pip:

```bash
pip install -r requirements.txt
```
### Option 2: Conda (environment.yml)

Create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate <environment_name>
```
---

## 🛠️ Technology Stack

- **Language:** Python  
- **Framework:** PgZero  
- **Architecture:** Object-Oriented Design  
- **AI:** Finite State Machines

---

## 🚧 Possible Extensions

- **AI:** Finite State Machines
- Save / load system  
- Procedural world expansion  
- Advanced pathfinding (A*)  
- Improved physics and collision response  
- UI overlays (map, inventory, missions)  
- Cross-platform packaging  

---

## 👤 Author

**MD Tahmid Hamim**

---

## 💳 Credits

- Sprites by: Johannes Sjölund (wulax), Michael Whitlock (bigbeargames), Matthew Krohn (makrohn), Nila122, David Conway Jr. (JaidynReiman), Carlo Enrico Victoria (Nemisys), Thane Brimhall (pennomi), laetissima, bluecarrot16, Luke Mehl, Benjamin K. Smith (BenCreating), MuffinElZangano, Durrani, kheftel, Stephen Challener (Redshrike), William.Thompsonj, Marcel van de Steeg (MadMarcel), TheraHedwig, Evert, Pierre Vigier (pvigier), Eliza Wyatt (ElizaWy), Johannes Sjölund (wulax), Sander Frenken (castelonia), dalonedrau, Lanea Zimmerman (Sharm), Manuel Riecke (MrBeast), Barbara Riviera, Joe White, Mandi Paugh, Shaun Williams, Daniel Eddeland (daneeklu), Emilio J. Sanchez-Sierra, drjamgo, gr3yh47, tskaufma, Fabzy, Yamilian, Skorpio, kheftel, Tuomo Untinen (reemax), Tracy, thecilekli, LordNeo, Stafford McIntyre, PlatForge project, DCSS authors, DarkwallLKE, Charles Sanchez (CharlesGabriel), Radomir Dopieralski, macmanmatty, Cobra Hubbard (BlueVortexGames), Inboxninja, kcilds/Rocetti/Eredah, Napsio (Vitruvian Studio), The Foreman, AntumDeluge
- Sprites contributed as part of the Liberated Pixel Cup project from OpenGameArt.org: http://opengameart.org/content/lpc-collection
- License: Creative Commons Attribution-ShareAlike 3.0 (CC-BY-SA 3.0) <http://creativecommons.org/licenses/by-sa/3.0/>
- Detailed credits: [CREDITS.csv](/CREDITS.csv)
