import pytest
from src.cell import Cell
from src.mesh import Mesh
from src.snowflake import Snowflake
from src.initialization_params import InitParams
from src.physical_params import PhysicalParams
from src.simul_params import SimulParams
from typing import Callable

CellMaker = Callable[[tuple[int, int], set[tuple[int, int]], str, float, float, float, bool], Cell]
@pytest.fixture()
def simple_cell() -> CellMaker:
    def make_cell(id : tuple[int, int ]=(0,0), neighbors : set[tuple[int, int]] = {(1,i) for i in range(6)}, position : str = "center", temperature : float =-10., vapor : float =1., ice_potential : float =0., frozen : bool =True) -> Cell:
        c = Cell(id=id,
                neighbors=neighbors,
                position=position,
                temperature=temperature,
                vapor=vapor,
                ice_potential=ice_potential,
                frozen=frozen)
        return c
    return make_cell

MeshMaker = Callable[[int], Mesh]
@pytest.fixture()
def simple_mesh() -> MeshMaker:
    def make_mesh(size : int = 6) -> Mesh:
        m = Mesh(size)
        return m
    return make_mesh

SnowflakeMaker = Callable[[int, int, float, float, float, float, float, float, int], Snowflake]
@pytest.fixture()
def simple_snowflake() -> SnowflakeMaker:
    def make_snowflake(size : int = 6, iterations : int = 10, alpha_temperature : float = 0.5, alpha_vapor: float = 0.5, alpha_condensation : float = 0.5, vapor_saturation : float = 0.5, ice_threshold : float = 0, temperature_threshold : float = 0, n_frozen_neighbors_threshold : int = 3) -> Snowflake:
        s = Snowflake()
        init_params = InitParams(size= size
        )
        simul_params = SimulParams(iterations=iterations
                            )
        physical_params = PhysicalParams(alpha_temperature= alpha_temperature, 
                                         alpha_vapor=  alpha_vapor,
                                         alpha_condensation= alpha_condensation,
                                        vapor_saturation= vapor_saturation,
                                        ice_threshold= ice_threshold, 
                                        temperature_threshold= temperature_threshold,
                                        n_frozen_neighbors_threshold= n_frozen_neighbors_threshold
                            )
        s.update_initilization_params(init_params)
        s.update_physical_params(physical_params)
        s.update_simulation_params(simul_params)
        s.build()
        return s
    return make_snowflake