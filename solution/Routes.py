# -*- coding: utf-8 -*-
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
  #roads=(
  #("LB", "leuven",    "brussel",   27.0,  120),
  #("BL", "brussel",   "leuven",    30.0,  120),
  #("LA", "leuven",    "antwerpen", 61.0,  120),
  #("AL", "antwerpen", "leuven",    63.0,  120),
  #("BO", "brussel",   "oostende",  110.0, 120),
  #("OA", "oostende",  "antwerpen", 120.0, 120),
  #("AH", "antwerpen", "hasselt",   78.0,  120),
  #("HL", "hasselt",   "leuven",    60.0,  120))
  #0      1            2            3      4
  #road   city1        city2        lenght speedlimit
  id_road       = 0
  id_city1      = 1
  id_city2      = 2
  id_lenght     = 3
  id_speedlimit = 4
  network = ({},{})
  for element in roads:
    road       = element[id_road]
    city1      = element[id_city1]
    city2      = element[id_city2]
    lenght     = element[id_lenght]
    speedlimit = element[id_speedlimit]
    time       = element[id_lenght]/element[id_speedlimit]
	
	# On ajoute les informations de l'autoroute au dictionnaire
    network[0][road] = (city1,city2,lenght,speedlimit,time)
    
	
	# On ajoute la ville de départ comme clé dans le dictionnaire 
    if city1 not in network[1]:
      network[1][city1] = ([],[])
	# On ajoute l'autoroute dans les 'autoroutes de départ' de la ville
    if road not in network[1][city1]:
      network[1][city1][0].append(road)
      
	# On ajoute la ville de fin comme clé dans le dictionnaire 
    if city2 not in network[1]:
      network[1][city2] = ([],[])
    # On ajoute l'autoroute dans les 'autoroutes de fin' de la ville
    if road not in network[1][city2]:
      network[1][city2][1].append(road)
  
  return network
	  




  
    


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

  # On récupère la liste des villes
  list_city = network[1].keys()
  
  # Si la ville de départ ou de fin n'existe pas
  if start not in list_city or destination not in list_city:
    return None

  # On retire les villes à exclure
  list_city = [x for x in list_city if x not in excludings]


  # Initialisation de se qu'on a besoin
  matrix = []
  distance = []
  n = len(list_city)

  
  # On construit la matrice adjacente où indique la distance si il existe une autoroute entre 2 villes
  for x in range(n): 
    matrix.append( [] )
    distance.append( [] )
    for y in range(n):
      road_id = get_road_to(network,list_city[x],list_city[y])
      if road_id != None:
        matrix[x].append( get_length(network,road_id) )
      else:
        matrix[x].append( None )
      distance[x].append( [road_id] ) # Autoroute -> format: ['LA']

	  
  # Algorithme de Floyd
  for k in range(n):
    for i in range(n):
      for j in range(n):
        if ( matrix[i][k] != None and matrix[k][j] != None ) and ( ( matrix[i][j] == None  ) or ( matrix[i][j] > matrix[i][k] + matrix[k][j] ) ):
          matrix[i][j] = matrix[i][k] + matrix[k][j]
		  
		  # Hors Floyd / Ajout personnel
          if i != k and j != k: # Si i == k ou j == k, cela veut dire qu'on additionne un résultat supplémentaire à la case ij
            distance[i][j] = [] # Sinon ca signifie qu'on a trouvé un chemin plus court, du coup on supprime l'ancien chemin
          distance[i][j].extend( distance[i][k] ) # Chemin d'autoroute parcouru en plus -> format: ['LA','AH']
          distance[i][j].extend( distance[k][j] ) # Chemin d'autoroute parcouru en plus -> format: ['LA','AH']

		  
  # On récupère simplement la liste des autoroutes parcourus
  idx_start        = list_city.index( start )
  idx_destination  = list_city.index( destination )
  distance_minimum = distance[ idx_start ][ idx_destination ]

  
  # Si on ne trouve aucune solution, on renvoie None
  if distance_minimum == [None]:
    distance_minimum = None
  
  return distance_minimum








##############################################
# ALGORITHM 2: SHORTEST ROUTE INCLUDING VIAS #
##############################################


# The resulting route should not contain loops (each road can only be used once).
# Note that cities might be connected by multiple roads.
def get_quickest_route_via(network, start,destination, vias):
  """ Returns the quickest route from the given start city to the given destination city
        while visiting the intermediate cities (vias) in order. """
  # On récupère la liste des villes
  list_city = network[1].keys()
  
  # On vérifie que toutes les villes existent
  for via in vias:
    if via not in list_city:
	  return None
	  
  # On utilise Floyd pour parcourir les chemins les plus rapide de ville ne ville
  roads = []
  done = []
  city_previous = start
  for via in vias:
	road = get_shortest_route_floyd(network, city_previous, via) #done[:-1]) # dépend si on peut ou pas repasser par les villes déjà visité
	if road != None:
	  roads.extend( road )
	  done.append( via )
	  city_previous = via
	  
  # On utilise Floyd pour finir le parcourt jusqu'à la ville de fin
  road = get_shortest_route_floyd(network, city_previous,destination) #done[:-1]) # dépend si on peut ou pas repasser par les villes déjà visité
  if road != None:
    roads.extend( road )
	
  # Si on trouve rien, on renvoie None
  if roads == []:
    return None
  return roads





    


##########################
# ROUTE HELPER FUNCTIONS #
##########################

# Reminder: a route is a list consisting of road IDs

def get_length_of_route(network, route):
  """ Returns the total distance of the given route. """
  result = 0
  for road_id in route:
    result += get_length(network,road_id)
  return result


def get_time_of_route(network, route):
  """ Returns the estimated time of the route. """
  result = 0
  for road_id in route:
    result += get_time(network,road_id)
  return result
  

def get_cities_of_route(network, route):
  """ Returns a list that contains all visited cities (strings) in order of the given route """
  result = []
  if len(route) >= 1:
    road_id = route[0]
    result.append( get_start(network,road_id) )
    result.append( get_end(network,road_id) )
  for i in range(1,len(route)):
    road_id = route[i]
    result.append( get_end(network,road_id) )
  return result


def cities_occur_in_route(network, cities,route):
  """ Returns whether the entire collection of cities is visited during the route.
    Note that the cities do not necessarily have to be visited in order."""
  list_cities = get_cities_of_route(network, route)
  for i in cities:
    if i not in list_cities:
      return False
  return True


def route_contains_loop(route):
  """ Return whether a route contains a loop. A loop is defined as a road that occurs more than once. """
  for i in route:
    if 1 < route.count( i ):
      return True
  return False



def route_is_contained_in_other_route(route,target):
  """ Returns whether each road of the first route is contained in the target route.
    The order of the route should be respected, but the roads should not necessarily be used consecutively.
    (for example: ["AB", "BC", "CD"] is contained in ["ZA", "AX", "XA", "AB", "BY", "YW", "WY", "YB", "BC", "CD"])"""
  id_route = 0
  id_target = 0
  found = True
  while found and id_route < len(route) and id_target < len(target):
    found = False
    while not found and id_target < len(target):
      if route[id_route] == target[id_target]:
        found = True
      else:
        id_target += 1
    id_route += 1
  return found


def is_correct_route(network, route):
  """ Determines whether a given route is correct by examining
      whether the destination city of each road equals the origin city of the next road """
  id_actual = 0
  id_next = 1
  while id_next < len(route):
    road_id_actual = route[id_actual]
    road_id_next  = route[id_next]
    if get_end(network, road_id_actual) != get_start(network, road_id_next):
      return False
    id_actual += 1
    id_next += 1
  return True







#########################
# ROAD HELPER FUNCTIONS #
#########################

# ALL FUNCTIONS NEED TO BE EXECUTED IN CONSTANT TIME

def get_start(network, road_id):
  """ Returns the original city of the road identified by road_id """
  return network[0][road_id][0]

def get_end(network, road_id):
  """ Returns the destination city of the road identified by road_id """
  return network[0][road_id][1]

def get_length(network, road_id):
  """ Returns the distance of the road identified by road_id """
  return network[0][road_id][2]
  
def get_speed(network, road_id):
  """ Returns the allowed speed of the road identified by road_id """
  return network[0][road_id][3]

def get_time(network, road_id):
  """ Returns the estimated time of the road identified by road_id """
  return network[0][road_id][4]


#########################
# CITY HELPER FUNCTIONS #
#########################



# 16+ requirement: this function should execute in constant time
def get_all_roads_starting_from(network, city):
  """ Returns a list containing all the roads that depart in the given city """
  return network[1][city][0]

def get_road_to(network, start, end):
  """ Returns the shortest (direct) road from the given start city to the given end city.
    When no such road exists, return None. """
  roads_common = list( set(network[1][start][0]).intersection(network[1][end][1]) )

  minimum = None
  if 0 < len(roads_common):
    minimum = roads_common[0]
  
  for road in roads_common:
    if get_length(network,minimum) > get_length(network,road):
      minimum = road
  
  return minimum


  



 


