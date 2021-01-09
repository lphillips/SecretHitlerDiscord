import unittest
import asyncio
from unittest.mock import Mock, MagicMock
from discord.ext import commands
import discord
from secret_hitler import app


class AsyncMock(unittest.mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class StartGameAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        mock_guild = Mock()
        mock_guild.create_role = AsyncMock()
        mock_guild.categories = [Mock(), Mock(), Mock()]
        mock_guild.categories[0].name = "Category 1"
        mock_guild.categories[1].name = "Secret Hitler"
        mock_guild.categories[2].name = "The Last One"

        self.mock_ctx = Mock()
        self.mock_ctx.guild = mock_guild
        self.mock_ctx.send = AsyncMock()

    def test_start_game_no_category(self):
        """Tests if start_game fails gracefully when the app's Discord category is missing"""
        self.mock_ctx.guild.categories = [Mock(), Mock()]
        self.mock_ctx.guild.categories[0].name = "Not Secret Hitler"
        self.mock_ctx.guild.categories[1].name = "Croissants"
        asyncio.run(app.start_game(self.mock_ctx, "private", 10))
        self.mock_ctx.send.assert_called()

    def test_start_game_missing_create_role_permission(self):
        """Tests if start_game fails gracefully when the create_role permission is not set"""
        mock_response = MagicMock()
        mock_response.status = 403
        self.mock_ctx.guild.create_role.side_effect = discord.Forbidden(mock_response, "mock Forbidden exception")
        asyncio.run(app.start_game(self.mock_ctx, "private", 10))
        self.mock_ctx.send.assert_called()


if __name__ == '__main__':
    unittest.main()
