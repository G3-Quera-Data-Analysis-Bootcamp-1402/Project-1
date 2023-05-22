# Data: Big 5 European Leagues

## Tables

### Players

- Player_ID
- Date_of_birth
- Place_of_birth
- Age (can be Dynamic?)
- Height
- Citizenship
- foot
- agent
- outfitter
- Social_Media

### League

- League_ID
- League_Name
- UEFA_coefficient
- Record_holding_Champion

### Teams

- Team_ID
- Team_name
- League_level
- Table_Position
- In_league_since
- National_team_players
- Stadium
- Current_transfer_record
- Club_Awards

### Market_value

- Player_ID
- Season_ID
- Market_value

### Contract (Transfer)

- Contract_ID
- Player_ID
- Season_ID
- Date
- Left_team
- Joined_Team
- Fee_of_Transfer
- Contract_Length
- Contract_Type (Loan, Hamishegi)

### Player_appearances

- Match_ID
- Team_ID
- Player_ID
- Shirt_Number
- Starter (boolean and optional)
- Substitute_on
- Substitute_off (nollable
- Minutes_played
- On_the_bench (boolean)
- Injured (type of injury)
- Position_Code
- Postion_Name
- captain
- Num_of_Goals
- Num_of_Assists
- Num_of_Owngoals
- Yellow_Card_Time
- Second_Yellow_Card_Time
- Red_Card_Time

### Match

- Match_ID
- Season_ID
- League_ID
- Home_Team_ID
- Away_team_ID
- Date
- Stadium
- Attendence
- Match_Day
- Referee
- Result
- Home_Team_Goals
- Away_Team_Goals
- Home_team_win
- Away_Team_Win
- Draw

### Goals

- Match_ID
- Scorrer_ID
- Assist_ID
- Time
- Team_Scorer_ID
- Match_Period (?)
- Goal_Type (categical: penalty, own_goal ,...)

### Awards

- Award_ID
- Award_name
- Award_description

### Award_Winners

- Award_ID
- Season_ID
- Player_ID

### Season

- Season_ID
- Season

### We can add (Substitution and Cards Tables too)

## Relationships

