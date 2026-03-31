#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 run.py <input_dir>")
    sys.exit(1)

input_dir = os.path.expanduser(sys.argv[1])
name = os.path.basename(input_dir.rstrip("/"))

sys.argv = [
    "pydeps",
    input_dir,
    "--max-module-depth", "3",
    "--max-module-depth-override", "aiter:5",
    "--max-module-depth-override", "sglang.srt.models.deepseek_v2:4",
    "--max-module-depth-override", "sglang.srt.layers.attention.nsa.nsa_indexer:5",
    "--include-missing",
    "--rankdir", "LR",
    "--include-external", "aiter",
    "-o", f"{name}_depth3.svg",
    "--dot-output", f"{name}_depth3.dot",
    "--highlight", "sglang.srt.models.deepseek_v2", "sglang.srt.layers.attention.nsa",
]

from pydeps.pydeps import pydeps
pydeps()
