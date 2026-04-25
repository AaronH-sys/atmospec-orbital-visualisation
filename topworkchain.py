from subworkchains import OrcaWorkChain, NTOProcessingWorkChain
from parsercalcfunction import parse_orca_output
from aiida.orm import Dict, SinglefileData, FolderData
from aiida.engine import WorkChain, run_get_node, run

class PrototypeTopWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)

        spec.output("cube_folder",
                    valid_type=FolderData,
                    help="Compressed cube files")
        
        spec.output("transition_info",
                    valid_type=Dict,
                    help="Information about the relevant electronic transitions.")

        spec.outline(
            cls.calc,
            cls.parse,
            cls.convert
        )

    def calc(self):
        # Geometry optimization using B3LYP functional and DEF2-SVP basis set, then
        # TDDFT calculation of 30 excited states, with NTOs calculated for each.

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
        print(node)

        #Return nto_folder to context for other functions to use
        self.ctx.nto_folder = results["nto_folder"]
    
    
    def parse(self):
        # Parses the ORCA output file to find relevant molecular orbitals to plot as cube files for each excited state.
        # In this case, relevant orbitals are ones above the contribution threshold of 5%.

        self.ctx.relevant_dict = parse_orca_output(self.ctx.nto_folder, "aiida.out", threshold=5.0)
        self.out("transition_info", self.ctx.relevant_dict)

    
    def convert(self):
        builder = NTOProcessingWorkChain.get_builder()
        builder.nto_folder = self.ctx.nto_folder
        #results, node = run_get_node(NTOProcessingWorkChain, builder)
        #Returns a folder containing all of the compressed cube files (currently just one).
        cube_folder = FolderData()
        #Create a list of tuples containing relevant mo data for each excitation. 
        relevant_items = list(self.ctx.relevant_dict.items())
        #Iterating through the list.
        for excitation in relevant_items:
            #Set excitation.
            s=excitation[0]
            builder.s = s
            for electron_hole_pair in excitation[1]:

                for moa in electron_hole_pair[0]:
                    #Set specific mo.
                    mo = moa[:-1]
                    builder.mo = mo
                    results, node = run_get_node(NTOProcessingWorkChain, builder)
                    for label, value in results.items():
                        print(value)
                        with value.open(mode="rb") as file:
                            cube_folder.put_object_from_filelike(file, path=("s"+s+"."+mo))
        cube_folder.store()
        self.out("cube_folder", cube_folder)



    






