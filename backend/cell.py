from backend.utils import verif_alpha, verif_non_negativity
from dataclasses import dataclass
from statistics import mean

@dataclass
class Cell:
    id : tuple[int, int]
    neighbors : set[tuple[int, int]]
    position : str
    temperature : float = 0
    vapor : float = 0
    ice_potential : float = 0
    frozen : bool = False

    def condensation(self, alpha_condensation : float, vapor_saturation : float):
        verif_alpha(alpha_condensation = alpha_condensation)
        verif_non_negativity(vapor_saturation = vapor_saturation)
        if self.vapor > vapor_saturation:
            self.ice_potential+= alpha_condensation *(self.vapor - vapor_saturation)
            self.vapor-= alpha_condensation * (self.vapor - vapor_saturation)
    
    def vapor_diffusion(self, alpha_vapor : float, vapor_neighbors : list[float]):
        verif_alpha(alpha_vapor = alpha_vapor)
        if len(self.neighbors) != len(vapor_neighbors):
            raise ValueError("The number of vapors in vapors_neighbors must be equal to the neighbors number of this cell.")
        self.vapor = (alpha_vapor * mean([vapor for vapor in vapor_neighbors]) 
                    + (1 - alpha_vapor) * self.vapor)
        
    def vapor_diffusion_2(self, alpha_vapor : float, beta_vapor : float, LIST : list[tuple[float, float]], pour_moi : float):
        verif_alpha(alpha_vapor = alpha_vapor)
        if len(self.neighbors) != len(LIST):
            raise ValueError("The number of vapors in vapors_neighbors must be equal to the neighbors number of this cell.")
        self.vapor = (alpha_vapor * mean([vapor for vapor,_ in LIST]) 
                    + (1 - alpha_vapor) * self.vapor
                    +beta_vapor * (pour_moi - mean([A_neigh for _,A_neigh in LIST]))
        )

    def temperature_diffusion(self, alpha_temperature : float, temp_neighbors : list[float]):
        verif_alpha(alpha_temperature = alpha_temperature)
        if len(self.neighbors) != len(temp_neighbors):
            raise ValueError("The number of temperatures in temp_neighbors must be equal to the neighbors number of this cell.")
        self.temperature = (alpha_temperature * mean([temp for temp in temp_neighbors]) 
                         + (1 - alpha_temperature) * self.temperature)

    def freeze(self, ice_threshold : float, temperature_threshold : float, n_frozen_neighbors_threshold : int, n_frozen_neighbors : int):
        if self.temperature <= temperature_threshold and self.ice_potential >= ice_threshold and n_frozen_neighbors >= 1:
            self.frozen = True
            self.ice_potential = 0
        elif n_frozen_neighbors >= n_frozen_neighbors_threshold:
            self.frozen = True
            self.ice_potential = 0
        return self.frozen