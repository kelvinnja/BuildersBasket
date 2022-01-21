import streamlit as st
import pickle
import pandas as pd

hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.set_page_config(page_title="Builders Basket", page_icon=":house_buildings:")
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title('Builders Basket - Nairobi')
st.markdown('<style>h1{color: darkgreen;}</style>', unsafe_allow_html=True)

st.sidebar.header('About')
st.sidebar.info("""This project uses the data collected (Web Scrapped) from a website that list the houses for sale in Kenya, 
and employs machine learning to predict the price of a house given its neighborhood, plot size, number of bedrooms and bathrooms, etc.""")
st.sidebar.header('Info')
st.sidebar.info("""Kelvin Kahura Njau  \n Computer Science Student \n Email: kelvin.njau@strathmore.edu  \n Tel: +254748172058""")
     
def predict(features):
    with open('nairobi houses model.sav', 'rb') as saved_model:
         model = pickle.load(saved_model)
         price = model.predict(features)
    return price

neighborhoods = ['','Kibra','Ruaraka','Imaradaima','Jogooroad','Dagoretti','Komarock','Ngongroad','Muthaiga','Langata',
                 'Ngara','Uthiru','Ruai','Kahawa','Karen','Kasarani','Kariobangi','Kilimani',
                 'Mathare','Ngumo','Kinoo','Gigiri','Makadara','Westlands','Kawangware','Umoja','Githurai44']
neighborhood = st.selectbox('Choose the Neighborhood',neighborhoods)
plotsize = ['','300 - 400', '400 - 500', '500 - 600', '700 - 800', '800 - 900', '900+']
plotsizes = st.selectbox('Choose the plotsize in sqm', plotsize)
bedrooms = st.slider('Select the number of bedrooms',3,5)
bathrooms = st.slider('Select the number of bathrooms',1,4)
parking = st.checkbox('Check if has parking')
wardrobes = st.checkbox('Check if has built-in wardrobes')
cabinets = st.checkbox('Check if has kitchen with cabinets')
balcony = st.checkbox('Check if has balcony')
boys_quarters = st.checkbox("Check if has boys' quarter/annex")
col1, col2, col3 = st.beta_columns(3)
predict_button = col2.button('Predict')
prediction_space = st.empty()
 
def prepare_predictors():
    selected_features = ['Bedrooms', 'Bathrooms', 'Wardrobes_No', 'Cabinets_No',
    'Balcony_No', 'Parking_No', 'Quarters_No', 'Neighborhood_Kibra', 'Neighborhood_Ruaraka',
    'Neighborhood_Imaradaima/Jogooroad', 'Neighborhood_Dagoretti', 'Neighborhood_Komarock',
     'Neighborhood_Ngongroad/Muthaiga/Langata', 'Neighborhood_Ngara', 'Neighborhood_Uthiru',
     'Neighborhood_Ruai', 'Neighborhood_Kahawa', 'Neighborhood_Karen', 'Neighborhood_Kasarani',
     'Neighborhood_Kariobangi', 'Neighborhood_Kilimani', 'Neighborhood_Mathare', 'Neighborhood_Kinoo',
     'Neighborhood_Gigiri', 'Neighborhood_Makadara', 'Neighborhood_Westlands', 'Neighborhood_Kawangware',
     'Neighborhood_Umoja', 'Plot Category_2', 'Plot Category_3', 'Plot Category_4', 'Plot Category_5',
     'Plot Category_6', 'Plot Category_7']
     
    predictors = {}
    for feature in selected_features:
        predictors[feature] = [0]
    predictors = pd.DataFrame(predictors)
    
    #Bedrooms & Bathrooms
    predictors['Bedrooms'] = bedrooms
    predictors['Bathrooms'] = bathrooms
    
    #Neighboorhood
    for column in predictors.columns:
        if column.find(neighborhood) != -1:
            predictors[column]=1
    
    #Plot Size
    if plotsizes == '400 - 500':
        predictors['Plot Category_2'] = 1
    
    elif plotsizes == '500 - 600':
        predictors['Plot Category_3'] = 1
    
    elif plotsizes == '600 - 700':
        predictors['Plot Category_4'] = 1
    
    elif plotsizes == '700 - 800':
        predictors['Plot Category_5'] = 1
    
    elif plotsizes == '800 - 900':
        predictors['Plot Category_6'] = 1
    
    elif plotsizes == '900+':
        predictors['Plot Category_7'] = 1
        
    #Parking
    if not parking:
        predictors['Parking_No'] = 1
    
    #Wardrobes
    if not wardrobes:
        predictors['Wardrobes_No'] = 1
        
    #Kitchen with Cabinets
    if cabinets:
        predictors['Cabinets_No'] = 1
    
    #Balcony
    if not balcony:
        predictors['Balcony_No'] = 1
        
    #Quarters
    if not boys_quarters:
        predictors['Quarters_No'] = 1
    
    return predictors

if predict_button:
    if (neighborhood == '') | (plotsizes == ''):
        st.error('Please select the neighborhood and the plotsize!')
    else:
        with st.spinner('Please wait. Predicting ...'):            
            predictors = prepare_predictors()
            predicted_price = round(predict(predictors)[0], -6)
            prediction_space.header(f'The predicted price is {int(predicted_price):,} Rwf')
 
st.write('#')
disclaimer = st.beta_expander('Details & Disclaimer!')
#disclaimer.markdown("""  :warning: This project was developed for practice purposes. Due to some information 
#that would help to accurately predict the house price that were not given when listing the houses
#in the scraped data, I don't advise to consider and use the predicted prices here as ground truth!""")
#disclaimer.markdown(""" :information_source: The notebook used to for explaratory data analysis and building machine learning models can be found [here](https://github.com/nzagaspard/Predicting-House-Prices-In-Kigali/blob/ce89583c83afc587161b31a597913b3f1f32b7b4/Modeling/Predicting%20House%20Price%20In%20Kigali%20Using%20Machine%20Learning.ipynb)""")