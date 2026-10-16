import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    output = pd.DataFrame(columns=["anon_id", "matched_name"])
    for i, anon_row in anon_df.iterrows():
        count = 0
        chosen_row = anon_row
        for i, row in aux_df.iterrows():
            if anon_row["age"] == row["age"] and anon_row["zip3"] == row["zip3"] and anon_row["gender"] == row["gender"]:
                chosen_row = row
                count += 1
            if count > 1: break
        if count == 1:
            anon_id = anon_row["anon_id"]
            name = chosen_row["name"]
            output.loc[len(output)] = [anon_id, name]
    return output
                


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
