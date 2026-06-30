#!/usr/bin/env python3
"""
M13 AAA-ELITE Défi de la Relève 2025-26
Calculate and display player statistics from game data.
"""

import json
from collections import defaultdict


def load_games(filepath="data/games.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_stats(data):
    """Returns player_stats and team_scores dicts."""
    # player_stats: {(team, name, number): {goals, assists, points, games}}
    player_stats = defaultdict(lambda: {"goals": 0, "assists": 0, "points": 0, "games": set()})
    team_scores = defaultdict(lambda: {"wins": 0, "losses": 0, "goals_for": 0, "goals_against": 0})
    game_results = []

    for game in data["games"]:
        gn = game["game_number"]
        home = game["home_team"]
        away = game["away_team"]
        shootout_winner = game.get("shootout_winner")
        goals_by_team = defaultdict(int)

        for goal in game["goals"]:
            team = goal["team"]
            scorer = goal["scorer"]
            goals_by_team[team] += 1

            key = (team, scorer["name"], scorer["number"])
            player_stats[key]["goals"] += 1
            player_stats[key]["points"] += 1
            player_stats[key]["games"].add(gn)

            for assist in goal["assists"]:
                akey = (team, assist["name"], assist["number"])
                player_stats[akey]["assists"] += 1
                player_stats[akey]["points"] += 1
                player_stats[akey]["games"].add(gn)

        home_goals = goals_by_team[home]
        away_goals = goals_by_team[away]

        # Shootout: winner gets an extra goal in the final score
        if shootout_winner == home:
            home_goals_final = home_goals + 1
            away_goals_final = away_goals
        elif shootout_winner == away:
            home_goals_final = home_goals
            away_goals_final = away_goals + 1
        else:
            home_goals_final = home_goals
            away_goals_final = away_goals

        team_scores[home]["goals_for"] += home_goals_final
        team_scores[home]["goals_against"] += away_goals_final
        team_scores[away]["goals_for"] += away_goals_final
        team_scores[away]["goals_against"] += home_goals_final

        if shootout_winner:
            winner = shootout_winner
            loser = away if shootout_winner == home else home
            team_scores[winner]["wins"] += 1
            team_scores[loser]["losses"] += 1
        elif home_goals > away_goals:
            team_scores[home]["wins"] += 1
            team_scores[away]["losses"] += 1
            winner = home
        elif away_goals > home_goals:
            team_scores[away]["wins"] += 1
            team_scores[home]["losses"] += 1
            winner = away
        else:
            winner = "TIE"

        game_results.append({
            "game": gn,
            "home": home,
            "away": away,
            "home_goals": home_goals_final,
            "away_goals": away_goals_final,
            "winner": winner,
            "shootout": bool(shootout_winner),
        })

    return player_stats, team_scores, game_results


def format_leaderboard(player_stats, top_n=None):
    rows = []
    for (team, name, number), s in player_stats.items():
        rows.append({
            "team": team,
            "name": name,
            "number": number,
            "goals": s["goals"],
            "assists": s["assists"],
            "points": s["points"],
            "gp": len(s["games"]),
        })
    rows.sort(key=lambda r: (-r["points"], -r["goals"], r["name"]))
    if top_n:
        rows = rows[:top_n]
    return rows


def print_report(data, player_stats, team_scores, game_results):
    games_played = len(data["games"])
    total_games = data["total_games"]

    print("=" * 70)
    print(f"  {data['tournament']}")
    print(f"  {data['location']}")
    print(f"  Games recorded: {games_played} / {total_games}")
    print("=" * 70)

    print("\n📅 GAME RESULTS")
    print("-" * 70)
    print(f"  {'#':>3}  {'HOME TEAM':<28} {'SCORE':^7} {'AWAY TEAM':<28}")
    print("-" * 70)
    for gr in game_results:
        score = f"{gr['home_goals']} - {gr['away_goals']}"
        if gr.get("shootout"):
            score += " SO"
        print(f"  {gr['game']:>3}  {gr['home']:<28} {score:^10} {gr['away']:<28}")

    print("\n\n🏒 PLAYER LEADERBOARD (by points)")
    print("-" * 70)
    print(f"  {'#':>3}  {'NAME':<30} {'TEAM':<28} {'GP':>3}  {'G':>3}  {'A':>3}  {'PTS':>4}")
    print("-" * 70)
    leaderboard = format_leaderboard(player_stats)
    for rank, row in enumerate(leaderboard, 1):
        print(
            f"  {rank:>3}  {row['name']:<30} {row['team']:<28} "
            f"{row['gp']:>3}  {row['goals']:>3}  {row['assists']:>3}  {row['points']:>4}"
        )

    print("\n\n🏆 TEAM STANDINGS")
    print("-" * 50)
    print(f"  {'TEAM':<30} {'W':>4}  {'L':>4}  {'GF':>4}  {'GA':>4}")
    print("-" * 50)
    teams_sorted = sorted(team_scores.items(), key=lambda x: (-x[1]["wins"], -x[1]["goals_for"]))
    for team, s in teams_sorted:
        print(f"  {team:<30} {s['wins']:>4}  {s['losses']:>4}  {s['goals_for']:>4}  {s['goals_against']:>4}")
    print()


def write_markdown(data, player_stats, team_scores, game_results, filepath="STATS.md"):
    games_played = len(data["games"])
    total_games = data["total_games"]
    lines = []

    lines.append(f"# {data['tournament']}\n")
    lines.append(f"**Location:** {data['location']}  ")
    lines.append(f"**Games recorded:** {games_played} / {total_games}\n")

    lines.append("\n## Game Results\n")
    lines.append("| # | Home Team | Score | Away Team |")
    lines.append("|---|-----------|:-----:|-----------|")
    for gr in game_results:
        score = f"{gr['home_goals']} - {gr['away_goals']}"
        if gr.get("shootout"):
            score += " SO"
        lines.append(f"| {gr['game']} | {gr['home']} | {score} | {gr['away']} |")

    lines.append("\n## Player Leaderboard\n")
    lines.append("| Rank | Name | Team | GP | G | A | PTS |")
    lines.append("|------|------|------|----|---|---|-----|")
    for rank, row in enumerate(format_leaderboard(player_stats), 1):
        lines.append(
            f"| {rank} | {row['name']} #{row['number']} | {row['team']} | "
            f"{row['gp']} | {row['goals']} | {row['assists']} | {row['points']} |"
        )

    lines.append("\n## Team Standings\n")
    lines.append("| Team | W | L | GF | GA |")
    lines.append("|------|---|---|----|----|")
    teams_sorted = sorted(team_scores.items(), key=lambda x: (-x[1]["wins"], -x[1]["goals_for"]))
    for team, s in teams_sorted:
        lines.append(f"| {team} | {s['wins']} | {s['losses']} | {s['goals_for']} | {s['goals_against']} |")

    lines.append(f"\n---\n*Last updated after game {games_played}*\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown stats written to {filepath}")


if __name__ == "__main__":
    data = load_games()
    player_stats, team_scores, game_results = calculate_stats(data)
    print_report(data, player_stats, team_scores, game_results)
    write_markdown(data, player_stats, team_scores, game_results)
