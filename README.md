# Défi de la Relève M13 AAA-ÉLITE 2025-26 — Statistiques

Ce dépôt calcule et affiche les statistiques individuelles (Buts, Passes, Points) de tous les joueurs des **12 équipes** qui ont participé au tournoi **Défi de la Relève M13 AAA-ÉLITE 2025-26** à Sherbrooke (1, 2 et 3 mai 2026) — **21 parties** au total.

## Voir les statistiques

Ouvrez le fichier [`index.html`](index.html) dans un navigateur web **ou** démarrez un serveur local :

```bash
# Python 3
python3 -m http.server 8080
# Puis visitez http://localhost:8080
```

La page affiche :
- Le classement de **tous les joueurs** par **Points** (décroissant)
- En cas d'égalité en points, les **Buts** départagent les joueurs
- Filtrage par équipe et recherche par nom de joueur
- Tri interactif sur toutes les colonnes

## Structure du projet

```
index.html          ← Page web des statistiques (ouvrir dans un navigateur)
stats.py            ← Script Python pour recalculer STATS.md
STATS.md            ← Classement généré automatiquement
data/
  games.json        ← Données des 21 parties (buts, passes, équipes, joueurs)
```

## Mettre à jour les données de parties

Les données sont dans `data/games.json`. Chaque partie suit ce format :

```json
{
  "game_number": 1,
  "home_team": "DRAKKAR DR M13",
  "away_team": "OCÉANIC DR M13",
  "goals": [
    {
      "period": 1,
      "time": "0:23",
      "team": "DRAKKAR DR M13",
      "scorer": { "name": "MAXENCE LANGLOIS", "number": 78 },
      "assists": [{ "name": "CHRISTOPHE BERNARD", "number": 86 }]
    }
  ]
}
```

Après modification du fichier JSON, rechargez `index.html` ou regénérez `STATS.md` :

```bash
python3 stats.py
```

## Format des statistiques

| Colonne | Description |
|---------|-------------|
| **PTS** | Points (Buts + Passes) |
| **B**   | Buts |
| **A**   | Passes décisives |

Classement : **Points décroissants**, buts comme critère de départage en cas d'égalité.
