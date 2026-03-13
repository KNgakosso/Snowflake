from src.mesh import Mesh
from src.cell import Cell
from collections.abc import KeysView, ValuesView, ItemsView
import pytest
from unittest.mock import patch, PropertyMock

def test_now(simple_mesh):
     m = simple_mesh(4)
     assert len(m[4,1].neighbors) == 4
# TEST __GET_ITEM__
#########################################
def test_get_item_OK(simple_mesh):
     m : Mesh = simple_mesh()
     result = m[4,10]
     assert isinstance(result, Cell)
     assert result.id == (4, 10)

def test_get_item_NOT_OK(simple_mesh):
     m : Mesh = simple_mesh(size = 6)
     with pytest.raises(IndexError):
          result = m[8,10]


# TEST __SET_ITEM__
#########################################
def test_set_item_OK(simple_cell, simple_mesh):
     c : Cell = simple_cell(temperature= 15, vapor= 22)
     m : Mesh = simple_mesh()
     m[4,10] = c
     assert isinstance(m[4, 10], Cell)
     assert m[4, 10].temperature == 15
     assert m[4, 10].vapor == 22

# TEST CELLS_IDS
#########################################
def test_cells_ids(simple_mesh):
     m : Mesh = simple_mesh()
     result = m.cells_ids()
     assert isinstance(result, KeysView)
     assert result == m._dict_cells.keys()


# TEST ITEMS
#########################################
def test_items(simple_mesh):
     m : Mesh = simple_mesh()
     result = m.items()
     assert isinstance(result, ItemsView)
     assert result == m._dict_cells.items()


# TEST CELLS
#########################################
def test_cells(simple_mesh):
     m : Mesh = simple_mesh()
     result = m.cells()
     assert isinstance(result, ValuesView)
     #assert result == m._dict_cells.values()

# TEST FROZEN CELLS IDS
#########################################
def test_frozen_cells_ids_empty(simple_mesh):
     m : Mesh = simple_mesh()
     result = m.frozen_cells_ids()

     assert isinstance(result, set)
     assert result == m._frozen_cells

def test_frozen_cells_ids_non_empty(simple_mesh):
     m : Mesh = simple_mesh()
     m._dict_cells[0,0].frozen = True
     m._frozen_cells.add((0,0))
     result = m.frozen_cells_ids()

     assert isinstance(result, set)
     assert result == m._frozen_cells

# TEST ADD FROZEN CELLS
#########################################
@pytest.mark.parametrize("new_frozen_cells", [
     {(1,1), (1,2), (5,5)},
     {},
     {(4,10)}
])
def test_add_frozen_cells_empty(simple_mesh, new_frozen_cells):
     m : Mesh = simple_mesh()
     m.add_frozen_cells(new_frozen_cells)

     assert isinstance(m._frozen_cells, set)
     assert len(m._frozen_cells) == len(new_frozen_cells)
     assert len(m._non_frozen_cells) == len(m._dict_cells) - len(new_frozen_cells)


@pytest.mark.parametrize("new_frozen_cells", [
     {(1,1), (1,2), (5,5)},
     {},
     {(4,10)}
])
def test_add_frozen_cells_non_empty(simple_mesh, new_frozen_cells):
     m : Mesh = simple_mesh()
     m._dict_cells[0,0].frozen = True
     m._frozen_cells.add((0,0))
     m._non_frozen_cells.discard((0,0))

     m.add_frozen_cells(new_frozen_cells)

     assert len(m._frozen_cells) == len(new_frozen_cells) + 1
     assert len(m._non_frozen_cells) == len(m._dict_cells) - len(new_frozen_cells) - 1

def test_add_frozen_cells_already_frozen(simple_mesh):
     m : Mesh = simple_mesh()
     m._dict_cells[0,0].frozen = True
     m._frozen_cells.add((0,0))
     m._non_frozen_cells.discard((0,0))

     m._dict_cells[1,1].frozen = True
     m._frozen_cells.add((1,1))
     m._non_frozen_cells.discard((1,1))


     m._dict_cells[2,2].frozen = True
     m._frozen_cells.add((2,2))
     m._non_frozen_cells.discard((2,2))

     m.add_frozen_cells({(0,0), (2,2), (3,3), (4,4)})

     assert len(m._frozen_cells) == 5
     assert len(m._non_frozen_cells) == len(m._dict_cells) - 5


# TEST NON FROZEN CELLS IDS
#########################################
@pytest.mark.parametrize("new_non_frozen_cells", [
     {(1,1), (1,2), (5,5)},
     {},
     {(4,10)}
])
def test_add_non_frozen_cells_empty(simple_mesh, new_non_frozen_cells):
     m : Mesh = simple_mesh()
     m._non_frozen_cells = set()
     m._frozen_cells = {id for id in m._dict_cells.keys()}
     m.add_non_frozen_cells(new_non_frozen_cells)

     assert isinstance(m._frozen_cells, set)
     assert len(m._non_frozen_cells) == len(new_non_frozen_cells)
     assert len(m._frozen_cells) == len(m._dict_cells) - len(new_non_frozen_cells)


@pytest.mark.parametrize("new_non_frozen_cells", [
     {(1,1), (1,2), (5,5)},
     {},
     {(4,10)}
])
def test_add_non_frozen_cells_non_empty(simple_mesh, new_non_frozen_cells):
     m : Mesh = simple_mesh()
     m._non_frozen_cells = set()
     m._frozen_cells = {id for id in m._dict_cells.keys()}
     m._non_frozen_cells.add((0,0))
     m._frozen_cells.discard((0,0))

     m.add_non_frozen_cells(new_non_frozen_cells)

     assert len(m._non_frozen_cells) == len(new_non_frozen_cells) + 1
     assert len(m._frozen_cells) == len(m._dict_cells) - len(new_non_frozen_cells) - 1

def test_add_non_frozen_cells_already_non_frozen(simple_mesh):
     m : Mesh = simple_mesh()
     m._non_frozen_cells = set()
     m._frozen_cells = {id for id in m._dict_cells.keys()}

     m._non_frozen_cells.add((0,0))
     m._frozen_cells.discard((0,0))

     m._non_frozen_cells.add((1,1))
     m._frozen_cells.discard((1,1))


     m._non_frozen_cells.add((2,2))
     m._frozen_cells.discard((2,2))

     m.add_non_frozen_cells({(0,0), (2,2), (3,3), (4,4)})

     assert len(m._non_frozen_cells) == 5
     assert len(m._frozen_cells) == len(m._dict_cells) - 5

# TEST COMPUTE_NEIGHBORS
#########################################
def test_compute_neighbors_center():
     result = Mesh._compute_neighbors_center()
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
     result = Mesh._compute_neighbors_arrete(id)
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
     result = Mesh._compute_neighbors_bords(id)
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
     result = Mesh._compute_neighbors_sommet(id)
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
     result = Mesh._compute_neighbors_interieur(id)
     for neighbor in expec_res:
          assert neighbor in result
     assert len(result) == 6


# TEST CELL MAKER
#####################################

@pytest.mark.parametrize("id, size", [
     [(0,0), 1],      #center
     [(1,1), (1)],    #sommet
     [(7,40), (9)],  #interieur
     [(11,0), 15],    #arrete
     [(6,9), 6]       #bords
])
def test_cell_maker_default_values(id, size):
     cell = Mesh.cell_maker(id, size)
     assert cell.id == id
     assert len(cell.neighbors) != 0
     assert cell.temperature == 0
     assert cell.vapor == 0
     assert cell.ice_potential == 0
     assert not cell.frozen
     assert len(cell.position) != 0
@pytest.mark.parametrize("id, size", [
     #[(0,0), 1],       #center
     [(1,14), 0],      #sommet
     [(7,0), 2],       #interieur
     [(11,8), 10],     #arrete
     [(6,32), 1]       #bords
])
def test_cell_maker_incompatible_parameters(id, size):
     with pytest.raises(ValueError) as e:
          cell = Mesh.cell_maker(id, size)

@pytest.mark.parametrize("size", [1,2,10])
def test_cell_maker_for_center(size, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.Mesh._compute_neighbors_center", return_value = result_mock)
     cell = Mesh.cell_maker((0,0), size)
     assert cell.position == "center"
     assert cell.neighbors == result_mock
     mock_neighbors.assert_called_once()

@pytest.mark.parametrize("id, size", [
     ((1,0), 1),        #sommet 0 bas
     ((1,4), 1),        #sommet 4 bas
     ((1,5), 1),        #sommet 5 bas
     
     ((7,0), 7),        #sommet 0
     ((2,4), 2),        #sommet 2
     ((6,30), 6)        #sommet 5
])
def test_cell_maker_for_sommet(id, size, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.Mesh._compute_neighbors_sommet", return_value = result_mock)
     cell = Mesh.cell_maker(id, size)
     mock_neighbors.assert_called_once()
     assert cell.position == "sommet"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

@pytest.mark.parametrize("id, size", [
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
def test_cell_maker_for_interieur(id, size, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.Mesh._compute_neighbors_interieur", return_value = result_mock)
     cell = Mesh.cell_maker(id, size)
     mock_neighbors.assert_called_once()
     assert cell.position == "interieur"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

@pytest.mark.parametrize("id, size", [
     ((1,0), 8),       #arrete 0 bas
     ((1,1), 2),        #arrete 1 bas
     ((1,5), 10),      #arrete 5 bas
     
     ((4,0), 5),      #arrete 0
     ((3,3), 10),        #arrete 1
     ((5,25), 60)  #arrete 5
])
def test_cell_maker_for_arrete(id, size, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.Mesh._compute_neighbors_arrete", return_value = result_mock)
     cell = Mesh.cell_maker(id, size)
     mock_neighbors.assert_called_once()
     assert cell.position == "arrete"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}


@pytest.mark.parametrize("id, size", [
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
def test_cell_maker_for_bords(id, size, mocker):
     result_mock = mocker.Mock()
     mock_neighbors = mocker.patch("src.mesh.Mesh._compute_neighbors_bords", return_value = result_mock)
     cell = Mesh.cell_maker(id, size)
     mock_neighbors.assert_called_once()
     assert cell.position == "bords"
     assert cell.neighbors == result_mock
     assert mock_neighbors.call_args_list[0].args == (id,)
     assert mock_neighbors.call_args_list[0].kwargs == {}

# TEST COMPUTE NUMBER FROZEN NEIGHBORS
######################################
def test_compute_number_frozen_nieighbors(simple_mesh):
     m : Mesh = simple_mesh()
     m[1,1].frozen = True

     assert m._compute_number_frozen_neighbors((0,0)) == 1

def test_compute_number_frozen_nieighbors_2(simple_mesh):
     m : Mesh = simple_mesh()

     m[0,0].frozen = True
     m[2,1].frozen = True
     m[1,5].frozen = True

     assert m._compute_number_frozen_neighbors((1,0)) == 3

def test_compute_number_frozen_nieighbors_3(simple_mesh):
     m : Mesh = simple_mesh(5)
     m[0,0].frozen = True

     assert m._compute_number_frozen_neighbors((5,0)) == 0
# TEST_INIT
#####################################
@pytest.mark.parametrize("size", [1, 2, 10])
def test_init_mesh(size):
     m = Mesh(size)
     assert m.size == size
     assert isinstance(m._dict_cells, dict)
     assert isinstance(m._frozen_cells, set)
     assert isinstance(m._non_frozen_cells, set)

@pytest.mark.parametrize("size, expec_cells_number", [(1, 7), (2, 19), (5, 91), (10, 331)])
def test_init_mesh_exact_number_created_cells(size, expec_cells_number, mocker):
     list_ids = [id_i for id_i in range(expec_cells_number)]
     mock_create_list_ids = mocker.patch("src.mesh.create_list_ids", return_value= list_ids)
     mock_cell_maker = mocker.patch("src.mesh.Mesh.cell_maker")
     m = Mesh(size)

     mock_create_list_ids.assert_called_once()
     assert mock_create_list_ids.call_args_list[0].args == (size,)

     assert mock_cell_maker.call_count == expec_cells_number

@pytest.mark.parametrize("size", [1, 10, 100])
def test_init_mesh_exact_ids(size, mocker):
     n = 10
     list_mocker_ids = [mocker.Mock() for i in range(n)]
     mock_create_list_ids = mocker.patch("src.mesh.create_list_ids", return_value= list_mocker_ids)

     returned_values = []
     def side_effect(*args, **kwargs):
          result = mocker.Mock()
          returned_values.append(result)
          return result
     mock_cell_maker = mocker.patch("src.mesh.Mesh.cell_maker", side_effect=side_effect)

     m = Mesh(size)

     mock_create_list_ids.assert_called_once()
     assert mock_create_list_ids.call_args_list[0].args == (size,)

     for i in range(n):
          mock_cell_maker.assert_any_call(list_mocker_ids[i], size)

