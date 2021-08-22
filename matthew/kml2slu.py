# work on increasing efficiency

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def kml2slu(file, write=False):
    """Converts Polygons drawn in Google Earth to slu used by GeoClaw flag_regions

    :param str file: path to .kml file downloaded from Google Earth
            - there must not be any three points on the polygon with the same latitude
    :param bool write: will write slus to a .txt file named slu_outputs
    :return: a dictionary of polygon names with their slus in ndarray format
    """
    class Segment:
        # Stores info needed for each line segment making up the polygon
        def __init__(self, x0, x1, y0, y1):
            self.x = x0
            self.y = y0
            self.ylower = np.min([y0, y1])
            self.yupper = np.max([y0, y1])
            self.slope = (y1 - y0) / (x1 - x0)

    polygons = {}

    placemark = False
    name = None
    polygon = False
    grab_next = False

    threats = []

    with open(file, "r") as kml_file:
        for num, line in enumerate(kml_file, 1):
            if "<Placemark>" in line:
                placemark = True

            elif placemark:
                if "<name>" in line:
                    name = line[line.find(">") + 1:line.find("</")]
                elif "<Polygon>" in line:
                    polygon = True
                elif ("<coordinates>" in line) and polygon:
                    grab_next = True
                elif grab_next:
                    tmp_threats = ["\n" + name]
                    # Grabs coordinates of points and puts them in dataframe with [lat, lon]
                    s = pd.Series(np.array(line.strip().split(" "))).str.split(",")
                    df = pd.concat([s.str.get(0).astype(float), s.str.get(1).astype(float)], axis=1)
                    df.columns = ["lon", "lat"]

                    # Identify polygon segments
                    segments = [
                        Segment(df["lon"].iloc[i], df["lon"].iloc[i + 1], df["lat"].iloc[i], df["lat"].iloc[i + 1])
                        for i in df.index.to_list() if i != len(df) - 1]

                    # Get longitudes for each latitude
                    df["lon 0"] = None
                    df["lon 1"] = None
                    for i in df.index.to_list():
                        lat = df["lat"].iloc[i]
                        lon_orig = df["lon"].iloc[i]
                        for segment in segments:
                            if segment.ylower <= lat <= segment.yupper:
                                lon = ((lat - segment.y) / segment.slope) + segment.x
                                if lon != lon_orig:
                                    if df["lon 0"].iloc[i] is not None:
                                        # Found three points with same latitude
                                        tmp_threats.append(str(lat))
                                    elif lon > lon_orig:
                                        df["lon 1"].iloc[i] = lon
                                        df["lon 0"].iloc[i] = lon_orig
                                    else:
                                        df["lon 1"].iloc[i] = lon_orig
                                        df["lon 0"].iloc[i] = lon

                        # For top and bottom verticies
                        if df["lon 0"].iloc[i] is None and df["lon 1"].iloc[i] is None:
                            df["lon 0"].iloc[i] = lon_orig
                            df["lon 1"].iloc[i] = lon_orig

                    polygons[name] = df[["lat", "lon 0", "lon 1"]].drop_duplicates(subset=['lat']).sort_values(
                        by=['lat']).reset_index(drop=True).to_numpy()

                    if len(tmp_threats) > 1:
                        threats += tmp_threats

                    polygon = False
                    grab_next = False
                    placemark = False

    if threats:
        raise TypeError("The following polygons have three points with the same latitude. Each latitude "
                        "can belong to at most two points on a polygon." + '\n'.join(threats))

    if write:
        with open("slu_ouputs.txt", "w") as slu_file:
            [slu_file.writelines([p, ":\n", str(polygons.get(p)), "\n\n"]) for p in polygons]

    return polygons
