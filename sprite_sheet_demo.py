"""Teaching demo: using a 32x32 sprite sheet with Pygame.

This file is a standalone example for OCR A-Level style coursework.
It shows how to:
- load a PNG sprite sheet
- slice it into 32x32 frames
- store animations in a dictionary
- switch between idle, walk, and attack states
"""

from __future__ import annotations

from pathlib import Path

import pygame


class AnimatedSprite:
    """Simple reusable animated sprite class.

    Encapsulation:
        Animation frames, current state, and timing are stored internally.

    Abstraction:
        Other classes only need to call set_state(), update(), and draw().

    Reuse:
        This can be used directly inside Player or Enemy classes.
    """

    FRAME_SIZE = 32

    def __init__(self, sprite_sheet_path: str, x: int, y: int) -> None:
        """Load sprite sheet and prepare animation states."""
        self._sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        # Position is stored separately from drawing rectangle.
        self._x = x
        self._y = y

        # Current animation state.
        self._state = "idle"
        self._current_frame_index = 0

        # Frame timing (seconds per frame).
        self._frame_duration = {
            "idle": 0.40,
            "walk": 0.12,
            "attack": 0.08,
        }
        self._time_since_last_frame = 0.0

        # True means animation repeats forever.
        self._looping = {
            "idle": True,
            "walk": True,
            "attack": False,
        }

        # Sprite sheet layout (example):
        # Row 0 = idle frames, row 1 = walk frames, row 2 = attack frames.
        # Each frame is 32x32 pixels.
        self._animations = {
            "idle": self._extract_row_frames(row=0, frame_count=4),
            "walk": self._extract_row_frames(row=1, frame_count=4),
            "attack": self._extract_row_frames(row=2, frame_count=4),
        }

    def _extract_row_frames(self, row: int, frame_count: int) -> list[pygame.Surface]:
        """Extract a full animation row from the sprite sheet.

        Sprite sheet idea:
        - x coordinate picks the frame column
        - y coordinate picks the animation row
        - each rectangle is 32x32
        """
        frames: list[pygame.Surface] = []

        for column in range(frame_count):
            source_rect = pygame.Rect(
                column * self.FRAME_SIZE,
                row * self.FRAME_SIZE,
                self.FRAME_SIZE,
                self.FRAME_SIZE,
            )
            frame_surface = pygame.Surface((self.FRAME_SIZE, self.FRAME_SIZE), pygame.SRCALPHA)
            frame_surface.blit(self._sprite_sheet, (0, 0), source_rect)
            frames.append(frame_surface)

        return frames

    def set_state(self, new_state: str) -> None:
        """Change animation state when needed.

        If a new state is selected, frame playback restarts from frame 0.
        """
        if new_state not in self._animations:
            return

        if new_state != self._state:
            self._state = new_state
            self._current_frame_index = 0
            self._time_since_last_frame = 0.0

    def is_state(self, state_name: str) -> bool:
        """Return True when the sprite is currently in the given state."""
        return self._state == state_name

    def update(self, delta_time: float) -> None:
        """Advance animation using a simple timer-based frame system."""
        frames = self._animations[self._state]
        if len(frames) <= 1:
            return

        self._time_since_last_frame += delta_time
        if self._time_since_last_frame < self._frame_duration[self._state]:
            return

        self._time_since_last_frame = 0.0
        self._current_frame_index += 1

        # Looping animations wrap around.
        if self._current_frame_index >= len(frames):
            if self._looping[self._state]:
                self._current_frame_index = 0
            else:
                # Non-looping attack returns to idle after the final frame.
                self.set_state("idle")

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the current animation frame."""
        frame = self._animations[self._state][self._current_frame_index]
        surface.blit(frame, (self._x, self._y))



def run_demo() -> None:
    """Run a minimal demo loop showing idle, walk, and attack animations.

    Controls:
    - Left/Right arrow or A/D: walk
    - Space: attack
    - Window close: quit
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    pygame.display.set_caption("Sprite Sheet Demo (32x32)")
    clock = pygame.time.Clock()

    sprite_sheet_file = Path(__file__).resolve().parent / "assets" / "character_sheet_32x32.png"
    if not sprite_sheet_file.exists():
        raise SystemExit(
            "Missing PNG: /tmp/workspace/nuast/orko/assets/character_sheet_32x32.png\n"
            "Add a 32x32 sprite sheet with rows for idle, walk, and attack."
        )

    animated_sprite = AnimatedSprite(str(sprite_sheet_file), x=304, y=164)

    # Integration idea for this project:
    # In player.py, create self._animated_sprite in Player.__init__.
    # In Player.update, call set_state(...) based on input or attack action,
    # then call self._animated_sprite.update(delta_time).
    # In Player.draw, call self._animated_sprite.draw(surface).

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                animated_sprite.set_state("attack")

        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]

        # If we are not attacking, walking input changes state.
        if moving and not animated_sprite.is_state("attack"):
            animated_sprite.set_state("walk")
        elif not moving and not animated_sprite.is_state("attack"):
            animated_sprite.set_state("idle")

        animated_sprite.update(delta_time)

        screen.fill((25, 25, 25))
        animated_sprite.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_demo()
