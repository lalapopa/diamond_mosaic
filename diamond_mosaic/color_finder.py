import math
import numpy as np
from scipy.spatial import cKDTree



def close_color(rgb_color, color_data):
    rgb_colors = np.array(list(color_data.values()))
    dmc_code = np.array(list(color_data.keys()))
    similar_color_idx = cKDTree(rgb_colors).query(rgb_color, k=1)[1]
    return rgb_colors[similar_color_idx], dmc_code[similar_color_idx]
