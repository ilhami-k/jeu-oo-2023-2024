# Projet Jeu video survie

Bienvenue dans notre projet de jeu ! Ce guide vous expliquera comment configurer votre environnement de développement, installer les dépendances nécessaires et lancer le jeu.

## Prérequis
### Contrôles dans le jeu
- Les mouvements sont gérés par les ZQSD directionnelles.
- bouton "f" pour intéragir avec PNJ
- bouton "e" pour ramasser des items
- bouton "i" pour ouvrir l'inventaire
- bouton "t" pour ouvrir les quêtes
- bouton "escape" pour ouvrir le menu pause
- bouton "enter" pour passer les dialogues
- clic "gauche" pour tirer et intéragir avec quêtes
- clic "droit" pour intéragir avec l'inventaire
### Assurez-vous d'avoir les éléments suivants installés sur votre machine :
- [Python 3.x](https://www.python.org/downloads/)

## Si vous lancez le jeu à partir d'un ZIP, veuillez le deziper et suivre le readme. 
## !!LANCEZ LE JEU A PARTIR DU TERMINAL ET PAS DANS VISUAL STUDIO CODE!! 
## Configuration de l'environnement de développement

### 1. Créer un Environnement Virtuel

Pour éviter les conflits de dépendances entre différents projets Python, il est recommandé d'utiliser un environnement virtuel. Voici comment le créer :

1. **Ouvrez votre terminal.**

2. **Accédez au répertoire de votre projet :**
    ```sh
    cd /chemin/vers/le/projet
    ```

3. **Créez un environnement virtuel :**
    - Sous Windows :
      ```sh
      python -m venv env
      ```
    - Sous macOS et Linux :
      ```sh
      python3 -m venv env
      ```

4. **Activez l'environnement virtuel :**
    - Sous Windows :
      ```sh
      .\env\Scripts\activate
      ```
    - Sous macOS et Linux :
      ```sh
      source env/bin/activate
      ```

### 2. Installation des Dépendances

Une fois l'environnement virtuel activé, vous devez installer les dépendances nécessaires à partir du fichier `requirements.txt`.

1. **Installez les dépendances :**
    ```sh
    pip install -r requirements.txt
    ```

## Lancement du Jeu

Après avoir installé les dépendances, vous pouvez aller sur le dossier Application lancer le jeu à l'aide du fichier `main.py`.

1. **Allez sur le dossier `Application`**
  ```sh
  cd Application
  ```
2. **Exécutez le fichier `main.py` :**
  ```sh
  python main.py
  ```

Votre jeu devrait maintenant se lancer et être prêt à jouer !
