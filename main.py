"""VOICEVOX playground entrypoint."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the playground entrypoint."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Hello from voicevox-playground!")


if __name__ == "__main__":
    main()
