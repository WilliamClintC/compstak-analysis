import pandas as pd
import numpy as np

#test

# Set paths here
path = ''
path_census = ''

# Load the data
sales = pd.read_csv(path + 'university-of-british-columbia-sales-2025-04-02.csv')
leases = pd.read_csv(path + 'university-of-british-columbia-leases-2025-04-02.csv')

###################################
# Summarize categorical variables #
###################################

# Group by prop subtype and size, and sort
sales_summary = sales.groupby(['Property Subtype']).size().reset_index(name='Count')

# Manual labels for subtypes -> categories
property_subtype_warehouse = ['Warehouse/Distribution']
property_subtype_manuf = ['Manufacturing', 'Light Industrial', 'Heavy Industrial', 'Life Science/Lab', 'Flex/R&D', 'Processing']
property_subtype_retail = ['General Retail', 'Super-Regional Center/Mall', 'Convenience/Strip Center', 'Neighborhood Shopping Center', 'Shopping Centers', 'Street Retail/Storefront', 'Community Shopping Center' ]

categories = [property_subtype_warehouse, property_subtype_manuf, property_subtype_retail]

# Create map from property_subtype to my categories
subtypes = sales['Property Subtype'].unique()
subtypes_df = pd.DataFrame(subtypes, columns=['Property Subtype'])
subtypes_df['Category_Industry'] = np.nan
for i, subtype in enumerate(subtypes):
    if subtype in property_subtype_warehouse:
        subtypes_df.at[i, 'Category_Industry'] = 'Warehouse/Distribution'
    elif subtype in property_subtype_manuf:
        subtypes_df.at[i, 'Category_Industry'] = 'Manufacturing'
    elif subtype in property_subtype_retail:
        subtypes_df.at[i, 'Category_Industry'] = 'Retail'
    else:
        subtypes_df.at[i, 'Category_Industry'] = 'Other'

# Merge Category back onto sales and leases
sales = sales.merge(subtypes_df, on='Property Subtype', how='left')
leases = leases.merge(subtypes_df, on='Property Subtype', how='left')

# summarize_property_data: summarize sales and leases by property subtype

def summarize_property_data(sales, leases, subtype_list):
    # Quantify number of sales/lease observations of this subtype
    sales_subtype = sales[sales['Property Subtype'].isin(subtype_list)]
    leases_subtype = leases[leases['Property Subtype'].isin(subtype_list)]

    # Count the number of observations
    sales_count = sales_subtype.shape[0]
    leases_count = leases_subtype.shape[0]

    # Count number of unique street address / city / state combinations among sales and leases
    sales_unique = sales_subtype[['Street Address', 'City', 'State']].drop_duplicates()
    leases_unique = leases_subtype[['Street Address', 'City', 'State']].drop_duplicates()
    sales_unique_count = sales_unique.shape[0]
    leases_unique_count = leases_unique.shape[0]

    # Filter for our INRIX sample: CA, AZ, UT, NV, and our subtype
    state_filter = ['CA', 'AZ', 'UT', 'NV']

    # Filter the sales and leases dataframes
    sales_filtered = sales_subtype[sales_subtype['State'].isin(state_filter)]
    leases_filtered = leases_subtype[leases_subtype['State'].isin(state_filter)]

    # Count the number of observations in the filtered dataframes
    sales_filtered_count = sales_filtered.shape[0]
    leases_filtered_count = leases_filtered.shape[0]

    # Count the number of unique street address / city / state combinations in the filtered dataframes
    sales_filtered_unique = sales_filtered[['Street Address', 'City', 'State']].drop_duplicates()
    leases_filtered_unique = leases_filtered[['Street Address', 'City', 'State']].drop_duplicates()

    sales_filtered_unique_count = sales_filtered_unique.shape[0]
    leases_filtered_unique_count = leases_filtered_unique.shape[0]

    # Format all the counts into one table
    count_table = pd.DataFrame({
        'Category': ['Sales', 'Leases'],
        'Total Count': [sales_count, leases_count],
        'Unique Addr': [sales_unique_count, leases_unique_count],
        '4-State Count': [sales_filtered_count, leases_filtered_count],
        '4-State Unique Addr': [sales_filtered_unique_count, leases_filtered_unique_count]
    })

    return count_table

tables = [summarize_property_data(sales, leases, subtypelist) for subtypelist in categories]

# Format all the tables into one big table, with a "category" column
summary_table = pd.concat(tables, keys=['Warehouse/Distribution', 'Manufacturing', 'Retail'], names=['Property Subtype', 'Category'])
summary_table = summary_table.reset_index(level=0)
summary_table = summary_table.rename(columns={'level_1': 'Category'})

# Write to file
summary_file_path = path + 'tables/compstak_summary_table.tex'
summary_table.to_latex(summary_file_path, index=False, float_format="%.0f", escape=False)

#######################
# Geographic Coverage #
#######################

# We're going to summarize geographic coverage by ZCTA

# split "Geo Point" column into lat/lon
sales[['Latitude', 'Longitude']] = sales['Geo Point'].str.split(' ', expand=True)
leases[['Latitude', 'Longitude']] = leases['Geo Point'].str.split(' ', expand=True)
for df in [sales, leases]:
    for var in ['Latitude', 'Longitude']:
        df[var] = df[var].str.strip()
        df[var] = pd.to_numeric(df[var], errors='coerce')
        df[var] = df[var].fillna(0)

# Filter by Category_Industry, and take unique lat/lon values
all_addr = pd.concat([sales, leases])

locations = {}
for category in ['Warehouse/Distribution', 'Manufacturing', 'Retail']:
    mask = (all_addr['Category_Industry'] == category) & (all_addr.State.isin(['CA', 'AZ', 'UT', 'NV']))
    locations[category] = all_addr[mask][['Latitude', 'Longitude']].drop_duplicates()
    locations[category] = locations[category].reset_index(drop=True)

# Load state shape files
import geopandas as gpd


state_shapefile_path = path_census + 'cb_2018_us_state_5m/cb_2018_us_state_5m.shp'
state_shapes = gpd.read_file(state_shapefile_path)

color_map = {
    'Warehouse/Distribution': 'blue',
    'Manufacturing': 'green',
    'Retail': 'orange'
}

# Plot 4 states
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(30, 30))

# Create geodataframe of the locations in each category
for category, loc in locations.items():
    loc_gdf = gpd.GeoDataFrame(loc, geometry=gpd.points_from_xy(loc['Longitude'], loc['Latitude']))
    loc_gdf.crs = 'EPSG:4326'  # Set the coordinate reference system to WGS84
    loc_gdf = loc_gdf.to_crs(state_shapes.crs)  # Convert to the same CRS as the state shapes

    ax = axes[0] if category == 'Warehouse/Distribution' else axes[1] if category == 'Manufacturing' else axes[2]
    ax.set_title(category)
    ax.set_xlim([-127, -108])
    ax.set_ylim([31, 43])

    state_shapes[state_shapes['STUSPS'].isin(['CA', 'AZ', 'UT', 'NV'])].plot(ax=ax, color='lightgray', edgecolor='black')

    loc_gdf.plot(ax=ax, marker='o', color=color_map[category], 
                 markersize=1, 
                 label=category,
                 alpha=0.5)

fig.savefig(path + 'plots/compstak_geographic_coverage.png', dpi=300, bbox_inches='tight')