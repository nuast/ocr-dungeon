"""Tests for player spell visual behaviour."""

import unittest

import pygame

from enemy import Enemy
from player import Player
from settings import SPELL_EFFECT_DURATION_FRAMES


class _NoMovementKeys:
    """Minimal key wrapper that reports no keys as pressed."""

    def __getitem__(self, _: int) -> int:
        return 0


class TestPlayerSpellVisual(unittest.TestCase):
    """Validate spell casting visual state changes."""

    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def test_cast_spell_starts_visual_effect(self) -> None:
        player = Player(100, 100)
        enemy = Enemy(120, 100)

        did_cast = player.cast_spell([enemy])

        self.assertTrue(did_cast)
        self.assertTrue(player.has_active_spell_effect)

    def test_failed_cast_does_not_start_visual_effect(self) -> None:
        player = Player(100, 100)
        enemy = Enemy(350, 350)

        did_cast = player.cast_spell([enemy])

        self.assertFalse(did_cast)
        self.assertFalse(player.has_active_spell_effect)

    def test_spell_visual_expires_after_duration(self) -> None:
        player = Player(100, 100)
        enemy = Enemy(120, 100)

        player.cast_spell([enemy])
        keys = _NoMovementKeys()
        for _ in range(SPELL_EFFECT_DURATION_FRAMES):
            player.update(keys, [enemy])

        self.assertFalse(player.has_active_spell_effect)
