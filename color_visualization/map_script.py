import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

# NOTE: SET THE FOLDER CONTAINING THE DATA FILES !
files_path = './data_visualization/data'

def hsv2rgb(h, s, v): # supporting function converting hsv to rgb
    hsv = np.zeros(shape=(1, 3), dtype=float)
    hsv[0, 0] = h
    hsv[0, 1] = s
    hsv[0, 2] = v
    rgb = colors.hsv_to_rgb(hsv)
    r, g, b = rgb[0, 0], rgb[0, 1], rgb[0, 2]
    return (r, g, b)

# calculate the gradient for each pixel individually
def map_gradient(value, angle):
    hue = (1/3 - ((value - 43.252) / (153.833 - 43.252) / 3))
    saturation = (np.clip(1 - ((angle - 0.52) / (2.778 - 0.52) - 0.4) * (1/0.6), 0, 1))
    brightness = np.clip((np.log(angle) + 0.654) / (1.022 + 0.654) * (1/0.7), 0, 1)

    return hsv2rgb(hue, saturation, brightness)


# calculate the gradient for the entire data
def compound_map_gradient(values, angles):
    min_value = np.min(values) # 43.2528741577922
    max_value = np.max(values) # 153.832040129247
    # normalize to get values between 0 and 1
    normalized_values = (values - min_value) / (max_value - min_value) 
    # calculate hue based on normalized values
    hue = 1/3 - (normalized_values / 3)

    min_angle = np.min(angles) # 0.5201196094972295
    max_angle = np.max(angles) # 2.7774647881769297
    # normalize to get values between 0 and 1
    normalized_angles = (angles - min_angle) / (max_angle - min_angle)
    # calculate saturation based on normalized angles
    saturation = np.clip(1 - (normalized_angles - 0.4) * (1/0.6), 0, 1)

    # transform min and max values
    log_min = np.log(min_angle) # -0.6536964755929061
    log_max = np.log(max_angle) # 1.0215385649272297
    # calculate log values for the angles (BUG: angle == 0)
    log_angles = np.log(angles)
    # normalize to get values between 0 and 1
    normalized_log_angles = (log_angles - log_min) / (log_max - log_min)
    # calculate brightness based on normalized log angles
    brightness = np.clip(normalized_log_angles * (1/0.7), 0, 1)

    return colors.hsv_to_rgb(np.stack((hue, saturation, brightness), axis=-1))

def read_file(file_path):
    with open(file_path, 'r') as file:
        # read the first line
        line = file.readline()  
        values = line.strip().split()
        params = np.array([np.int32(values[0]), np.int32(values[1]), np.float64(values[2]) / 1000], dtype=object)

        # read the rest of the file
        data = np.loadtxt(file)

        return (data, params)
    
def draw_map(data, angles, params):
    # set the font
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams['font.size'] = 10
    # set the rest of the paramethers
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['xtick.top'] = True
    plt.rcParams['xtick.bottom'] = True
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.right'] = True
    plt.rcParams['ytick.left'] = True
    
    fig, ax = plt.subplots(figsize=(4, 4))


    # NOTE calculate the image using the map_gradient
    
    # create a matrix holding the rgb values of the map points
    img = np.empty((params[0], params[1], 3))
    for (i, j), v in np.ndenumerate(data):
        img[i, j] = map_gradient(v, angles[i, j])

    # convert to image and set the axes's range
    im = ax.imshow(img, aspect='auto')
    im.set_extent([0, params[0] - 1, params[1] - 1, 0])


    # NOTE calculate the image using the compound_map_gradient
    
    # img = compound_map_gradient(data, angles)
    # im = ax.imshow(img, aspect='auto')
    # im.set_extent([0, params[0] - 1, params[1] - 1, 0])

    fig.savefig('map.pdf')

def calculate_normals(data, params):
    normal_vectors = np.empty((params[0], params[1], 3))
    dist = params[2]

    # calculate normals for the main grid, excluding the last row and column
    x_diffs = data[1:, :-1] - data[:-1, :-1]
    y_diffs = data[:-1, 1:] - data[:-1, :-1]
    vec1 = np.stack((dist * np.ones_like(y_diffs), 
                     np.zeros_like(y_diffs), 
                     y_diffs), axis=-1)
    vec2 = np.stack((np.zeros_like(x_diffs), 
                     dist * np.ones_like(x_diffs), 
                     x_diffs), axis=-1)
    normal_vectors[:-1, :-1] = np.cross(vec1, vec2)

    # calculate normals for the last row, excluding the last value
    x = params[0] - 1
    x_diffs = data[x - 1, :-1] - data[x, :-1]
    y_diffs = data[x, 1:] - data[x, :-1]
    vec1 = np.stack((np.zeros_like(x_diffs), 
                     -dist * np.ones_like(x_diffs), 
                     x_diffs), axis=-1)
    vec2 = np.stack((dist * np.ones_like(y_diffs), 
                     np.zeros_like(y_diffs), 
                     y_diffs), axis=-1)
    normal_vectors[x, :-1] = np.cross(vec1, vec2)

    # calculate normals for the last column, excluding the last value
    y = params[1] - 1
    x_diffs = data[1:, y] - data[:-1, y] 
    y_diffs = data[:-1, y - 1] - data[:-1, y]
    vec1 = np.stack((np.zeros_like(x_diffs), 
                     dist * np.ones_like(x_diffs), 
                     x_diffs), axis=-1)
    vec2 = np.stack((-dist * np.ones_like(y_diffs), 
                     np.zeros_like(y_diffs), 
                     y_diffs), axis=-1)
    normal_vectors[:-1, y] = np.cross(vec1, vec2)

    # calculate the normal for the bottom-right value
    v = data[x, y]
    vec1 = np.array([-dist, 0, data[x, y - 1] - v])
    vec2 = np.array([0, -dist, data[x - 1, y] - v])
    normal_vectors[x, y] = np.cross(vec1, vec2)

    return normal_vectors

def calculate_angles(data, normal_vectors, params, sun):
    angles = np.empty((params[0], params[1]))
    dist = params[2]

    # set the world positions for each point
    x_coords, y_coords = np.meshgrid(dist * np.arange(params[0]), 
                                     dist * np.arange(params[1]), indexing='ij')
    z_coords = data

    # calculate direction vectors from the sun to each point
    dir_vec = np.stack((x_coords - sun[0], 
                        y_coords - sun[1], 
                        z_coords - sun[2]), axis=-1)

    # calculate the dot products between direction vectors and normal vectors
    dot_products = np.sum(dir_vec * normal_vectors, axis=-1)

    # calculate norms for direction vectors and normal vectors
    dir_vec_norms = np.linalg.norm(dir_vec, axis=-1)
    normal_vec_norms = np.linalg.norm(normal_vectors, axis=-1)

    # calculate cosines and clamp the values
    angle_cosines = np.clip(dot_products / (dir_vec_norms * normal_vec_norms), -1, 1)

    # calculate angles
    angles = np.arccos(angle_cosines)

    return angles

if __name__ == '__main__':
    data, params = read_file(f'{files_path}/big.dem')
    dist = params[2]

    # define sun's position
    sun = (-150 * dist, -100 * dist, 150)
        
    normal_vectors = calculate_normals(data, params)

    angles = calculate_angles(data, normal_vectors, params, sun)

    draw_map(data, angles, params)