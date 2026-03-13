from src.snowflake import Snowflake
import pytest

#TEST CONDENSATION STEP
#################################

@pytest.mark.parametrize("alpha_condensation", [0, 0.1, 0.999, 1])
@pytest.mark.parametrize("vapor_saturation", [0, 0.5, 15])
def test_condensation_step(alpha_condensation, vapor_saturation, simple_snowflake, mocker):
     mock_cell_condensation = mocker.patch("src.cell.Cell.condensation", autospec = True)
     s : Snowflake = simple_snowflake(alpha_condensation= alpha_condensation,
                                      vapor_saturation= vapor_saturation
                        )
     s._condensation_step()
     assert mock_cell_condensation.call_count == 127
     for cell in s._mesh.cells():
          mock_cell_condensation.assert_any_call(cell, alpha_condensation, vapor_saturation)

# TEST TEMPERATURE STEP
#################################

@pytest.mark.parametrize("size", [1,2,5])
@pytest.mark.parametrize("alpha_temperature", [0, 0.1, 0.999, 1])
def test_temperature_step(size, alpha_temperature, simple_snowflake, mocker):
     s : Snowflake = simple_snowflake(size = size,
                                      alpha_temperature= alpha_temperature
                        )
     for id, cell_id in s._mesh.items():
          cell_id.temperature = mocker.Mock()
     mock_cell_temp_diff = mocker.patch("src.cell.Cell.temperature_diffusion", autospec = True)
          
     s._temperature_diffusion_step()
     assert mock_cell_temp_diff.call_count == len(s._mesh.items())
     for cell in s._mesh.cells():
          mock_cell_temp_diff.assert_any_call(cell, alpha_temperature, [s._mesh[(neighbor_id)].temperature for neighbor_id in cell.neighbors])

# TEST VAPOR STEP
###################################

@pytest.mark.parametrize("size", [1,2,5])
@pytest.mark.parametrize("alpha_vapor", [0, 0.7, 0.9989, 1])
def test_vapor_step(size, alpha_vapor, simple_snowflake, mocker):
     s : Snowflake = simple_snowflake(size= size,
                                      alpha_vapor = alpha_vapor
                        )
     for id, cell_id in s._mesh.items():
          cell_id.vapor = mocker.Mock()
     mock_cell_temp_diff = mocker.patch("src.cell.Cell.vapor_diffusion", autospec = True)
          
     s._vapor_diffusion_step()
     assert mock_cell_temp_diff.call_count == len(s._mesh.items())
     for cell in s._mesh.cells():
          mock_cell_temp_diff.assert_any_call(cell, alpha_vapor, [s._mesh[(neighbor_id)].vapor for neighbor_id in cell.neighbors])


# TEST SET TEMPERATURE
##################################

def test_set_temperature_all_cells(simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_temperature(7)

     for cell in s._mesh.cells():
          assert cell.temperature == 7

@pytest.mark.parametrize("set_cells_id", [
     {(3,4)},
     {(2,i) for i in range(12)}
])
def test_set_temperature_on_partition(set_cells_id, simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_temperature(temperature=7, set_cells_id=set_cells_id)

     for id, cell in s._mesh.items():
          if id in set_cells_id:
               assert cell.temperature == 7
          else:
               assert cell.temperature == 0

# TEST SET VAPOR
##################################
def test_set_vapor_all_cells(simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_vapor(7)

     for cell in s._mesh.cells():
          assert cell.vapor == 7

@pytest.mark.parametrize("set_cells_id", [
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_vapor_on_partition(set_cells_id, simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_vapor(vapor=7, set_cells_id=set_cells_id)

     for id, cell in s._mesh.items():
          if id in set_cells_id:
               assert cell.vapor == 7
          else:
               assert cell.vapor == 0

# TEST SET ICE POTENTIAL
##################################
def test_set_ice_potential_all_cells(simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_ice_potential(10)

     for cell in s._mesh.cells():
          assert cell.ice_potential == 10

@pytest.mark.parametrize("set_cells_id", [
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_ice_potential_on_partition(set_cells_id, simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_ice_potential(ice_potential=10, set_cells_id=set_cells_id)

     for id, cell in s._mesh.items():
          if id in set_cells_id:
               assert cell.ice_potential == 10
          else:
               assert cell.ice_potential == 0


# TEST SET FROZEN TRUE
##################################
def test_set_frozen_true_all_cells(simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_frozen_true()

     for cell in s._mesh.cells():
          assert cell.frozen
     assert len(s._mesh.frozen_cells_ids()) == 127
     assert len(s._mesh.non_frozen_cells_ids()) == 0

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_frozen_true_on_partition(set_cells_id, simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_frozen_true(set_cells_id=set_cells_id)

     for id in set_cells_id:
          assert s._mesh[id].frozen
          assert id in s._mesh.frozen_cells_ids()
          assert not id in s._mesh.non_frozen_cells_ids()

# TEST SET FROZEN FALSE
##################################
def test_set_frozen_false_all_cells(simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_frozen_false()

     for cell in s._mesh.cells():
          assert not cell.frozen
     assert len(s._mesh.non_frozen_cells_ids()) == 127
     assert len(s._mesh.frozen_cells_ids()) == 0

@pytest.mark.parametrize("set_cells_id", [
     {},
     {(0,0)},
     {(2,i) for i in range(12)}.union({(3,0), (3,1)})
])
def test_set_frozen_false_on_partition(set_cells_id, simple_snowflake):
     s : Snowflake = simple_snowflake()
     s.set_frozen_false(set_cells_id=set_cells_id)

     for id in set_cells_id:
          assert not s._mesh[id].frozen
          assert id in s._mesh.non_frozen_cells_ids()
          assert not id in s._mesh.frozen_cells_ids()

# TEST FREEZE
######################""
@pytest.mark.parametrize("size", [6])
@pytest.mark.parametrize("ice_threshold", [10])
@pytest.mark.parametrize("temperature_threshold", [10])
@pytest.mark.parametrize("n_frozen_neighbors_threshold", [10])
def test_freeze(size, ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, simple_snowflake, mocker):
    mock_compute_frozen_neighbors = mocker.patch("src.mesh.Mesh._compute_number_frozen_neighbors", side_effect=lambda _, id: f"frozen_neighbors_{id}", autospec= True)
    mock_freeze = mocker.patch("src.cell.Cell.freeze", autospec = True)

    s : Snowflake = simple_snowflake(ice_threshold= ice_threshold,
                                     temperature_threshold = temperature_threshold,
                                     n_frozen_neighbors_threshold = n_frozen_neighbors_threshold
                        )
    
    s._freeze_step()
     
    assert mock_compute_frozen_neighbors.call_count == 127
    assert mock_freeze.call_count == 127

    for id, cell in s._mesh.items():
        mock_compute_frozen_neighbors.assert_any_call(s._mesh, id)
        mock_freeze.assert_any_call(cell, ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, f"frozen_neighbors_{id}")