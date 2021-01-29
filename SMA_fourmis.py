# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 9:44:05 2020

@author: MAEVA
"""

import numpy as np
import copy
from random import randint
import pygame

_CITIES = (("Bordeaux", (195,427)), ("Paris",(325,181)),("Nice",(537,493)),
("Lyon",(432,371)),("Nantes",(154,271)),("Brest",(30,196)),("Lille",(353,62)),
("Clermont-Ferrand",(335,375)),("Strasbourg",(560,189)),("Poitiers",(243,314)),
("Angers",(200,249)),("Montpellier",(393,504)),("Caen",(207,148)),("Rennes",(152,216)),("Pau",(199,511)),("Toulouse", (296, 504)), ("Reims", (393, 150)), ("Troyes", (394, 209)))
    
class colony:
    def __init__(self, colony_size, nb_iterations, rho):
        
        self.colony_size = colony_size
        self.nb_iterations = nb_iterations
        self.rho = rho
        self.first_pass = True
        self.ants = []
        self.pheromone_map = self._init_matrix_(len(_CITIES))
        self.global_shortest_route = list(copy_cities)
        
        self.global_shortest_route.append(copy_cities[0])
        self.global_distance = self._init_global_distance()
        
    
    
    def _init_ants(self):
        if self.first_pass:
            for i in range(self.colony_size):
                new_ant = self.ant(self.pheromone_map) 
                self.ants.append(new_ant)
        else:
            for ant in self.ants:
                ant.__init__(self.pheromone_map, first_pass=False)
        
            
    
    def _init_matrix_(self, len_map, value=0.0):
        mat=[]
        for row in range(len_map):
            mat.append([float(value) for column in range(len_map)])
        
        return mat
        
        
        
    def _init_global_distance(self):
        global_route = self.global_shortest_route
        distance = 0
        
        for i in range(len(global_route)-1):
            distance += self.distance(global_route[i][1], global_route[i+1][1])
            
        return distance
            
        
        
    def update_pheromone_map(self):
        cumul_pheromone = self._init_matrix_(len(_CITIES))
        for ant in self.ants:
            for i in range(len(_CITIES)):
                for j in range(len(_CITIES)):
                    cumul_pheromone[i][j] += ant.pheromone_map[i][j]
        
        # do the mean
        for i in range(len(_CITIES)):
            for j in range(len(_CITIES)):
                cumul_pheromone[i][j] /= self.colony_size
                    
        pheromone_amount = self._init_matrix_(len(_CITIES))
        for i in range(len(_CITIES)):
            for j in range(len(_CITIES)):
                pheromone_amount[i][j] = self.pheromone_map[i][j]
                self.pheromone_map[i][j] = self.rho*pheromone_amount[i][j] + cumul_pheromone[i][j]
    
    
    
    
    def shortest_route(self):
        shortest_route=list(copy_cities).append(copy_cities[0])
        shortest_distance=100000.0
        
        for ant in self.ants:
            if shortest_distance > sum(ant.distance_map):
                shortest_distance = sum(ant.distance_map)
                shortest_route = ant.visited_cities
                
        return shortest_distance, shortest_route

    
    
    
    def global_shortest(self):
        shortest_distance, shortest_route = self.shortest_route()
        
        if (shortest_distance < self.global_distance):
            self.global_distance = shortest_distance
            self.global_shortest_route = shortest_route
            
            
            
    def distance(self,a,b):
        (x1,y1),(x2,y2) = (a,b) # a et b sont les coordonnées des villes
        return np.sqrt((x1-x2)**2+(y1-y2)**2)
        

        
    def mainloop(self):
        self._init_ants()
        for i in range(self.nb_iterations):
            print(f"Tour {i+1} :")
            for ant in self.ants:
                ant.city_choice()
                ant.add_pheromone()
                # print("Total distance : ", sum(ant.distance_map))
            
            shortest_distance, shortest_route = self.shortest_route()
            print("Min distance : ", shortest_distance)
            # print("Route : ", shortest_route)
            # print("Shortest Route : ", shortest_route)
            self.update_pheromone_map()
            self.global_shortest()
            
            if self.first_pass:
                self.first_pass=False
                
            self._init_ants()
            
        print("\n\n")
        print('Shortest distance : ', self.global_distance)
        print('Shortest path : ', self.global_shortest_route)
        # print(self.pheromone_map)
        
        

    class ant:
        def __init__(self, pheromone_map, alpha=0.8, beta=0.6, gamma=0.1, first_pass=True):
            
            
            self.init_city = _CITIES[randint(0, len(_CITIES)-1)] 
            self.possible_cities = list(copy_cities) # cities which haven't been visited yet
            self.pheromone_map = pheromone_map # each time ant ant goes to a city, it places pheromone on the road, according to the total distance
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.distance_map = [] # each time a new city is visited the distance between the last and the new city is added to this array
            self.visited_cities = [] # list of visited cities in the right order
            self.actual_city = self.init_city
            self.first_pass = first_pass
            self.complete_tour = False
            
            self.visited_cities.append(self.init_city)
            self.possible_cities.remove(self.init_city)
            
            
            
        def _init_matrix_(self, len_map, value=0.0):
            mat=[]
            for row in range(len_map):
                mat.append([float(value) for column in range(len_map)])
            
            return mat
        
        
        
        def distance(self,a,b):
            (x1,y1),(x2,y2) = (a,b) # a and b are the cities position
            return np.sqrt((x1-x2)**2+(y1-y2)**2)
        
        
        
        # we choose the next city by proximity or pheromone value
        def city_choice(self):
            while(self.possible_cities):
                if self.first_pass:
                    next_city=self.city_choice_by_proximity()
                else:
                    next_city=self.city_choice_by_pheromone()
                
                # genetic modification :
                # we pick a random city from the list of possible cities
                # if the distance between actual city and random city is smaller
                # than distance between actual city and next city,
                # we replace next city with random city
                if len(self.possible_cities)>1:
                    random_city = self.possible_cities[randint(0, len(self.possible_cities)-1)]
                    if self.distance(self.actual_city[1], next_city[1])>self.distance(self.actual_city[1], random_city[1]):
                        self.possible_cities.append(next_city)
                        self.visited_cities.remove(next_city)
                        self.distance_map.remove(self.distance(self.actual_city[1], next_city[1]))
                        
                        self.possible_cities.remove(random_city)
                        self.visited_cities.append(random_city)
                        self.distance_map.append(self.distance(self.actual_city[1], random_city[1]))
                        
                        next_city=random_city
                    
                self.actual_city=next_city
            self.complete_tour=True
            
            
                  
        def city_choice_by_proximity(self):
            
            next_city = self.possible_cities[0]
            for city in self.possible_cities:
                distance_1 = self.distance(self.actual_city[1], city[1])
                distance_2 = self.distance(self.actual_city[1], next_city[1])
                shortest_distance = min(distance_1, distance_2)
                if(shortest_distance==distance_1):
                    next_city = city
            
            self.visited_cities.append(next_city)
            self.distance_map.append(self.distance(self.actual_city[1], next_city[1]))
            self.possible_cities.remove(next_city)
            
            return next_city
        
        
        
        def city_choice_by_pheromone(self):
            # l'influence des phéromones sera calculée en fonction des params alpha, beta, gamma
            attractiveness = []
            for city in self.possible_cities:
                pheromone_amount = self.pheromone_map[_CITIES.index(self.actual_city)][_CITIES.index(city)]
                new_attractiveness = self.gamma + (pheromone_amount**self.alpha)*((1/self.distance(self.actual_city[1],city[1]))**self.beta)
                attractiveness.append(new_attractiveness)
            
            sum_attractiveness = sum(attractiveness)
            for i in range(len(attractiveness)):
                attractiveness[i] = attractiveness[i]/sum_attractiveness
            
            index = 0
            for i in range(len(attractiveness)-1):
                most_attractive = max(attractiveness[i], attractiveness[i+1])
                if(most_attractive == attractiveness[i]):
                    index = i
                else:
                    index = i+1
            
            next_city = self.possible_cities[index]
            self.visited_cities.append(next_city)
            self.possible_cities.remove(next_city)
            self.distance_map.append(self.distance(self.actual_city[1], next_city[1]))
            
            return next_city
                    
                
            
            
            
        def add_pheromone(self):
            pheromone_amount = 0.0
            if self.complete_tour:
                self.visited_cities.append(self.visited_cities[0])
                self.distance_map.append(self.distance(self.actual_city[1], self.visited_cities[0][1]))
                self.actual_city=self.visited_cities[0]
                self.first_pass = False
                pheromone_amount = const_pheromone/sum(self.distance_map)
                
            self.pheromone_map = self._init_matrix_(len(_CITIES))
            
            for i in range(len(self.visited_cities)-1):
                self.pheromone_map[_CITIES.index(self.visited_cities[i])][_CITIES.index(self.visited_cities[i+1])]= pheromone_amount
                self.pheromone_map[_CITIES.index(self.visited_cities[i+1])][_CITIES.index(self.visited_cities[i])]= pheromone_amount
            
            

def draw_city():
    font = pygame.font.SysFont('Arial',25)
    for city in _CITIES:
        # we draw a dot at the city location
        pygame.draw.circle(screen, (255,255,255), (city[1][0], city[1][1]), 4)
        # then we add the city name
        if city[0]=="Clermont-Ferrand" or city[0]=="Strasbourg":
            screen.blit(font.render(city[0], 1, (255, 255, 255)), (city[1][0]-60, city[1][1]+5))
        else:
            screen.blit(font.render(city[0], 1, (255, 255, 255)), (city[1][0]-20, city[1][1]-35))
                  


def draw_shortest_route(global_shortest):
    for i in range(len(global_shortest)-1):
        pygame.draw.line(screen, (255, 255, 255), global_shortest[i][1], global_shortest[i+1][1], width=1)

    
def get_mouse_coordinates():
    x,y = pygame.mouse.get_pos()
    print(f"({x}, {y})")
    
    
const_pheromone = 100.0
copy_cities=copy.deepcopy(_CITIES)
new_colony = colony(colony_size=100, nb_iterations=500, rho=0.4)
new_colony.mainloop()
shortest_route = new_colony.global_shortest_route

pygame.init()
 

__screensize__ = (600, 600)
screen = pygame.display.set_mode(__screensize__)
image = pygame.image.load("french_map.png").convert_alpha()

running = True

while running:
    screen.blit(image, (15, 15))
    draw_city()
    draw_shortest_route(shortest_route)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            get_mouse_coordinates()
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()

