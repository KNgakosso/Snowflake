from pydantic import BaseModel, Field
from backend.cell import Cell
from backend.mesh import Mesh
from backend.initialization_params import InitParams
from backend.physical_params import PhysicalParams
from backend.simul_params import SimulParams
from backend.snowflake import Snowflake

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
    size : int
    cells : list[CellModel] = Field(default_factory = list)
    
    @classmethod
    def from_domain(cls, mesh : Mesh):
        return MeshModel(
            size=mesh.size,
            cells=[CellModel.from_domain(cell) for cell in mesh.cells()],
        )

class PhysicalParamsModel(BaseModel):
    alpha_temperature : float
    alpha_vapor : float
    beta_vapor : float
    alpha_condensation : float
    vapor_saturation : float
    ice_threshold : float 
    temperature_threshold : float
    n_frozen_neighbors_threshold : int
    
    @classmethod
    def from_domain(cls, params : PhysicalParams):
        return PhysicalParamsModel(
            alpha_temperature= params.alpha_temperature,
            alpha_vapor= params.alpha_vapor,
            beta_vapor= params.beta_vapor,
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
            beta_vapor= self.beta_vapor,
            alpha_condensation= self.alpha_condensation,
            vapor_saturation= self.vapor_saturation,
            ice_threshold= self.ice_threshold, 
            temperature_threshold= self.temperature_threshold,
            n_frozen_neighbors_threshold= self.n_frozen_neighbors_threshold
        )
    
class SimulParamsModel(BaseModel):
    iterations : int
    
    @classmethod
    def from_domain(cls, params : SimulParams):
        return SimulParamsModel(
                iterations= params.iterations
        )    
    def to_domain(self):
        return SimulParams(
            iterations = self.iterations
        )
    
class InitParamsModel(BaseModel):
    size : int
    
    @classmethod
    def from_domain(cls, params : InitParams):
        return InitParamsModel(
                size = params.size
        )    
    def to_domain(self):
        return InitParams(
            size = self.size
        )

class SnowflakeModel(BaseModel):
    mesh : MeshModel
    physical_params : PhysicalParamsModel
    simulation_params: SimulParamsModel

    @classmethod
    def from_domain(cls, snowflake : Snowflake):
        return SnowflakeModel(
            mesh= MeshModel.from_domain(snowflake._mesh),
            physical_params= PhysicalParamsModel.from_domain(snowflake._physical_params),
            simulation_params= SimulParamsModel.from_domain(snowflake._simulation_params)
        )
    
class UpdateSelectionModel(BaseModel):
    value : float
    set_cells_id : set[tuple[int, int]] | None

class SelectionModel(BaseModel):
    set_cells_id : set[tuple[int, int]] | None