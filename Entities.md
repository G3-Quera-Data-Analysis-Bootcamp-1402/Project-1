# Data: Big 5 European Leagues

## Tables

### Players

- Player_ID
- Date_of_birth
- Place_of_birth
- Age (can be Dynamic?)
- Height
- Weight (!!!)
- Citizenship
- position
- foot
- agent
- Current_Cotract_ID
- Joined
- contract_expires
- contract_option
- outfitter
- Current_Club
- Team_ID
- Social_Media

### League

- League_ID
- League_Name
- UEFA_coefficient
- Recod_holding_Champion

### Teams

- Team_ID
- Team_name
- League_level
- Table_Position
- In_league_since
- Squad_size
- Average_age
- Foreigners
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

### Player_appearances

- Match_ID
- Team_ID
- Player_ID
- Shirt_Number
- Starter (boolean and optional)
- Substitute_on
- Substitute_off
- Minutes_played
- On_the_bench (boolean)
- Injured (type of injury)
- Position
- captain
- Num_of_Goals
- Num_of_Assists
- Num_of_Owngoals
- Yellow_Card_Time
- Second_Yellow_Card_Time
- Red_Card_Time

### Match (?)

- Match_ID
- League_ID
- Home_Team_ID
- Away_team_ID
- Date
- Result
- Home_Team_Goals
- Away_Team_Goals
- Stadium
- Attendence

### Goals (?)

- Match_ID
- Scorrer_ID
- Assist_ID
- Time
- Team_Reciver_Goal
- Match_period (?)

### Awards

- Award_ID
- Award_name
- Award_description

### Award_Winners

- Award_ID
- Player_ID

## Relationships

