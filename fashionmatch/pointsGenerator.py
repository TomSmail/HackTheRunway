# get inputs for each piece of clothing 
# more water used - higher the points
# where was the garment made
from geopy.geocoders import Nominatim

def get_coords(location): # gets coords from a given string value eg "India"
    geo = Nominatim(user_agent="SWAPIFY")
    place = geo.geocode(location)
    coords = [place.longitude, place.latitude]
    return coords

def calculate_distance(your_cords, garment_cords): # might be a bug here as this is a "dumb" system, ie thinks world is flat
    distance = ((your_cords[0]-garment_cords[0])**2 + (your_cords[1]-garment_cords[1])**2)**(1/2) # takes x and y coords and uses pythag to workout distance
    return distance

def calculate_score(your_cords, garment_cords, cotton_bool): # calculates a score based on material and how far it has travelled
    distance = calculate_distance(your_cords, garment_cords)

    if cotton_bool: # attempt at normalisation
        cotton = 1
    else:
        cotton = 0

    value = distance/100 + cotton 

    if value < 1: 
        points = 100
    elif value < 2:
        points = 200
    elif value < 3:
        points = 300
    else:
        points = 450

    return points
    