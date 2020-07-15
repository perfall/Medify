import skvideo.io  
import numpy as np
import sys
import argparse

def main(filename, output_filename, window, med):
	if window % 2 == 0:
		print("Window value (-w) has to be odd.")
		return None

	# Read video data
	videodata = skvideo.io.vread(filename)
	print(videodata.shape)

	# Set some parameters
	side_range = int((window-1)/2)
	start, stop = side_range, videodata.shape[0] - side_range

	# Process video
	output = []
	for i, frame in enumerate(videodata[start:stop]):
		if med == "med":
			output.append(np.median(videodata[i - side_range:i + side_range], axis=0))
		elif med == "avg":
			output.append(np.mean(videodata[i - side_range:i + side_range], axis=0))
		else:
			print("-m has to be set to 'med' or 'avg'.")
			print("Exiting")
	output = np.array(output)

	# Write to new video
	skvideo.io.vwrite(output_filename, output, outputdict={"-vcodec":"libx264", "-pix_fmt":"yuv420p"})


if __name__ == '__main__':
	# Initiate command line parser
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", default="input.mp4")
	parser.add_argument("-o", default="output.mp4")
	parser.add_argument("-w", default="11")
	parser.add_argument("-m", default="med")
	
	# Parse input
	args = vars(parser.parse_args())
	inp = args["i"]
	out = args["o"]
	window = int(args["w"])
	med = args["m"]
	

	main(inp, out, window, med)