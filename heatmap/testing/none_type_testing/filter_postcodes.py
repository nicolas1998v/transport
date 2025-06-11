import pandas as pd

# Read the original postcodes, failed postcodes, and never works postcodes
london_df = pd.read_csv('London postcodes.csv')
failed_df = pd.read_csv('failed_postcodes.csv')
never_works_df = pd.read_csv('time_reliability_testing/analysis/never_works.csv')

# Split failed postcodes into disambiguation and None types
disambiguation_failures = failed_df[
    failed_df['reason'].str.contains('DisambiguationResult|Invalid postcode \(Disambiguation\)', na=False)
]['postcode'].tolist()

none_type_failures = failed_df[
    failed_df['reason'].str.contains('None|NoneType', na=False)
]['postcode'].tolist()

# Get list of never works postcodes
never_works = never_works_df['postcode'].tolist()

# Create filtered dataframe excluding disambiguation failures and never works postcodes
valid_postcodes_df = london_df[
    ~london_df['Postcode'].isin(disambiguation_failures) & 
    ~london_df['Postcode'].isin(never_works)
]
valid_postcodes_df.to_csv('london_postcodes_filtered.csv', index=False)

# Create dataframe of None type failures for investigation
none_type_df = london_df[london_df['Postcode'].isin(none_type_failures)]
none_type_df.to_csv('none_type_postcodes.csv', index=False)

print(f"Original postcodes: {len(london_df)}")
print(f"Disambiguation failures removed: {len(disambiguation_failures)}")
print(f"Never works postcodes removed: {len(never_works)}")
print(f"None type failures: {len(none_type_failures)}")
print(f"Remaining valid postcodes: {len(valid_postcodes_df)}") 