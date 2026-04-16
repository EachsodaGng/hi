"""Regression tests to ensure the bot token is validated before the script runs."""

import importlib
import os
import sys
import unittest


class TestBotTokenPresence(unittest.TestCase):
    """Verify that bot.py requires a non-empty DISCORD_BOT_TOKEN."""

    def _import_bot(self):
        """Import (or re-import) bot.py and return the module."""
        # Remove cached module so the top-level guard runs again
        if "bot" in sys.modules:
            del sys.modules["bot"]
        return importlib.import_module("bot")

    def test_missing_token_raises(self):
        """bot.py must raise RuntimeError when DISCORD_BOT_TOKEN is unset."""
        env = os.environ.copy()
        os.environ.pop("DISCORD_BOT_TOKEN", None)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                self._import_bot()
            self.assertIn("DISCORD_BOT_TOKEN", str(ctx.exception))
        finally:
            os.environ.clear()
            os.environ.update(env)

    def test_empty_token_raises(self):
        """bot.py must raise RuntimeError when DISCORD_BOT_TOKEN is empty."""
        env = os.environ.copy()
        os.environ["DISCORD_BOT_TOKEN"] = ""
        try:
            with self.assertRaises(RuntimeError) as ctx:
                self._import_bot()
            self.assertIn("DISCORD_BOT_TOKEN", str(ctx.exception))
        finally:
            os.environ.clear()
            os.environ.update(env)

    def test_valid_token_does_not_raise(self):
        """bot.py must NOT raise when DISCORD_BOT_TOKEN is set to a non-empty value."""
        env = os.environ.copy()
        os.environ["DISCORD_BOT_TOKEN"] = "test-token-value"
        try:
            # The import will still fail later (e.g. missing network),
            # but it must get past the token guard without RuntimeError.
            try:
                self._import_bot()
            except RuntimeError as e:
                if "DISCORD_BOT_TOKEN" in str(e):
                    self.fail(
                        "RuntimeError about DISCORD_BOT_TOKEN raised even though "
                        "the token was provided."
                    )
        finally:
            os.environ.clear()
            os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
