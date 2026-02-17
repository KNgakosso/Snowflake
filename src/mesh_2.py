from src.cell import Cell
#from IPython import embed
from statistics import mean
import copy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon
import json

class Mesh:
    nb_rings : int = 1
    dict_cells : dict[tuple[int, int], Cell] = {}
    frozen_cells : set = set()
    non_frozen_cells : set = set()

    def __init__(self, nb_rings : int = 2):
        self.nb_rings = nb_rings
        self.dict_cells = {}
        self.frozen_cells = set()
        self.non_fozen_cells = set()

    def build(self):
        dict_cells = {}
        self.nb_rings = self.nb_rings
        if self.nb_rings == 0:
            dict_cells[(0,0)] = Cell((0,0), set())
        else:
            #centre
            dict_cells[(0,0)] = Cell((0,0), {(1, i) for i in range(6)})

            #sommet
            for side in range(6):
                id = (self.nb_rings, self.nb_rings * side)
                neighbors = {(self.nb_rings, (self.nb_rings * side + 1) % (self.nb_rings * 6)),
                                (self.nb_rings, (self.nb_rings * side - 1) % (self.nb_rings * 6)),
                                (self.nb_rings - 1, (self.nb_rings - 1) * side)
                }
                dict_cells[id] = Cell(id, neighbors)

            #bord
            for side in range(6):
                for i in range(1, self.nb_rings):
                    id = (self.nb_rings, self.nb_rings * side + i)
                    neighbors = {(self.nb_rings, (self.nb_rings * side + i + 1) % (6 * self.nb_rings)),
                                    (self.nb_rings, (self.nb_rings * side + i - 1) % (6 * self.nb_rings)),
                                    (self.nb_rings - 1, ((self.nb_rings - 1) * side + i) % (6 * (self.nb_rings - 1))),
                                    (self.nb_rings - 1, ((self.nb_rings - 1) * side + i -1) % (6 * (self.nb_rings -1)))
                    }
                    dict_cells[id] = Cell(id, neighbors)

            #arrete
            for side in range(6):
                for i in range(1, self.nb_rings):
                    id = (i, i * side)
                    neighbors = {(i+1, (i+1)*side),
                                    (i+1, ((i+1)*side+1) % (6 * (i+1))),
                                    (i+1, ((i+1)*side-1) % (6 * (i+1))),
                                    (i, (i*side+1) % (6*i)),
                                    (i, (i*side-1) % (6*i)),
                                    (i-1, (i-1)*side % max((6 * (i-1)), 1))
                    }
                    dict_cells[id] = Cell((id), neighbors)

            #interieur
            for ring in range(2, self.nb_rings):
                for side in range(6):
                    for i in range(1, ring):
                        id = (ring, ring * side + i)
                        neighbors = {(ring, (ring * side + i + 1) % (6 * ring)),
                                        (ring, (ring * side + i - 1) % (6 * ring)),
                                        (ring - 1, ((ring - 1) * side + i) % (6 * (ring - 1))),
                                        (ring - 1, ((ring - 1) * side + i - 1) % (6 * (ring - 1))),
                                        (ring + 1, ((ring + 1) * side + i) % (6 * (ring + 1))),
                                        (ring + 1, ((ring + 1) * side + i + 1) % (6*(ring + 1)))
                        }
                        dict_cells[id] = Cell((id), neighbors)
        self.dict_cells = dict_cells
        self.frozen_cells = set()
        self.non_frozen_cells = {id for id in self.dict_cells.keys()}

    def set_temperature(self, temperature):
        for cell in self.dict_cells.values():
            cell.temperature = temperature
    
    def set_vapor(self, vapor):
        for cell in self.dict_cells.values():
            cell.vapor = vapor

    def set_dirichlet_vapor(self, vapor : float = 1):
        for id, cell in self.dict_cells.items():
            if id[0] == self.nb_rings:
                cell.vapor = vapor

    def set_dirichlet_temperature(self, temperature : float = 0):
        for id, cell in self.dict_cells.items():
            if id[0] == self.nb_rings:
                cell.temperature = temperature


    def freeze_cell(self, id : tuple[int, int]):
        self.non_frozen_cells.discard(id)
        self.frozen_cells.add(id)
        self.dict_cells[id].state = 1

    def freeze_cells(self, set_ids : set[tuple[int, int]]):
        self.non_frozen_cells.difference_update(set_ids)
        self.frozen_cells.update(set_ids)
        for id in set_ids:
            self.dict_cells[id].state = 1

    def diffusion_vapor(self, alpha):
        new_dico = copy.deepcopy(self.dict_cells)
        for id in self.non_frozen_cells:
            #if id[0] != self.nb_rings:
            list_voisins_non_frozen = self.dict_cells[id].neighbors & self.non_frozen_cells
            list_vapor_neighbors_non_frozen = [self.dict_cells[id_voisin].vapor for id_voisin in list_voisins_non_frozen]
            mean_vapor = mean(list_vapor_neighbors_non_frozen + [self.dict_cells[id].vapor])
            new_dico[id].vapor+= alpha * (mean_vapor - self.dict_cells[id].vapor) 
        self.dict_cells = new_dico.copy()
    

    def diffusion_temperature(self, alpha):
        new_dico = copy.deepcopy(self.dict_cells)
        for id, cell in self.dict_cells.items():
            #if id[0] != self.nb_rings:
            mean_temperature = mean([self.dict_cells[id_voisin].temperature for id_voisin in cell.neighbors])
            new_dico[id].temperature+= alpha * (mean_temperature - self.dict_cells[id].temperature) 
        self.dict_cells = new_dico.copy()

    def condensation(self, alpha, vapor_sat):
        for id in self.non_frozen_cells:
            self.dict_cells[id].condensation(alpha=alpha, vapor_sat = vapor_sat)

    def freeze(self, ice_threshold, temperature_threshold):
        new_frozen = set()
        for id in self.non_frozen_cells:
            if self.dict_cells[id].temperature <= temperature_threshold and self.dict_cells[id].ice_potential > ice_threshold:
                new_frozen.add(id)
                n_frozen_voisins = len(self.dict_cells[id].neighbors & self.frozen_cells )
                if n_frozen_voisins >= 1:
                    new_frozen.add(id)
        self.freeze_cells(new_frozen)


    def generate_snowflake(self, nb_iter, condensation_rate, vapor_threshold, freeze_threshold, vapor_diffusion_rate, temperature_diffusion_rate, temperature_threshold):
        for i in range(nb_iter):
            self.diffusion_temperature(temperature_diffusion_rate)
            self.diffusion_vapor(vapor_diffusion_rate)
            self.condensation(condensation_rate, vapor_threshold)
            self.freeze(freeze_threshold, temperature_threshold)

    def random_mesh(self):
        for id, cell in self.dict_cells.items():
            cell.randomize_cell()
        if self.dict_cells[id].state == 1:
            self.non_frozen_cells.discard(id)
            self.frozen_cells.add(id)

    def to_dict(self):
        return {
            "nb_rings" : self.nb_rings,
            "frozen_cells" : self.frozen_cells,
            "non_frozen_cells" : self.non_frozen_cells,
            "dict_cells" : self.dict_cells
        }

    def print(self):
        def convert_id_to_cart(cell_id):
            if cell_id == (0,0):
                return 0,0
            side = cell_id[1]//cell_id[0]
            theta_a = side * np.pi/3 + np.pi/2
            theta_b = (side + 1) * np.pi/3 + np.pi/2
            sommet_a = cell_id[0] * np.array([np.cos(theta_a), np.sin(theta_a)])
            sommet_b = cell_id[0] * np.array([np.cos(theta_b), np.sin(theta_b)])
            
            alpha = cell_id[1] % cell_id[0] / cell_id[0]
            x,y = alpha * sommet_a + (1 - alpha) * sommet_b
            return x, y
    
        fig, ax = plt.subplots()

        for cell_id in self.dict_cells.keys():
            x, y = convert_id_to_cart(cell_id)
            center = convert_id_to_cart(cell_id)
            color = "blue" if self.dict_cells[cell_id].state == 1 else "red"
            hexagon = RegularPolygon(center, radius=1/np.sqrt(3), numVertices=6, orientation= np.pi/6, edgecolor = color, facecolor = color)
            ax.add_patch(hexagon)
            
        ax.set_xlim(-1.5*self.nb_rings, 1.5*self.nb_rings)
        ax.set_ylim(-1.5*self.nb_rings, 1.5*self.nb_rings)
        ax.set_aspect('equal')
        plt.title("Hexagone avec Patchs")
        plt.show()
    
    @classmethod
    def from_dict(cls, mesh_d):
        nb_rings = mesh_d["nb_rings"]
        mesh = cls(nb_rings=nb_rings)
        dict_cells = {}
        for key, cell_obj in mesh_d["dict_cells"].items():
            if isinstance(cell_obj, dict):
                dict_cells[key] = Cell.from_dict(cell_obj)
            else:
                dict_cells[key] = cell_obj

        mesh.dict_cells = dict_cells
        mesh.frozen_cells = mesh_d["frozen_cells"]
        mesh.non_frozen_cells = mesh_d["non_frozen_cells"]
        return mesh

    def bruit(self):
        pass
