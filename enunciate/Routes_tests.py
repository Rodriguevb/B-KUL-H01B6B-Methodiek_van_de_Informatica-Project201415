from Routes import *
from math import *


""" Helper function for tests """
def float_equals(x,y,threshold=0.00000001):
    "Whether two floating point number are approximately equal, up to a threshold"
    return abs(x-y) < threshold




print "TESTING ..."


print "initializing network"
# initialize network
roads=(("LB", "leuven", "brussel", 27.0, 120), ("BL", "brussel", "leuven", 30.0, 120), ("LA", "leuven", "antwerpen", 61.0, 120),
       ("AL","antwerpen", "leuven", 63.0, 120), ("BO", "brussel", "oostende", 110.0, 120),
       ("OA", "oostende", "antwerpen", 120.0, 120), ("AH", "antwerpen", "hasselt", 78.0, 120), ("HL", "hasselt", "leuven", 60.0, 120))
network = init_network(roads)








print "testing shortest path (Floyd)"

# shortest path - floyd algorithm
assert get_shortest_route_floyd(network, "leuven", "hasselt") ==  ['LA', 'AH']
assert get_shortest_route_floyd(network, "brussel", "hasselt") == ['BL', 'LA', 'AH']
# floyd with 1 excluding
assert get_shortest_route_floyd(network, "brussel", "hasselt", ["leuven"]) == ['BO', 'OA', 'AH']
# floyd with non-existing path
assert get_shortest_route_floyd(network, "hasselt", "antwerpen", ["leuven"]) == None



# testing with network with multiple roads between 2 cities
# Initializing
roads2=(("LB", "leuven", "brussel", 27.0, 120), ("BL", "brussel", "leuven", 30.0, 120), ("LA", "leuven", "antwerpen", 61.0, 120),
        ("AL","antwerpen", "leuven", 63.0, 120), ("BO", "brussel", "oostende", 110.0, 120), ("BO_2", "brussel", "oostende", 120.0, 120),
        ("OA", "oostende", "antwerpen", 120.0, 120), ("AH", "antwerpen", "hasselt", 78.0, 120), ("AH_2", "antwerpen", "hasselt", 60.0, 120),
        ("HL", "hasselt", "leuven", 60.0, 120))
network2 = init_network(roads2)

#testing
assert get_shortest_route_floyd(network2, "brussel", "hasselt") == ['BL', 'LA', 'AH_2']








print "testing quickest path (vias)"

# quickest path - vias algorithm
# no via
assert get_quickest_route_via(network, "oostende", "hasselt", []) == ['OA', 'AH']
# 1 via
assert get_quickest_route_via(network, "oostende", "hasselt", ["brussel"]) == ['OA', 'AL', 'LB', 'BL', 'LA', 'AH']
# via does not exist (no path is found)
assert get_quickest_route_via(network, "brussel", "hasselt", ["?"]) == None

# testing with network with multiple roads between two cities
assert get_quickest_route_via(network2, "oostende", "hasselt", ["brussel"]) == ['OA', 'AL', 'LB', 'BL', 'LA', 'AH_2']







print "testing route helper functions"

# route testing
route_leuven_hasselt = ['LA', 'AH']
route_oostende_hasselt = ['OA', 'AL', 'LB', 'BL', 'LA', 'AH']

assert get_length_of_route(network, route_leuven_hasselt) == 139

assert round(get_time_of_route(network, route_leuven_hasselt), 2) == 1.16
assert round(get_time_of_route(network, route_oostende_hasselt), 2)==3.16

assert get_cities_of_route(network, route_leuven_hasselt) == ["leuven", "antwerpen", "hasselt"]
assert get_cities_of_route(network, route_oostende_hasselt) == ['oostende', 'antwerpen', 'leuven', 'brussel', 'leuven', 'antwerpen', 'hasselt']


assert cities_occur_in_route(network,["leuven", "hasselt", "oostende"], route_oostende_hasselt)
assert not cities_occur_in_route(network,["leuven", "gent", "oostende"], route_oostende_hasselt)


assert not route_contains_loop(route_oostende_hasselt)
assert route_contains_loop(["BL", "LA", "AH", "HL", "LA", "AL"])


assert route_is_contained_in_other_route(["AB", "BC", "CD"],["ZA", "AX", "XA", "AB", "BY", "YW", "WY", "YB", "BC", "CD"])
assert route_is_contained_in_other_route(["AL", "LA"], route_oostende_hasselt)
assert not route_is_contained_in_other_route(["LA", "AL"], route_oostende_hasselt)


assert is_correct_route(network, route_oostende_hasselt)
assert not is_correct_route(network, ["AL", "LB","OA", "AH"])








print "testing road helper functions"

# road testing
assert get_start(network, "AH")=="antwerpen"
assert get_end(network, "AH")=="hasselt"
assert get_length(network, "AH")== 78.0
assert get_speed(network, "AH")== 120
assert get_time(network, "AH")== 0.65







print "testing city helper functions"

# city testing
assert get_all_roads_starting_from(network, "antwerpen")==["AL", "AH"] or get_all_roads_starting_from(network, "antwerpen")==["AH", "AL"]

assert get_road_to(network, "antwerpen", "hasselt")== "AH"
assert get_road_to(network2, "antwerpen", "hasselt")== "AH_2"
assert get_road_to(network, "brussel", "antwerpen") == None






print "extensive testing of small network"

#Testing the example network in the assignment (Figure 2)


roads=(("BL", "Brussel", "Leuven", 30.0, 120),
       ("LA", "Leuven", "Antwerpen", 61.0, 120),
       ("AB", "Antwerpen", "Brussel", 44.0,120))
network = init_network(roads)

# test get_all_roads_starting_from
assert "BL" in get_all_roads_starting_from(network,"Brussel")
assert "LA" in get_all_roads_starting_from(network,"Leuven")
assert "AB" in get_all_roads_starting_from(network,"Antwerpen")
assert len(get_all_roads_starting_from(network,"Brussel")) == 1
assert len(get_all_roads_starting_from(network,"Leuven")) == 1
assert len(get_all_roads_starting_from(network,"Antwerpen")) == 1

# test get_road_to
assert "BL" == get_road_to(network,"Brussel","Leuven")
assert "LA" == get_road_to(network,"Leuven","Antwerpen")
assert "AB" == get_road_to(network,"Antwerpen","Brussel")
assert None == get_road_to(network,"Brussel","Antwerpen")
assert None == get_road_to(network,"Brussel","Brussel")

route = ["BL","LA"]

# test get_length_of_route, get_time_of_route, get_cities_of_route
assert float_equals(91.0, get_length_of_route(network,route))
assert float_equals(91.0/120, get_time_of_route(network,route))
assert ["Brussel","Leuven","Antwerpen"] == get_cities_of_route(network,route)

# test cities_occur_in_route
assert cities_occur_in_route(network,["Brussel","Leuven","Antwerpen"],route)
assert cities_occur_in_route(network,["Leuven","Antwerpen"],route)
assert cities_occur_in_route(network,["Antwerpen","Leuven"],route)
assert cities_occur_in_route(network,("Antwerpen","Leuven"),route)
assert cities_occur_in_route(network,{"Antwerpen","Leuven"},route)
assert cities_occur_in_route(network,[],route)

# test route_contains_loop
assert not route_contains_loop(route)
assert not route_contains_loop(["BL","LA","AB"])
assert route_contains_loop(["BL","LA","AB","BL"])

# test route_is_contained_in_other_route
assert route_is_contained_in_other_route(["BL","LA"],["BL","LA"])
assert route_is_contained_in_other_route(["BL"],["BL","LA"])
assert route_is_contained_in_other_route(["LA"],["BL","LA"])
assert route_is_contained_in_other_route(["AB", "BC", "CD"],["ZA", "AX", "XA", "AB", "BY", "YW", "WY", "YB", "BC", "CD"])
assert not route_is_contained_in_other_route(["BL","LA"],["BL"])
assert not route_is_contained_in_other_route(["BL","LA"],["LA","BL"])

# test is_correct_route
assert is_correct_route(network,route)
assert is_correct_route(network,["BL"])
assert is_correct_route(network,["BL","LA","AB"])
assert not is_correct_route(network,["BL","AB"])
assert not is_correct_route(network,["LA","BL"])
assert not is_correct_route(network,["AB","LA","BL"])

# test get_start, get_end
assert "Brussel" == get_start(network,"BL")
assert "Antwerpen" == get_start(network,"AB")
assert "Leuven" == get_start(network,"LA")
assert "Leuven" == get_end(network,"BL")
assert "Brussel" == get_end(network,"AB")
assert "Antwerpen" == get_end(network,"LA")

# test get_length, get_speed, get_time
assert float_equals(30.0,get_length(network,"BL"))
assert float_equals(61.0,get_length(network,"LA"))
assert float_equals(44.0,get_length(network,"AB"))
assert 120 == get_speed(network,"BL")
assert 120 == get_speed(network,"LA")
assert 120 == get_speed(network,"AB")
assert float_equals(30.0/120,get_time(network,"BL"))
assert float_equals(61.0/120,get_time(network,"LA"))
assert float_equals(44.0/120,get_time(network,"AB"))

# test get_shortest_route_floyd
assert ["BL"] == get_shortest_route_floyd(network,"Brussel","Leuven")
assert ["AB"] == get_shortest_route_floyd(network,"Antwerpen","Brussel")
assert ["LA"] == get_shortest_route_floyd(network,"Leuven","Antwerpen")
assert ["LA"] == get_shortest_route_floyd(network,"Leuven","Antwerpen",["Brussel"])
assert ["BL","LA"] == get_shortest_route_floyd(network,"Brussel","Antwerpen")
assert ["AB","BL"] == get_shortest_route_floyd(network,"Antwerpen","Leuven")
assert ["LA","AB"] == get_shortest_route_floyd(network,"Leuven","Brussel")
assert ["LA","AB"] == get_shortest_route_floyd(network,"Leuven","Brussel",[])

# test get_quickest_route_via
assert ["BL"] == get_quickest_route_via(network,"Brussel","Leuven",[])
assert ["AB"] == get_quickest_route_via(network,"Antwerpen","Brussel",[])
assert ["LA"] == get_quickest_route_via(network,"Leuven","Antwerpen",[])
assert ["BL","LA"] == get_quickest_route_via(network,"Brussel","Antwerpen",[])
assert ["BL","LA"] == get_quickest_route_via(network,"Brussel","Antwerpen",["Leuven"])
assert ["AB","BL"] == get_quickest_route_via(network,"Antwerpen","Leuven",[])
assert ["AB","BL"] == get_quickest_route_via(network,"Antwerpen","Leuven",["Brussel"])
assert ["LA","AB"] == get_quickest_route_via(network,"Leuven","Brussel",[])
assert ["LA","AB"] == get_quickest_route_via(network,"Leuven","Brussel",["Antwerpen"])




print "TESTS SUCCEEDED !!!"




