from pydantic import BaseModel
from src.cell import Cell
from mesh import Mesh
from src.mesh_params import PhysicalParams


class CellModel(BaseModel):
    id : tuple[int, int]
    temperature : float = 0
    vapor : float = 0
    ice_potential : float = 0
    frozen : bool = False

    @classmethod
    def from_domain(cls, cell : Cell):
        return CellModel(
            id=cell.id,
            temperature=cell.temperature,
            vapor=cell.vapor,
            ice_potential=cell.ice_potential,
            frozen=cell.frozen
        )

class MeshModel(BaseModel):
    nb_rings : int
    dict_cells : dict[tuple[int, int], CellModel] = {}
    frozen_cells : set[tuple[int, int]] = set()
    non_frozen_cells : set[tuple[int, int]] = set()
    
    @classmethod
    def from_domain(cls, mesh : Mesh):
        return MeshModel(
            nb_rings=mesh.nb_rings,
            dict_cells={id : CellModel.from_domain(cell) for id, cell in mesh.dict_cells.items()},
            frozen_cells=mesh.frozen_cells,
            non_frozen_cells=mesh.non_frozen_cells
        )

class MeshParamsModel(BaseModel):
    alpha_temperature : float
    alpha_vapor : float
    alpha_condensation : float
    vapor_saturation : float
    ice_threshold : float 
    temperature_threshold : float
    n_frozen_neighbors_threshold : int
    
    @classmethod
    def from_domain(cls, params : PhysicalParams):
        return MeshParamsModel(
            alpha_temperature= params.alpha_temperature,
            alpha_vapor= params.alpha_vapor,
            alpha_condensation= params.alpha_condensation,
            vapor_saturation= params.vapor_saturation,
            ice_threshold= params.ice_threshold, 
            temperature_threshold= params.temperature_threshold,
            n_frozen_neighbors_threshold = params.n_frozen_neighbors_threshold
        )    
    def to_domain(self):
        return PhysicalParams(
            alpha_temperature= self.alpha_temperature,
            alpha_vapor= self.alpha_vapor,
            alpha_condensation= self.alpha_condensation,
            vapor_saturation= self.vapor_saturation,
            ice_threshold= self.ice_threshold, 
            temperature_threshold= self.temperature_threshold,
            n_frozen_neighbors_threshold= self.n_frozen_neighbors_threshold
        )