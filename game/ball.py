from dataclasses import dataclass
import random

import cv2


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: int
    color: tuple[int, int, int]
    alive: bool = True

    @classmethod
    def spawn(cls, width: int, height: int) -> "Ball":
        radius = random.randint(18, 36)
        x = random.randint(radius, width - radius)
        y = random.randint(radius, height - radius)
        vx = random.choice([-1, 1]) * random.uniform(3.0, 6.0)
        vy = random.choice([-1, 1]) * random.uniform(2.0, 5.0)
        color = (
            random.randint(120, 255),
            random.randint(120, 255),
            random.randint(120, 255),
        )
        return cls(x=x, y=y, vx=vx, vy=vy, radius=radius, color=color)

    def update(self, width: int, height: int) -> None:
        if not self.alive:
            return

        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.vx *= -1
            self.x = max(self.radius, min(width - self.radius, self.x))

        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.vy *= -1
            self.y = max(self.radius, min(height - self.radius, self.y))

    def draw(self, frame) -> None:
        if not self.alive:
            return

        center = (int(self.x), int(self.y))
        cv2.circle(frame, center, self.radius, self.color, -1)
        cv2.circle(frame, center, self.radius + 3, (255, 255, 255), 2)
        cv2.circle(frame, center, max(4, self.radius // 3), (255, 255, 255), -1)

    def contains(self, point: tuple[int, int]) -> bool:
        px, py = point
        dx = self.x - px
        dy = self.y - py
        return dx * dx + dy * dy <= self.radius * self.radius
