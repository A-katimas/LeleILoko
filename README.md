*This project has been created as part of the 42 curriculum by jtardieu*

# Fly-in

<table>
  <tr>
    <td>
      <img src="https://media1.tenor.com/m/gSGHDKauYz8AAAAC/toothless-how-to-train-your-dragon.gif" width="150">
    </td>
    <td align="center">
      <h2>Fly in to the moon</h2>
    </td>
  </tr>
</table>

# Description

Fly In is a graphical project from the 42 curriculum where the goal is to simulate a flying experience in a dynamic environment. The project focuses on real-time rendering, smooth user interaction, and precise control of movement, while handling visual feedback and performance constraints.

# Instructions

## 🚀 Installation

Clone the repository and build the project:

```bash
git clone <repository_url>
cd LeleILoko
make easy1
```

## Execution

| Commande | Description |
|---|---|
| `make install` | Install a dependesise |
| `make run` | Launch an asset map |
| `make easy1` | Launch the map for the topic. **easy**, 1 |
| `make easy2` | Launch the map for the topic. **easy**, 2 |
| `make easy3` | Launch the map for the topic. **easy**, 3 |
| `make medium1` | Launch the map for the topic. **medium**, 1 |
| `make medium2` | Launch the map for the topic. **medium**, 2 |
| `make medium3` | Launch the map for the topic. **medium**, 3 |
| `make hard1` | Launch the map for the topic. **hard**, 1 |
| `make hard2` | Launch the map for the topic. **hard**, 2 |
| `make hard3` | Launch the map for the topic. **hard**, 3 |
| `make chalenger` | Launch the map for the topic **chalenger** |
| `make lint` | launch the lint for all the projet |
| `make clean` | erase all of the cache project and temp folders |
| `make fclean` | make a clean and remove the venv |


## ⌨️ Controls
<p align="center">
  <img src="model_use/readmeused/controluseflyin.png" width="800"/>
</p>

## Change Asset

If you want to switch assets, two methods are possible.

### 🔹 Method 1 — via the command line

If you want to change the asset, use the following command:

```bash
uv run Flyin.py "the position of your asset"
```

### 🔹 Méthode 2 — via le Makefile

If you do not want to use this command, add a line to the `Makefile` with this:

```makefile
CONFIG ?= "the position of your asset"
```

⚠️ **Don't forget to comment out the old configuration.**

Then launch with:

```bash
make run
```

• An “Instructions” section containing any relevant information about compilation,
installation, and/or execution.
• A “Resources” section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used —
specifying for which tasks and which parts of the project.
➠ Additional sections may be required depending on the project (e.g., usage
examples, feature list, technical choices, etc.).

# Resources

## 📚 References

- [Reference / documentation 1 — e.g. official library docs used]
- [Reference / documentation 2 — e.g. tutorial or article followed]
- [Reference / documentation 3 — e.g. 42 subject or course material]

## 🤖 AI Usage

AI (Claude) was used during this project for the following tasks:

- [e.g. Drafting and formatting this README]
- [e.g. Debugging a specific rendering/movement issue]
- [e.g. Explaining a concept related to the 3D engine / physics]

No AI-generated code was used for [specify the parts kept fully manual, if relevant].

# Features

- [Feature 1 — e.g. Real-time flight simulation with smooth controls]
- [Feature 2 — e.g. Multiple difficulty maps: easy, medium, hard, challenger]
- [Feature 3 — e.g. Custom asset loading via command line or config]