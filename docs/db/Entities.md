# Data: Big 5 European Leagues

## Tables

### Players

- Player_ID
- Date_of_birth (timesamp)
- Height (int)
- Citizenship (string)
- foot (enumerate, string)
- Place_of_birth
- agent
- outfitter
- Social_Media

### League

- League_ID
- League_Name (string)
- UEFA_coefficient
- Record_holding_Champion

### Teams

- Team_ID
- Team_name (string)
- Club_Awards
- Stadium
- In_league_since

### Market_value

- Player_ID
- Season_ID
- Market_value (integer)

### Contract (Transfer)

- Contract_ID
- Player_ID
- Season_ID
- Date (date)
- Left_team (int, id)
- Joined_Team (int, id)
- Fee_of_Transfer (int)
- Contract_Length
- Contract_Type (Categorical: Loan, Hamishegi)

### Team_appearances

- Team_ID
- Season_ID
- League_ID
- National_team_players (int)
- Team_income_fee (int)
- Team_expenditure_fee (int)
- Team_arrivals
- Team_departures

### Player_appearances

- Match_ID
- Team_ID
- Player_ID
- Starter (boolean)
- Substitute_on (int, nullable)
- Substitute_off (int, nullable)
- Minutes_played
- On_the_bench (boolean)
- Injured (type of injury) (string, nullable)
- Position_Code (string)
- Postion_Name (string)
- captain (boolean, nullable)
- Num_of_Goals (int, nullable)
- Num_of_Assists (int, nullable)
- Num_of_Owngoals (int, nullable)
- Yellow_Card_Time (int, nullable)
- Second_Yellow_Card_Time (int, nullable)
- Red_Card_Time (int, nullable)
- Shirt_Number

### Match

- Match_ID
- Season_ID
- League_ID
- Home_Team_ID
- Away_team_ID
- Match_Day (int)
- Home_Team_Goals (int)
- Away_Team_Goals (int)
- Home_team_win (boolean)
- Away_Team_Win (boolean)
- Draw (boolean)
- Result (string): can be derived from HTG and ATG
- Referee (string)
- Date (datetime)
- Stadium (string)
- Attendence (int)

### Goals

- Match_ID
- Scorrer_ID
- Assist_ID
- Team_Scorer_ID
- Goal_Type (categical: penalty, own_goal ,...) (string)
- Time (int)
- Match_Period (?)

### Awards

- Award_ID
- Award_name (string)
- Award_description (string)

### Award_Winners

- Award_ID
- Season_ID
- Player_ID

### Award_Winners_Teams

- Award_ID
- Season_ID
- Team_ID
- Award_Name (string)

### Season

- Season_ID
- Season (string)

### We can add (Substitution and Cards Tables too)

### Optional: National_Team Table

## Relationships

### the relationships are already implemented in DB

