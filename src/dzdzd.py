import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, RegularPolygon
import numpy as np
nb_rings = 1


dict_cells = {(0,0)}
def print_():
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
    
    for rings in range (nb_rings+1):
        dict_cells.update({(rings,i) for i in range(6*rings)})
    fig, ax = plt.subplots()

    for cell_id in dict_cells:
        x, y = convert_id_to_cart(cell_id)
        center = convert_id_to_cart(cell_id)
        hexagon = RegularPolygon(center, radius=1/np.sqrt(3), numVertices=6, orientation= np.pi/6, edgecolor = 'black', facecolor = 'none')
        ax.add_patch(hexagon)
        
    ax.set_xlim(-1.5*nb_rings, 1.5*nb_rings)
    ax.set_ylim(-1.5*nb_rings, 1.5*nb_rings)
    ax.set_aspect('equal')
    plt.title("Hexagone avec Patchs")
    plt.show()
print_()