from src.mesh import Mesh
from cell_2 import Cell
import json

class MeshEncodeur(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)
    
    def encode(self, obj):
        obj = self.default(obj)
        def convert(obj):
            if isinstance(obj, dict):
                return {
                    str(k) if isinstance(k, tuple) else k: convert(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, set):
                return [convert(i) for i in obj]
            else:
                return obj

        obj = convert(obj)
        return super().encode(obj)


class MeshDecoder:
    def __call__(self, obj):
        if "id" in obj and "neighbors" in obj: #C'est une Cell
            obj["id"] = tuple(obj["id"])
            obj["neighbors"] = {tuple(cell_id) for cell_id in obj["neighbors"]}
            return Cell.from_dict(obj)
        if "dict_cells" in obj: # C'est un mesh
            obj["dict_cells"] = {eval(key): cell for key,cell in obj["dict_cells"].items()}
            obj["frozen_cells"] = {tuple(cell_id) for cell_id in obj["frozen_cells"]}
            obj["non_frozen_cells"] = {tuple(cell_id) for cell_id in obj["non_frozen_cells"]}
            return Mesh.from_dict(obj)

        return obj
    
def save_mesh(mesh : Mesh,  filename:str):
    m_str = json.dumps(mesh, cls=MeshEncodeur, indent = 4)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(m_str)

def load_mesh(filename:str) -> Mesh:
    with open(filename, "r", encoding="utf-8") as f:
        mesh = json.load(f, object_hook=MeshDecoder())
    return mesh