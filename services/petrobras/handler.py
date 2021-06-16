def get_available_increments():
    return [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]

def get_closest_value(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def get_first_word(value):
    return value.split(' ')[0]

def get_asset_description(dataframe, description_column, sort_by_column, how_many_rows):
    # gets the total number of rows in the dataframe
    total_rows = dataframe.count()[description_column]
    
    # retains in the dataframe only the first word of the original description
    for index, row in dataframe.iterrows():
        dataframe.at[index, description_column] = get_first_word(row[description_column])
    
    # sorts the dataframe by the requested column and retrieves only the unique values
    assets = dataframe.sort_values([sort_by_column], ascending=False)[description_column].unique()
    
    # stores the amount of unique rows found in the dataframe
    unique_rows = len(assets)
    
    # retrieves only the first n rows specified in the "how_many_rows" argument
    if unique_rows > how_many_rows:
        assets = assets[0:how_many_rows]
    
    # concatenates all the rows into a single description separated by commas
    asset_description = ''
    for asset in assets:
        asset_description = asset_description + asset + ', '
    
    # removes the trailing comma from the description
    asset_description = asset_description[0: len(asset_description) - 2]
    
    # if the asset contains more products than shown, adds "and more"
    if unique_rows > how_many_rows:
        asset_description = asset_description + ' e outros'

    # converts to uppercase
    asset_description = asset_description.upper()

    # limits the description to 225 characters
    asset_description = asset_description[0:225]

    return asset_description