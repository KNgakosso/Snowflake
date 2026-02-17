from src.mesh import Mesh, Cell
from src.mesh_io import MeshEncodeur, MeshDecoder, save_mesh, load_mesh
import pytest
import json

# TEST_SAVE_MESH
########################

def  test_save_mesh(tmp_path, simple_mesh):
    mesh: Mesh = simple_mesh()
    path = tmp_path / "mesh.json"
    save_mesh(mesh, path)

    with open(path) as f:
        data = json.load(f)

    assert "dict_cells" in data
    assert isinstance(data["dict_cells"], dict)
    assert len(data["dict_cells"]) == len(mesh.dict_cells)

# TEST_LOAD_MESH
########################
def test_mesh_load_from_known_json(tmp_path):
    json_data = {
        "nb_rings": 2,
        "dict_cells": {
            "(0, 0)": {
                "id" : [0,0],
                "neighbors" : [[1,0], [1,1], [1,2], [1,3], [1,4], [1,5]],
                "temperature": -10,
                "vapor": 1.0,
                "ice_potential": 0.0,
                "state": 0
            }
        },
        "frozen_cells" : [],
        "non_frozen_cells" : [[0,0]]
    }

    path = "mesh.json"
    with open(path, "w") as f:
        json.dump(json_data, f)

    mesh = load_mesh(path)
    assert mesh.nb_rings == 2
    assert (0, 0) in mesh.dict_cells
    cell = mesh.dict_cells[(0, 0)]
    assert cell.temperature == -10
    assert len(mesh.frozen_cells) == 0
    assert len(mesh.non_frozen_cells) == 1

def test_save_load(tmp_path, simple_mesh):
    mesh_1 : Mesh= simple_mesh()
    path = tmp_path / "mesh.json"
    save_mesh(mesh_1, path)

    mesh_2 = load_mesh(path)

    assert mesh_1.nb_rings == mesh_2.nb_rings
    assert mesh_1.dict_cells == mesh_2.dict_cells
    assert mesh_1.frozen_cells == mesh_2.frozen_cells
    assert mesh_1.non_fozen_cells == mesh_2.non_fozen_cells
    