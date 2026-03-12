from src.snowflake import Snowflake
from src.models import MeshModel, InitParamsModel, SimulParamsModel, PhysicalParamsModel, UpdateSelectionModel, SelectionModel
from pathlib import Path

def update_initialization_params(snowflake : Snowflake, init_params_model : InitParamsModel):
    init_params = init_params_model.to_domain()
    snowflake.update_initilization_params(init_params)
    return init_params_model

def update_simulation_params(snowflake : Snowflake, simul_params_model : SimulParamsModel):
    simul_params = simul_params_model.to_domain()
    snowflake.update_simulation_params(simul_params)
    return simul_params_model

def update_physical_params(snowflake : Snowflake, physical_parameters_model : PhysicalParamsModel):
    physical_parameters = physical_parameters_model.to_domain()
    snowflake.update_physical_params(physical_parameters)
    return physical_parameters

def set_temperature(snowflake : Snowflake, update_selection_model : UpdateSelectionModel):
    snowflake.set_temperature(temperature = update_selection_model.value,
                              set_cells_id= update_selection_model.set_cells_id
                    )
    return update_selection_model

def set_ice_potential(snowflake : Snowflake, update_selection_model : UpdateSelectionModel):
    snowflake.set_ice_potential(ice_potential= update_selection_model.value,
                              set_cells_id= update_selection_model.set_cells_id
                    )
    return update_selection_model

def set_vapor(snowflake : Snowflake, update_selection_model : UpdateSelectionModel):
    snowflake.set_vapor(vapor = update_selection_model.value,
                              set_cells_id= update_selection_model.set_cells_id
                    )
    return update_selection_model


def set_frozen_true(snowflake : Snowflake, selection_model : SelectionModel):
    snowflake.set_frozen_true(set_cells_id= selection_model.set_cells_id)
    return selection_model


def set_frozen_false(snowflake : Snowflake, selection_model : SelectionModel):
    snowflake.set_frozen_false(set_cells_id= selection_model.set_cells_id)
    return selection_model

def random_initial_state(snowflake : Snowflake):
    snowflake.randomize()
    return MeshModel.from_domain(snowflake._mesh)

def run_simulation(snowflake : Snowflake):
    snowflake.run_simulation()
    return MeshModel.from_domain(snowflake._mesh)

def get_mesh(snowflake : Snowflake):
    return MeshModel.from_domain(snowflake._mesh)

def get_initialization_params(snowflake : Snowflake):
    return InitParamsModel.from_domain(snowflake._initialization_params)

def get_simulation_params(snowflake : Snowflake):
    return SimulParamsModel.from_domain(snowflake._simulation_params)

def get_physical_params(snowflake : Snowflake):
    return PhysicalParamsModel.from_domain(snowflake._physical_params)

def save_snowflake(snowflake : Snowflake, path : Path):
    mesh_model = MeshModel.from_domain(snowflake._mesh)
    file_path = path / "mesh.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w") as f:
        f.write(mesh_model.model_dump_json())
"""
def load_snowflake(snowflake : Snowflake, snowflake_path : str):
    with open(snowflake_path + "mesh.json", "r") as f:
        data = json.load(f)
    mesh_model = MeshModel.model_validate(data)
    return mesh_model

def save_simulation(self):
    mesh_model = MeshModel.from_domain(self._mesh)
    with open(self._path + "mesh.json", "w") as f:
        f.write(mesh_model.model_dump_json())
"""