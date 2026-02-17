from src.cell import Cell
from src.mesh_params import MeshParams
from src.utils import verif_alpha, verif_non_negativity, verif_id, create_list_ids, above, above_left, above_right, below, below_left, below_right

class Mesh:
    nb_rings : int
    dict_cells : dict[tuple[int, int], Cell] = {}
    frozen_cells : set[tuple[int, int]] = set()
    non_frozen_cells : set[tuple[int, int]] = set()

    def __init__(self, nb_rings : int):
        """
        Docstring for __init__
        Create an empty hexagonal Mesh of ray nb_rings. The Mesh is composed of (nb_rings *) Cell objects.
        The Cells values are set by default to 0.

        :param nb_rings: The number of layers of the mesh. Must be a positive integer.
        :type nb_rings: int
        """
        verif_non_negativity(nb_rings=nb_rings)
        self.nb_rings = nb_rings
        self.dict_cells = {}
        self.non_frozen_cells = set()
        self.frozen_cells = set()
        
        list_ids = create_list_ids(nb_rings)
        for id in list_ids:
            cell = Mesh.cell_maker(id, nb_rings)
            self.add_cell(cell)

    @classmethod
    def cell_maker(cls, id : tuple[int, int], nb_rings : int):
        verif_id(id)
        verif_non_negativity(nb_rings)
        if id[0] > nb_rings:
            raise ValueError(f"The id of the cell is out of bound for a Mesh of {nb_rings} rings.")
        
        if id[0] == 0 and id[1] == 0:
            position = "center"
            neighbors = compute_neighbors_center()        
        elif id[0] == nb_rings and id[1] % nb_rings == 0:
            position = "sommet"
            neighbors = compute_neighbors_sommet(id) 
        elif id[0] == nb_rings and id[1] % nb_rings != 0:
            position = "bords"
            neighbors = compute_neighbors_bords(id) 
        elif id[0] != nb_rings and id[1] % id[0] == 0:
            position = "arrete"
            neighbors = compute_neighbors_arrete(id) 
        elif id[0] != nb_rings and id[1] % id[0] != 0:
            position = "interieur"
            neighbors = compute_neighbors_interieur(id)

        return Cell(id=id,
            neighbors= neighbors,
            temperature = 0,
            vapor = 0,
            ice_potential = 0,
            frozen = False,
            position=position
        )

    def add_cell(self, cell : Cell):
        self.dict_cells[cell.id] = cell
        self.non_frozen_cells.add(cell.id)

    def set_temperature(self, temperature : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id if not set_cells_id is None else self.dict_cells.keys()
        for cell_id in ids:
            self.dict_cells[cell_id].temperature = temperature

    def set_vapor(self, vapor : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id if not set_cells_id is None else self.dict_cells.keys()
        for cell_id in ids:
            self.dict_cells[cell_id].vapor = vapor

    def set_ice_potential(self, ice_potential : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id if not set_cells_id is None else self.dict_cells.keys()
        for cell_id in ids:
            self.dict_cells[cell_id].ice_potential = ice_potential

    def set_frozen_true(self, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id if not set_cells_id is None else self.dict_cells.keys()
        for cell_id in ids:
            self.dict_cells[cell_id].frozen = True
            self.frozen_cells.add(cell_id)
            self.non_frozen_cells.discard(cell_id)
    
    def set_frozen_false(self, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id if not set_cells_id is None else self.dict_cells.keys()
        for cell_id in ids:
            self.dict_cells[cell_id].frozen = False
            self.non_frozen_cells.add(cell_id)
            self.frozen_cells.discard(cell_id)

    def vapor_diffusion_step(self, alpha_vapor : float):
        verif_alpha(alpha_vapor)
        #compute all vapors
        prev_vapors = {id : cell.vapor for id, cell in self.dict_cells.items()}
        for id, cell in self.dict_cells.items():
            vapor_neighbors = [prev_vapors[neighbor_id] for neighbor_id in cell.neighbors]
            cell.vapor_diffusion(alpha_vapor, vapor_neighbors)

    def temperature_diffusion_step(self, alpha_temperature : float):
        verif_alpha(alpha_temperature)
        #compute all temperatures
        prev_temps = {id : cell.temperature for id, cell in self.dict_cells.items()}
        for id, cell in self.dict_cells.items():
            temp_neighbors = [prev_temps[neighbor_id] for neighbor_id in cell.neighbors]
            cell.temperature_diffusion(alpha_temperature, temp_neighbors)
    
    def condensation_step(self, alpha_condensation : float, vapor_saturation : float):
        verif_alpha(alpha_condensation)
        verif_non_negativity(vapor_saturation)
        for id, cell in self.dict_cells.items():
            cell.condensation(alpha_condensation=alpha_condensation, vapor_saturation=vapor_saturation)

    def freeze_step(self, ice_threshold : float, temperature_threshold : float, n_frozen_neighbors_threshold : int):
        verif_non_negativity(ice_threshold)
        new_frozen_cells = set()
        for id in self.non_frozen_cells:
            n_frozen_neighbors = self.compute_number_frozen_neighbors(id)
            self.dict_cells[id].freeze(ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, n_frozen_neighbors)
            if self.dict_cells[id].frozen:
                new_frozen_cells.add(id)
        self.non_frozen_cells.difference_update(new_frozen_cells)
        self.frozen_cells.update(new_frozen_cells)

    def freeze_step(self, ice_threshold : float, temperature_threshold : float, n_frozen_neighbors_threshold : int):
        verif_non_negativity(ice_threshold)
        new_frozen_cells = set()
        for id in self.non_frozen_cells:
            n_frozen_neighbors = self.compute_number_frozen_neighbors(id)
            result_is_frozen = self.dict_cells[id].freeze(ice_threshold, temperature_threshold, n_frozen_neighbors_threshold, n_frozen_neighbors)
            if result_is_frozen:
                new_frozen_cells.add(id)
        self.non_frozen_cells.difference_update(new_frozen_cells)
        self.frozen_cells.update(new_frozen_cells)

    def step(self, params : MeshParams):
        """
        Docstring for step

        Perform a single change on the Mesh.
        Diffusion, condesation etc
        
        :param self: Description
        """
        verif_non_negativity(params.vapor_saturation, params.ice_threshold)
        verif_alpha(params.alpha_temperature, params.alpha_vapor, params.alpha_condensation)
        self.temperature_diffusion_step(params.alpha_temperature)
        self.vapor_diffusion_step(params.alpha_vapor)
        self.condensation_step(params.alpha_condensation, params.vapor_saturation)
        self.freeze_step(params.ice_threshold, params.temperature_threshold, params.n_frozen_neighbors_threshold)

    def compute_number_frozen_neighbors(self, id : tuple[int, int]):  
        return len([self.dict_cells[neighbor_id].frozen for neighbor_id in self.dict_cells[id].neighbors])
    
def compute_neighbors_center():
    return { (1,0), (1,1), (1,2), (1,3), (1,4), (1,5) }

def compute_neighbors_arrete(id : tuple[int, int]) -> set[tuple[int, int]]:
    verif_id(id)
    r, i = id
    return{
        above(r,i),
        above_right(r,i),
        below_right(r,i),
        below(r,i),
        below_left(r,i),
        above_left(r, i)
    }

def compute_neighbors_bords(id : tuple[int, int]) -> set[tuple[int, int]]:
    verif_id(id)
    r, i = id
    return {
        below_right(r,i),
        below(r,i),
        below_left(r,i),
        above_left(r, i)
    }

def compute_neighbors_sommet(id : tuple[int, int]) -> set[tuple[int, int]]:
    verif_id(id)
    r, i = id
    return {
        below_right(r,i),
        below(r,i),
        below_left(r,i)
    }

def compute_neighbors_interieur(id : tuple[int, int]) -> set[tuple[int, int]]:
    verif_id(id)
    r, i = id
    return{
        above(r,i),
        above_right(r,i),
        below_right(r,i),
        below(r,i),
        below_left(r,i),
        above_left(r,i)
    }