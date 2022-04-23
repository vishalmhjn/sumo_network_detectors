import pandas as pd
import geopandas as gpd
import geojson
import csv, json
from geojson import Feature, FeatureCollection, Point
class Sumo_Network:
	def __init__(self,
				path_network_csv="../data/paris_auto.net.csv",
				path_edge_csv="../data/plainnet.edg.csv"):
		# XML2CSV
		self.path_edge = path_edge_csv
		# XML2CSV
		self.path_network_csv = path_network_csv

	def write_edges(self):
		"""function to write the number of lanes and length of an edge, for placing the detectors
		shst match ../data/sumo_network.geojson --out=sumo_network.geojson --snap-intersections --follow-line-direction"""
		df_net = pd.read_csv(self.path_network_csv, sep=';', error_bad_lines=False)
		temp = df_net[['edge_id','lane_id','lane_length']].dropna()
		temp = temp.drop_duplicates(subset='edge_id')
		edge_len = temp[['edge_id', 'lane_length']]
		edge_len.reset_index(inplace=True, drop=True)

		df_edge = pd.read_csv(self.path_edge, sep=";", error_bad_lines=False)
		df_edge = df_edge[df_edge['edge_id'].notna()]
		df_edge = df_edge[df_edge['edge_shape'].notna()]
		df_edge_lanes = df_edge[["edge_id", "edge_numLanes"]]

		df_edge_length = pd.merge(df_edge_lanes, edge_len, on="edge_id")
		df_edge_length = df_edge_length.drop_duplicates(subset='edge_id')
		# df_edge_length.to_csv("../scenario_munich/temp_check.csv", index=None)
		return df_edge_length, df_edge_lanes

	def sumo_net_to_geojson(self, output_path="../data/sumo_network.geojson"):
		"""convert sumo network to geojson for later use in shared streets and
		TAZs"""
		df_edge = pd.read_csv(self.path_edge, sep=";")
		
		df_edge = df_edge[df_edge['edge_id'].notna()]
		df_edge = df_edge[df_edge['edge_type'].notna()]
		try:
			df_edge = df_edge[df_edge['edge_shape'].notna()]
		except Exception as e:
			print(e)
			raise("Check first show of *.edg.xml is it has edge_shape attribute")
		df_edge.reset_index(inplace=True, drop=True)
		df_edge = df_edge[['edge_id', 'edge_shape','edge_speed', 'edge_type']]

		edge_id = df_edge['edge_id']
		shapes = df_edge['edge_shape']
		edge_type = df_edge['edge_type']

		conv_shapes = []
		for shape in shapes:
			shape_list = shape.split(" ")
			edge_shape = []
			for point in shape_list:
				lat = float(point.split(",")[0])
				lon = float(point.split(",")[1])
				node = [lat, lon]
				edge_shape.append(node)
			conv_shapes.append(edge_shape)

		li = []
		for i, edge in enumerate(zip(edge_id, conv_shapes, edge_type)):
			d = {}
			d['type'] = 'Feature'
			d['geometry'] = {'type': 'LineString','coordinates': edge[1]}
			d['properties'] = {'id': edge[0], 'type': edge[2]}
			li.append(d)
		d = {}
		d['type'] = 'FeatureCollection'
		d['features'] = li
		with open(output_path, 'w') as f:
			f.write(json.dumps(d, sort_keys=False, indent=4))

if __name__ == "__main__":
	# convert sumo network_to_geojson
	geo = Sumo_Network()
	geo.sumo_net_to_geojson()