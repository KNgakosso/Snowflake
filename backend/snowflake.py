from backend.mesh import Mesh
from backend.initialization_params import InitParams
from backend.physical_params import PhysicalParams
from backend.simul_params import SimulParams
from backend.utils import verif_alpha, verif_non_negativity
import random

class Snowflake:
    _mesh : Mesh
    _initialization_params : InitParams
    _physical_params : PhysicalParams
    _simulation_params: SimulParams
    def __init__(self):
        self._initialization_params = InitParams(
            size= 20
        )

        self._simulation_params = SimulParams(
            iterations= 10
        )

        self._physical_params = PhysicalParams(
            alpha_temperature= 0.1,
            alpha_vapor= 0.1,
            beta_vapor = 1000,
            alpha_condensation= 0.4,
            vapor_saturation= 1,
            ice_threshold= 30, 
            temperature_threshold= 0,
            n_frozen_neighbors_threshold= 6
        )
        self._mesh = Mesh(self._initialization_params.size)
        self.randomize()
    
    def update_initilization_params(self, init_params : InitParams):
        self._initialization_params = init_params
        self.build()
        self.randomize()

    def update_simulation_params(self, simul_params : SimulParams):
        self._simulation_params = simul_params

    def update_physical_params(self, physical_params : PhysicalParams):
        self._physical_params = physical_params

    def build(self):
        self._mesh = Mesh(self._initialization_params.size)

    def set_temperature(self, temperature : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id or self._mesh.cells_ids()
        for cell_id in ids:
            self._mesh[cell_id].temperature = temperature

    def set_vapor(self, vapor : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id or self._mesh.cells_ids()
        for cell_id in ids:
            self._mesh[cell_id].vapor = vapor

    def set_ice_potential(self, ice_potential : float, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id or self._mesh.cells_ids()
        for cell_id in ids:
            self._mesh[cell_id].ice_potential = ice_potential

    def set_frozen_true(self, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id or self._mesh.cells_ids()
        for cell_id in ids:
            self._mesh[cell_id].frozen = True
        self._mesh.add_frozen_cells(ids)
    
    def set_frozen_false(self, set_cells_id : set[tuple[int, int]] | None = None):
        ids = set_cells_id or self._mesh.cells_ids()
        for cell_id in ids:
            self._mesh[cell_id].frozen = False
        self._mesh.add_non_frozen_cells(ids)

    def _vapor_diffusion_step(self):
        #compute all vapors
        prev_vapors = {id : cell.vapor for id, cell in self._mesh.items()}
        for cell in self._mesh.cells():
            vapor_neighbors = [prev_vapors[neighbor_id] for neighbor_id in cell.neighbors]
            cell.vapor_diffusion(self._physical_params.alpha_vapor, 
                                 vapor_neighbors
                    )

    def _vapor_diffusion_step_2(self):
        #compute all vapors
        prev_vapors = {id : cell.vapor for id, cell in self._mesh.items()}
        for cell in self._mesh.cells():
            LIST = [(prev_vapors[neighbor_id], self._A(neighbor_id)) for neighbor_id in cell.neighbors]
            cell.vapor_diffusion_2(
                    alpha_vapor=self._physical_params.alpha_vapor,
                    beta_vapor=self._physical_params.beta_vapor,
                    LIST=LIST, 
                    pour_moi=self._A(cell.id)
            )

    def _temperature_diffusion_step(self):
        #compute all temperatures
        prev_temps = {id : cell.temperature for id, cell in self._mesh.items()}
        for cell in self._mesh.cells():
            temp_neighbors = [prev_temps[neighbor_id] for neighbor_id in cell.neighbors]
            cell.temperature_diffusion(self._physical_params.alpha_temperature,
                                       temp_neighbors
                    )
    
    def _condensation_step(self):
        for cell in self._mesh.cells():
            cell.condensation(
                alpha_condensation=self._physical_params.alpha_condensation,
                vapor_saturation=self._physical_params.vapor_saturation
            )
    
    def _freeze_step(self):
        new_frozen_cells_ids = set()
        DICT = {id : self._mesh._compute_number_frozen_neighbors(id) for id in self._mesh.non_frozen_cells_ids()}
        for id in self._mesh.non_frozen_cells_ids():
            n_frozen_neighbors = DICT[id]
            result_is_frozen = self._mesh[id].freeze(
                ice_threshold= self._physical_params.ice_threshold, 
                temperature_threshold= self._physical_params.temperature_threshold,
                n_frozen_neighbors_threshold= self._physical_params.n_frozen_neighbors_threshold,
                n_frozen_neighbors=n_frozen_neighbors
            )
            if result_is_frozen:
                new_frozen_cells_ids.add(id)
        self._mesh.add_frozen_cells(new_frozen_cells_ids)

    def step(self):
        """
        Docstring for step

        Perform a single change on the Mesh.
        Diffusion, condesation etc
        
        :param self: Description
        """
        verif_non_negativity(self._physical_params.vapor_saturation, self._physical_params.ice_threshold)
        verif_alpha(self._physical_params.alpha_temperature, self._physical_params.alpha_vapor, self._physical_params.alpha_condensation)
        self._temperature_diffusion_step()
        self._vapor_diffusion_step_2()
        self._condensation_step()
        self._freeze_step()

    def _randomize_temperature(self):
        temperature = - random.random() * 200 + 50
        self.set_temperature(temperature, {(0,0)})
        for layer in range(1, self._mesh.size+1):
            for j in range(layer // 2 + 1):
                selection = {(layer, j + i * layer) for i in range(6)}.union(
                    {(layer, (-j - i * layer) % (6 * layer)) for i in range(6)}
                )
                temperature = - random.random() * 200 + 50
                self.set_temperature(temperature, selection)

    def _randomize_vapor(self):
        vapor = random.random() * 100
        self.set_vapor(vapor, {(0,0)})
        for layer in range(1, self._mesh.size+1):
            for j in range(layer // 2 + 1):
                selection = {(layer, j + i * layer) for i in range(6)}.union(
                    {(layer, (-j - i * layer) % (6 * layer)) for i in range(6)}
                )
                vapor = random.random() * 100
                self.set_vapor(vapor, selection)

    def _randomize_ice_potential(self):
        ice_potential = random.random() * 20
        self.set_ice_potential(ice_potential, {(0,0)})
        for layer in range(1, self._mesh.size+1):
            for j in range(layer // 2 + 1):
                selection = {(layer, j + i * layer) for i in range(6)}.union(
                    {(layer, (-j - i * layer) % (6 * layer)) for i in range(6)}
                )
                ice_potential = random.random() * 20
                self.set_ice_potential(ice_potential, selection)
    
    def _A(self, id : tuple[int, int]) -> float:
        r, i = id
        if r == 0:
            return 1
        return (2 * abs(i%r - r/2) / r)**2
    
    def _randomize_frozen(self):
        self.set_frozen_false()
        self.set_frozen_true({(0,0)})

    def randomize(self):
        self._randomize_temperature()
        self._randomize_vapor()
        self._randomize_ice_potential()
        self._randomize_frozen()

    def run_simulation(self):
        for i in range(self._simulation_params.iterations):
            self.step()
        return self._mesh

    def set_mesh(self, mesh : Mesh):
        self._mesh = mesh
    
    def mesh_dirichlet(self):
        pass

    def initial_state_triangle(self):
        pass