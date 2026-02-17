from src.mesh import Mesh
from src.mesh_io import save_mesh, load_mesh, MeshEncodeur
import json
# m = Mesh(40)
# m.set_vapor(20)
# m.set_temperature(-10)
# m.freeze_cell((0,0))
# m.generate_snowflake(nb_iter= 10, 
#                     condensation_rate = 0.1,
#                     vapor_threshold = 1.,
#                     freeze_threshold = 1.,
#                     vapor_diffusion_rate = 0.1,
#                     temperature_diffusion_rate = 0.1,
#                     temperature_threshold = 0
#                     )
# m.print()

m = Mesh(2)
m.build()
m.random_mesh()
m.generate_snowflake(nb_iter= 1, 
                    condensation_rate = 0.1,
                    vapor_threshold = 0.,
                    freeze_threshold = 0.5,
                    vapor_diffusion_rate = 0.1,
                    temperature_diffusion_rate = 0.1,
                    temperature_threshold = 20
                    )
#m.print()
c = m.dict_cells[(0,0)]

#print("ID : ",c.id, " | vapor : ",  c.vapor, " | temperature : ", c.temperature, " | ice_potential : ", c.ice_potential , " | state : ", c.state)


test = json.dumps(m, cls=MeshEncodeur)
print(test)
save_mesh(m, "premier_mesh.json")
m2 = load_mesh("premier_mesh.json")
print("nb_rings", m2.dict_cells[(0,0)])


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