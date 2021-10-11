# LuxPollen
Predicting pollen concentration in Luxembourg from past pollen and weather data.

The repo contains 2 Notebooks:
- LuxPollen_Data_loading.ipynb
    We perform the data collection via scraping of the website pollen.lu for the pollen data, and direct load from data.public.lu for weather data
    We then save the merged data into a csv file 'data.csv'
    See the 'Conclusion and next steps' section for considerations on how to improve the data set and collection process

- LuxPollen_Data_analysis_with_historical_regression.ipynb
    We perform the data visualization and analysis, and apply Historical Linear Regression functional model on the temperature to predict birch pollen concentration
    See the 'Conclusion and next steps' section for considerations on how to improve the model, including adding features, dimensionality reduction and references
    
The repo also contains 1 csv file:
- data.csv
    Data collected in the first notebook
    Contains header, date format YYYY-MM-DD, comma separated
    
Thanks for reading and please take some time to send me your feedback!
