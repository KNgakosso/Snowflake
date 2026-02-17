from src.mesh import Mesh, compute_neighbors_arrete, compute_neighbors_bords, compute_neighbors_center, compute_neighbors_interieur, compute_neighbors_sommet
from src.cell import Cell
import pytest
from unittest.mock import patch, PropertyMock
import random
# TEST COMPUTE_NEIGHBORS
#########################################

def test_compute_neighbors_center():
     result = compute_neighbors_center()
     for neighbor in [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]:
          assert neighbor in result
     assert len(result) == 6


@pytest.mark.parametrize("id, expec_res", [
     ((1,0), [(0,0), (2,11), (2,0), (2,1), (1,1), (1,5)]),       #arrete 0 bas
     ((1,1), [(1,0), (2,1), (2,2), (2,3), (1,2), (0,0)]),        #arrete 1 bas
     ((1,5), [(1,4), (1,0), (0,0), (2,9), (2,10), (2,11)]),      #arrete 5 bas
     
     ((4,0), [(3,0), (5,29), (5,0), (5,1), (4,1), (4,23)]),      #arrete 0
     ((3,3), [(3,2), (4,4), (4,3), (4,5), (3,4), (2,2)]),        #arrete 1
     ((5,25), [(6,30), (6,31), (6,29), (4,20), (5,24), (5,26)])  #arrete 5
])
def test_compute_neighbors_arrete(id, expec_res):
     result = compute_neighbors_arrete(id)
     for neighbor in expec_res:
          assert neighbor in result
     assert len(result) == 6


@pytest.mark.parametrize("id, expec_res", [
     ((2,1), [(2,0), (2,2), (1,0), (1,1)]),           #entre l'arrete 0 et l'arrete 1
     ((2,7), [(2,8), (2,6), (1,4), (1,3)]),           #entre l'arrete 3 et l'arrete 4
     ((2,11), [(2,10), (2,0), (1,5), (1,0)]),         #entre l'arrete 5 et l'arrete 0

     ((5,1), [(5,0), (5,2), (4,0), (4,1)]),           #à droite de l'arrete 0
     ((3,4), [(2,2), (3,3), (3,5), (2,3)]),           #à droite de l'arrete 1
     ((6,31), [(6,30), (6,32), (5,25), (5,26)]),      #à droite de l'arrete 5
     

     ((3,17), [(3,16), (3,0), (2,11), (2,0)]),        #à gauche de l'arrete 0
     ((4,15), [(4,16), (4,14), (3,12), (3,11)]),      #à gauche de l'arrete 4
     ((6,29), [(6,30), (6,28), (5,24), (5,25)]),      #à gauche de l'arrete 5

     ((4,10), [(4,9), (4,11), (3,7), (3,8)])          #au milieu du bord 2
])
def test_compute_neighbors_bords(id, expec_res):
     result = compute_neighbors_bords(id)
     for neighbor in expec_res:
          assert neighbor in result
     assert len(result) == 4

@pytest.mark.parametrize("id, expec_res", [
     ((1,0), [(1,5), (1,1), (0,0)]),        #sommet 0 bas
     ((1,4), [(1,5), (1,3), (0,0)]),        #sommet 4 bas
     ((1,5), [(1,0), (1,4), (0,0)]),        #sommet 5 bas
     
     ((5,0), [(5,29), (5,1), (4,0)]),       #sommet 0
     ((3,6), [(2,4), (3,7), (3,5)]),        #sommet 2
     ((6,30), [(6,29), (6,31), (5,25)])     #sommet 5
     
])
def test_compute_neighbors_sommet(id, expec_res):
     result = compute_neighbors_sommet(id)
     for neighbor in expec_res:
          assert neighbor in result
     assert len(result) == 3

@pytest.mark.parametrize("id, expec_res", [
     ((2,1), [(2,0), (3,1), (3,2), (2,2), (1,0), (1,1)]),          #entre l'arrete 0 et l'arrete 1
     ((2,3), [(2,2), (3,4), (3,5), (2,4), (1,1), (1,2)]),          #entre l'arrete 3 et l'arrete 4
     ((2,11), [(2,10), (3,16), (3,17), (2,0), (1,0), (1,5)]),      #entre l'arrete 5 et l'arrete 0


     ((5,1), [(5,0), (6,1), (6,2), (5,2), (4,1), (4,0)]),          #à droite de l'arrete 0
     ((3,10), [(2,7), (2,6), (3,9), (4,13), (4,14), (3,11)]),      #à droite de l'arrete 3
     ((4,21), [(4,20), (5,26), (5,27), (4,22), (3,16), (3,15)]),   #à droite de l'arrete 5

     ((3,17), [(3,16), (3,0), (2,11), (2,0), (4,22), (4,23)]),     #à gauche de l'arrete 0
     ((4,3), [(4,2), (3,2), (3,3), (5,3), (4,4), (5,4)]),          #à gauche de l'arrete 1
     ((5,24), [(5,25), (5,23), (6,28), (6,29), (4,19), (4,20)]),   #à gauche de l'arrete 5 

     ((4,18), [(4,19), (3,14), (3,13), (4,17), (5,22), (5,23)])    #au milieu de la face 4
])
def test_compute_neighbors_interieur(id, expec_res):
     result = compute_neighbors_interieur(id)
     for neighbor in expec_res:
          assert neighbor in result
     assert len(result) == 6


# TEST CELL MAKER
#####################################

@pytest.mark.parametrize("id, nb_rings", [
     [(0,0), 1],      #center
     [(1,1), (1)],    #sommet
     [(7,40), (9)],  #interieur
     [(11,0), 15],    #arrete
     [(6,9), 6]       #bords
])
def test_cell_maker_default_values(id, nb_rings):
     cell = Mesh.cell_maker(id, nb_rings)
     assert cell.id == id
     assert len(cell.neighbors) != 0
     assert cell.temperature == 0
     assert cell.vapor == 0
     assert cell.ice_potential == 0
     assert not cell.frozen
     assert len(cell.position) != 0
@pytest.mark.parametrize("id, nb_rings", [
     #[(0,0), 1],       #center
     [(1,14), 0],      #sommet
     [(7,0), 2],       #interieur
     [(11,8), 10],     #arrete
     [(6,32), 1]       #bords
])
def test_cell_maker_incompatible_parameters(id, nb_rings):
     with pytest.raises(ValueError) as e:
          cell = Mesh.cell_maker(id, nb_rings)

@pytest.mark.parametrize("nb_rings", [1,2,10])
def test_cell_maker_for_center(nb_rings, mocker):
     mock_neighbors = mocker.patch("src.mesh.compute_neighbors_center", return_value = "compute_neighbors_center")
     cell = Mesh.cell_maker((0,0), nb_rings)
     assert cell.position == "center"
     assert cell.neighbors == "compute_neighbors_center"
     mock_neighbors.assert_called_once()

@pytest.mark.parametrize("id, nb_rings", [
     ((1,0), 1),        #sommet 0 bas
     ((1,4), 1),        #sommet 4 bas
     ((1,5), 1),        #sommet 5 bas
     
     ((7,0), 7),        #sommet 0
     ((2,4), 2),        #sommet 2
     ((6,30), 6)        #sommet 5
])
def test_cell_maker_for_sommet(id, nb_rings, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.compute_neighbors_sommet", return_value = result_mock)
     cell = Mesh.cell_maker(id, nb_rings)
     mock_neighbors.assert_called_once()
     assert cell.position == "sommet"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

@pytest.mark.parametrize("id, nb_rings", [
     ((2,1), 3),          #entre l'arrete 0 et l'arrete 1
     ((2,3), 5),          #entre l'arrete 3 et l'arrete 4
     ((2,11), 15),      #entre l'arrete 5 et l'arrete 0

     ((5,1), 9),          #à droite de l'arrete 0
     ((3,10), 4),      #à droite de l'arrete 3
     ((4,21), 10),   #à droite de l'arrete 5

     ((3,17), 45),     #à gauche de l'arrete 0
     ((4,3), 10),       #à gauche de l'arrete 1
     ((5,24), 6),   #à gauche de l'arrete 5 

     ((4,18), 10)    #au milieu de la face 4
])
def test_cell_maker_for_interieur(id, nb_rings, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.compute_neighbors_interieur", return_value = result_mock)
     cell = Mesh.cell_maker(id, nb_rings)
     mock_neighbors.assert_called_once()
     assert cell.position == "interieur"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

@pytest.mark.parametrize("id, nb_rings", [
     ((1,0), 8),       #arrete 0 bas
     ((1,1), 2),        #arrete 1 bas
     ((1,5), 10),      #arrete 5 bas
     
     ((4,0), 5),      #arrete 0
     ((3,3), 10),        #arrete 1
     ((5,25), 60)  #arrete 5
])
def test_cell_maker_for_arrete(id, nb_rings, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.compute_neighbors_arrete", return_value = result_mock)
     cell = Mesh.cell_maker(id, nb_rings)
     mock_neighbors.assert_called_once()
     assert cell.position == "arrete"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}


@pytest.mark.parametrize("id, nb_rings", [
     ((2,1), 2),           #entre l'arrete 0 et l'arrete 1
     ((2,7), 2),           #entre l'arrete 3 et l'arrete 4
     ((2,11), 2),         #entre l'arrete 5 et l'arrete 0

     ((5,1), 5),           #à droite de l'arrete 0
     ((3,4), 3),           #à droite de l'arrete 1
     ((6,31), 6),      #à droite de l'arrete 5
     

     ((3,17), 3),        #à gauche de l'arrete 0
     ((4,15), 4),      #à gauche de l'arrete 4
     ((6,29), 6),      #à gauche de l'arrete 5

     ((4,10), 4)          #au milieu du bord 2
])
def test_cell_maker_for_bords(id, nb_rings, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.compute_neighbors_bords", return_value = result_mock)
     cell = Mesh.cell_maker(id, nb_rings)
     mock_neighbors.assert_called_once()
     assert cell.position == "bords"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

# TEST_INIT
#####################################
@pytest.mark.parametrize("nb_rings", [1, 2, 10])
def test_init_mesh(nb_rings):
     m = Mesh(nb_rings)
     assert m.nb_rings == nb_rings
     assert isinstance(m.dict_cells, dict)
     assert isinstance(m.frozen_cells, set)
     assert isinstance(m.non_frozen_cells, set)

@pytest.mark.parametrize("nb_rings, expec_cells_number", [(1, 7), (2, 19), (5, 91), (10, 331)])
def test_init_mesh_exact_number_created_cells(nb_rings, expec_cells_number, mocker):
     list_ids = [id_i for id_i in range(expec_cells_number)]
     mock_create_list_ids = mocker.patch("src.mesh.create_list_ids", return_value= list_ids)
     mock_cell_maker = mocker.patch("src.mesh.Mesh.cell_maker")
     mock_add_cell = mocker.patch("src.mesh.Mesh.add_cell")
     m = Mesh(nb_rings)

     mock_create_list_ids.assert_called_once()
     assert mock_create_list_ids.call_args_list[0].args == (nb_rings,)

     assert mock_cell_maker.call_count == expec_cells_number
     assert mock_add_cell.call_count == expec_cells_number

@pytest.mark.parametrize("nb_rings", [1, 10, 100])
def test_init_mesh_exact_ids(nb_rings, mocker):
     n = 10
     list_mocker_ids = [mocker.Mock() for i in range(n)]
     mock_create_list_ids = mocker.patch("src.mesh.create_list_ids", return_value= list_mocker_ids)

     returned_values = []
     def side_effect(*args, **kwargs):
          result = mocker.Mock()
          returned_values.append(result)
          return result
     mock_cell_maker = mocker.patch("src.mesh.Mesh.cell_maker", side_effect=side_effect)

     mock_add_cell = mocker.patch("src.mesh.Mesh.add_cell")
     m = Mesh(nb_rings)

     mock_create_list_ids.assert_called_once()
     assert mock_create_list_ids.call_args_list[0].args == (nb_rings,)

     for i in range(n):
          mock_cell_maker.assert_any_call(list_mocker_ids[i], nb_rings)
          mock_add_cell.assert_any_call(returned_values[i])

# TEST CONDENSATION STEP
#################################

@pytest.mark.parametrize("alpha_condensation", [0, 0.1, 0.999, 1])
@pytest.mark.parametrize("vapor_saturation", [0, 0.5, 15])
def test_condensation_step(alpha_condensation, vapor_saturation, simple_mesh, mocker):
     mock_cell_condensation = mocker.patch("src.cell.Cell.condensation", autospec = True)
     m : Mesh = simple_mesh()
     m.condensation_step(alpha_condensation, vapor_saturation)
     assert mock_cell_condensation.call_count == 127
     for cell in m.dict_cells.values():
          mock_cell_condensation.assert_any_call(cell, alpha_condensation, vapor_saturation)

# TEST TEMPERATURE STEP
#################################

@pytest.mark.parametrize("nb_rings", [1,2,5])
@pytest.mark.parametrize("alpha_temperature", [0, 0.1, 0.999, 1])
def test_temperature_step(nb_rings, alpha_temperature, simple_mesh, mocker):
     m : Mesh = simple_mesh(nb_rings=nb_rings)
     for id, cell_id in m.dict_cells.items():
          cell_id.temperature = mocker.Mock()
     mock_cell_temp_diff = mocker.patch("src.cell.Cell.temperature_diffusion", autospec = True)
          
     m.temperature_diffusion_step(alpha_temperature)
     assert mock_cell_temp_diff.call_count == len(m.dict_cells)
     for cell in m.dict_cells.values():
          mock_cell_temp_diff.assert_any_call(cell, alpha_temperature, [m.dict_cells[(neighbor_id)].temperature for neighbor_id in cell.neighbors])

@pytest.mark.parametrize("nb_rings", [1,2,5])
@pytest.mark.parametrize("alpha_vapor", [0, 0.7, 0.9989, 1])
def test_vapor_step(nb_rings, alpha_vapor, simple_mesh, mocker):
     m : Mesh = simple_mesh(nb_rings=nb_rings)
     for id, cell_id in m.dict_cells.items():
          cell_id.vapor = mocker.Mock()
     mock_cell_temp_diff = mocker.patch("src.cell.Cell.vapor_diffusion", autospec = True)
          
     m.vapor_diffusion_step(alpha_vapor)
     assert mock_cell_temp_diff.call_count == len(m.dict_cells)
     for cell in m.dict_cells.values():
          mock_cell_temp_diff.assert_any_call(cell, alpha_vapor, [m.dict_cells[(neighbor_id)].vapor for neighbor_id in cell.neighbors])


# TEST SET TEMPERATURE
##################################

def test_set_temperature_all_cells(simple_mesh):
     m : Mesh = simple_mesh()
     m.set_temperature(7)

     for cell in m.dict_cells.values():
          assert cell.temperature == 7

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(3,4)},
     {(2,i) for i in range(12)}
])
def test_set_temperature_on_partition(set_cells_id, simple_mesh):
     m : Mesh = simple_mesh()
     m.set_temperature(temperature=7, set_cells_id=set_cells_id)

     for id, cell in m.dict_cells.items():
          if id in set_cells_id:
               assert cell.temperature == 7
          else:
               assert cell.temperature == 0

# TEST SET VAPOR
##################################
def test_set_vapor_all_cells(simple_mesh):
     m : Mesh = simple_mesh()
     m.set_vapor(7)

     for cell in m.dict_cells.values():
          assert cell.vapor == 7

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_vapor_on_partition(set_cells_id, simple_mesh):
     m : Mesh = simple_mesh()
     m.set_vapor(vapor=7, set_cells_id=set_cells_id)

     for id, cell in m.dict_cells.items():
          if id in set_cells_id:
               assert cell.vapor == 7
          else:
               assert cell.vapor == 0

# TEST SET ICE POTENTIAL
##################################
def test_set_ice_potential_all_cells(simple_mesh):
     m : Mesh = simple_mesh()
     m.set_ice_potential(10)

     for cell in m.dict_cells.values():
          assert cell.ice_potential == 10

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_ice_potential_on_partition(set_cells_id, simple_mesh):
     m : Mesh = simple_mesh()
     m.set_ice_potential(ice_potential=10, set_cells_id=set_cells_id)

     for id, cell in m.dict_cells.items():
          if id in set_cells_id:
               assert cell.ice_potential == 10
          else:
               assert cell.ice_potential == 0


# TEST SET FROZEN TRUE
##################################
def test_set_frozen_true_all_cells(simple_mesh):
     m : Mesh = simple_mesh()
     m.set_frozen_true()

     for cell in m.dict_cells.values():
          assert cell.frozen
     assert len(m.frozen_cells) == 127
     assert len(m.non_frozen_cells) == 0

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_frozen_true_on_partition(set_cells_id, simple_mesh):
     m : Mesh = simple_mesh()
     m.set_frozen_true(set_cells_id=set_cells_id)

     for id in set_cells_id:
          assert m.dict_cells[id].frozen
          assert id in m.frozen_cells
          assert not id in m.non_frozen_cells

# TEST SET FROZEN TRUE
##################################
def test_set_frozen_false_all_cells(simple_mesh):
     m : Mesh = simple_mesh()
     m.set_frozen_false()

     for cell in m.dict_cells.values():
          assert not cell.frozen
     assert len(m.non_frozen_cells) == 127
     assert len(m.frozen_cells) == 0

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_frozen_false_on_partition(set_cells_id, simple_mesh):
     m : Mesh = simple_mesh()
     m.set_frozen_false(set_cells_id=set_cells_id)

     for id in set_cells_id:
          assert not m.dict_cells[id].frozen
          assert id in m.non_frozen_cells
          assert not id in m.frozen_cells

# TEST FREEZE
######################""
@pytest.mark.parametrize("nb_rings", [6])
@pytest.mark.parametrize("ice_threshold", [10])
@pytest.mark.parametrize("temperature_threshold", [10])
@pytest.mark.parametrize("n_frozen_neighbors_threshold", [10])
def test_freeze(nb_rings, ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, mocker):
     mock_compute_frozen_neighbors = mocker.patch("src.mesh.Mesh.compute_number_frozen_neighbors", side_effect=lambda _, id: f"frozen_neighbors_{id}", autospec= True)
     mock_freeze = mocker.patch("src.cell.Cell.freeze", autospec = True)
     m = Mesh(nb_rings)
     m.freeze_step(ice_threshold, temperature_threshold, n_frozen_neighbors_threshold)
     
     assert mock_compute_frozen_neighbors.call_count == 127
     assert mock_freeze.call_count == 127

     for id, cell in m.dict_cells.items():
          mock_compute_frozen_neighbors.assert_any_call(m, id)
          mock_freeze.assert_any_call(cell, ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, f"frozen_neighbors_{id}")