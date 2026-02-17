from mesh import Mesh
from src.models import MeshModel, MeshParamsModel
from src.mesh_params import PhysicalParams
import json

class Snowflake:
    _mesh : Mesh
    _params : PhysicalParams

    def __init__(self, path : str):
        self._path = path

    @classmethod
    def mesh(cls, nb_rings : int):
        return Mesh(nb_rings)

    def initial_state_triangle(self):
        list_cells = [(0,0), (1,0), (1,2), (1,4)]
        for id in list_cells:
            pass
    
    def save_simulation(self):
        mesh_model = MeshModel.from_domain(self._mesh)
        with open(self._path + "mesh.json", "w") as f:
            f.write(mesh_model.model_dump_json())
    
    def load_simulation(self):
        with open(self._path + "mesh.json", "r") as f:
            data = json.load(f)
        mesh_model = MeshModel.model_validate(data)
        return mesh_model
    
    @classmethod
    def mesh_dirichlet(cls):
        pass
    def run_simulation(self, number_iterations : int = 100):
        for i in range(number_iterations):
            self._mesh.step(self._params)
        return self._mesh
    
    def update_params(self, mesh_params_model : MeshParamsModel):
        self._params = mesh_params_model.to_domain()
        return mesh_params_model