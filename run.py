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
    "--max-module-depth-override", "sglang.srt.layers.attention:4",
    "--max-module-depth-override", "sglang.srt.layers.attention.nsa_backend:5",
    "--max-module-depth-override", "sglang.srt.layers.attention.aiter_backend:5",
    "--max-module-depth-override", "sglang.srt.layers.moe.rocm_moe_utils:5",
    "--max-module-depth-override", "sglang.srt.layers.quantization:4",
    "--max-module-depth-override", "sglang.srt.layers.quantization.fp8:5",
    "--max-module-depth-override", "sglang.srt.layers.quantization.rocm_mxfp4_utils.py:5",
    "--max-module-depth-override", "sglang.srt.layers.attention.nsa.nsa_indexer:6",
    "--include-missing",
    "--rankdir", "LR",
    "--include-external", "aiter",
    "-xx", "sglang", "aiter", "sglang.srt",
    "-o", f"{name}_depth3.svg",
    "--dot-output", f"{name}_depth3.dot",
    "--highlight", "sglang.srt.models.deepseek_v2", "sglang.srt.layers.attention.nsa", "sglang.srt.layers.attention.nsa.nsa_indexer", "sglang.srt.layers.attention.nsa_backend", "sglang.srt.layers.attention.aiter_backend", "sglang.srt.layers.quantization:yellow", "sglang.srt.speculative:orange"
]

from pydeps.pydeps import pydeps
pydeps()
