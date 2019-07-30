from urllib.request import urlopen
from urllib.parse import quote
import json

# These functions make HTTP calls to Seattle's GIS server. If you use it too
# frequently, the server may stop responding.

def geocode(addr):
    """
    Input: First line of a Seattle address, in string form
      (eg "111 S Jackson St")
    Output: tuple, (latitude, longitude)
    """

    # construct a url for the webservice request
    base = "https://gisrevprxy.seattle.gov" \
    "/ArcGIS/rest/services/locators/SND/GeocodeServer/" \
    "findAddressCandidates?Single+Line+Input={}&outSR=4326&f=pjson"
    url = base.format(quote(addr))

    # make the webservice request
    resp = json.load( urlopen(url) )

    # if there are no results, return None
    if "candidates" not in resp or len(resp["candidates"])==0:
        return None

    # return location on (latitude, longitude) form
    loc = resp["candidates"][0]["location"]
    return loc['y'], loc['x']

def findbeat(addr):
    """
    Input: First line of a Seattle address, in string form
      (eg "111 S Jackson St")
    Output: Beat code, in string form (eg "J2"), or None if none could
      be found.
    """

    coord = geocode(addr)
    if coord is None:
        return None

    lat, lon = coord

    baseurl ="https://gisrevprxy.seattle.gov/ArcGIS/rest/services/DoIT_ext/" \
    "SP_Precincts_Beats/MapServer/2/query?" \
    "text=&geometry={},{}" \
    "&geometryType=esriGeometryPoint&inSR=4326" \
    "&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=" \
    "&where=&time=&returnCountOnly=false&returnIdsOnly=false" \
    "&returnGeometry=false&maxAllowableOffset=&outSR=&outFields=&f=pjson"
    url = baseurl.format(lon, lat) #coord is in lon/lat format
    print(url)
    # make the webservice request
    resp = json.load( urlopen(url) )

    # get the first feature from the response
    features = resp.get("features")
    if features is None:
        return None
    if len(features)==0:
        return None
    feature = features[0]

    # get the list of attributes for the feature
    attributes = feature.get("attributes")
    if attributes is None:
        return None

    # get the beat from the attributes
    return attributes.get("beat")

if __name__ == '__main__':
    import sys

    if len(sys.argv)!=2:
        print( "usage: %s \"address\""%(sys.argv[0]) )
        exit()

    addr = sys.argv[1]

    print( findbeat(addr) )
    