Notes

Strategy
1. read each field one by one
    all fields seem to be important

2. read summarize_compstak.py
    classifications can use improvements

3. study sales and lease dataset
    Does this dataset cover industries well?
        we can test this by no grouping in order to do this we must first take columns of interest

"What are industries that you think this covers well, and industries that this covers poorly?"
        'Property Type',
        'Property Subtype',
        'Space Type',
        'Tenant SIC Code',
        'Tenant SIC Description',
        'Tenant NAICS Code',
        'Tenant NAICS Description'

Official insutry classification codes are not avialable, it is a premium add on. Space type can aslso be useful but is only available for lease data (not sales data)
Clsffications are stbale 
 8 unique values
 56 unique values

 Available columns in Sales:
Property Type: 94.9% filled, 8 unique values
Property Subtype: 74.4% filled, 56 unique values

Available columns in Leases:
Property Type: 99.0% filled, 8 unique values
Property Subtype: 65.5% filled, 56 unique values

fill rate is concerning for sales and lease datasets

4. in order to understand its coverage we need to have a general idea of the lease and sales market to develope a benchmark

lets start big. Lets see if the number of buildings match up using property id
this is the strategy 

check the number of buildings and see if it matches up to the known number of buildings and work our way downwards by category
use Property Id to check for the building 


we study how much the data can observe. compare totla number of buildings  then compare totla number of buildings by category type. 

Total unique buildings in our dataset: 759,623
Total commercial buildings in the U.S.: 5,900,000 (https://css.umich.edu/publications/factsheets/built-environment/commercial-buildings-factsheet , university of michigan)
Our dataset represents 12.87% of all U.S. commercial buildings

there seems to be a big discrepancy with land and multi family dataset. The defintion doesnt not seem to be the issue. defintion does not seem to be the source of the problem. 

condlusion is that some idnsutries are not covered well at all. industrial office and retail are covered well the rest not so much

What are the best ways to cluster/group industries together into a smaller set of types?
the fill rate for subtypes is really bad so its best to just use the main property types depending on our needs

dataset seems to be consistent statewise
property type wise it may be inconsistent

it may be wrthwhile to use the offical NAICS SIC codes depending on needs

I also investigaed weather the number observations bias the osbervation count ehwerei the more observatons they have the more they specialized in increasingk converage and we find mild evidenec for this as show in pictures

we see inconsistent coverage geography wise ansd state wise too

I will check if the inconcistencies exist statewise and geoegraphywise at the same time


we see the property ids show consistent state code

\we realized online estimates have their limitaions therefore I gathered my own estimates from US DOE.

using these estimates I will rerun my analysis
NaN values in 'Property Type' column of compstak_df: 37020 concerining

NaN values in 'reported_propertytype' column of doe_df: 0

incosnsitent categories So i needed to make a callwhere each category falls

https://www.costar.com/about/costar-glossary