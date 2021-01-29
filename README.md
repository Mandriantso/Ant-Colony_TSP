# Ant-Colony_TSP
Ce TP consistait à optimiser l'algorithme du voyageur de commerce en utilisant une colonie de fourmis. Les fourmis doivent trouver le plus court chemin. Pour cela, elles partent d'une ville choisie aléatoirement sur la carte et doivent obligatoirement visiter chaque ville une seule et unique fois avant de retourner à leur ville de départ. L'intérêt d'utiliser des colonies de fourmis est de trouver le meilleur chemin, non pas seulement en choisissant la ville la plus proche à chaque fois, mais aussi en prenant en compte l'intensité des phéromones déposées par la colonie à chaque tour. Plus le chemin sera court, plus l'intensité des phéromones déposés sera importante. On joue aussi sur des modifications génétiques en laissant la possibilité à la fourmi de choisir une ville au hasard si elle est plus proche que la ville choisie par proximité ou par phéromone.

### Composition du code
Le code se divise en deux classes: la classe **colony** et la classe **ant**.

#### Classe ant
La classe ant est en fait une sous-classe de la classe colony. Il s'agit de la classe où l'on s'occupe des fourmis individuellement. Elle est composée de 6 fonctions mis à part la fonction ```__init__```, et prend en entrée 5 paramètres:
- **pheromone_map** qui est une matrice de taille nb_villes * nb_villes, constituée de la quantité de phéromone entre chaque ville. On a besoin d'appeler ce paramètre en entrée car il est donné par la classe colony après avoir fait la somme des pheromone_map de toutes les fourmis composant la colonie.


