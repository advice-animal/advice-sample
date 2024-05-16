import ast
import json
import subprocess

def main():
    linters = json.loads(subprocess.check_output(["ruff", "linter", "--output-format=json"], encoding="utf-8"))
    select = json.loads(subprocess.check_output(["ruff", "config", "lint.select", "--output-format=json"], encoding="utf-8"))

    default = ast.literal_eval(select["default"])
    outputs = []

    def handle(a, b):
        if a in default:
            outputs.append((a, f"{a!r}, # {b}"))
        else:
            outputs.append((a, f"#{a!r}, # {b}"))
            if t := [d for d in default if d.startswith(a)]:
                for i in t:
                    outputs.append((i, f"{i!r}, # {b}"))

    for entry in linters:
        if "categories" in entry:
            for cat in entry["categories"]:
                prefix = entry["prefix"] + cat["prefix"]
                name = entry["name"] + " " + cat["name"]
                handle(prefix, name)
        else:
            handle(entry["prefix"], entry["name"])

    print("[tool.ruff.lint]")
    print("select = [")
    for _, line in sorted(outputs):
        print("    " + line)
    print("]")

if __name__ == "__main__":
    main()

