from SpotAnnotationAnalysis import SpotAnnotationAnalysis
from BaseAnnotation import BaseAnnotation
from QuantiusAnnotation import QuantiusAnnotation


worker_marker_size = 4
cluster_marker_size = 40
bigger_window_size = True

csv_filepath = None
show_correctness_workers = False
show_correctness_clusters = False
correctness_threshold = None
show_NN_inc = False
show_ref_points = False

img_filename = 'C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_300_inv.png'
img_filepath = '/Users/jenny.vo-phamhi/Documents/StarFISH-tools/Annotation/C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_300.png'
json_filepath = '/Users/jenny.vo-phamhi/Documents/StarFISH-tools/Annotation/smFISH_cells_inv.json'

ba = QuantiusAnnotation(json_filepath)
sa = SpotAnnotationAnalysis(ba)
anno_all = ba.df()
anno_one_image = ba.slice_by_image(anno_all, img_filename)


from skimage import data, feature, exposure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2


img_filename = 'C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_300_copy.png'
img = cv2.imread(img_filename)					# img is a numpy 2D array
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)	
img = exposure.equalize_hist(img)  # improves detection
blobs = feature.blob_log(img, threshold = .3)

plt.imshow(img)

for blob in blobs:
	plt.scatter([blob[1]], [blob[0]], s=20, color='r')

plt.show()
print(blobs)






# show_workers  = False
# show_clusters = False
# clustering_params = None
# sa.plot_annotations(anno_one_image, img_filename, img_filepath, csv_filepath, worker_marker_size, cluster_marker_size, show_ref_points, show_workers, show_clusters, show_correctness_workers, show_correctness_clusters, show_NN_inc, correctness_threshold, clustering_params, bigger_window_size)


# show_workers  = True
# sa.plot_annotations(anno_one_image, img_filename, img_filepath, csv_filepath, worker_marker_size, cluster_marker_size, show_ref_points, show_workers, show_clusters, show_correctness_workers, show_correctness_clusters, show_NN_inc, correctness_threshold, clustering_params, bigger_window_size)

# show_clusters = True
# clustering_params = ['AffinityPropagation', -350]
# sa.plot_annotations(anno_one_image, img_filename, img_filepath, csv_filepath, worker_marker_size, cluster_marker_size, show_ref_points, show_workers, show_clusters, show_correctness_workers, show_correctness_clusters, show_NN_inc, correctness_threshold, clustering_params, bigger_window_size)


# show_workers = False
# sa.plot_annotations(anno_one_image, img_filename, img_filepath, csv_filepath, worker_marker_size, cluster_marker_size, show_ref_points, show_workers, show_clusters, show_correctness_workers, show_correctness_clusters, show_NN_inc, correctness_threshold, clustering_params, bigger_window_size)


