from src.config import CONDENSATION_RATE, VAPOR_THRESHOLD
import numpy as np
class Cell:
    id : tuple[int, int] = (0,0)
    neighbors : set[tuple[int, int]] = set()
    temperature :float = 0
    vapor : float = 0
    ice_potential : float = 0 
    state : int = 0

    def __init__(self, id : tuple[int, int], neighbors : set[tuple[int, int]], temperature : float = 0, vapor : float = 0, ice_potential : float = 0, state : int = 0):
        self.id = id
        self.neighbors = neighbors
        self.temperature = temperature
        self.vapor = vapor
        self.ice_potential = ice_potential
        self.state = state
    
    def condensation(self, alpha, vapor_sat):
        # def vapor_saturation_threshold(temperature : float) -> float:
        #     return 1
        #vapor_sat = vapor_saturation_threshold(self.temperature)        
        if self.vapor > vapor_sat:
            self.ice_potential+= alpha *(self.vapor - vapor_sat)
            self.vapor-= alpha * (self.vapor - vapor_sat)

    def randomize_cell(self):
        self.vapor = np.random.rand() * 10
        self.temperature = (np.random.rand() - 1) * 20
        self.ice_potential = np.random.rand() * 10
        self.state = np.random.randint(2)

    def to_dict(self):
        return {
            "id" : self.id,
            "neighbors" : self.neighbors,
            "vapor" : self.vapor,
            "temperature" : self.temperature,
            "ice_potential" : self.ice_potential,
            "state" : self.state
        }

    @classmethod
    def from_dict(cls, cell_d):
        id = cell_d["id"]
        neighbors = cell_d["neighbors"]
        temperature = cell_d["temperature"]
        vapor = cell_d["vapor"]
        ice_potential = cell_d["ice_potential"]
        state = cell_d["state"]
        return cls(id=id, neighbors= neighbors, temperature=temperature, vapor = vapor, ice_potential=ice_potential, state= state)