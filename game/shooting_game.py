from dataclasses import dataclass

import cv2

from game.ball import Ball


@dataclass
class Explosion:
    x: int
    y: int
    age: int = 0
    max_age: int = 12

    def draw(self, frame) -> bool:
        progress = self.age / self.max_age
        radius = int(12 + progress * 40)
        color = (
            max(0, int(255 * (1 - progress))),
            max(0, int(220 * (1 - progress))),
            255,
        )
        cv2.circle(frame, (self.x, self.y), radius, color, 3)
        cv2.circle(frame, (self.x, self.y), max(4, radius // 3), color, -1)
        self.age += 1
        return self.age < self.max_age


class ShootingGame:
    def __init__(self, width: int, height: int, num_balls: int = 6):
        self.width = width
        self.height = height
        self.num_balls = num_balls
        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.taps = 0
        self.hit_flash = 0
        self.balls = [Ball.spawn(self.width, self.height) for _ in range(self.num_balls)]
        self.explosions: list[Explosion] = []

    def update(self) -> None:
        for ball in self.balls:
            ball.update(self.width, self.height)

    def draw(self, frame) -> None:
        for ball in self.balls:
            ball.draw(frame)

        active_explosions = []
        for explosion in self.explosions:
            if explosion.draw(frame):
                active_explosions.append(explosion)
        self.explosions = active_explosions

        if self.hit_flash > 0:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (self.width, self.height), (40, 90, 20), -1)
            cv2.addWeighted(overlay, 0.12, frame, 0.88, 0, frame)
            self.hit_flash -= 1

    def tap(self, pointer: tuple[int, int]) -> bool:
        hit_ball = None

        for ball in self.balls:
            if ball.contains(pointer):
                hit_ball = ball
                break

        if hit_ball is None:
            return False

        self.taps += 1
        self.score += 1
        self.hit_flash = 4
        self.explosions.append(Explosion(int(hit_ball.x), int(hit_ball.y)))
        self.balls.remove(hit_ball)
        self.balls.append(Ball.spawn(self.width, self.height))
        return True

    def draw_hud(self, frame, tap_ready: bool, time_left: int) -> None:
        cv2.putText(
            frame,
            f"Score: {self.score}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Taps: {self.taps}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (180, 180, 180),
            2,
        )
        cv2.putText(
            frame,
            f"Time: {time_left}s",
            (self.width - 210, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        status = "Tap mode: READY" if tap_ready else "Tap mode: index finger only"
        status_color = (0, 255, 0) if tap_ready else (0, 190, 255)
        cv2.putText(
            frame,
            status,
            (20, self.height - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_color,
            2,
        )

    def draw_crosshair(self, frame, pointer: tuple[int, int], tap_ready: bool) -> None:
        x, y = pointer
        color = (0, 255, 0) if tap_ready else (255, 255, 255)
        cv2.circle(frame, (x, y), 14, color, 2)
        cv2.line(frame, (x - 20, y), (x + 20, y), color, 2)
        cv2.line(frame, (x, y - 20), (x, y + 20), color, 2)
