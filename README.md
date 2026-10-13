# Outil d'administration réseau

Petite application web (Python / Flask) pour gérer un petit parc : recherche d'un serveur dans l'inventaire, dépôt d'un fichier de configuration, et test d'une machine par ping.

Application réalisée dans le cadre d'un TP. Le code contient des failles volontaires (injection SQL, upload non contrôlé, injection de commande), destinées à être repérées par les outils d'analyse et à servir de support à l'exercice. À ne pas déployer en production.

## Lancer en local

```
pip install -r requirements.txt
python app.py
```

L'application écoute sur le port 5000.

Avec Docker :

```
docker build -t tp-proactif-1 .
docker run -d -p 5000:5000 tp-proactif-1
```

## Mini CTF

L'application sert aussi de support à trois challenges, hébergés sur CTFd pendant le TP :

- injection SQL sur la page de recherche (le flag est dans la table `secret`) ;
- upload de fichier, avec le bouton « Appliquer la configuration » qui exécute le fichier déposé (flag dans `flag_upload.txt`) ;
- injection de commande sur la page ping (flag dans `flag_ping.txt`).

Les deux fichiers de flags sont créés au démarrage de l'application. Les fiches d'aide données aux joueurs sont dans le dossier `ctf/`.
