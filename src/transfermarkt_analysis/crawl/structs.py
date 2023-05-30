from collections import defaultdict
from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchGoal:
    match_id: str = None
    scorrer_id: str = None
    scorrer: str = None
    goal_type: str = None
    assist_id: str = None
    assist: str = None


@dataclass
class MatchSubstitute:
    match_id: str = None
    player_in_id: str = None
    player_in: str = None
    player_out_id: str = None
    player_out: str = None


@dataclass
class MatchCard:
    match_id: str = None
    player_id: str = None
    player: str = None
    card: str = None


@dataclass
class MatchStatistics:
    home_total_shots: str = None
    away_total_shots: str = None
    home_shots_off_target: str = None
    away_shots_off_target: str = None
    home_shots_saved: str = None
    away_shots_saved: str = None
    home_corners: str = None
    away_corners: str = None
    home_freekicks: str = None
    away_freekicks: str = None
    home_fouls: str = None
    away_fouls: str = None
    home_offsides: str = None
    away_offsides: str = None


@dataclass
class Match:
    match_id: str = None
    home_team_id: str = None
    away_team_id: str = None
    home_team: str = None
    away_team: str = None
    result: str = None
    matchday: str = None
    match_date: str = None
    home_goals: List[MatchGoal] = field(default_factory=list)
    away_goals: List[MatchGoal] = field(default_factory=list)
    home_substitutions: MatchSubstitute = field(
        default_factory=list
    )
    away_substitutions: MatchSubstitute = field(
        default_factory=list
    )
    home_cards: List[MatchCard] = field(default_factory=list)
    away_cards: List[MatchCard] = field(default_factory=list)
    statistics: MatchStatistics = field(
        default_factory=defaultdict(MatchStatistics)
    )


@dataclass
class MatchPlayer:
    match_id: str = None
    team_id: str = None
    player_id: str = None
    player: str = None


@dataclass
class MatchPenalty:
    match_id: str = None
    team_id: str = None
    kicker_id: str = None
    gk_id: str = None
    gk: str = None
    kicker: str = None


@dataclass
class MatchPlayersPenalties:
    match_id: str = None
    players: List[MatchPlayer] = field(default_factory=list)
    penalties: List[MatchPenalty] = field(default_factory=list)