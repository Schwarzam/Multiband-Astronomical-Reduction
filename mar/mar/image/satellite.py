import os
import cv2

import numpy as np
from astropy.io import fits
from astropy.table import Table

import mar
from mar.config import MarManager

try:
    import lacosmicx
except:
    print('SatMask - Could not import lacosmicx.')


try:
	configVal = mar.AttributeDict(mar.env.marConf.Reduction)
except:
	print('Could not get reduction config.')

def cluster_lines(lines, angle_threshold, distance_threshold):
    """
    Clusters lines based on their angles and distances, and returns a list of line clusters.

    Parameters
    ----------
    lines : list
        A list of lines represented as numpy arrays of shape (1, 4) with (x1, y1, x2, y2) coordinates.
    angle_threshold : float
        The maximum angle difference (in degrees) between two lines for them to be considered in the same cluster.
    distance_threshold : float
        The maximum distance (in pixels) between the centers of two lines for them to be considered in the same cluster.

    Returns
    -------
    clusters : list
        A list of line clusters, where each cluster is a list of lines represented as numpy arrays of shape (1, 4).
    """
    clusters = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        added_to_cluster = False
        line_angle = angle_between_points(x1, y1, x2, y2)

        for cluster in clusters:
            for cluster_line in cluster:
                cx1, cy1, cx2, cy2 = cluster_line[0]
                cluster_line_angle = angle_between_points(cx1, cy1, cx2, cy2)
                angle_difference = abs(line_angle - cluster_line_angle)

                if angle_difference < angle_threshold:
                    line_center = ((x1 + x2) / 2, (y1 + y2) / 2)
                    cluster_line_center = ((cx1 + cx2) / 2, (cy1 + cy2) / 2)
                    distance = np.sqrt((line_center[0] - cluster_line_center[0])**2 + (line_center[1] - cluster_line_center[1])**2)

                    if distance < distance_threshold:
                        cluster.append(line)
                        added_to_cluster = True
                        break

            if added_to_cluster:
                break

        if not added_to_cluster:
            clusters.append([line])

    return clusters


def merge_lines(lines):
    """
    Merges a list of lines into a single line by computing the bounding box of the lines.

    Parameters
    ----------
    lines : list
        A list of lines represented as numpy arrays of shape (1, 4) with (x1, y1, x2, y2) coordinates.

    Returns
    -------
    merged_line : numpy.ndarray
        A numpy array of shape (1, 4) representing the merged line with (x1, y1, x2, y2) coordinates.
    """
    x_coords = []
    y_coords = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        x_coords.extend([x1, x2])
        y_coords.extend([y1, y2])

    min_x, min_y = min(x_coords), min(y_coords)
    max_x, max_y = max(x_coords), max(y_coords)

    return np.array([[min_x, min_y, max_x, max_y]], dtype=np.int32)

def angle_between_points(x1, y1, x2, y2):
    """
    Computes the angle (in degrees) between two points (x1, y1) and (x2, y2).

    Parameters
    ----------
    x1 : float
        The x-coordinate of the first point.
    y1 : float
        The y-coordinate of the first point.
    x2 : float
        The x-coordinate of the second point.
    y2 : float
        The y-coordinate of the second point.

    Returns
    -------
    angle : float
        The angle (in degrees) between the two points.
    """
    return np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

def line_intersects_object(line, obj_center, radius):
    """
    Check if a line intersects with a circle.
    
    Parameters
    ----------
    line : list
        The line parameters in the format [x1, y1, x2, y2].
    obj_center : tuple
        The center coordinates of the circle in the format (x, y).
    radius : int
        The radius of the circle.
    
    Returns
    -------
    intersects : bool
        True if the line intersects with the circle, False otherwise.
    """
    x1, y1, x2, y2 = line
    x0, y0 = obj_center
    
    # Calculate the distance between the line and the circle's center
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    distance = numerator / denominator

    return distance <= radius


def get_satellite_trace(image, folder, segmentation_name, catname):
    """
    Detects satellite traces in an astronomical image and returns a binary mask of the traces.
    
    Parameters
    ----------
    image : str
        The filename of the input image.
    folder : str
        The folder where the output segmentation and catalog files will be saved.
    segmentation_name : str
        The filename for the output segmentation map.
    catname : str
        The filename for the output catalog.
    
    Returns
    -------
    filled_result : numpy.ndarray
        A binary mask of the detected satellite traces.
    """
    MarManager.INFO("Searching satellite traces...")
    sextr = mar.wrappers.SExtr(image=image, folder=folder, catname=catname)

    segmentation_name = os.path.join(folder, segmentation_name)

    sextr.config['DEBLEND_NTHRESH']['value'] = 5
    sextr.config["PHOT_APERTURES"]['value'] = 20
    sextr.config["CHECKIMAGE_TYPE"]['value'] = "SEGMENTATION"
    sextr.config["CHECKIMAGE_NAME"]['value'] = segmentation_name

    sextr.config["DETECT_MINAREA"]["value"] = configVal["SAT_DETECT_MINAREA"]

    sextr.params = [
        "NUMBER",
        "X_IMAGE",
        "Y_IMAGE",
        "ALPHA_J2000",
        "DELTA_J2000",
        "FLUX_ISO",
        "FLUXERR_ISO",
        "MAG_ISO",
        "MAGERR_ISO",
        "ELONGATION",
        "ELLIPTICITY",
        "FLAGS"
    ]

    sextr.run()
    
    with fits.open(segmentation_name) as hdulist:
        segmentation_map = hdulist[0].data

    catalog = Table.read(os.path.join(folder, catname), hdu=2)
    elongated_objects = catalog[(catalog["ELONGATION"] > int(configVal["SAT_ELONGATION"])) & (catalog["ELLIPTICITY"] > int(configVal["SAT_ELLIPTICITY"]))]
    elongated_objects = np.array(elongated_objects["NUMBER"])

    # Create a mask of the values that match the list
    mask = np.isin(segmentation_map, elongated_objects)
    filled_result = lacosmicx.improve_pixel_mask_cython(segmentation_map.astype('uint8'), mask.astype('uint8'))
    filled_result *= 255

    edges = cv2.Canny(filled_result, 100, 108)

    kernel = np.ones((3,3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    edges_eroded = cv2.erode(edges_dilated, kernel, iterations=1)

    lines = cv2.HoughLinesP(edges_eroded, 1, np.pi/180, 
                            threshold=int(configVal["HOUGH_LINES_THRESH"]), 
                            minLineLength=int(configVal["HOUGH_LINES_MINLENGTH"]), 
                            maxLineGap=int(configVal["HOUGH_LINES_MAXGAP"]))
    
    if lines is None:
        MarManager.INFO("No lines detected.")
        return None

    filled_result = np.zeros_like(segmentation_map, dtype=np.uint8)
    
    found_line = False
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        
        if abs(angle) > 89 and abs(angle) < 91:
            MarManager.DEBUG("Bad pixel column found, discarting")
            continue
        
        found_line = True
        cv2.line(filled_result, (x1, y1), (x2, y2), 1, 10)
    
    if not found_line:
        MarManager.INFO("No lines detected")
        return 

    filled_result = lacosmicx.improve_pixel_mask_cython(segmentation_map.astype('uint8'), filled_result.astype('uint8'))
    return filled_result
