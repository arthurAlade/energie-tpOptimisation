# Compte rendu
## Auteurs

- Aladenise Arthur
- Charre Kyllian
- Chazeau Vincent

## Modélisation

Variables:

Contraintes:

Solution réalisable ?

Instance de solution non réalisable

## Premières Heuristiques


## Recherche locale


Demande : A partir du sujet suivant, modélise oi le problème sous forme de programme linéaire: Dans une usine, on doit effectuer des tâches (jobs) comportant chacune plusieurs opérations. Ces opérations peuvent être effectuées sur un ensemble de machines (spécifique à chaque opération) et leur durée et la quantité d'énergie nécessaire dépend de la machine choisie pour effectuer l'opération. On doit effectuer les opérations d'une même tâche l'une après l'autre : l'opération i de la tâche ne peut commencer que si l'opération i+1 est terminée. Les machines peuvent être allumées ou éteintes. Lorsqu'une machine est allumée, elle a besoin d'une quantité importante d'énergie et de temps avant d'être opérationnelle, de même, lorsqu'on l'éteint. Si elle reste allumée, mais n'effectue aucune opération, sa consommation est basse. Lorsqu'elle effectue une opération, sa consommation est haute. On peut allumer et éteindre une même machine plusieurs fois durant son planning si cela permet de diminuer sa consommation d'énergie. Si ce n'est pas le cas, elle sera au moins allumée en début de planning et éteinte en fin de planning. L'entreprise souhaite utiliser le moins d'énergie possible, mais la durée d'exécution des tâches est aussi importante et elle peut être amenée à utiliser plus d'énergie pour baisser la durée totale du planning ou la durée moyenne pour effectuer une tâche. En effet, le planning de chaque machine ne peut pas dépasser une durée maximale fixée par l'entreprise et toutes les tâches doivent être effectuées. L'objectif du TP est de proposer des solutions d'optimisation à l'entreprise pour obtenir pour chaque ensemble de tâches des plannings précisant pour chaque opération la machine sur laquelle elle est effectuée, son heure de départ, ainsi que les heures de démarrage et d'arrêt des différentes machines.
Détails
event
8 avril, 16:44
apps
Applications Gemini
chat

Okay, modélisons ce problème sous forme de programme linéaire (ou plus précisément, un programme linéaire en nombres entiers mixtes - MILP - car il y aura des variables binaires).

1. Ensembles et Indices

    J: Ensemble des tâches (jobs). Index j.
    O_j: Ensemble des opérations pour la tâche j. Index i. Les opérations sont numérotées séquentiellement (1, 2, ... , |O_j|). Nous noterons une opération spécifique par (j, i).
    M: Ensemble des machines. Index m.
    M_{j,i}: Sous-ensemble des machines M capables d'effectuer l'opération (j, i). M_{j,i} ⊆ M.

2. Paramètres (Données du problème)

    p_{j,i,m}: Durée (temps de traitement) de l'opération (j, i) si elle est effectuée sur la machine m (m ∈ M_{j,i}).
    e_{op, j,i,m}: Taux de consommation d'énergie (énergie par unité de temps) lorsque la machine m effectue l'opération (j, i).
    E_{idle, m}: Taux de consommation d'énergie lorsque la machine m est allumée mais inactive (basse consommation).
    E_{on, m}: Quantité d'énergie fixe consommée pour allumer la machine m.
    T_{on, m}: Temps nécessaire pour que la machine m soit opérationnelle après l'allumage (temps de chauffe).
    E_{off, m}: Quantité d'énergie fixe consommée pour éteindre la machine m.
    T_{off, m}: Temps pendant lequel la machine m est occupée lors de l'extinction (temps de refroidissement).
    D_{max}: Durée maximale autorisée pour l'ensemble du planning (makespan).
    D_{max, m}: Durée maximale autorisée pour le planning de la machine m (depuis son premier allumage jusqu'à sa dernière extinction complète).
    H: Une constante "suffisamment grande" (Big-M) utilisée pour les contraintes logiques.

3. Variables de Décision

    Assignation et Séquencement :
        x_{j,i,m}: Variable binaire. x_{j,i,m} = 1 si l'opération (j, i) est assignée à la machine m, 0 sinon. (Doit être 0 si m ∉ M_{j,i}).
        s_{j,i}: Variable continue ≥ 0. Heure de début de l'opération (j, i).
        c_{j,i}: Variable continue ≥ 0. Heure de fin de l'opération (j, i).
        y_{j,i,j',i'}: Variable binaire. Utilisée pour le séquencement sur une même machine. y_{j,i,j',i'} = 1 si l'opération (j, i) précède l'opération (j', i') sur la même machine (si elles sont assignées à la même machine), 0 sinon. Défini pour toutes paires d'opérations (j, i) ≠ (j', i').

    État des Machines (Modèle simplifié : 1 seul cycle On/Off par machine) :
        u_m: Variable binaire. u_m = 1 si la machine m est utilisée (allumée au moins une fois), 0 sinon.
        t_{start, m}: Variable continue ≥ 0. Instant où la machine m commence sa phase d'allumage. La machine devient disponible à t_{start, m} + T_{on, m}.
        t_{end, m}: Variable continue ≥ 0. Instant où la machine m commence sa phase d'extinction. La machine n'est plus disponible après cet instant et est complètement éteinte à t_{end, m} + T_{off, m}.
        IdleTime_m: Variable continue ≥ 0. Temps total pendant lequel la machine m est allumée mais inactive.

    Variables d'Objectif et de Performance :
        C_{max}: Variable continue ≥ 0. Makespan global (heure de fin de la dernière opération terminée).
        C_j: Variable continue ≥ 0. Heure de fin de la tâche j.

4. Fonction Objectif

L'objectif principal est de minimiser l'énergie totale consommée. Celle-ci se décompose en :

    Énergie des opérations : E_Operations = ∑_{j∈J} ∑_{i∈O_j} ∑_{m∈M_{j,i}} x_{j,i,m} * p_{j,i,m} * e_{op, j,i,m}
    Énergie d'allumage/extinction : E_OnOff = ∑_{m∈M} u_m * (E_{on, m} + E_{off, m})
    Énergie en veille (idle) : E_Idle = ∑_{m∈M} IdleTime_m * E_{idle, m}

Objectif : Minimiser Z = E_Operations + E_OnOff + E_Idle

Minimiser Z = ∑_{j∈J} ∑_{i∈O_j} ∑_{m∈M_{j,i}} (x_{j,i,m} * p_{j,i,m} * e_{op, j,i,m}) + ∑_{m∈M} (u_m * (E_{on, m} + E_{off, m})) + ∑_{m∈M} (IdleTime_m * E_{idle, m})

Note : Pour prendre en compte les compromis avec la durée, on pourrait : a) Utiliser cet objectif et ajouter une contrainte sur C_{max} (comme C_{max} ≤ D_{max}). b) Minimiser C_{max} en ajoutant une contrainte sur l'énergie totale Z ≤ BudgetEnergie. c) Minimiser une fonction pondérée, e.g., w1 * Z + w2 * C_{max}.

5. Contraintes

    Assignation Unique : Chaque opération doit être assignée à exactement une machine éligible.

    ∑_{m ∈ M_{j,i}} x_{j,i,m} = 1   ∀ j ∈ J, ∀ i ∈ O_j

    Relation Début/Fin Opération : La fin d'une opération dépend de son début et de la durée sur la machine choisie.

    c_{j,i} = s_{j,i} + ∑_{m ∈ M_{j,i}} x_{j,i,m} * p_{j,i,m}   ∀ j ∈ J, ∀ i ∈ O_j

    Précédence Interne aux Tâches : L'opération i doit finir avant que l'opération i+1 de la même tâche puisse commencer.

    s_{j, i+1} ≥ c_{j,i}   ∀ j ∈ J, ∀ i = 1, ..., |O_j|-1

    Non-chevauchement sur les Machines : Deux opérations (j, i) et (j', i') assignées à la même machine m ne peuvent pas s'exécuter en même temps.

    Pour chaque paire d'opérations distinctes (j, i) ≠ (j', i') et chaque machine m :
    s_{j',i'} ≥ c_{j,i} - H * (1 - y_{j,i,j',i'}) - H * (2 - x_{j,i,m} - x_{j',i',m})
    s_{j,i} ≥ c_{j',i'} - H * y_{j,i,j',i'} - H * (2 - x_{j,i,m} - x_{j',i',m})

    (Ces contraintes Big-M assurent que si les deux opérations sont sur m (x_{j,i,m}=1 et x_{j',i',m}=1), alors soit s_{j',i'} ≥ c_{j,i} (si y=1), soit s_{j,i} ≥ c_{j',i'} (si y=0). Si l'une des opérations n'est pas sur m, les termes H*(...) rendent la contrainte triviale).

    Lien Utilisation Machine (u_m) : La machine m est utilisée si au moins une opération lui est assignée.

    H * u_m ≥ ∑_{j∈J} ∑_{i∈O_j | m∈M_{j,i}} x_{j,i,m}   ∀ m ∈ M
    u_m ≤ ∑_{j∈J} ∑_{i∈O_j | m∈M_{j,i}} x_{j,i,m}   ∀ m ∈ M

    (La première force u_m=1 si la somme est > 0. La seconde force u_m=0 si la somme est 0).

    Disponibilité Machine (Warm-up/Cool-down) : Une opération sur m ne peut commencer qu'après le warm-up et doit finir avant le cool-down.

    s_{j,i} ≥ t_{start, m} + T_{on, m} - H * (1 - x_{j,i,m})   ∀ j, i, m ∈ M_{j,i}
    c_{j,i} ≤ t_{end, m} + H * (1 - x_{j,i,m})             ∀ j, i, m ∈ M_{j,i}

    (Contraintes actives seulement si x_{j,i,m}=1).

    Cohérence Temps On/Off Machine : Le début de l'extinction doit être après le début de l'allumage (+ warm-up). Ces temps ne sont définis que si la machine est utilisée.

    t_{end, m} ≥ t_{start, m} + T_{on, m} - H * (1 - u_m)   ∀ m ∈ M
    t_{start, m} ≤ H * u_m   ∀ m ∈ M  // t_start = 0 if u_m = 0
    t_{end, m} ≤ H * u_m     ∀ m ∈ M  // t_end = 0 if u_m = 0

    Calcul du Temps Inactif (IdleTime_m) : Temps total où la machine est ON moins le temps où elle est en warm-up moins le temps où elle exécute des opérations.

    DuréeTotaleON_m = t_{end, m} - t_{start, m}
    TempsOpérationTotal_m = ∑_{j∈J} ∑_{i∈O_j | m∈M_{j,i}} x_{j,i,m} * p_{j,i,m}
    TempsActifTotal_m = T_{on, m} * u_m + TempsOpérationTotal_m // Inclut le warm-up si utilisée

    // IdleTime_m doit être la différence, mais seulement si u_m = 1, sinon 0.
    IdleTime_m ≥ (DuréeTotaleON_m - TempsActifTotal_m) - H * (1 - u_m)  ∀ m ∈ M
    IdleTime_m ≤ (DuréeTotaleON_m - TempsActifTotal_m) + H * (1 - u_m)  ∀ m ∈ M
    IdleTime_m ≤ H * u_m  ∀ m ∈ M // Force IdleTime_m = 0 if u_m = 0
    IdleTime_m ≥ 0         ∀ m ∈ M

    (Note : Remplacer DuréeTotaleON_m et TempsActifTotal_m par leurs expressions en termes de variables de décision dans les contraintes réelles).

    Calcul du Makespan (C_{max}) : Maximum des temps de fin de toutes les opérations.

    C_{max} ≥ c_{j,i}   ∀ j ∈ J, ∀ i ∈ O_j

    Calcul Fin de Tâche (C_j) : Temps de fin de la dernière opération de la tâche j.

    C_j = c_{j, |O_j|}   ∀ j ∈ J

    Contrainte de Durée Maximale Globale :

    C_{max} ≤ D_{max}

    Contrainte de Durée Maximale par Machine : La durée entre le début de l'allumage et la fin de l'extinction ne doit pas dépasser D_{max, m}.

    (t_{end, m} + T_{off, m}) - t_{start, m} ≤ D_{max, m} + H * (1 - u_m)   ∀ m ∈ M

    (La contrainte est relaxée si u_m=0).

    Non-négativité : Toutes les variables de temps (s, c, t_start, t_end, IdleTime, C_max, C_j) sont ≥ 0.

    Variables Binaires : x_{j,i,m}, y_{j,i,j',i'}, u_m ∈ {0, 1}.

Limitations et Complexité

    Cycles On/Off Multiples : Ce modèle suppose un seul cycle allumage/extinction par machine utilisée. Gérer des cycles multiples (k cycles (t_{start, m, k}, t_{end, m, k}) avec des variables binaires u_{m, k} pour les activer) complexifie énormément le modèle (nombre de variables, contraintes de non-chevauchement des cycles, lien avec les opérations). Cela pourrait nécessiter des approches plus avancées ou une discrétisation du temps.
    Taille du Modèle : Le nombre de variables y_{j,i,j',i'} et les contraintes de non-chevauchement associées peuvent rendre le modèle très grand si le nombre d'opérations est élevé.
    Big-M : La valeur de H doit être choisie avec soin (assez grande pour ne pas couper de solutions réalisables, mais pas trop pour éviter des problèmes numériques).

Ce modèle MILP fournit une base formelle pour résoudre le problème d'ordonnancement en minimisant l'énergie sous diverses contraintes, en supposant un seul cycle on/off par machine. Pour explorer les compromis énergie/durée, on peut ajuster la contrainte D_{max} ou modifier la fonction objectif.
