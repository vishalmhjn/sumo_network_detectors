import geojson
import pandas as pd
import sys

scenario = sys.argv[1]


if scenario =="munich":
    OUT_FILE="../sharedstreets/detector_sumo_mapping_munich.csv"
    with open('../sharedstreets/bast_munich.matched.geojson') as f:
        munich_detectors = geojson.load(f)

    with open('../sharedstreets/sumo_network_munich.matched.geojson') as f:
        sumo_network = geojson.load(f)
    
    df_detectors = pd.DataFrame(munich_detectors)
    df_detectors['geometry']  = df_detectors['features'].apply(lambda x: x['geometry'])
    df_detectors['shst_id']  = df_detectors['features'].apply(lambda x: x['properties']['shstReferenceId'])
    df_detectors['length']  = df_detectors['features'].apply(lambda x: x['properties']['referenceLength'])
    df_detectors['munich_id']  = df_detectors['features'].apply(lambda x: x['properties']['pp_id'])
    df_detectors['direction']  = df_detectors['features'].apply(lambda x: x['properties']['pp_direction'])
    df_detectors['detector_lat']  = df_detectors['features'].apply(lambda x: x['properties']['pp_lat'])
    df_detectors['detector_lon']  = df_detectors['features'].apply(lambda x: x['properties']['pp_lon'])

    df_detectors.drop(columns=['type'], inplace=True)

    df_sumo_network = pd.DataFrame(sumo_network)
    df_sumo_network['geometry']  = df_sumo_network['features'].apply(lambda x: x['geometry'])
    df_sumo_network['shst_id']  = df_sumo_network['features'].apply(lambda x: x['properties']['shstReferenceId'])
    df_sumo_network['sumo_id']  = df_sumo_network['features'].apply(lambda x: x['properties']['pp_id'])
    df_sumo_network.drop(columns=['type'], inplace=True)

    df_detector_sumo_map = pd.merge(df_detectors, df_sumo_network, left_on='shst_id', right_on='shst_id')
    df_detector_sumo_map[~df_detector_sumo_map[['shst_id', 'length', 'munich_id', 'sumo_id']].duplicated(subset=None, keep='first')]
    df_detector_sumo_map.to_csv(OUT_FILE, index=False)

else:
    raise("Specify a valid scenario in CLI")



print("Finished!")