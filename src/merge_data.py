import pandas as pd

REPORTS_PATH = 'data/match_reports.csv'
RESULTS_PATH = 'data/match_results.csv'
MERGED_PATH = 'data/merged_data.csv'

def merge_dfs(df_reports, df_results):
    """Merge .csv files into one .csv file with all of the needed data 

    Arguments:
        match_reports: The list of match reports 
    """
    # Create match keys for each of the matches, example: Liverpool_United
    df_reports['match_key'] = df_reports.apply(lambda x: '_'.join(sorted([x['Team_1'], x['Team_2']])), axis=1)
    df_results['match_key'] = df_results.apply(lambda x: '_'.join(sorted([x['Home_Team'], x['Away_Team']])), axis=1)

    # Merge the datasets by matching the match keys 
    df_merged = pd.merge(df_reports, df_results, on='match_key')

    # Removes the unneccesary columns 'Team_1' and 'Team_2' and the no longer needed column 'match_key'
    df_cropped = df_merged.drop(columns=['Team_1', 'Team_2', 'match_key'])

    # Rearranges the columns to the wanted format
    column_order = ["Home_Team", "Home_Score", "Away_Team", "Away_Score", "Headline", "URL", "Date", "Article"]
    df_rearranged = df_cropped[column_order]

    return df_rearranged

def create_csv(df_merged):
    """Save the merged .csv files as a .csv file

    Arguments:
        df_merged: The merged .csv file
    """
    df_merged.to_csv(MERGED_PATH, index=False)

df_reports = pd.read_csv(REPORTS_PATH)
df_results = pd.read_csv(RESULTS_PATH)

df_merged = merge_dfs(df_reports, df_results)

create_csv(df_merged)