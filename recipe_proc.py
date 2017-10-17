
# coding: utf-8

# # Processing Recipes
# Load in all recipes and reduce dimensions

# In[21]:

import json
import pandas as pd
import numpy as np

with open('./data/train.json') as json_data:
    d = json.load(json_data)

# create a list of cuisines with recipe counts
cuisines=[]
for i in range(len(d)):
    cuisines.append(d[i]['cuisine'])
cuisines_list=np.unique(cuisines, return_counts=True)

# Create a dataframe in descending order of cuisines and recipe counts
df_cuisines=pd.DataFrame({"cuisine": cuisines_list[0], "count":cuisines_list[1]}, index=None)
df_cuisines=df_cuisines.sort_values("count", ascending=False)

# create a full ingredient list with counts
all_ingred = []
for recipe in range(len(d)): 
    all_ingred.extend(d[recipe]['ingredients'])
ingred_list = np.unique(all_ingred, return_counts=True)

# Create a dataframe in descending order of ingredients and recipe count
df_ingredients=pd.DataFrame({"ingredient": ingred_list[0], "count":ingred_list[1]}, index=None)
df_ingredients=df_ingredients.sort_values("count", ascending=False)

cuisines_dict={}
for cuisine in df_cuisines['cuisine']:
    cuisines_dict[cuisine]=[x for x in d if x['cuisine']==cuisine]

# Initialize ingredients as a dictionary
ingredients={}

# For each cuisine, create an entry in the dictionary that 
# maps cuisine to a list of lists of ingredients from each recipe

for cuisine in df_cuisines['cuisine']:
    ingredients[cuisine]=[]
    for i in range(len(cuisines_dict[cuisine])):
        ingredients[cuisine].extend(cuisines_dict[cuisine][i]['ingredients'])

# initialize ingredient list dictionary	
ingr_list={}

# add dict entries mapping cuisine to unique ingredients with counts
for cuisine in df_cuisines['cuisine']:
    ingr_list[cuisine]=np.unique(ingredients[cuisine], return_counts=True)

# Loop through cuisines, merge cuisine ingredient counts with our master

for cuisine in df_cuisines['cuisine']:
    cuisine_ingredient_dict= dict(zip(ingr_list[cuisine][0],ingr_list[cuisine][1]))
    df_ingredients[cuisine]=0
    df_ingredients[cuisine] = df_ingredients['ingredient'].apply(lambda x: cuisine_ingredient_dict.get(x,0))

df_ingredients.to_csv("./data/ingredients_by_cuisine.csv")
# print(df_ingredients[0][:10])
# print(df_ingredients[0][:10])

