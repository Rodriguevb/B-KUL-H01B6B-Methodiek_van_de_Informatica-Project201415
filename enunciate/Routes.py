# SOME GUIDELINES:
# 1) Please keep the order of the functions in this skeleton and do not re-arrange them.
# 2) You can add as many (useful) helper functions as you prefer, either at the bottom of the file or in between the
#       required functions
# 3) If required, you may extend the function heading with additional parameters. However, make sure that our tests still work!
#       (only add parameters at the end of the parameter list, and make sure that you provide them with a default value)
# 4) You can write your invariants, documentation strings and comments in either Dutch or English. Both are fine, however, be consistent!





#############################
# INITIALISATION OF NETWORK #
#############################

# The result of the init_network function is a representation of the network of roads
# and will be used throughout the program as such (as parameter 'network').
# Keep in mind that it should be possible to retrieve the properties of a road (distance, speed, cities)
# in constant time.
# 16+ extension: You should extend the network with a representation that enables retrieval of all roads
# departing from a city in constant time. This extension thus implies that the function returns a tuple
# containing the network representations.
def init_network(roads):
  """ Returns a network of roads.
    A road is a tuple consisting of a road id, the two cities it connects, the length, and the average speed limit.
    The function translates these tuples to a more useful representation that will be used throughout the program."""
	  




  
    


#####################################
# ALGORITHM 1: FLOYD SHORTEST ROUTE #
#####################################


# the algorithm assumes no loops (i.e. no road should be used more than once).
# multiple roads between two cities are however possible.
# The lookup function (part 3 of the algorithm) should be implemented as a recursive helper function
def get_shortest_route_floyd(network, start,destination, excludings=[]):
  """ Returns the shortest route between the given start city and given destination city,
      which avoids all cities in excludings.
      The function calculates the shortest routes between all cities based on the roads in the provided network. 
	  Once all shortest routes are computed,
      the function returns the shortest route (as a list of road IDs).
      Cities to be avoided (excludings) are dealt with by the algorithm. """
 








##############################################
# ALGORITHM 2: SHORTEST ROUTE INCLUDING VIAS #
##############################################


# The resulting route should not contain loops (each road can only be used once).
# Note that cities might be connected by multiple roads.
def get_quickest_route_via(network, start,destination, vias):
  """ Returns the quickest route from the given start city to the given destination city
        while visiting the intermediate cities (vias) in order. """
 





    


##########################
# ROUTE HELPER FUNCTIONS #
##########################

# Reminder: a route is a list consisting of road IDs

def get_length_of_route(network, route):
  """ Returns the total distance of the given route. """
  

def get_time_of_route(network, route):
  """ Returns the estimated time of the route. """


def get_cities_of_route(network, route):
  """ Returns a list that contains all visited cities (strings) in order of the given route """
  
 


def cities_occur_in_route(network, cities,route):
  """ Returns whether the entire collection of cities is visited during the route.
    Note that the cities do not necessarily have to be visited in order."""
   


def route_contains_loop(route):
  """ Return whether a route contains a loop. A loop is defined as a road that occurs more than once. """
  



def route_is_contained_in_other_route(route,target):
  """ Returns whether each road of the first route is contained in the target route.
    The order of the route should be respected, but the roads should not necessarily be used consecutively.
    (for example: ["AB", "BC", "CD"] is contained in ["ZA", "AX", "XA", "AB", "BY", "YW", "WY", "YB", "BC", "CD"])"""



def is_correct_route(network, route):
  """ Determines whether a given route is correct by examining
      whether the destination city of each road equals the origin city of the next road """
 







#########################
# ROAD HELPER FUNCTIONS #
#########################

# ALL FUNCTIONS NEED TO BE EXECUTED IN CONSTANT TIME

def get_start(network, road_id):
  """ Returns the original city of the road identified by road_id """
 

def get_end(network, road_id):
  """ Returns the destination city of the road identified by road_id """
 

def get_length(network, road_id):
  """ Returns the distance of the road identified by road_id """
  
def get_speed(network, road_id):
  """ Returns the allowed speed of the road identified by road_id """

def get_time(network, road_id):
  """ Returns the estimated time of the road identified by road_id """


#########################
# CITY HELPER FUNCTIONS #
#########################



# 16+ requirement: this function should execute in constant time
def get_all_roads_starting_from(network, city):
  """ Returns a list containing all the roads that depart in the given city """


def get_road_to(network, start, end):
  """ Returns the shortest (direct) road from the given start city to the given end city.
    When no such road exists, return None. """
 


  



 


