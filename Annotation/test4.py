from SpotAnnotationAnalysis import SpotAnnotationAnalysis
from BaseAnnotation import BaseAnnotation
from QuantiusAnnotation import QuantiusAnnotation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

worker_marker_size = 4
cluster_marker_size = 40
bigger_window_size = False

csv_filepath = None
show_correctness_workers = False
show_correctness_clusters = False
correctness_threshold = None
show_NN_inc = False
show_ref_points = False
img_height = 450

img_filename = 'C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_700_inv.png'
img_filepath = '/Users/jenny.vo-phamhi/Documents/StarFISH-tools/Annotation/C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_700.png'
json_filepath = '/Users/jenny.vo-phamhi/Documents/StarFISH-tools/Annotation/smFISH_cells_inv.json'

ba = QuantiusAnnotation(json_filepath)
sa = SpotAnnotationAnalysis(ba)
anno_all = ba.df()
df = ba.slice_by_image(anno_all, img_filename)

sa.plot_annotations_zoom(df, x_min, x_max, y_min, y_max, img_height, clustering_params, img_filepath, show_clusters, show_workers, cluster_marker_size, worker_marker_size):
