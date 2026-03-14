# Gesture Shooting Game

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Build_Enabled-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-0097A7?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Array_Processing-013243?style=for-the-badge&logo=numpy&logoColor=white)

Gesture Shooting Game is a webcam-based hand tracking game built with Python, OpenCV, and MediaPipe. The player uses their index finger as a pointer and performs a tap gesture to "shoot" moving targets on screen.

## Purpose

This project demonstrates how hand tracking can be used to build a simple interactive game without a mouse or keyboard. It combines real-time webcam input, finger landmark detection, gesture recognition, and game logic into a playable desktop experience.

## How To Play

1. Launch the game.
2. Allow your webcam to face your hand clearly.
3. Enter your name on the start screen using the keyboard.
4. Point at the `Start Game` button using your index finger.
5. Make a tap gesture with only your index finger raised to begin.
6. During the 60-second round, move your index finger over the balls.
7. Keep only the index finger raised to enable tap mode.
8. Tap on a ball to score a hit.
9. When time runs out, your final score is shown on the game over screen.
10. Point at `Exit` and tap to close the game, or press `Esc` at any time.

## Controls

- `Index finger position`: aim the on-screen pointer
- `Index finger only`: enables tap mode
- `Tap gesture`: selects buttons and hits targets
- `Backspace`: delete name input on the menu
- `Enter`: start the game from the menu
- `Esc`: quit the game

## Run Locally

1. Install Python 3.11 or newer.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the game:

```bash
python game.py
```

## Download The Windows Build

The repository includes a GitHub Actions workflow that builds a Windows executable and publishes a zipped release artifact.

To download it:

1. Open the repository on GitHub.
2. Go to the `Releases` section.
3. Open the latest release tagged like `build-<number>`.
4. Download `gesture_shooting.zip`.
5. Extract the zip and run the executable from the extracted `game` build folder.

If you want to inspect the automation, see [`.github/workflows/build-exe.yml`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/.github/workflows/build-exe.yml).

## Folder Structure

```text
Gesture_Shooting_Game/
|-- .github/
|   `-- workflows/
|       `-- build-exe.yml
|-- game/
|   |-- __init__.py
|   |-- ball.py
|   `-- shooting_game.py
|-- hand_tracking/
|   `-- hand_detector.py
|-- game.py
|-- game_ui.py
|-- game.spec
|-- requirements.txt
`-- README.md
```

## Project Files

- [`game.py`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/game.py): main entry point and game state flow
- [`game_ui.py`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/game_ui.py): menu, countdown, and UI helpers
- [`game/shooting_game.py`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/game/shooting_game.py): core gameplay, scoring, HUD, and hit effects
- [`hand_tracking/hand_detector.py`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/hand_tracking/hand_detector.py): MediaPipe hand detection and gesture support
- [`game.spec`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/game.spec): PyInstaller spec file
- [`requirements.txt`](/c:/Users/abhis/Documents/GitHub/Gesture_Shooting_Game/requirements.txt): Python dependencies

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- PyInstaller
- GitHub Actions

## Notes

- A webcam is required.
- The game is designed for a single hand.
- Good lighting improves hand tracking accuracy.
