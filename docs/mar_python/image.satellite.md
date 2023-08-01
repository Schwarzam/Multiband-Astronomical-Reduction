<!-- markdownlint-disable -->

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `image.satellite`





---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `cluster_lines`

```python
cluster_lines(lines, angle_threshold, distance_threshold)
```

Clusters lines based on their angles and distances, and returns a list of line clusters. 

Parameters 
---------- lines : list  A list of lines represented as numpy arrays of shape (1, 4) with (x1, y1, x2, y2) coordinates. angle_threshold : float  The maximum angle difference (in degrees) between two lines for them to be considered in the same cluster. distance_threshold : float  The maximum distance (in pixels) between the centers of two lines for them to be considered in the same cluster. 

Returns 
------- clusters : list  A list of line clusters, where each cluster is a list of lines represented as numpy arrays of shape (1, 4). 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `merge_lines`

```python
merge_lines(lines)
```

Merges a list of lines into a single line by computing the bounding box of the lines. 

Parameters 
---------- lines : list  A list of lines represented as numpy arrays of shape (1, 4) with (x1, y1, x2, y2) coordinates. 

Returns 
------- merged_line : numpy.ndarray  A numpy array of shape (1, 4) representing the merged line with (x1, y1, x2, y2) coordinates. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `angle_between_points`

```python
angle_between_points(x1, y1, x2, y2)
```

Computes the angle (in degrees) between two points (x1, y1) and (x2, y2). 

Parameters 
---------- x1 : float  The x-coordinate of the first point. y1 : float  The y-coordinate of the first point. x2 : float  The x-coordinate of the second point. y2 : float  The y-coordinate of the second point. 

Returns 
------- angle : float  The angle (in degrees) between the two points. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `line_intersects_object`

```python
line_intersects_object(line, obj_center, radius)
```

Check if a line intersects with a circle. 

Parameters 
---------- line : list  The line parameters in the format [x1, y1, x2, y2]. obj_center : tuple  The center coordinates of the circle in the format (x, y). radius : int  The radius of the circle. 

Returns 
------- intersects : bool  True if the line intersects with the circle, False otherwise. 


---

<a href="https://github.com/Schwarzam/MAR/blob/master/mar/mar/image/satellite.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_satellite_trace`

```python
get_satellite_trace(image, folder, segmentation_name, catname)
```

Detects satellite traces in an astronomical image and returns a binary mask of the traces. 

Parameters 
---------- image : str  The filename of the input image. folder : str  The folder where the output segmentation and catalog files will be saved. segmentation_name : str  The filename for the output segmentation map. catname : str  The filename for the output catalog. 

Returns 
------- filled_result : numpy.ndarray  A binary mask of the detected satellite traces. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
