# Simulation de croissance de flocon de neige

Application interactive permettant de simuler et de visualiser la croissance d’un flocon de neige sur un maillage hexagonal.

Le projet comprend :

* un **moteur de simulation** côté backend
* une **interface web interactive** permettant de visualiser et modifier l’état du système en temps réel.

L’application est déployée en ligne et peut être utilisée directement depuis un navigateur.

---

# Démonstration

Application accessible ici :

https://snowflake-81s6.onrender.com

---

# Présentation du projet

La simulation modélise la croissance d’un flocon de neige à l’aide d’un **maillage hexagonal**.
Chaque cellule du maillage représente une position dans le cristal en formation.

Chaque cellule possède plusieurs attributs physiques :

* **temperature**
* **vapor**
* **ice_potential**
* **frozen**

La simulation évolue par **itérations discrètes**, et l’état du maillage peut être visualisé selon différents modes.

---

# Fonctionnalités

* Visualisation interactive d’un **maillage hexagonal**
* Plusieurs **modes d’affichage**

  * état gelé (frozen)
  * température
  * vapeur
  * potentiel de glace
* **Barres de couleur dynamiques** indiquant l’échelle des valeurs
* **Sélection de cellules à la souris**
* Modification des attributs des **cellules sélectionnées**
* Possibilité de modifier **toutes les cellules simultanément**
* Paramétrage de la **taille du maillage**
* Simulation **pas à pas** ou continue

---

# Technologies utilisées

## Frontend

* JavaScript
* HTML
* Canvas API

## Backend

* Python
* FastAPI

## Déploiement

* Render

---

# API Backend

Le backend expose plusieurs endpoints utilisés par l’interface web.

## Simulation

```text
PUT /simulation
```

Exécute une itération de la simulation.

---

## Récupération du maillage

```text
GET /mesh
```

Retourne l’ensemble du maillage avec les attributs de chaque cellule.

---

## Modification des paramètres de simulation

```text
PATCH /simulation_params
```

Permet de modifier par exemple :

* la taille du maillage
* le nombre d’itérations

---

## Modification des attributs des cellules

```text
PATCH /temperature
PATCH /vapor
PATCH /ice_potential
PATCH /frozen/true
PATCH /frozen/false
```

Ces endpoints permettent de modifier les attributs des cellules sélectionnées.

Si aucune cellule n’est sélectionnée, la modification est appliquée **à toutes les cellules du maillage**.

---

# Structure du maillage

Le maillage est organisé en **anneaux hexagonaux** autour d’une cellule centrale.

Chaque cellule est identifiée par un couple :

```
(r, i)
```

où :

* `r` est l’indice de l’anneau
* `i` est la position dans l’anneau

La **taille du maillage** correspond au nombre d’anneaux autour de la cellule centrale.

Exemple pour `size = 1` :

```
(0,0)

(1,0) (1,1) (1,2)
(1,3) (1,4) (1,5)
```

---

# Lancer le projet en local

Cloner le dépôt :

```
git clone https://github.com/ton-username/snowflake-simulation.git
cd snowflake-simulation
```

Installer les dépendances :

```
pip install -r requirements.txt
```

Lancer le serveur backend :

```
uvicorn main:app --reload
```

Puis ouvrir l’interface web dans le navigateur.

---

# Structure du projet

```
backend/
    main.py
    models.py
    wrapper.py

frontend/
    index.html
    app.js
```

---

# Améliorations possibles

Plusieurs extensions sont envisageables :

* échelles logarithmiques pour certaines grandeurs
* statistiques sur les cellules sélectionnées
* zoom et déplacement dans le maillage
* optimisation du rendu graphique
* export des états de simulation

---

# Auteur

Projet réalisé par Kévin N'gakosso

---

# Licence

Ce projet est open-source et distribué sous licence **MIT**.
