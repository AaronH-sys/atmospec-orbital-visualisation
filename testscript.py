from basic_orca_calc import OrcaWorkChain
from aiida.orm import Dict
from aiida.engine import run

inputs = {
    "parameters" : Dict(dict={
        "charge": 0,
        "multiplicity": 1,
        "input_blocks":{
            "tddft": {"nroots": 30, "donto": True}
        },
        "input_keywords": ["B3LYP", "DEF2-SVP", "LARGEPRINT"]
    })
}

run(OrcaWorkChain, **inputs)