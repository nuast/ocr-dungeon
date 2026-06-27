"""Player implementation for the dungeon crawler."""

from __future__ import annotations

import math

import pygame

from entity import Entity
from settings import (
    PLAYER_COLOR,
    PLAYER_MAX_HEALTH,
    PLAYER_MAX_MANA,
    PLAYER_SIZE,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPELL_COST,
    SPELL_DAMAGE,
    SPELL_EFFECT_COLOR,
    SPELL_EFFECT_DURATION_FRAMES,
    SPELL_RANGE,
)


class Player(Entity):
    """Controllable player character.

    Inheritance: Player extends Entity with movement input and mana-based spells.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create the player with default stats."""
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SPEED, PLAYER_MAX_HEALTH, PLAYER_COLOR)
        self._mana = PLAYER_MAX_MANA
        self._max_mana = PLAYER_MAX_MANA
        self._spell_effect = SpellCastEffect()

        # Placeholder sprite for now.
        # Later load Piskel sprite, for example: assets/player.png

    @property
    def mana(self) -> int:
        """Return current mana value."""
        return self._mana

    @property
    def max_mana(self) -> int:
        """Return maximum mana value."""
        return self._max_mana

    @property
    def has_active_spell_effect(self) -> bool:
        """Return True while the cast visual is still animating."""
        return self._spell_effect.is_active

    def cast_spell(self, enemies: list[Entity]) -> bool:
        """Spend mana to damage the nearest enemy within range.

        Returns True when a spell is cast, otherwise False.
        """
        if self._mana < SPELL_COST:
            return False

        nearest_enemy = None
        nearest_distance = SPELL_RANGE
        for enemy in enemies:
            if not enemy.is_alive:
                continue
            distance = math.dist(self.rect.center, enemy.rect.center)
            if distance <= nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        if nearest_enemy is None:
            return False

        self._mana -= SPELL_COST
        self._spell_effect.trigger(nearest_enemy.rect.center)
        nearest_enemy.take_damage(SPELL_DAMAGE)
        return True

    def _read_input(self, keys: pygame.key.ScancodeWrapper) -> tuple[int, int]:
        """Read keyboard state and return movement direction."""
        move_x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        move_y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        return move_x, move_y

    def update(self, keys: pygame.key.ScancodeWrapper, *_: object) -> None:
        """Update player state from keyboard input.

        Polymorphism: Player update responds to input.
        """
        move_x, move_y = self._read_input(keys)
        self._x += move_x * self._speed
        self._y += move_y * self._speed

        self._rect.x = int(self._x)
        self._rect.y = int(self._y)

        self._clamp_to_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Very simple passive mana regeneration.
        if self._mana < self._max_mana:
            self._mana += 1
        self._spell_effect.tick()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player and any active spell cast visual."""
        super().draw(surface)
        self._spell_effect.draw(surface, self.rect.center)


class SpellCastEffect:
    """Small retro spell visual that animates for a few frames."""

    def __init__(self) -> None:
        """Initialise an inactive visual effect."""
        self._target: tuple[int, int] | None = None
        self._frames_left = 0
        self._duration_frames = SPELL_EFFECT_DURATION_FRAMES
        self._color = SPELL_EFFECT_COLOR

    @property
    def is_active(self) -> bool:
        """Return True while the effect should be drawn."""
        return self._target is not None and self._frames_left > 0

    def trigger(self, target: tuple[int, int]) -> None:
        """Start the visual animation toward the spell target."""
        self._target = target
        self._frames_left = self._duration_frames

    def tick(self) -> None:
        """Advance animation by one frame."""
        if self._frames_left <= 0:
            self._target = None
            return
        self._frames_left -= 1
        if self._frames_left == 0:
            self._target = None

    def draw(self, surface: pygame.Surface, origin: tuple[int, int]) -> None:
        """Render a fading retro beam and target marker."""
        if not self.is_active or self._target is None:
            return

        progress = self._frames_left / self._duration_frames
        beam_width = max(1, int(4 * progress))
        marker_size = max(4, int(10 * progress))
        marker_rect = pygame.Rect(
            self._target[0] - marker_size // 2,
            self._target[1] - marker_size // 2,
            marker_size,
            marker_size,
        )

        pygame.draw.line(surface, self._color, origin, self._target, beam_width)
        pygame.draw.rect(surface, self._color, marker_rect, width=1)
