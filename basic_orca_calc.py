from aiida.engine import WorkChain, ToContext, run_get_node
from aiida.orm import SinglefileData, StructureData, Dict, load_code
from aiida.plugins import CalculationFactory


OrcaCalculation = CalculationFactory("orca.orca")
# Workchain for a basic ORCA calculation.
class OrcaWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        #spec.input("geometry", valid_type = SinglefileData, help="Test geometry (.xyz file)")
        spec.input("parameters", valid_type = Dict, help = "Dictionary of orca parameters")
        spec.outline(
            cls.submit_calc
        )
    
    def submit_calc(self):
        #Create a builder object for the orca plugin.
        builder = OrcaCalculation.get_builder()
        #Load orca
        builder.code = load_code("orca@localhost")
        #Construct a test molecule (acrolein)
        structure = StructureData()
        structure.append_atom(position=(-0.58780, -0.39670, -0.00030), symbols="C")
        structure.append_atom(position=(-1.68290, 0.12550, -0.00000), symbols="O")
        structure.append_atom(position=(0.61750, 0.43190, 0.00020), symbols="C")
        structure.append_atom(position=(1.82210, -0.14250, -0.00010), symbols="C")
        structure.append_atom(position=(-0.50290, -1.47330, 0.00350), symbols="H")
        structure.append_atom(position=(0.53260, 1.50860, 0.00090), symbols="H")
        structure.append_atom(position=(1.90700, -1.21920, -0.00080), symbols="H")
        structure.append_atom(position=(2.71210, 0.46930, 0.00030), symbols="H")
        structure.pbc = (False, False, False)
        #Pass structure to the builder object
        builder.structure = structure
        #set parameters
        builder.parameters = self.inputs.parameters

        # builder.metadata.options.resources = {
        #     'num_machines': 1,
        #     'num_mpiprocs_per_machine': 1
        # }

        builder.metadata.options = {
            "additional_retrieve_list": ["*.nto", "aiida.gbw"],
            "resources": {'num_machines': 1, 'num_mpiprocs_per_machine': 1},
        }
        #Run ORCA (requires RabbitMQ, not configured by default on the "presto" profile)
        #process = self.submit(builder)
        _result, process = run_get_node(builder)
        self.ctx.orca_calc = process

        #return ToContext(calc=process)

    