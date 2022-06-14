import pandas as pd
from pandas.api.types import is_numeric_dtype
import argparse
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

class Ranker:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.source_folder_path = kwargs['data_path']
        self.predicates_path = kwargs['predicates_path']
        
        self.compiled_file_source = pd.read_csv(self.source_folder_path)
        predicates, weights = self.parse_csv()
        self.predicates, self.weights = predicates.to_list(), weights.to_list()
        self.raw, self.ranking = self.query_rankings()

        self.raw.to_csv("Results/Individual Predicate Rankings")
        self.ranking.to_csv("Results/Overall Total Ranking")

    def parse_csv(self):
        df = pd.read_csv(self.predicates_path)
        df['Weight'] = df['Weight'].fillna(1)
        df.dropna(axis='rows', how='any', inplace=True)
        return df['Predicate'], df['Weight']

    def find_smallest(self):
        smallest = ""
        smallest_count = 10000
        for predicate in self.predicates:
            count = self.compiled_file_source.loc[self.compiled_file_source["Predicate"] == predicate].shape[0]
            if count < smallest_count and not count < 20: #THE COUNT < 20 CHECK IS A FAILSAFE DURING TEST
                smallest = predicate
                smallest_count = count
        return smallest, smallest_count

    def query_rankings(self):
        # Create a set of lists containing all applicable data to be put in a dataframe later to obtain the rankings
        get_locations_from, count = self.find_smallest()
        tmp = self.compiled_file_source.loc[self.compiled_file_source["Predicate"] == get_locations_from].copy()
        query_dataframe = tmp["Subject"].to_frame().copy()
        # Now go through all predicates and add the numerical columns
        for predicate in self.predicates:
            # Set predicate name for column naming
            col_name = predicate
            # Check whether the predicate is numerical, if not, skip
            tmp = self.compiled_file_source.loc[self.compiled_file_source["Predicate"] == predicate].copy()
            tmp.rename(columns = {'Object': col_name}, inplace = True)
            if tmp.shape[0] < count: # Temporary failsafe if column is too small
                continue
            cleaned_predicate_df = tmp.drop(["Predicate"], axis=1).copy()
            query_dataframe = query_dataframe.merge(cleaned_predicate_df, how='inner')
            # Now remove any rows containing at least one empty slot (failsafe)
            query_dataframe = query_dataframe[query_dataframe[col_name].notna()]
        # query_dataframe should now contain all >Complete< locations to be ranked
        # meaning each location has a value in all surviving numerical predicates
        # Now, rank all remaining predicates
        for predicate in query_dataframe.columns.values.tolist():
            # Skip "Subject"
            if predicate == "Subject":
                continue
            # Create a new column containing the rank for each predicate and drop the old raw data column
            query_dataframe[predicate] = query_dataframe[predicate].rank()
        # query_dataframe now contains for each subject and all provided (surviving) predicates the ranking amongst each predicate
        # Now, go through the surviving predicates and apply their weights to their ranking
        for predicate in query_dataframe.columns.values.tolist():
            # Skip "Subject"
            if predicate == "Subject":
                continue
            index = self.predicates.index(predicate)
            weight = self.weights[index]
            query_dataframe[predicate] = weight * query_dataframe[predicate]
        # Now create a final ranking consisting of the summation of all non-Subject ranks
        query_dataframe["Total_Rank"] = query_dataframe.sum(axis=1, numeric_only=True)
        # Drop the intermediate ranks for the final output
        query_ranked = query_dataframe.copy()
        for col in query_ranked.columns.values.tolist():
            if col == "Subject" or col == "Total_Rank":
                continue
            query_ranked = query_ranked.drop([col], axis=1)
        # Finally, output the subjects based on their final rank order
        query_ranked = query_ranked.sort_values("Total_Rank", ascending=True)
        query_ranked["Rank"] = query_ranked["Total_Rank"].rank()
        return query_dataframe, query_ranked

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that consumes a data source CSV and a CSV with predicates and weights and returns a weighted ranking of cities based on provided predicates.")
    parser.add_argument("data_path", type=str, help="Path to CSV file where each row is a tuple of form (City, Predicate, Value)")
    parser.add_argument("predicates_path", type=str, help="Path to CSV file where each row is a tuple of form (Predicate, Weight)")
    args = parser.parse_args()

    Ranker(**vars(args))