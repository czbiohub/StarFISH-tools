#import matplotlib.pyplot as plt
import numpy as np
import importlib
import os
import sys

# TODO add to path permanently
module_path = '/Users/kevin.yamauchi/Documents/imagingDB'

if module_path not in sys.path:
    sys.path.append(module_path)

import imaging_db.database.db_session as db_session

import imaging_db.filestorage.s3_storage as s3_storage
    
# Import all our tables
from imaging_db.database.base import Base
from imaging_db.database.file_global import FileGlobal
from imaging_db.database.frames_global import FramesGlobal
from imaging_db.database.frames import Frames
# This is the overall table containing the identifier and description
from imaging_db.database.dataset import DataSet

class ImageDatabase:
	def __init__(self, credentials_filename):
		self.credentials_filename = credentials_filename

	def getAcqMeta(self, dataset_identifier):
		importlib.reload(db_session)

		with db_session.session_scope(self.credentials_filename) as session:
			datasets = session.query(DataSet)
			
			# Find the Frames of interest
			all_frames = session.query(Frames) \
			    .join(FramesGlobal) \
			    .join(DataSet) \
			    .filter(DataSet.dataset_serial == dataset_identifier) \
				.all()

			acq_meta = all_frames[0].frames_global.metadata_json['IJMetadata']

		return acq_meta

	def getImageMeta(self, dataset_identifier):
		importlib.reload(db_session)

		with db_session.session_scope(self.credentials_filename) as session:
			datasets = session.query(DataSet)
			
			# Find the Frames of interest
			all_frames = session.query(Frames) \
				.join(FramesGlobal) \
				.join(DataSet) \
				.filter(DataSet.dataset_serial == dataset_identifier) \
				.all()

			# Get the image metadata
			image_metadata = []
			for im in all_frames:
				image_metadata.append(im.metadata_json['MicroManagerMetadata'])

		return image_metadata

	def getFrames(self, dataset_identifier, channels='all', Frames='all'):
		# Open the session
		importlib.reload(db_session)
		
		with db_session.session_scope(self.credentials_filename) as session:
			datasets = session.query(DataSet)
			
			# Find the Frames of interest
			all_frames = session.query(Frames) \
				.join(FramesGlobal) \
				.join(DataSet) \
				.filter(DataSet.dataset_serial == dataset_identifier)

			# Filter by channel
			if channels == 'all':
				pass

			elif type(channels) is tuple:
				slice_filtered = all_frames.filter(Frames.channel_name.in_(channels))

			else:
				print('Invalid channel query')

			# Filter by slice
			if Frames == 'all':
				pass

			elif type(channels) is tuple:
				slice_filtered = all_frames.filter(Frames.slice_idx.in_(Frames))

			else:
				print('Invalid slice query')

			# Get the names of the files
			file_names = [im.filename for im in all_frames]
			# for im in all_frames:
			# 	file_names.append(im.file_name)

			# Get the bit depth 
			bit_depth = all_frames[0].frames_global.bit_depth

			# Get the shape of the stack
			# TODO: get the shape from the acq meta
			stack_shape = (
    			all_frames[0].frames_global.im_width,
    			all_frames[0].frames_global.im_height,
    			all_frames[0].frames_global.im_colors,
    			len(all_frames),
			)

			# Get the folder
			folder_name = all_frames[0].frames_global.folder_name

			# Download the files
			data_loader = s3_storage.DataStorage(folder_name=folder_name)
			im_stack = data_loader.fetch_im_stack(file_names, stack_shape, bit_depth)
			
		session.rollback()
		session.close()

		return im_stack

	def getStack(self, dataset_identifier, channel, verbose=False):
		# Open the session
		importlib.reload(db_session)
		
		with db_session.session_scope(self.credentials_filename) as session:
			datasets = session.query(DataSet)
			
			# Find the Frames of interest
			all_frames = session.query(Frames) \
				.join(FramesGlobal) \
				.join(DataSet) \
				.filter(DataSet.dataset_serial == dataset_identifier) \
				.filter(Frames.channel_name == channel) \
				.all()

			# Get the names of the files
			file_names = [im.file_name for im in all_frames]

			if len(file_names) == 0:
				raise ValueError('No images match query')

			# Get the bit depth 
			bit_depth = all_frames[0].frames_global.bit_depth

			# Get the shape of the stack
			# TODO: get the shape from the acq meta
			stack_shape = (
    			all_frames[0].frames_global.im_width,
    			all_frames[0].frames_global.im_height,
    			all_frames[0].frames_global.im_colors,
    			len(all_frames),
			)

			# Get the folder
			folder_name = all_frames[0].frames_global.folder_name

			# Download the files
			data_loader = s3_storage.DataStorage(folder_name=folder_name)
			im_stack = data_loader.fetch_im_stack(file_names, stack_shape, bit_depth, verbose=verbose)

			im_ordered = np.zeros((1, 1, stack_shape[3], stack_shape[0], stack_shape[1]))

			for im_idx in range(len(all_frames)):
				im_ordered[0, 0, im_idx, :, :] = im_stack[:, :, 0, im_idx]
			
		session.rollback()
		session.close()

		return im_ordered

if __name__ == "__main__":
	from ImageDatabase import ImageDatabase
	
	dataset_identifier = "ISP-2018-06-08-15-45-00-0001"
	credentials_filename = "/Users/kevin.yamauchi/Documents/db_credentials.json"

	db = ImageDatabase(credentials_filename)

	images = db.getImage(dataset_identifier)

	print(type(meta))


