# Beta - Coordinates for Mobile Robot Based on User Defined Dimensions

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.patches as patches
import matplotlib.axes as ax
import numpy as np


arena = img.imread("r_arena.png")
figure, ax = plt.subplots(1)


def elu_dist(p1, p2):
	return (np.sqrt((np.square(p2[0] - p1[0]) + np.square(p2[1] - p1[1]))))	

def plot_robot(position):
    center = position
    center_dist = 55 
    robot_rad = 85
    
    wheel1 = [center[0], center[1] +55]
    wheel2 = [center[0] + 47.6, center[1] - 27.5]
    wheel3 = [center[0] - 47.6, center[1] - 27.5]

    r = plt.Circle((center), robot_rad, color = 'white')
    ax.add_artist(r)
    w1 = plt.Circle((wheel1), 19, color = 'black')
    ax.add_artist(w1)
    w2 = plt.Circle((wheel2), 19, color = 'black')
    ax.add_artist(w2)
    w3 = plt.Circle((wheel3), 19,  color = 'black')
    ax.add_artist(w3)

def plot_point(position):
	wp = plt.Circle((position[0], position[1]), 10)
	ax.add_artist(wp)

def get_tri_params(x, y, l, b):
	if(l>=b):
		top = [(x+(l/2)), (y+(b*3/4))]
		print(top) #imp
		h = [(x+(l/2)), (y+(b*1/4))]
		height = top[1] - h[1]
		side_length = (height*2)/np.sqrt(3)
	elif(b>l):
		top = [(x+l/4), (y+b/2)]
		h = [(x+3*(l/4)), (y+b/2)]
		height = top[0] - h[0]
		side_length = (height*2)/np.sqrt(3)
		print(side_length)
	
	print("Area = ", ((1/2)*side_length*height))
	#Center = plt.Circle((h[0], h[1]), 2)
	#ax.add_artist(Center)

	return(top, h, side_length, height)

###########################################
## Gives the Coords for Robots Job Location
###########################################

def get_robot_params(x, y, l, b):
	package = patches.Rectangle((x, y), l, b, edgecolor='grey', facecolor="grey")
	ax.add_patch(package)

	params = get_tri_params(x, y, l, b)

	#plot_point([params[1][0], params[1][1]])
	
	if(l>=b):
		box_center = [(x+l/2), (y+b/2)]
		tri_center = [(x+l/2) , (params[0][1]- (params[3]*2/3))] 
		mr1_coords = params[0]
		mr2_coords = [(params[1][0]-params[2]/2), (y+(b*1/4))]
		mr3_coords = [(params[1][0] + params[2]/2), (y+(b*1/4))]
	
	elif(l<b):
		box_center = [(x+l/2), (y+b/2)]
		tri_center = [(x+l/2) , (params[0][0] + (params[3]*2/3))] 
		mr1_coords = params[0]
		mr2_coords = [(x+(3*l/4)), (params[1][1] - params[2]/2)]
		mr3_coords = [(x+(3*l/4)), (params[1][1] + params[2]/2)]

	d = elu_dist(mr3_coords, tri_center)



	return (mr1_coords, mr2_coords, mr3_coords, box_center, tri_center, d)

###############################
## Gives Intermediate Waypoints
###############################

def get_int_waypoints(start_position, goal_position):
	slope = (goal_position[1] - start_position[1]) / (goal_position[0] - start_position[0])
	print(slope)
	intercept = start_position[1] - slope * start_position[0]
	theta = 0

	for var_x in range(start_position[0], goal_position[0], int(slope)*50):
		var_y = slope*var_x + intercept
		#plot_point([var_x, var_y])
		int_waypoints.append([var_x, var_y])
		
	return(int_waypoints)

###############################################
## Gives the waypoints for induvidual waypoints
###############################################

def get_split_waypoints(waypoints):
	split = get_tri_params(x, y, l, b)
	mr1_waypoint = []
	mr2_waypoint = []
	mr3_waypoint = []
	for waypoint in waypoints:
		if(l>=b):
		#print("The split waypoints for ", waypoint)
			mr1_waypoint = [(waypoint[0]), (waypoint[1] + diag_dist)]
			plot_point([mr1_waypoint[0], mr1_waypoint[1]])
		#print("Aplha Waypoints = ", mr1_waypoint)

			mr2_waypoint = [(waypoint[0] - (split[1][0] - mr2_coords[0])), (waypoint[1] - (	tri_center[1] - split[1][1]))]
			plot_point([mr2_waypoint[0], mr2_waypoint[1]])
		#print("Beta Waypoints = ", mr2_waypoint)

			mr3_waypoint = [(waypoint[0] + (mr3_coords[0]) - split[1][0]), (waypoint[1] - (	tri_center[1] - split[1][1]))]
			plot_point([mr3_waypoint[0], mr3_waypoint[1]])
		#print("Gamma Waypoints = ", mr3_waypoint)

		elif(l<b):
			mr1_waypoint = [(waypoint[0] - diag_dist ), (waypoint[1])]
			plot_point([mr1_waypoint[0], mr1_waypoint[1]])
		#print("Aplha Waypoints = ", mr1_waypoint)

			mr2_waypoint = [(waypoint[0] + split[3]/3), (waypoint[1] - split[2]/2)]
			plot_point([mr2_waypoint[0], mr2_waypoint[1]])
		#print("Beta Waypoints = ", mr2_waypoint)

			mr3_waypoint = [(waypoint[0] + split[3]/3), (waypoint[1] + split[2]/2)]
			plot_point([mr3_waypoint[0], mr3_waypoint[1]])
		#print("Gamma Waypoints = ", mr3_waypoint)


	return (mr1_waypoint, mr2_waypoint, mr3_waypoint)


##########################
#######		Main	######
##########################

start_position = [500, 500]
goal_position = [ 1500, 1500]

l = 500
b = 700	
print("Areaaa = ", l*b)

var_y = 0
var_x = 0
int_waypoints = []

x = start_position[0] - l/2
y = start_position[1] - b/2

xg = goal_position[0] - l/2
yg = goal_position[1] - b/2


[mr1_coords, mr2_coords, mr3_coords, box_center, tri_center, diag_dist] = get_robot_params(x, y, l, b)
[g_mr1_coords, g_mr2_coords, g_mr3_coords, g_box_center, g_tri_center, g_diag_dist] = get_robot_params(xg, yg, l, b)

tri_center[0] = int(tri_center[0])
tri_center[1] = int(tri_center[1])
g_tri_center[0] = int(g_tri_center[0])
g_tri_center[1] = int(g_tri_center[1])

start_location = tri_center
goal_location = g_tri_center

int_waypoints = get_int_waypoints(start_location, goal_location)

[AlphaWaypoints , BetaWaypoints , GammaWaypoints] = get_split_waypoints(int_waypoints)

plot_robot(mr1_coords)
plot_robot(mr2_coords)
plot_robot(mr3_coords)

plot_robot(g_mr1_coords)
plot_robot(g_mr2_coords)
plot_robot(g_mr3_coords)

plot_point(start_position)
plot_point(goal_position)

print("Alpha Coordinates = ", mr1_coords)
print("Beta Coordinates = ", mr2_coords)
print("Gamma Coordinates = ", mr3_coords)
print("Box Center = ", box_center)
print("Triangle Center = ", tri_center)

ax.imshow(arena)
plt.gca().invert_yaxis()
plt.show()
