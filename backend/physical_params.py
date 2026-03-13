from dataclasses import dataclass

@dataclass
class PhysicalParams():
    alpha_temperature : float
    alpha_vapor : float
    beta_vapor : float
    alpha_condensation : float
    vapor_saturation : float
    ice_threshold : float 
    temperature_threshold : float
    n_frozen_neighbors_threshold : int