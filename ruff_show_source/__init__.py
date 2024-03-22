from pathlib import Path
import imperfect

import advice_animal

FIXABLE_ENTRIES = ("commands",)

class Check(advice_animal.Check):
    def pred(self) -> bool:
        return (f:=(self.env.path / "tox.ini")).exists() and "--show-source" in f.read_text()

    def apply(self, workdir: Path) -> None:
        path = workdir / "tox.ini"
        obj = imperfect.parse_string(path.read_text())
        for section in obj.sections:
            if section.name.startswith("testenv"):
                try:
                    entry = section.entries[section.index("commands")]
                    for line in entry.value:
                        line.text = line.text.replace("--show-source", "--output=full")
                except KeyError:
                    pass
        path.write_text(obj.text)
