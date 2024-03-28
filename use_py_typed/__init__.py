"""
Your library should provide a py.typed file.
"""

from pathlib import Path

import advice_animal

PY_TYPED = "py.typed"


class Check(advice_animal.BaseCheck):
    confidence = advice_animal.FixConfidence.GREEN

    def check(self) -> bool:
        """
        Returns whether this advice wants to run
        """
        if self.env.top_level_dir is None:
            return False
        return not (self.env.path / self.env.top_level_dir / PY_TYPED).exists()

    def apply(self, workdir: Path) -> None:
        (workdir / self.env.top_level_dir / PY_TYPED).touch()
