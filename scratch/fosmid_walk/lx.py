import os, sys
import shutil
from pathlib import Path
import time
import random
from typing import Any
import limes_x as lx
from limes_x import Item, Params, InputGroup

modules = lx.LoadComputeModules("/home/tony/workspace/grad/Limes-hts/submodules/Limes-compute-modules/high_throughput_screening")
wf = lx.Workflow(modules, "/home/tony/workspace/grad/Limes-hts/data/ref")

inputs = [
    InputGroup(by=(Item("all"), "all"), children={
        Item("fosmid vector backbone sequence"): "pcc1",
        Item("fosmid reads"): Path("/home/tony/workspace/grad/Fosmid_walk/scratch/lake-test.fastq"),
    })
]

wf.Run(
    workspace="/home/tony/workspace/grad/Limes-hts/scratch/fosmid_walk/cache/lx_test",
    targets=[Item("fosmid pool population estimate csv")],
    given=inputs,
    executor=lx.Executor(),
)
