# Ant-Colony_TSP
Ce TP consistait à optimiser l'algorithme du voyageur de commerce en utilisant une colonie de fourmis. Les fourmis doivent trouver le plus court chemin. Pour cela, elles partent d'une ville choisie aléatoirement sur la carte et doivent obligatoirement visiter chaque ville une seule et unique fois avant de retourner à leur ville de départ. L'intérêt d'utiliser des colonies de fourmis est de trouver le meilleur chemin, non pas seulement en choisissant la ville la plus proche à chaque fois, mais aussi en prenant en compte l'intensité des phéromones déposées par la colonie à chaque tour. Plus le chemin sera court, plus l'intensité des phéromones déposés sera importante. On joue aussi sur des modifications génétiques en laissant la possibilité à la fourmi de choisir une ville au hasard si elle est plus proche que la ville choisie par proximité ou par phéromone.

### Composition du code
Le code se divise en deux classes: la classe **colony** et la classe **ant**.

#### Classe ant
La classe ant est en fait une sous-classe de la classe colony. Il s'agit de la classe où l'on s'occupe des fourmis individuellement. Elle est composée de 6 fonctions mise à part la fonction ```__init__(self)```, et prend en entrée 5 paramètres:
- **pheromone_map** qui est une matrice de taille nb_villes * nb_villes, constituée de la quantité de phéromone entre chaque ville. On a besoin d'appeler ce paramètre en entrée car il est donné par la classe colony après avoir fait la moyenne des pheromone_map de toutes les fourmis composant la colonie.
- **alpha**, **beta** et **gamma** qui sont des paramètres utilisés pour choisir la prochaine ville à visiter en fonction de l'intensité du phéromone. Ces paramètres sont fixés par défaut respectivement à 0.8, 0.6 et 0.1.
- **first_pass** qui est un bouléen permettant de savoir s'il s'agit du premier tours des fourmis ou si elles ont en déjà fait au moins 1. Par défaut, on l'initialise à True.  

Les différentes fonctions implémentées dans cette classe sont:
- ```_init_matrix_(self, len_map, value=0.0)``` qui permet de créer une matrice de zéros. Elle est utilisée pour remettre à zéro la pheromone_map de la fourmi une fois qu'elle a fini son tour afin d'ajouter ces valeurs à la pheromone_map globale de la colonie.
- ```distance(self, a, b)``` qui retourne la distance entre deux villes. Cette fonction est utilisée au premier tour pour choisir la prochaine ville à visiter en fonction de sa proximité. Elle est aussi utilisée pour ajouter des valeurs dans le tableau **self.distance_map** afin de calculer la distance totale parcourue par la fourmi à la fin de son tour.
- ```city_choice_by_proximity(self)``` qui parcours le tableau **self.possible_cities** - tableau contenant toutes les villes qui n'ont pas encore été visitées - pour essayer de trouver la ville la plus proche de la ville dans laquelle la fourmi se trouve (**self.actual_city**). Les tableaux **self.visited_cities** - tableau contenant la liste des villes visitées - , **self.possible_cities** et **self.distance_map** sont mis à jour à la fin de la fonction.
```python
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
```
- ```city_choice_by_pheromone(self)```. Cette fonction calcule l'attractivité d'une ville en fonction de la quantité de phéromone déposée entre cette ville et la ville actuelle. L'attractivité de la ville est déterminée par l'équation:
```python
new_attractiveness = self.gamma + (pheromone_amount**self.alpha)*((1/self.distance(self.actual_city[1],city[1]))**self.beta)
```
où gamma est un facteur permettant de trouver de nouvelles routes/branches.  
On calcule donc l'attractivité de toutes les villes restantes, et on cherche celle qui est la plus attractive.
- ```city_choice(self)``` est la fonction principale pour choisir la prochaine ville. Elle appelle la fonction ```city_choice_by_proximity(self)``` s'il s'agit du premier tour et ```city_choice_by_pheromone(self)``` sinon. On fait ensuite une modification génétique en choisissant une ville aléatoirement dans les villes qui n'ont pas encore été visitées. Si la distance entre la ville choisie aléatoirement et la ville actuelle est inférieure à la distance entre la ville choisie avec l'une des deux fonctions citées précédemment et la ville actuelle, alors la ville choisie aléatoirement devient la prochaine destination.
```python
                if len(self.possible_cities)>1:
                    random_city = self.possible_cities[randint(0, len(self.possible_cities)-1)]
                    if self.distance(self.actual_city[1], next_city[1])>self.distance(self.actual_city[1], random_city[1]):
                        self.possible_cities.append(next_city)
                        self.visited_cities.remove(next_city)
                        self.distance_map.remove(self.distance(self.actual_city[1], next_city[1]))
                        
                        self.possible_cities.remove(random_city)
                        self.visited_cities.append(random_city)
                        self.distance_map.append(self.distance(self.actual_city[1], random_city[1]))
```
Cette opération semble nécessaire afin de trouver de nouvelles routes qui peuvent potentiellement être meilleures.
- ```add_pheromone(self)``` calcule la quantité de phéromone que la fourmi doit déposer sur chaque branche en fonction de la distance totale parcourue. On remet alors la pheromone_map de la fourmi à zéro pour ensuite l'instancier avec la nouvelle quantité de phéromone.

### Classe colony
La classe colony est la classe principale qui met en commun les données de chaque fourmi pour s'occuper de la colonie dans sa globalité. Elle a 3 paramètres en entrée:
- **colony_size** qui est le nombre de fourmis souhaité dans la colonie.
- **nb_iterations** qui est le nombre de tours à faire par fourmi.
- **rho**, le coefficient d'évaporation des phéromones.

Elle comporte 8 fonctions:
- ```_init_ants(self)``` qui appelle la classe ant pour initialiser autant de fourmis que la taille de la colonie.
- ```_init_matrix_(self, len_map, value=0.0)``` qui est la même fonction que celle de la classe ant. On aurait pu écrire cette fonction en dehors des classes.
- ```





