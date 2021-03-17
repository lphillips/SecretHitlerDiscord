import unittest
import asyncio
import logging
from unittest.mock import Mock, MagicMock
from discord.ext import commands
import discord
from secret_hitler import app
from secret_hitler import config

# Disable logging during testing
logging.disable()


class AsyncMock(unittest.mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


def create_mock_named(name):
    mock_named = Mock()
    mock_named.name = name
    return mock_named


class SetupAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_guild = Mock()
        self. mock_guild.emojis = map(create_mock_named, config.configuration["emoji"])

        mock_category = Mock()
        mock_category.name = config.configuration["category"]
        mock_category.channels = map(create_mock_named, config.configuration["channels"])
        self.mock_guild.categories = [mock_category]

        self.mock_ctx = Mock()
        self.mock_ctx.guild = self.mock_guild

    def test_setup_missing_permissions(self):
        mock_permissions = discord.Permissions()
        mock_permissions.update(
            manage_roles=True,
            manage_emojis=True,
            manage_channels=True,
            send_messages=False
        )
        self.mock_guild.me = Mock()
        self.mock_guild.me.guild_permissions = mock_permissions
        setup_success = asyncio.get_event_loop().run_until_complete(app.setup(self.mock_guild))
        self.assertFalse(setup_success)

    def test_setup_success(self):
        mock_permissions = discord.Permissions()
        mock_permissions.update(
            manage_roles=True,
            manage_emojis=True,
            manage_channels=True,
            send_messages=True
        )
        self.mock_guild.me = Mock()
        self.mock_guild.me.guild_permissions = mock_permissions
        setup_success = asyncio.get_event_loop().run_until_complete(app.setup(self.mock_guild))
        self.assertTrue(setup_success)


if __name__ == '__main__':
    unittest.main()
