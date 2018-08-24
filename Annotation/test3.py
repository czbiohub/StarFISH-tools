from SpotAnnotationAnalysis import SpotAnnotationAnalysis
from BaseAnnotation import BaseAnnotation
from QuantiusAnnotation import QuantiusAnnotation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import AffinityPropagation

colors = ['#3399FF', '#CC33FF', '#FFFF00', '#FF33CC', 
    '#9966FF', '#009999', '#99E3FF', '#B88A00', 
    '#33FFCC', '#FF3366', '#F5B800', '#FF6633',
    '#FF9966', '#FF9ECE', '#CCFF33', '#FF667F',
    '#EB4E00', '#FFCC33', '#FF66CC', '#33CCFF', 
    '#ACFF07', '#667FFF', '#FF99FF', '#FF1F8F',
    '#9999FF', '#99FFCC', '#FF9999', '#91FFFF',
    '#8A00B8', '#91BBFF', '#FFB71C', '#FF1C76']

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
anno_one_image = ba.slice_by_image(anno_all, img_filename)

show_workers = True

show_clusters = True
clustering_params = ['AffinityPropagation', -350]
#sa.plot_annotations(anno_one_image, img_filename, img_filepath, csv_filepath, worker_marker_size, cluster_marker_size, show_ref_points, show_workers, show_clusters, show_correctness_workers, show_correctness_clusters, show_NN_inc, correctness_threshold, clustering_params, bigger_window_size)

xmin = 100
xmax = 200
ymin = 220
ymax = 320

ymin_flipped = img_height-ymax
ymax_flipped = img_height-ymin

worker_list = ba.get_workers(anno_one_image)

worker_and_coords = []
handle_list = []

coords = ba.get_click_properties(anno_one_image)[:,:2]
af = AffinityPropagation(preference = -350).fit(coords)
cluster_centers_indices = af.cluster_centers_indices_									# Get the indices of the cluster centers (list)
num_clusters = len(cluster_centers_indices)

labels = af.labels_																		# Each point that was in coords now has a label saying which cluster it belongs to.

cluster_centroids_list = []
for k in range(num_clusters):
	cluster_center = coords[cluster_centers_indices[k]]	# np array
	plt.scatter([cluster_center[0]], [img_height-cluster_center[1]], s = 20, facecolors = 'none', edgecolors = 'white')

for worker, color in zip(worker_list, colors):			# For each worker, use a different color.
	anno = ba.slice_by_worker(anno_one_image, worker)		
	coords = ba.get_click_properties(anno)[:,:2]
	cropped_coords = []
	for coord in coords:
		if (coord[0] >= xmin) and (coord[0] <= xmax) and (coord[1] >= ymin_flipped) and (coord[1] <= ymax_flipped):
			cropped_coords.append(coord)
	cropped_coords = np.asarray(cropped_coords)
	worker_and_coords.append([worker, cropped_coords])

	# for plotting
	x_coords = []
	y_coords = []
	for coord in cropped_coords:
		x_coords.append(coord[0])
		y_coords.append(coord[1])
	y_coords_flipped = [(img_height - y) for y in y_coords]
	handle = plt.scatter(x_coords, y_coords_flipped, s = worker_marker_size, facecolors = color, alpha = 0.5, label = worker)
	handle_list.append(handle)
plt.legend(handles = handle_list, loc = 9, bbox_to_anchor = (1.2, 1.015))

img = mpimg.imread(img_filepath)
plt.imshow(img, cmap = 'gray')

for element in workers_and_coords:
	worker = element[0]
	coords = element[1]
	

mean_coords = sa.get_cluster_means(anno_one_image, ['AffinityPropagation',-350])

for coord in mean_coords:
	x_coords.append(coord[0])
	y_coords.append(img_height - coord[1])
plt.scatter(x_coords, y_coords, s=40, facecolors = 'none',edgecolors='yellow')

plt.show()






# x_coords = coords[:,0]
# y_coords = coords[:,1]
# y_coords_flipped = ba.flip(y_coords, img_height)