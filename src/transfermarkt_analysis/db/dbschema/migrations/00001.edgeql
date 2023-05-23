CREATE MIGRATION m15rgjtpu36prytkgfffinwx6ihsoemq2kzdldrgyy3jkh3cgtnpoa
    ONTO initial
{
  CREATE FUTURE nonrecursive_access_policies;
  CREATE ABSTRACT TYPE default::Named {
      CREATE REQUIRED PROPERTY name -> std::str {
          CREATE CONSTRAINT std::max_len_value(64);
      };
  };
  CREATE TYPE default::Award EXTENDING default::Named {
      CREATE PROPERTY description -> std::str;
  };
  CREATE TYPE default::Season EXTENDING default::Named;
  CREATE ABSTRACT TYPE default::BaseAwardWinner {
      CREATE REQUIRED LINK award -> default::Award;
      CREATE REQUIRED LINK season -> default::Season;
  };
  CREATE SCALAR TYPE default::Foot EXTENDING enum<right, left>;
  CREATE TYPE default::Player EXTENDING default::Named {
      CREATE REQUIRED PROPERTY citizenship -> std::str {
          CREATE CONSTRAINT std::max_len_value(32);
      };
      CREATE REQUIRED PROPERTY date_of_birth -> std::duration;
      CREATE REQUIRED PROPERTY foot -> default::Foot;
      CREATE REQUIRED PROPERTY height -> std::int16;
  };
  CREATE TYPE default::AwardWinner EXTENDING default::BaseAwardWinner {
      CREATE REQUIRED LINK player -> default::Player;
  };
  CREATE TYPE default::Team EXTENDING default::Named;
  CREATE TYPE default::AwardWinnerTeam EXTENDING default::BaseAwardWinner {
      CREATE REQUIRED LINK team -> default::Team;
  };
  CREATE TYPE default::Contract {
      CREATE REQUIRED LINK joined_team -> default::Team;
      CREATE REQUIRED LINK left_team -> default::Team;
      CREATE REQUIRED LINK player -> default::Player;
      CREATE REQUIRED LINK season -> default::Season;
      CREATE REQUIRED PROPERTY date -> cal::local_date;
      CREATE REQUIRED PROPERTY fee_of_transfer -> std::int32;
  };
  CREATE TYPE default::League EXTENDING default::Named {
      CREATE PROPERTY uefa_coefficient -> std::int32;
  };
  CREATE TYPE default::LeagueMatch {
      CREATE REQUIRED LINK league -> default::League;
      CREATE REQUIRED LINK away_team -> default::Team;
      CREATE REQUIRED LINK home_team -> default::Team;
      CREATE REQUIRED LINK season -> default::Season;
      CREATE REQUIRED PROPERTY away_team_goals -> std::int16;
      CREATE REQUIRED PROPERTY away_team_win -> std::bool;
      CREATE REQUIRED PROPERTY draw -> std::bool;
      CREATE REQUIRED PROPERTY home_team_goals -> std::int16;
      CREATE REQUIRED PROPERTY home_team_win -> std::bool;
      CREATE REQUIRED PROPERTY match_day -> std::int16;
  };
  CREATE TYPE default::Goal {
      CREATE REQUIRED LINK assist_player -> default::Player;
      CREATE REQUIRED LINK league_match -> default::LeagueMatch;
      CREATE REQUIRED LINK scorred_player -> default::Player;
      CREATE REQUIRED LINK team_scorer -> default::Team;
      CREATE PROPERTY goal_type -> std::str {
          CREATE CONSTRAINT std::max_len_value(32);
      };
  };
  CREATE TYPE default::TeamAppearance {
      CREATE REQUIRED LINK league -> default::League;
      CREATE REQUIRED LINK team -> default::Team;
      CREATE PROPERTY national_team_players -> std::int16;
      CREATE PROPERTY overall_balance_fee -> std::int32;
      CREATE PROPERTY team_expenditure_fee -> std::int32;
      CREATE PROPERTY team_income_fee -> std::int32;
  };
  CREATE TYPE default::PlayerAppearance {
      CREATE REQUIRED LINK league_match -> default::LeagueMatch;
      CREATE REQUIRED LINK player -> default::Player;
      CREATE REQUIRED LINK team -> default::Team;
      CREATE PROPERTY captain -> std::bool;
      CREATE PROPERTY injured -> std::str {
          CREATE CONSTRAINT std::max_len_value(32);
      };
      CREATE REQUIRED PROPERTY minutes_played -> std::int16;
      CREATE PROPERTY num_of_assits -> std::int16;
      CREATE PROPERTY num_of_goals -> std::int16;
      CREATE PROPERTY num_of_owngoals -> std::int16;
      CREATE REQUIRED PROPERTY on_the_bench -> std::bool;
      CREATE REQUIRED PROPERTY position_code -> std::str {
          CREATE CONSTRAINT std::max_len_value(4);
      };
      CREATE REQUIRED PROPERTY position_name -> std::str {
          CREATE CONSTRAINT std::max_len_value(32);
      };
      CREATE PROPERTY red_card_time -> std::int16;
      CREATE PROPERTY second_yellow_card_time -> std::int16;
      CREATE PROPERTY starter -> std::bool;
      CREATE PROPERTY subtitute_off -> std::int16;
      CREATE PROPERTY subtitute_on -> std::int16;
      CREATE PROPERTY yellow_card_time -> std::int16;
  };
  CREATE TYPE default::MarketValue {
      CREATE REQUIRED LINK player -> default::Player;
      CREATE REQUIRED LINK season -> default::Season;
      CREATE REQUIRED PROPERTY market_value -> std::int32;
  };
};
