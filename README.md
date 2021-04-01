# Visualizing the Geographical Data of Singapore

 A data science project to visualize the various Planning Areas of Singapore as drawn by the Urban Redevelopment Authority of Singapore.

 This project serves as a "starter dashboard" that will allow various datasets to be plotted against it for use as a Business Intelligence tool.

 As I am currently an employee of Koufu, the dashboard will render the location of outlets belonging to the organization. Only publicly available information will be used in this project.

 The link to the dashboard (not optimized for mobile devices) can be found here:
 > <https://koufu-sg-map.herokuapp.com/>

The project is broken down into the following components:

## Initial collection of raw data

- `r_outletsdata.py` is used to collect existing outlets and their brands from [the company website](https://www.koufu.com.sg/our-brands/food-halls/). Returns a csv file that can be found in the data folder and can be reused.
- `r_boundarydata.py` is used to generate a GeoJSON file from [data.gov.sg](https://data.gov.sg/dataset/master-plan-2019-subzone-boundary-no-sea). URL in the script is hard-coded because of extraction logic. Boundary data is unlikely to change often so this is not an issue for now.
- `r_demographics.py` collects information from [singstat.gov](https://www.singstat.gov.sg/find-data/search-by-theme/population/geographic-distribution/latest-data) and filters for 2020 data.

## Pre-processing of data

- `r2_cleanboundary.py` took the raw GeoJSON file and appended 3 additional columns:
  - **Area** of each subzone in km2. Calculated using geopandas with epsg set to 6933. To ensure accuracy of the algorithm, I compared the output to the data found in [citypopulation.de](https://www.citypopulation.de/en/singapore/admin/).
  - **Population** data from the demographics set. If I intend to analyze more years than 1 singular year, the processing has to be done differently.
  - **Population Density** calculated by dividing population by area. Casted to integer because that level of specificity doesn't add value to the conversation.
- `r2_outletgeocode.py` utilizes Google Places API to append latitude-longitude data for use in map plotting.
  - Extra care had to be taken to ensure that lat-lng returned was accurate. However, repeated querying of the API could lead to unexpected costs. Therefore `r2a_outletgeocode.py` was used as an intermediate step in additional data cleaning.
  - `r2b_outletgeocode.py` was the final step in cleaning the outlet data. It used their retrieved coordinates and matched it against the geometry shapes found in `r2_cleanboundary.py` and returned a final csv file.

## Visualizations

- `helper_drawmap.py` was used to create the map.html found in the root folder. Some notes:
  - Low-population density (<2500) regions had a side effect of making the choropleth overloaded with information. As a result, I applied a filter against these regions, effectively turning them "null" for the purposes of analysis.
  - Various methods were explored in trying to make the outlet markers on the map visually distinctive (too much information is no information at all), finally settling on a crude colored icon with the brand's initials.
  - An initial filter of a few choice brands was also applied to ensure that the consumer would not be overwhelmed by the information presented on the map.
- `helper_drawtable.py` does some simple dataframe transformations for use in the dashboard.

## Publishing of App

- `app.py` was my first foray into open-sourced dashboarding using Plotly's Dash and combines the visualizations generated in the previous section. Some additional conditional formatting had to be applied to the table to improve information transfer.

## Discussion (you can skip this if you're just here for the code)

### Future Work

- Appending sales data will allow us to observe as a standardized metric the performance of each outlet (sales per population density) within their zones.
- Appending age-distribution will allow us to identify the zone's suitability for some of our other concept brands.

### Limitations

- If you're currently living in Singapore, you might have noticed that I've only used the population data of people living in HDBs. Future work can possibly include foot traffic in commercial/industrial zones (e.g. Downtown Core), although an open discussion should be had on how best to combine these two distinct datasets together (employees go home at the end of the day, so how do we combine worker population data with residential population data cleanly?)

### Reflection

I started this project with the goal of doing a full-stack(-ish) data-science project from the collection of data to the delivery of the final product to the most important customer: the business manager who will actually use that information.

I was particularly interested in the Extraction and Transformation (of data) portion of the project. Most course materials provide readily available datasets and we know that this is rarely the case in the real world.

If you dig deeper into my code you will find that I've tried my best to make my processing functions as isolated from each other as possible to allow for easy trouble-shooting.

I've come a long way in terms of structuring my project folder (from a loose assortment of variables in 1 single Jupyter Notebook) to scripts that are able to reference one another to keep the code base clean. Comments and feedback on how the code and structure can be improved are welcome.

Finally, I started thinking about the best way to deliver the information I had collected to the stakeholder to whom it mattered the most. I initially started off waving the map.html file around at my bosses, quickly realizing that people stop paying attention the moment they had to take more than 1 minute to digest and understand the information.

So down a rabbithole I went, trying to find the best way to deliver information. I considered Jupyter Notebooks (but if it's going to end up showing code, it's going to confuse some people) to linking up my datasets to Google's Data Studio and just producing a pdf report (but no interactivity!). I finally discovered Heroku and Dash, and after many painful hours I'm pleased to say that I've figured out how to get a basic web-based dashboard up and running.

So yes, my first ever dashboard. I'll continue working on improving some features (and with any luck, I'll look back on the code here in a year and think "who the hell wrote this, it's trash").
