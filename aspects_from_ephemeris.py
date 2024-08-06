import pandas as pd

# Read the CSV files
df1 = pd.read_csv('ephemerides/ephemeris/sun.csv')
df2 = pd.read_csv('ephemerides/ephemeris/moon.csv')
df3 = pd.read_csv('ephemerides/ephemeris/mercury.csv')
df4 = pd.read_csv('ephemerides/ephemeris/venus.csv')
df5 = pd.read_csv('ephemerides/ephemeris/mars.csv')
df6 = pd.read_csv('ephemerides/ephemeris/jupiter.csv')
df7 = pd.read_csv('ephemerides/ephemeris/saturn.csv')

# Merge dataframes on 'date' and 'time'
merged_df = pd.merge(df1, df3, on=['date', 'time'], suffixes=('_sun', '_mercury'))
merged_df = pd.merge(merged_df, df2, on=['date', 'time'],suffixes=('', '_moon'))
merged_df = pd.merge(merged_df, df4, on=['date', 'time'], suffixes=('', '_venus'))
merged_df = pd.merge(merged_df, df5, on=['date', 'time'], suffixes=('', '_mars'))
merged_df = pd.merge(merged_df, df6, on=['date', 'time'], suffixes=('', '_jupiter'))
merged_df = pd.merge(merged_df, df7, on=['date', 'time'], suffixes=('', '_saturn'))

def calculate_aspect_moon_other(row,planet):
    aspect = abs(row['absolute_position'] - row[f'absolute_position_{planet}'])
    return aspect


def calculate_aspect_dynamic(row,planet1, planet2):
    aspect = abs(row[f'absolute_position_{planet1}'] - row[f'absolute_position_{planet2}'])
    return aspect

merged_df['aspect_moon_sun'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'sun'), axis=1)
merged_df['aspect_moon_mercury'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'mercury'), axis=1)
merged_df['aspect_moon_venus'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'venus'), axis=1)
merged_df['aspect_moon_mars'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'mars'), axis=1)
merged_df['aspect_moon_jupiter'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'jupiter'), axis=1)
merged_df['aspect_moon_saturn'] = merged_df.apply(lambda row:calculate_aspect_moon_other(row, 'saturn'), axis=1)

merged_df['aspect_sun_mercury'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'sun', 'mercury'), axis=1)
merged_df['aspect_sun_venus'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'sun', 'venus'), axis=1)
merged_df['aspect_sun_mars'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'sun', 'mars'), axis=1)
merged_df['aspect_sun_jupiter'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'sun', 'jupiter'), axis=1)
merged_df['aspect_sun_saturn'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'sun', 'saturn'), axis=1)

merged_df['aspect_mercury_venus'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mercury', 'venus'), axis=1)
merged_df['aspect_mercury_mars'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mercury', 'mercury'), axis=1)
merged_df['aspect_mercury_jupiter'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mercury', 'mercury'), axis=1)
merged_df['aspect_mercury_saturn'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mercury', 'mercury'), axis=1)

merged_df['aspect_venus_mars'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'venus', 'mercury'), axis=1)
merged_df['aspect_venus_jupiter'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'venus', 'mercury'), axis=1)
merged_df['aspect_venus_saturn'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'venus', 'mercury'), axis=1)

merged_df['aspect_mars_jupiter'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mars', 'mercury'), axis=1)
merged_df['aspect_mars_saturn'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'mars', 'mercury'), axis=1)

merged_df['aspect_jupiter_saturn'] = merged_df.apply(lambda row: calculate_aspect_dynamic(row, 'jupiter', 'saturn'), axis=1)

print('------------------- start -------------------')
merged_df.to_csv('ephemerides/ephemeris_aspects/aspects.csv', index=False)
print('------------------- Finished  -------------------')
