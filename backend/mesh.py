from typing import Any
from backend.cell import Cell
from backend.utils import verif_non_negativity, verif_id, create_list_ids, above, above_left, above_right, below, below_left, below_right

from typing import Iterable

class Mesh:
    size : int
    _dict_cells : dict[tuple[int, int], Cell]
    _frozen_cells : set[tuple[int, int]]
    _non_frozen_cells : set[tuple[int, int]]

    def __init__(self, size : int):
        """
        Docstring for __init__
        Create an empty hexagonal Mesh of ray size. The Mesh is composed of (size *) Cell objects.
        The Cells values are set by default to 0.

        :param size: The number of layers of the mesh. Must be a positive integer.
        :type size: int
        """
        verif_non_negativity(size=size)
        self.size = size
        self._dict_cells = {}
        self._non_frozen_cells = set()
        self._frozen_cells = set()
        
        list_ids = create_list_ids(size)
        for id in list_ids:
            cell = Mesh.cell_maker(id, size)
            self[cell.id] = cell
            self._non_frozen_cells.add(cell.id)

    def __getitem__(self, index : tuple[int, int]) -> Cell:
        if not index in self._dict_cells.keys():
            raise IndexError
        return self._dict_cells[index]

    def __setitem__(self, index : tuple[int, int], value : Cell):
        self._dict_cells[index] = value

    def cells_ids(self):
        return self._dict_cells.keys()
    
    def cells(self):
        return self._dict_cells.values()
    
    def items(self):
        return self._dict_cells.items()
    
    def frozen_cells_ids(self)  -> set[tuple[int, int]]:
        return self._frozen_cells
    
    def add_frozen_cells(self, set_cells_id : Iterable[tuple[int, int]]):
        self._frozen_cells.update(set_cells_id)
        self._non_frozen_cells.difference_update(set_cells_id)

    def non_frozen_cells_ids(self) -> set[tuple[int, int]]:
        return self._non_frozen_cells
    
    def add_non_frozen_cells(self, set_cells_id : Iterable[tuple[int, int]]):
        self._frozen_cells.difference_update(set_cells_id)
        self._non_frozen_cells.update(set_cells_id)
    
    @classmethod
    def cell_maker(cls, id : tuple[int, int], size : int) -> Cell:
        verif_id(id)
        verif_non_negativity(size)
        if id[0] > size:
            raise ValueError(f"The id of the cell is out of bound for a Mesh of {size} rings.")
        
        if id[0] == 0 and id[1] == 0:
            position = "center"
            neighbors = cls._compute_neighbors_center()        
        elif id[0] == size and id[1] % size == 0:
            position = "sommet"
            neighbors = cls._compute_neighbors_sommet(id) 
        elif id[0] == size and id[1] % size != 0:
            position = "bords"
            neighbors = cls._compute_neighbors_bords(id) 
        elif id[0] != size and id[1] % id[0] == 0:
            position = "arrete"
            neighbors = cls._compute_neighbors_arrete(id) 
        elif id[0] != size and id[1] % id[0] != 0:
            position = "interieur"
            neighbors = cls._compute_neighbors_interieur(id)

        return Cell(id=id,
            neighbors= neighbors,
            temperature = 0,
            vapor = 0,
            ice_potential = 0,
            frozen = False,
            position=position
        )
    
    @staticmethod
    def _compute_neighbors_center() -> set[tuple[int, int]]:
        return { (1,0), (1,1), (1,2), (1,3), (1,4), (1,5) }

    @staticmethod
    def _compute_neighbors_arrete(id : tuple[int, int]) -> set[tuple[int, int]]:
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
    
    @staticmethod
    def _compute_neighbors_bords(id : tuple[int, int]) -> set[tuple[int, int]]:
        verif_id(id)
        r, i = id
        return {
            below_right(r,i),
            below(r,i),
            below_left(r,i),
            above_left(r, i)
        }

    @staticmethod
    def _compute_neighbors_sommet(id : tuple[int, int]) -> set[tuple[int, int]]:
        verif_id(id)
        r, i = id
        return {
            below_right(r,i),
            below(r,i),
            below_left(r,i)
        }

    @staticmethod
    def _compute_neighbors_interieur(id : tuple[int, int]) -> set[tuple[int, int]]:
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
    
    def _compute_number_frozen_neighbors(self, id : tuple[int, int]) -> int:  
        return sum([self[neighbor_id].frozen for neighbor_id in self[id].neighbors])