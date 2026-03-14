import cv2


GAME_DURATION_SECONDS = 60
COUNTDOWN_SECONDS = 3


def wrap_text(text: str, max_width: int, font, scale: float, thickness: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        width = cv2.getTextSize(candidate, font, scale, thickness)[0][0]
        if width <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def is_tap_pose(detector, landmarks) -> bool:
    if len(landmarks) < 21:
        return False

    fingers = detector.fingers_up(landmarks)
    return fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0


def point_in_rect(point: tuple[int, int], rect: tuple[int, int, int, int]) -> bool:
    x, y = point
    left, top, right, bottom = rect
    return left <= x <= right and top <= y <= bottom


def draw_button(frame, rect, label, active=False) -> None:
    left, top, right, bottom = rect
    fill = (40, 120, 40) if active else (55, 55, 55)
    border = (0, 255, 0) if active else (220, 220, 220)
    cv2.rectangle(frame, (left, top), (right, bottom), fill, -1)
    cv2.rectangle(frame, (left, top), (right, bottom), border, 2)
    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
    text_x = left + (right - left - text_size[0]) // 2
    text_y = top + (bottom - top + text_size[1]) // 2
    cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)


def draw_panel(frame, title, subtitle="", bounds=(60, 50, 1220, 670)) -> None:
    left, top, right, bottom = bounds
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (10, 10, 10), -1)
    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)
    cv2.rectangle(frame, (left, top), (right, bottom), (18, 18, 18), -1)
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
    cv2.putText(frame, title, (left + 70, top + 90), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)
    if subtitle:
        subtitle_lines = wrap_text(
            subtitle,
            max_width=(right - left) - 140,
            font=cv2.FONT_HERSHEY_SIMPLEX,
            scale=0.8,
            thickness=2,
        )
        for index, line in enumerate(subtitle_lines):
            y = top + 140 + index * 34
            cv2.putText(frame, line, (left + 70, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)


def draw_name_field(frame, name: str, active: bool) -> None:
    rect = (230, 290, 1050, 380)
    left, top, right, bottom = rect
    border = (0, 255, 0) if active else (255, 255, 255)
    cv2.putText(frame, "Enter your name", (left, top - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 2)
    cv2.rectangle(frame, (left, top), (right, bottom), (35, 35, 35), -1)
    cv2.rectangle(frame, (left, top), (right, bottom), border, 2)
    display_name = name if name else "Player"
    cv2.putText(frame, display_name, (left + 20, top + 52), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
