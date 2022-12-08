# To create sumo detector file : addition.add.xml
import pandas as pd
import sumo_class
from tqdm import tqdm

if __name__=="__main__":

    # location of the detector from the node
    DETECTOR_POS = -20

    # path to the SUMO network in CSV format. Use xml2csv tool to generate this
    NETWORK_CSV = "../sample_files/network.net.csv"
    # path to the output from merge.py which contains mapping of detectors to OSM edges
    DETECTOR_MAPPING = "../sharedstreets_outputs/point_edge_mapping.csv"
    # path to the network edge file
    PATH_EDGE_CSV = "../sample_files/network.edg.csv"

    # column ids from DETECTOR_MAPPING file
    SUMO_COLUMN = 'sumo_id'
    DETECTOR_COLUMN = 'munich_id'
    DETECTOR_LATITUDE = 'detector_lat'
    DETECTOR_LONGITUDE = 'detector_lon'

    # path to the output/ SUMO detector file
    OUTPUT = "../sample_files/additional.add.xml"

    detector_locations = pd.read_csv(DETECTOR_MAPPING)
    temp = detector_locations

    # we need edge file, to know the number of lanes in addition.add.xml
    # get the length and num lanes of the edges
    sumo_obj = sumo_class.Sumo_Network(NETWORK_CSV, PATH_EDGE_CSV)
    df_edge_length, df_edge_lanes = sumo_obj.write_edges()

    # start wrtiting the additional file
    a = """<additional>""" 
    b = ""
    check_list_sumo_edge = []
    check_list_id = []
    temp[DETECTOR_COLUMN] = temp.apply(lambda x: str(x[DETECTOR_COLUMN])+"_"+str(int(x.direction)), axis=1)
    temp.drop_duplicates(subset=[DETECTOR_COLUMN], inplace=True)
    for i, j in tqdm(enumerate(zip(temp[SUMO_COLUMN], temp[DETECTOR_COLUMN], temp[DETECTOR_LATITUDE], temp[DETECTOR_LONGITUDE]))):
        try:
            # try except added to cater the cases when some of the detector links are not in the matched
            # sumo network. but there are many links for one detector.
            len_lane = float(df_edge_length[df_edge_length.edge_id==j[0]]['lane_length'])
            if j[0] in check_list_sumo_edge:
                # only one detector on one sumo edge
                pass
            elif j[1] in check_list_id:
                # only one detector with one name
                pass
            ## insufficient length of the lane for detector
            elif len_lane < DETECTOR_POS:
                pass
            else:
                temp_len = len(df_edge_lanes[df_edge_lanes.edge_id==j[0]])
                if temp_len==1:
                    n_lanes = int(df_edge_lanes[df_edge_lanes.edge_id==j[0]]["edge_numLanes"])
                else:
                    n_lanes = list((df_edge_lanes[df_edge_lanes.edge_id==j[0]]["edge_numLanes"]).astype(int))[0]
                for k in range(0, n_lanes):
                    b = b+"""<e1Detector file="out.xml" freq="900.0" id="""+"\""+"e1Detector_"+j[0]+"_"+str(k)+"\""+" lane="+"\""+j[0]+"_"+str(k)+"\""+""" pos="""+"\""+str(DETECTOR_POS)+"\""+""" name="""+"\""+str(j[1])+"\""+"""><param key="C" value="""+"\""+str(j[2])+", "+str(j[3])+"\""+"""/></e1Detector>"""
                check_list_sumo_edge.append(j[0])
                check_list_id.append(j[1])
        except Exception as e:

            print(e)
            pass
            
    c = """</additional>"""
    file_text = a+b+c
    # stop wrtiting the additional file

    with open(OUTPUT, "w") as f:
        f.write(file_text)
        f.close()