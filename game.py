import time

import cv2
import numpy as np

from game.shooting_game import ShootingGame
from game_ui import COUNTDOWN_SECONDS, GAME_DURATION_SECONDS, draw_button, draw_name_field, draw_panel, is_tap_pose, point_in_rect
from hand_tracking.hand_detector import HandDetector


WINDOW_NAME = "Gesture Shooting Game"


def build_menu_frame(width: int, height: int, detector: HandDetector, frame, pointer, tap_ready, name: str):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    detector.draw_cached_landmarks(canvas)
    draw_panel(
        canvas,
        "Gesture Tap Game",
        "Type your name, then point at Start Game and tap with your index finger.",
    )
    draw_name_field(canvas, name, True)

    start_rect = (430, 465, 850, 555)
    draw_button(canvas, start_rect, "Start Game", active=pointer is not None and point_in_rect(pointer, start_rect))

    if pointer is not None:
        color = (0, 255, 0) if tap_ready else (255, 255, 255)
        cv2.circle(canvas, pointer, 12, color, 2)

    cv2.putText(canvas, "Press Backspace to edit name", (400, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)
    return canvas, start_rect


def build_countdown_frame(width: int, height: int, detector: HandDetector, frame, count_value: int):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    detector.draw_cached_landmarks(canvas)
    draw_panel(canvas, "Get Ready", "Touch the balls with your index finger when the game starts.")
    cv2.putText(canvas, str(count_value), (590, 430), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 8)
    return canvas


def build_game_over_frame(width: int, height: int, detector: HandDetector, frame, pointer, tap_ready, player_name: str, score: int):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    detector.draw_cached_landmarks(canvas)
    draw_panel(canvas, "Time Up", "Point to Retry to return to the menu, or point to Exit to close the game.")
    cv2.putText(canvas, f"Player: {player_name}", (330, 320), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(canvas, f"Final Score: {score}", (330, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)

    retry_rect = (280, 500, 600, 590)
    exit_rect = (680, 500, 1000, 590)
    draw_button(canvas, retry_rect, "Retry", active=pointer is not None and point_in_rect(pointer, retry_rect))
    draw_button(canvas, exit_rect, "Exit", active=pointer is not None and point_in_rect(pointer, exit_rect))

    if pointer is not None:
        color = (0, 255, 0) if tap_ready else (255, 255, 255)
        cv2.circle(canvas, pointer, 12, color, 2)

    return canvas, retry_rect, exit_rect


def main():
    cap = cv2.VideoCapture(0)

    width = 1280
    height = 720

    cap.set(3, width)
    cap.set(4, height)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    detector = HandDetector()
    game = ShootingGame(width, height)

    smooth = 4
    px, py = width // 2, height // 2
    pointer = None
    player_name = ""
    state = "menu"
    countdown_started_at = 0.0
    game_started_at = 0.0
    tap_latched = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        detector.detect(frame)
        landmarks = detector.get_landmarks(frame)
        tap_ready = False
        pointer = None

        if landmarks:
            x, y = landmarks[8]
            cx = px + (x - px) / smooth
            cy = py + (y - py) / smooth
            px, py = cx, cy
            pointer = (int(cx), int(cy))
            tap_ready = is_tap_pose(detector, landmarks)

        tap_triggered = tap_ready and not tap_latched
        tap_latched = tap_ready

        if state == "menu":
            canvas, start_rect = build_menu_frame(width, height, detector, frame, pointer, tap_ready, player_name)
            if tap_triggered and pointer is not None and point_in_rect(pointer, start_rect):
                game.reset()
                countdown_started_at = time.time()
                state = "countdown"

        elif state == "countdown":
            elapsed = time.time() - countdown_started_at
            count_value = max(1, COUNTDOWN_SECONDS - int(elapsed))
            canvas = build_countdown_frame(width, height, detector, frame, count_value)
            if elapsed >= COUNTDOWN_SECONDS:
                game_started_at = time.time()
                state = "playing"

        elif state == "playing":
            canvas = np.zeros((height, width, 3), dtype=np.uint8)
            detector.draw_cached_landmarks(canvas)

            time_left = max(0, GAME_DURATION_SECONDS - int(time.time() - game_started_at))
            if pointer is not None and tap_ready:
                game.tap(pointer)

            game.update()
            game.draw(canvas)
            if pointer is not None:
                game.draw_crosshair(canvas, pointer, tap_ready)
            game.draw_hud(canvas, tap_ready, time_left)

            if time.time() - game_started_at >= GAME_DURATION_SECONDS:
                state = "game_over"

        else:
            final_name = player_name if player_name else "Player"
            canvas, retry_rect, exit_rect = build_game_over_frame(
                width, height, detector, frame, pointer, tap_ready, final_name, game.score
            )
            if tap_triggered and pointer is not None:
                if point_in_rect(pointer, retry_rect):
                    game.reset()
                    player_name = ""
                    state = "menu"
                elif point_in_rect(pointer, exit_rect):
                    break

        cv2.imshow(WINDOW_NAME, canvas)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        if state == "menu":
            if key in (8, 127):
                player_name = player_name[:-1]
            elif key == 13:
                game.reset()
                countdown_started_at = time.time()
                state = "countdown"
            elif 32 <= key <= 126 and len(player_name) < 16:
                player_name += chr(key)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
