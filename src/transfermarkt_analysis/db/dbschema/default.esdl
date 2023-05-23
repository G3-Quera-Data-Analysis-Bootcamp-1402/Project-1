module default {
  scalar type Foot extending enum<right, left>;

  abstract type Named {
    required property name -> str {
      constraint max_len_value(64);
    }
  }

  type Player extending Named {
    required property date_of_birth -> duration; 
    required property height -> int16;
    required property citizenship -> str {
      constraint max_len_value(32);
    }
    required property foot -> Foot;
  }

  type League extending Named {
    property uefa_coefficient -> int32;
  }

  type Team extending Named;

  type Season extending Named;

  type MarketValue {
    required link player -> Player;
    required link season -> Season;
    required property market_value -> int32;
  }

  type Contract {
    required link player -> Player;
    required link season -> Season;
    required link left_team -> Team;
    required link joined_team -> Team;
    required property date -> cal::local_date;
    required property fee_of_transfer -> int32;
  }

  type PlayerAppearance {
    required link player -> Player;
    required link team -> Team;
    required link league_match -> LeagueMatch;
    required property minutes_played -> int16;
    required property on_the_bench -> bool;
    required property position_code -> str {
      constraint max_len_value(4);
    }
    required property position_name -> str {
      constraint max_len_value(32);
    }
    property starter -> bool;
    property subtitute_on -> int16;
    property subtitute_off -> int16;
    property injured -> str {
      constraint max_len_value(32);
    }
    property captain -> bool;
    property num_of_goals -> int16;
    property num_of_assits -> int16;
    property num_of_owngoals -> int16;
    property yellow_card_time -> int16;
    property second_yellow_card_time -> int16;
    property red_card_time -> int16;
  }

  type TeamAppearance {
    required link team -> Team;
    required link league -> League;
    property national_team_players -> int16;
    property team_income_fee -> int32;
    property team_expenditure_fee -> int32;
    property overall_balance_fee -> int32;
  }

  type LeagueMatch {
    required link season -> Season;
    required link league -> League;
    required link home_team -> Team;
    required link away_team -> Team;
    required property match_day -> int16;
    required property home_team_goals -> int16;
    required property away_team_goals -> int16;
    required property home_team_win -> bool;
    required property away_team_win -> bool;
    required property draw -> bool;
  }

  type Goal {
    required link league_match -> LeagueMatch;
    required link scorred_player -> Player;
    required link assist_player -> Player;
    required link team_scorer -> Team;
    property goal_type -> str {
      constraint max_len_value(32);
    }
  }

  type Award extending Named {
    property description -> str;
  }

  abstract type BaseAwardWinner {
    required link award -> Award;
    required link season -> Season;
  }

  type AwardWinner extending BaseAwardWinner {
    required link player -> Player;
  }

  type AwardWinnerTeam extending BaseAwardWinner {
    required link team -> Team;
  }

}
