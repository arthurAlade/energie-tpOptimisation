# Compte rendu
## Auteurs

- Aladenise Arthur
- Charre Kyllian
- Chazeau Vincent

## Modélisation

### Variables de Décision (Q1)

Pour chaque opération o de chaque tâche j:

- Affectation machine: La machine m sur laquelle l'opération o est exécutée.
- Temps de début d'opération: L'instant to,d​ où l'opération o débute.

Pour chaque machine m:

- Temps de démarrage: L'instant tm,start​ où la machine m est allumée.
- Temps d'arrêt: L'instant tm,end​ où la machine m est éteinte.

### Contraintes

- Séquencement des opérations: Pour chaque tâche j, si l'opération oi​ précède l'opération oi+1​, alors oi+1​ ne peut commencer qu'une fois oi​ terminée. Mathématiquement, toi+1​,d​≥toi​,d​+Duree(oi​,moi​​), où Duree(oi​,moi​​) est la durée de l'opération oi​ sur la machine moi​​ qui lui est assignée.
- Capacité maximale des machines: Chaque machine m a une durée d'utilisation maximale Dmax​ définie par l'entreprise. L'intervalle de temps entre son démarrage et son arrêt ne doit pas la dépasser.
- Toutes les tâches effectuées: L'ensemble des opérations de toutes les tâches doit être planifié.
- Disponibilité des machines: Une opération ne peut être exécutée sur une machine que si celle-ci est allumée et disponible (non occupée par une autre opération).

### Objectifs (Q2)

L'entreprise vise à optimiser les critères suivants, souvent antagonistes :

- Minimisation de la consommation d'énergie totale: Réduire au maximum l'énergie consommée par toutes les machines.
- Minimisation de la durée totale du planning: Achever toutes les tâches le plus rapidement possible.
- Minimisation de la durée moyenne d'exécution des tâches: Réduire le temps moyen nécessaire pour compléter chaque tâche.

#### Fonction Objectif Agrégée

Une fonction objectif unique peut être formulée comme une combinaison pondérée des différents objectifs, permettant de trouver un compromis. L'objectif est de minimiser la valeur Z:

    Z=α⋅Etotale​+β⋅Cmax+γ⋅Cmoy​

Où :

- Etotale​ est la consommation totale d'énergie de toutes les machines.
- Cmax est la durée totale du planning (l'instant de fin de la dernière opération).
- Cmoy​ est la durée moyenne pour effectuer une tâche.
    α, β, γ sont des coefficients de pondération positifs, déterminés par l'entreprise en fonction de l'importance relative de chaque objectif.

### Évaluation d'une Solution (Q3)

Solution réalisable: Une solution est réalisable si elle respecte toutes les contraintes. Sa valeur est calculée en substituant les valeurs Etotale​, Cmax, et Cmoy​ dans la fonction objectif agrégée Z.

Solution non réalisable: Une solution est non réalisable si au moins une contrainte est violée. Pour la pénaliser et la distinguer des solutions réalisables, on peut lui assigner une valeur infinie (+∞) ou une valeur très élevée pour la fonction objectif Z, reflétant son inacceptabilité. Alternativement, des pénalités proportionnelles à l'ampleur de la violation des contraintes peuvent être ajoutées à Z.

### Instance Non Réalisable (Q4)

Considérons une instance où :

- Une seule tâche J1​ avec une seule opération O1​.
- L'opération O1​ ne peut être effectuée que sur une seule machine M1​.
- La durée de l'opération O1​ sur M1​ est de 10 heures.
- La durée maximale autorisée pour le planning de n'importe quelle machine est de 8 heures.

Dans cette instance, il est impossible de planifier l'opération O1​ car sa durée dépasse la capacité maximale allouée à la machine M1​. Par conséquent, aucune solution réalisable n'existe pour cette instance.

## Premières Heuristiques


## Recherche locale