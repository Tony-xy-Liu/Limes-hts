import os
from pathlib import Path
from typing import Any
import limes_x as lx
from limes_x import Item, Params, InputGroup

modules = lx.LoadComputeModules("../../submodules/Limes-compute-modules/high_throughput_screening")
wf = lx.Workflow(modules, "../../data/ref")

def slurm(job: lx.Job) -> tuple[bool, str]:
    job.context.output_folder
    return job.Shell(f"""\
        export SLURM_TMPDIR={os.path.abspath(job.workspace.joinpath('../tmp'))}
        cd {job.context.output_folder}
        /bin/sh -c "{job.run_command}"
    """)

workspace = "./cache/ws01"
os.system(f"rm -r {workspace}")
given: Any = {
    InputGroup(by=(Item('sample'), "test-lake"), children={
        Item('fosmid hits'): Path("../../data/test/LAKE_ligninases_pool_primary_hits.fastq"),
        Item('read parity'): "interleaved",
        Item('fosmid background'): Path("../../data/test/ecoli_k12_mg1655.fasta"),
        Item('assembler name'): "megahit",
        Item('fosmid count estimate'): "384",
    })
}

targets = {
    Item('fosmid assembly')
}

params = Params(
    threads=2,
    file_system_wait_sec=0,
)
x = wf.Run(
    workspace=workspace,
    targets=targets, given=given,
    executor=lx.CloudExecutor(cloud_procedure=slurm, tmp_dir_name="SLURM_TMPDIR"),
    # executor=lx.CloudExecutor(zipped_inputs=Path(os.path.realpath("./cache/zipped/")), execute_procedure=slurm),
    # executor=lx.Executor(),
    params=params,
    _catch_errors = False,
)