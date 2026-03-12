from src.cell import Cell
import pytest
from typing import Callable

CellMaker = Callable[[tuple[int, int], set[tuple[int, int]], str, float, float, float, bool], Cell]


# TEST __INIT__
##########################################
def test_init_cell_default_values():
    id = (0,0)
    neighbors = set()
    position = "center"
    c = Cell(id=id,
             neighbors=neighbors,
             position=position
        )
    assert c.temperature == 0
    assert c.vapor == 0
    assert c.ice_potential == 0
    assert not c.frozen

# TEST CONDENSATION
##########################################

@pytest.mark.parametrize("vapor, vapor_saturation, ice_potential, alpha",[
    (2.,  4,  0.,  1.,),
    (0.09, 0.1,  10., 0.001),
    (2, 40.,   1.,  0.),
    (0.,  10.,  4.,  0.5),
    (10.3, 10.3, 70, 0.5)
])
def test_condensation_vapor_saturated(vapor, vapor_saturation, ice_potential, alpha, simple_cell):
    cell : Cell = simple_cell(vapor=vapor, ice_potential=ice_potential)
    cell.condensation(alpha_condensation=alpha, vapor_saturation=vapor_saturation)
    assert cell.vapor == vapor
    assert cell.ice_potential == ice_potential

@pytest.mark.parametrize("vapor, vapor_saturation, ice_potential, alpha",[
    (10.,  1,  0.,  1.),
    (1., 0.999,  10., 0.001),
    (2.,   0, 1.,  0.),
    (1e10,   3., 2,  0.5)
])
def test_condensation_vapor_non_saturated(vapor, vapor_saturation, ice_potential, alpha, simple_cell):
    cell : Cell = simple_cell(vapor=vapor, ice_potential=ice_potential)
    cell.condensation(alpha_condensation=alpha, vapor_saturation=vapor_saturation)
    assert cell.vapor <= vapor
    assert cell.vapor >= vapor_saturation
    assert cell.ice_potential >= ice_potential

@pytest.mark.parametrize("vapor, vapor_saturation, ice_potential, alpha",[
    (2.,   1e7,  0.,  0.),
    (0.09,  0.2, 10., 0.),
    (40.,   90, 1.,  0),
    (4.,  1,  4.,  0)
])
def test_condensation_alpha_0(simple_cell, vapor, ice_potential, alpha, vapor_saturation):
    cell: Cell = simple_cell(vapor=vapor, ice_potential=ice_potential)
    cell.condensation(alpha_condensation=alpha, vapor_saturation=vapor_saturation)
    assert cell.vapor == pytest.approx(vapor)
    assert cell.ice_potential == pytest.approx(ice_potential)

@pytest.mark.parametrize("vapor, vapor_saturation, ice_potential, alpha",[
    (4.,  2,   0.,  1.),
    (0.1, 0.09,   10., 1.),
    (40.,  2,   1., 1),
    (4.,   0,   4.,  1)
])
def test_condensation_alpha_1_vapor_saturated(simple_cell, vapor, ice_potential, alpha, vapor_saturation):
    cell: Cell = simple_cell(vapor=vapor, ice_potential=ice_potential)
    cell.condensation(alpha_condensation=alpha, vapor_saturation=vapor_saturation)
    assert cell.vapor == pytest.approx(vapor_saturation)
    assert cell.ice_potential > ice_potential

# TEST VAPOR DIFFUSION
####################################

@pytest.mark.parametrize("neighbors, vapor_neighbors",[
    ({(2, 10), (1,1), (0, 0), (1,3), (1,4), (5, 1)},
     [2, 1, 0]), # 2 vapors missing
    ({(1,1), (1,0), (1,4), (2,3)}, # too much vapors
     [5, 4, 3, 2, 1]),  
])
def test_vapor_diffusion_wrong_amount_of_vapors(neighbors, vapor_neighbors, simple_cell):
    cell: Cell = simple_cell(neighbors=neighbors)

    with pytest.raises(ValueError):
        cell.vapor_diffusion(alpha_vapor=0.5, vapor_neighbors=vapor_neighbors)

@pytest.mark.parametrize("neighbors, vapor_neighbors, vapor, alpha_vapor",[
    ({(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)},
     [1, 2, 3, 4, 5, 6], 7, 0.2),
    ({(0,0), (1,0), (1,4)},
     [1, 2, 3], 4, 0.98),  
])
def test_vapor_diffusion_good_amount_of_vapors(neighbors, vapor_neighbors, vapor, alpha_vapor, simple_cell):
    cell: Cell = simple_cell(neighbors=neighbors, vapor = vapor)
    cell.vapor_diffusion(alpha_vapor=alpha_vapor, vapor_neighbors=vapor_neighbors)
    assert cell.vapor != vapor

@pytest.mark.parametrize("vapor_value",(-1e-7, 0, 9.6))
def test_vapor_diffusion_same_vapors(vapor_value, simple_cell):
    neighbors = {(3,0), (3,2), (2,0), (2,1)}
    vapor_neighbors = [vapor_value] * 4
    cell: Cell = simple_cell(neighbors=neighbors, vapor = vapor_value)
    cell.vapor_diffusion(alpha_vapor=1, vapor_neighbors=vapor_neighbors)
    assert cell.vapor == pytest.approx(vapor_value)

def test_vapor_diffusion_alpha_vapor_0(simple_cell):
    neighbors = {(3,0), (3,2), (2,0), (2,1)}
    vapor_neighbors = [1e1, 1e2, 1e3, 1e4]
    cell: Cell = simple_cell(neighbors=neighbors, vapor = 100)
    cell.vapor_diffusion(alpha_vapor=0, vapor_neighbors=vapor_neighbors)
    assert cell.vapor == pytest.approx(100)


# TEST TEMPERATURE DIFFUSION
####################################

@pytest.mark.parametrize("neighbors, temp_neighbors",[
    ({(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)},
     [1,2,3]), # 2 temperatures missing
    ({(0,0), (1,0), (1,4)}, # too much temperatures
     [1,2,3, 4, 5]),  
])
def test_temperature_diffusion_wrong_amount_of_temperatures(neighbors, temp_neighbors, simple_cell):
    cell: Cell = simple_cell(neighbors=neighbors)

    with pytest.raises(ValueError):
        cell.temperature_diffusion(alpha_temperature=0.5, temp_neighbors=temp_neighbors)

@pytest.mark.parametrize("neighbors, temp_neighbors, temperature, alpha_temperature",[
    ({(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)},
     [1, 2, 3, 4, 5, 6], 7, 0.2),
    ({(0,0), (1,0), (1,4)},
     [1, 2, 3], 4, 0.98),  
])
def test_temperature_diffusion_good_amount_of_temperatures(neighbors, temp_neighbors, temperature, alpha_temperature, simple_cell):
    cell: Cell = simple_cell(neighbors=neighbors, temperature = temperature)
    cell.temperature_diffusion(alpha_temperature=alpha_temperature, temp_neighbors=temp_neighbors)
    assert cell.temperature != temperature

@pytest.mark.parametrize("temp_value",(-10.555, 0, 1e-9, 50))
def test_temparature_diffusion_same_temperatures(temp_value, simple_cell):
    neighbors = {(3,0), (3,2), (2,0), (2,1)}
    temp_neighbors = [temp_value] * 4
    cell: Cell = simple_cell(neighbors=neighbors, temperature = temp_value)
    cell.temperature_diffusion(alpha_temperature=1, temp_neighbors=temp_neighbors)
    assert cell.temperature == pytest.approx(temp_value)

def test_temparature_diffusion_alpha_temp_0(simple_cell):
    neighbors = {(3,0), (3,2), (2,0), (2,1)}
    temp_neighbors = [1e1, 1e2, 1e3, 1e4]
    cell: Cell = simple_cell(neighbors=neighbors, temperature = 1e5)
    cell.temperature_diffusion(alpha_temperature=0, temp_neighbors=temp_neighbors)
    assert cell.temperature == pytest.approx(1e5)


# TEST FREEZE
####################################
@pytest.mark.parametrize("temperature,temperature_threshold", [(-10, -4.), (-1e-15, 0.), (5, 5.)])
@pytest.mark.parametrize("ice_potential,ice_threshold", [(7.4, 5), (4 + 1e-15, 4), (1,1)])
@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(1,4), (3,3), (6,2)])
def test_freeze_low_temp_high_ice(temperature, temperature_threshold, ice_potential, ice_threshold, n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = temperature, ice_potential = ice_potential, frozen = False)
    cell.freeze(ice_threshold=ice_threshold,
                temperature_threshold=temperature_threshold,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert cell.frozen
    assert cell.ice_potential == 0

@pytest.mark.parametrize("temperature,temperature_threshold", [(-10, 0.), (0, 0.), (5, 15.)])
@pytest.mark.parametrize("ice_potential,ice_threshold", [(7.4, 5), (4, 4), (14.1, 1)])
@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(1, 1), (6, 3), (4, 2)])
def test_freeze_cond1_and_cond2_OK_True(temperature, temperature_threshold, ice_potential, ice_threshold, n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = temperature, ice_potential = ice_potential, frozen = False)
    result = cell.freeze(ice_threshold=ice_threshold,
                temperature_threshold=temperature_threshold,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert cell.frozen
    assert cell.ice_potential == 0
    assert result


@pytest.mark.parametrize("temperature,temperature_threshold", [(-70, 0.), (1, 1.), (-200, 2.)])
@pytest.mark.parametrize("ice_potential,ice_threshold", [(10, 0), (14, 4), (14.1, 14.1)])
@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(1, 5), (5, 6)])
def test_cond1_OK_True(temperature, temperature_threshold, ice_potential, ice_threshold, n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = temperature, ice_potential = ice_potential, frozen = False)
    result = cell.freeze(ice_threshold=ice_threshold,
                temperature_threshold=temperature_threshold,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert cell.frozen
    assert cell.ice_potential == 0
    assert result

@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(6, 6), (2, 1)])
def test_freeze_cond2_OK_True(n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = 0, ice_potential = 0, frozen = False)
    result = cell.freeze(ice_threshold=40,
                temperature_threshold=-5,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert cell.frozen
    assert cell.ice_potential == 0
    assert result

@pytest.mark.parametrize("temperature,temperature_threshold", [(0, -70), (2, -22.)])
@pytest.mark.parametrize("ice_potential,ice_threshold", [(0, 10), (4, 14)])
@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(1, 3), (2, 4)])
def test_freeze_NOT_OK_False(temperature, temperature_threshold, ice_potential, ice_threshold, n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = temperature, ice_potential = ice_potential, frozen = False)
    result = cell.freeze(ice_threshold=ice_threshold,
                temperature_threshold=temperature_threshold,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert not cell.frozen
    assert not result


@pytest.mark.parametrize("temperature,ice_potential,temperature_threshold,ice_threshold", [
    (5, 0, 0., 10),     #too hot and not enough ice
    (-7, 0, 0., 10),    #not enough ice
    (5, 0, 15, 10),     #too hot
    ])
@pytest.mark.parametrize("n_frozen_neighbors,n_frozen_neighbors_threshold", [(0, 1), (2, 5)])
def test_freeze_frozen_neighbors(temperature, temperature_threshold, ice_potential, ice_threshold, n_frozen_neighbors,n_frozen_neighbors_threshold, simple_cell):
    cell: Cell = simple_cell(temperature = temperature, ice_potential = ice_potential, frozen = False)
    cell.freeze(ice_threshold=ice_threshold,
                temperature_threshold=temperature_threshold,
                n_frozen_neighbors_threshold=n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
    assert not cell.frozen
"""
# TEST TO_DICT
##########################################
@pytest.mark.parametrize("id, neighbors, vapor, temperature, ice_potential, state", [
    ((5,0), {(1,1), (2,2)}, 42., 3, 10., 1),
    ((9,9), {(3,4), (5,6)}, 0.00001, -13.1656, 40, 0),
    ((0,0), {(7,8), (9,10), (11,12)}, 7, -34656, 0, 0),
    ((18,60), {(13,14), (15,16), (17,18), (19,20)}, 0., -3, 0.0184, 0),
    ((1650,124), {(21,22), (23,24), (25,26), (27,28), (29,30)}, 24., 0.1458, 15.2, 1),
    ((2,1), {}, 0,0,0,0)
])
def test_cell_to_dict(id, neighbors, vapor, temperature, ice_potential, state):
    cell = Cell(id=id, neighbors=neighbors, vapor=vapor, temperature=temperature, ice_potential=ice_potential, state=state)
    cell_d = cell.to_dict()
    assert cell.id == cell_d["id"]
    assert cell.neighbors == cell_d["neighbors"]
    assert cell.vapor == cell_d["vapor"]
    assert cell.temperature == cell_d["temperature"]
    assert cell.ice_potential == cell_d["ice_potential"]
    assert cell.state == cell_d["state"]


# TEST_FROM_DICT
#############################
@pytest.mark.parametrize("id, neighbors, vapor, temperature, ice_potential, state", [
    ((5,11), {(1,1), (2,2)}, 2.4, 0.3, 100., 1),
    ((9,1), {(3,4), (5,6)}, 9.00001, -3.16, 420, 0),
    ((0,0), {(7,8), (9,10), (11,12)}, 77, -3466.99, 0, 0),
    ((20,0), {(13,14), (15,16), (17,18), (19,20)}, 0., -3, 20.0184, 1),
    ((2561,984), {(21,22), (23,24), (25,26), (27,28), (29,30)}, 274, 16, 15.2, 1)
])
def test_cell_from_dict(id, neighbors, vapor, temperature, ice_potential, state):
    cell_d ={
        "id" : id,
        "neighbors" : neighbors,
        "vapor" : vapor,
        "temperature" : temperature,
        "ice_potential" : ice_potential,
        "state" : state
    }
    cell = Cell.from_dict(cell_d)
    assert cell.id == cell_d["id"]
    assert cell.neighbors == cell_d["neighbors"]
    assert cell.vapor == cell_d["vapor"]
    assert cell.temperature == cell_d["temperature"]
    assert cell.ice_potential == cell_d["ice_potential"]
    assert cell.state == cell_d["state"]
"""