from subworkchains import OrcaWorkChain, NTOProcessingWorkChain
from aiida.orm import Dict, SinglefileData, FolderData
from aiida.engine import WorkChain, run_get_node, run

class PrototypeTopWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.output("cube_folder", valid_type=FolderData, help="Compressed cube files")
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
        #Returns a folder containing all of the compressed cube files (currently just one).
        cube_folder = FolderData()
        for label, value in results.items():
            print(value)
            with value.open(mode="rb") as file:
                cube_folder.put_object_from_filelike(file, path=label)
        cube_folder.store()
        self.out("cube_folder", cube_folder)



    






