from enum import Enum as PyEnum
from os import getenv

import dotenv
from sqlalchemy import (TIMESTAMP, Boolean, Column, Date, Enum, ForeignKey, Integer,
                        MetaData, String, Table, Text, create_engine)



__all__ = [
    "db_url",
    "create_tables"
]


# read configuration from .env file and store it in dict
dotenv.load_dotenv()

db_conf = {
    "user": getenv("DB_USER", "root"),
    "password": getenv("DB_PASSWORD", ""),
    "host": getenv("DB_HOST", "localhost"),
    "port": getenv("DB_PORT", "3306"),
    "name": getenv("DB_NAME", "transfermarkt"),
}

db_url = f"mysql+mysqlconnector://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['name']}"

# create tables

class FootType(PyEnum):
    """
        Enum value used for players's foot column
    """
    right = "right"
    left = "left"
    both = "both"


def create_tables():
    """
    definition and creation of database tables
    """
    db_engine = create_engine(db_url)
    metadata = MetaData()
    # players table
    players = Table(
        "players", 
        metadata, 
        Column("player_id", Integer, autoincrement=True, primary_key=True),
        Column("player_name", String(64)),
        Column("date_of_birth", TIMESTAMP),
        Column("height", Integer),
        Column("citizenship", String(32)),
        Column("foot", Enum(FootType), default=FootType.right)
    )
    # leagues table
    leagues = Table(
        "leagues",
        metadata,
        Column("league_id", Integer, autoincrement=True, primary_key=True),
        Column("league_name", String(32)),
        Column("uefa_coefficient", Integer)
    )
    # teams table
    teams = Table(
        "teams",
        metadata,
        Column("team_id", Integer, autoincrement=True, primary_key=True),
        Column("team_name", String(64))
    )
    # seasons table
    seasons = Table(
        "seasons",
        metadata,
        Column("season_id", Integer, autoincrement=True, primary_key=True),
        Column("season_name", String(8))
    )
    # market_values table
    market_values = Table(
        "market_values",
        metadata,
        Column("player_id", Integer, ForeignKey("players.player_id")),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("market_value", Integer)
    )
    # contracts table
    contracts = Table(
        "contracts",
        metadata,
        Column("contract_id", Integer, autoincrement=True, primary_key=True),
        Column("player_id", Integer, ForeignKey("players.player_id")),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("date", Date),
        Column("left_team", Integer, ForeignKey("teams.team_id")),
        Column("joined_team", Integer, ForeignKey("teams.team_id")),
        Column("fee_of_transfer", Integer)
    )
    # player_appearances table
    player_appearances = Table(
        "player_appearances",
        metadata,
        Column("player_id", Integer, ForeignKey("players.player_id")),
        Column("team_id", Integer, ForeignKey("teams.team_id")),
        Column("match_id", Integer, ForeignKey("matches.match_id")),
        Column("starter", Boolean, nullable=True),
        Column("subtitute_on", Integer, nullable=True),
        Column("subtitute_off", Integer, nullable=True),
        Column("minutes_played", Integer),
        Column("on_the_bench", Boolean),
        Column("injured", String(32), nullable=True),
        Column("position_code", String(4)),
        Column("position_name", String(32)),
        Column("captain", Boolean, nullable=True),
        Column("num_of_goals", Integer, nullable=True),
        Column("num_of_assists", Integer, nullable=True),
        Column("num_of_owngoals", Integer, nullable=True),
        Column("yellow_card_time", Integer, nullable=True),
        Column("second_yellow_card_time", Integer, nullable=True),
        Column("red_card_time", Integer, nullable=True)
    )
    # team_appearances table
    team_appearances = Table(
        "team_appearances",
        metadata,
        Column("team_id", Integer, ForeignKey("teams.team_id")),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("league_id", Integer, ForeignKey("leagues.league_id")),
        Column("national_team_players", Integer),
        Column("team_income_fee", Integer),
        Column("team_expenditure_fee", Integer),
        Column("overall_balance_fee", Integer)
    )
    # matches table
    matches = Table(
        "matches",
        metadata,
        Column("match_id", Integer, autoincrement=True, primary_key=True),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("league_id", Integer, ForeignKey("leagues.league_id")),
        Column("home_team_id", Integer, ForeignKey("teams.team_id")),
        Column("away_team_id", Integer, ForeignKey("teams.team_id")),
        Column("match_day", Integer),
        Column("home_team_goals", Integer),
        Column("away_team_goals", Integer),
        Column("home_team_win", Boolean),
        Column("away_team_win", Boolean),
        Column("draw", Boolean)
    )
    # goals table
    goals = Table(
        "goals",
        metadata,
        Column("match_id", Integer, ForeignKey("matches.match_id")),
        Column("scorred_id", Integer, ForeignKey("players.player_id")),
        Column("assist_id", Integer, ForeignKey("players.player_id")),
        Column("team_scorer_id", Integer, ForeignKey("teams.team_id")),
        Column("goal_type", String(32), nullable=True)
    )
    # awards table
    awards = Table(
        "awards",
        metadata,
        Column("award_id", Integer, autoincrement=True, primary_key=True),
        Column("award_name", String(32)),
        Column("award_description", Text)
    )
    # award_winners table
    award_winners = Table(
        "award_winners",
        metadata,
        Column("award_id", Integer, ForeignKey("awards.award_id")),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("player_id", Integer, ForeignKey("players.player_id")),
    )
    # award_winners_teams table
    award_winners_teams = Table(
        "award_winners_teams",
        metadata,
        Column("award_id", Integer, ForeignKey("awards.award_id")),
        Column("season_id", Integer, ForeignKey("seasons.season_id")),
        Column("team_id", Integer, ForeignKey("teams.team_id")),
    )
    # create all tables
    metadata.create_all(db_engine)