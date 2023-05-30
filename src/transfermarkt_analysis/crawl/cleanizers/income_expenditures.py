import pandas as pd
import regex as re

incomes = pd.read_csv("data/team_income_expenditures.csv")
teams = pd.read_csv("data/cleanized/teams.csv")


clean_incomes = pd.DataFrame(columns = ["team_id", "season_id",\
                                         "league_id", "team_income_fee", "team_expenditure_fee", "overall_balance_fee"])

def value_cleanizer(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    cleanize column used for fee, market_value, income
    1- replace -, ? with np.nan
    2- replace leihe with loan -> 1
    3- replace leih-ende with end-loan -> -1.0
    4- replace ablösefrei with free -> 0.0
    5- replace <num>,<num> Mio with <num><num>0000.0
    6- replace <num>,<num> Tsd with <num><num>000.0
    7- replace <num>,<num> € with <num><num>
    """
    df[col] = (
        df[col]
        .mask(df[col].str.lower() == "leihe", "-1")
        .mask(df[col].str.contains("Leih-Ende"), "-2")
        .mask(df[col].str.contains("ablösefrei"), "0")
        .apply(
            lambda x: ",".join(re.findall(r"\d+", x)).replace(",", "") + "0000"
            if "Mio" in x
            else x
        )
        .apply(lambda x: "".join(re.findall(r"\d+", x)) + "000" if "Tsd" in x else x)
        .apply(lambda x: "".join(re.findall(r"\d+", x)) if "€" in x else x)
        .mask(df[col].isin(["-", "?", "draft"]), "-3")
        .astype("int")
    )
    return df

incomes.replace("Einnahmen: 0", "0 €", inplace= True)
incomes.replace("Ausgaben: 0", "0 €", inplace= True)
incomes = value_cleanizer(value_cleanizer(incomes, "income"),"expenditure")

for row in incomes.itertuples():
    try:
        team_id = teams[teams["team_name"] == row[3]]["team_id"].iat[0]
        league_id = teams[teams["team_name"] == row[3]]["league_id"].iat[0]
    except:
        continue
    season_id = int(str(row[2])[:4])
    team_income_fee = row[4]
    team_expenditure_fee = row[5]
    overall_balance_fee = team_income_fee - team_expenditure_fee
    clean_incomes.loc[len(clean_incomes)] = {"team_id":team_id, "season_id":season_id,\
                                            "league_id":league_id, "team_income_fee":team_income_fee,\
                                            "team_expenditure_fee":team_expenditure_fee,\
                                            "overall_balance_fee":overall_balance_fee}

clean_incomes.reset_index(inplace= True, drop= True)
clean_incomes.to_csv("data/cleanized/team_income_expenditures.csv")
