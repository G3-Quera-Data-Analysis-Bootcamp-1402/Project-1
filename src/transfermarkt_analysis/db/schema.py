from enum import Enum as PyEnum
from os import getenv

import dotenv
from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer,
                        MetaData, String, Table, Text, create_engine)



__all__ = [
    "db_url",
    "FootType",
    "create_tables",
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
        Column("player_id", Integer),
        Column("player_name", String(64)),
        Column("date_of_birth", Integer),
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
        Column("team_id", Integer),
        Column("team_name", String(64)),
        Column("league_id", Integer)
    )
    # seasons table
    seasons = Table(
        "seasons",
        metadata,
        Column("season_id", Integer, primary_key=True),
    )
    # market_values table
    market_values = Table(
        "market_values",
        metadata,
        Column("player_id", Integer, nullable=True),
        Column("season_id", Integer),
        Column("market_value", Integer)
    )
    # contracts table
    contracts = Table(
        "contracts",
        metadata,
        Column("contract_id", Integer, autoincrement=True, primary_key=True),
        Column("player_id", Integer, nullable=True),
        Column("season_id", Integer, nullable=True),
        Column("left_team_id", Integer, nullable=True),
        Column("joined_team_id", Integer, nullable=True),
        Column("fee_of_transfer", Integer)
    )
    # player_appearances table
    player_appearances = Table(
        "player_appearances",
        metadata,
        Column("player_id", Integer, nullable=True),
        Column("team_id", Integer, nullable=True),
        Column("match_id", Integer, nullable=True),
        Column("season_id", Integer),
        Column("position_code", String(2)),
        Column("position_name", String(32)),
    )
    # team_appearances table
    team_appearances = Table(
        "team_appearances",
        metadata,
        Column("team_id", Integer),
        Column("season_id", Integer),
        Column("league_id", Integer),
        Column("team_income_fee", Integer),
        Column("team_expenditure_fee", Integer),
    )
    # matches table
    matches = Table(
        "matches",
        metadata,
        Column("match_id", Integer),
        Column("season_id", Integer),
        Column("home_team_id", Integer),
        Column("away_team_id", Integer),
        Column("home_team", String(64)),
        Column("away_team", String(64)),
        Column("matchday", Integer),
        Column("home_team_score", Integer),
        Column("away_team_score", Integer),
        Column("home_team_win", Boolean),
        Column("away_team_win", Boolean),
        Column("draw", Boolean),
        Column("home_total_shots", Integer),
        Column("away_total_shots", Integer),
        Column("home_shots_off_target", Integer),
        Column("away_shots_off_target", Integer),
        Column("home_shots_saved", Integer),
        Column("away_shots_saved", Integer),
        Column("home_corners", Integer),
        Column("away_corners", Integer),
        Column("home_freekicks", Integer),
        Column("away_freekicks", Integer),
        Column("home_fouls", Integer),
        Column("away_fouls", Integer),
        Column("home_offsides", Integer),
        Column("away_offsides", Integer),
    )
    # goals table
    goals = Table(
        "goals",
        metadata,
        Column("match_id", Integer),
        Column("team_id", Integer),
        Column("scorrer_id", Integer),
        Column("assist_id", Integer),
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
        Column("award_id", Integer),
        Column("season_id", Integer),
        Column("player_id", Integer),
    )
    # award_winners_teams table
    award_winners_teams = Table(
        "award_winners_teams",
        metadata,
        Column("award_id", Integer),
        Column("season_id", Integer),
        Column("team_id", Integer),
    )
    # penalties table
    penalties = Table(
        "penalties",
        metadata,
        Column("match_id", Integer),
        Column("team_id", Integer),
        Column("kicker_id", Integer),
        Column("gk_id", Integer),
        Column("gk", String(64)),
        Column("kicker", String(64))
    )
    # cards table
    cards = Table(
        "cards",
        metadata,
        Column("match_id", Integer),
        Column("team_id", Integer),
        Column("player_id", Integer),
        Column("card", String(16)),
    )
    # substitutions table
    substitutions = Table(
        "substitutions",
        metadata,
        Column("match_id", Integer),
        Column("team_id", Integer),
        Column("player_in_id", Integer),
        Column("player_out_id", Integer)
    )
    # create all tables
    metadata.create_all(db_engine)