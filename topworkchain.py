from subworkchains import OrcaWorkChain, NTOProcessingWorkChain
from aiida.orm import Dict
from aiida.engine import WorkChain, run_get_node, run

class PrototypeTopWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.outline(
            cls.calc,
            cls.convert
        )

    def calc(self):
        inputs = {
        "parameters" : Dict(dict={
        "charge": 0,
        "multiplicity": 1,
        "input_blocks":{
            "tddft": {"nroots": 30, "donto": True}
        },
        "input_keywords": ["B3LYP", "DEF2-SVP", "LARGEPRINT"]
        })}
        results, node = run_get_node(OrcaWorkChain, **inputs)
        self.ctx.nto_folder = results["nto_folder"]
    
    def convert(self):
        builder = NTOProcessingWorkChain.get_builder()
        builder.nto_folder = self.ctx.nto_folder
        results, node = run_get_node(NTOProcessingWorkChain, builder)

    






