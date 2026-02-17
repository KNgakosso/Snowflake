import pytest
from src.cell import Cell
from src.mesh import Mesh
from typing import Callable

CellMaker = Callable[[tuple[int, int], set[tuple[int, int]], str, float, float, float, bool], Cell]
@pytest.fixture()
def simple_cell() -> CellMaker:
    def cell_make(id : tuple[int, int ]=(0,0), neighbors : set[tuple[int, int]] = {(1,i) for i in range(6)}, position : str = "center", temperature : float =-10., vapor : float =1., ice_potential : float =0., frozen : bool =True) -> Cell:
        c = Cell(id=id,
                neighbors=neighbors,
                position=position,
                temperature=temperature,
                vapor=vapor,
                ice_potential=ice_potential,
                frozen=frozen)
        return c
    return cell_make

MeshMaker = Callable[[int], Mesh]
@pytest.fixture()
def simple_mesh() -> MeshMaker:
    def make_mesh(nb_rings : int = 6, temperature : float = 0, vapor : float = 0) -> Mesh:
        m = Mesh(nb_rings)
        m.set_temperature(temperature)
        m.set_vapor(vapor)
        return m
    return make_mesh