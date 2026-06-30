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
data/
  games.json        ← Données des 21 parties (buts, passes, équipes, joueurs)
```

## Mettre à jour les données de parties

Les données sont dans `data/games.json`. Chaque partie suit ce format :

```json
{
  "id": 1,
  "date": "2026-05-01",
  "home_team": "Cantons de l'Estrie",
  "away_team": "Phénix du Lac-St-Louis",
  "score": { "home": 3, "away": 2 },
  "goals": [
    {
      "scorer": "Alexis Tremblay",
      "scorer_team": "Cantons de l'Estrie",
      "assists": ["Mathieu Gagnon", "William Côté"]
    }
  ]
}
```

Modifiez le fichier JSON avec les vraies données de parties, puis rechargez `index.html`.

## Format des statistiques

| Colonne | Description |
|---------|-------------|
| **PTS** | Points (Buts + Passes) |
| **B**   | Buts |
| **A**   | Passes décisives |

Classement : **Points décroissants**, buts comme critère de départage en cas d'égalité.
