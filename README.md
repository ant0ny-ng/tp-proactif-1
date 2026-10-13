# Outil d'administration réseau

Petite application web (Python / Flask) pour gérer un petit parc : recherche d'un serveur dans l'inventaire, dépôt d'un fichier de configuration, et test d'une machine par ping.

Application réalisée dans le cadre d'un TP. Le code contient des failles volontaires (injection SQL, upload non contrôlé, injection de commande), destinées à être repérées par les outils d'analyse et à servir de support à l'exercice. À ne pas déployer en production.

## Lancer en local

```
pip install -r requirements.txt
python app.py
```

L'application écoute sur le port 5000.
