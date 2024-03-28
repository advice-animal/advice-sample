"""
Functions decorated with @click.command should also use @click.version_option
"""

import ast
import glob
from pathlib import Path

import advice_animal


class Check(advice_animal.BaseCheck):
    confidence = advice_animal.FixConfidence.GREEN

    def check(self) -> bool:
        """
        Returns whether this advice wants to run
        """
        return bool(self._internal(self.env.path, dry_run=True))

    def _internal(self, path: Path, dry_run: bool):
        all_py_files = self.env.get(glob.glob, "**/*.py", root_dir=path, recursive=True)
        for f in all_py_files:
            data = (path / f).read_text()
            if "click" not in data:
                continue

            mod = self.env.get(ast.parse, data)
            lines = data.splitlines(True)

            # Only check top-level definitions for now, in reverse order in case
            # lines get modified.
            for node in mod.body[::-1]:
                if isinstance(node, ast.FunctionDef) and node.decorator_list:
                    if (
                        # must be click-decorated
                        ast.unparse(node.decorator_list[0])
                        in ("click.command()", "click.group()")
                        and
                        # must not already have version_option
                        not any(
                            ast.unparse(x).startswith("click.version_option(")
                            for x in node.decorator_list[1:]
                        )
                    ):
                        if dry_run:
                            return True
                        else:
                            # TODO indent if we ever check deeper ones
                            line = node.decorator_list[0].end_lineno
                            lines[line:line] = ["@click.version_option()\n"]
            if not dry_run:
                (path / f).write_text("".join(lines))

    def apply(self, workdir: Path) -> None:
        self._internal(workdir, dry_run=False)
