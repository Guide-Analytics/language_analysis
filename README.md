# Language Analysis Tool - For Reviews (Information and Question Extraction)
### Author: Michael Li

## NLP Toolkits Knowledge Base:
- Spacy
- NLTK
- NER extraction
- TextBlob

## Some other toolkit for NLP
- Gingerit (API)
- Cleantext (**clean** folder > *clean.py*)

## Some data process toolkits:
- Vaex
- PySpark

## Process to enhance information extraction

- Create a 2-layer corpora (multiple corpus for different industries)
    - First layer is "Aspects"
    - Second layer is "Keywords"
- Clean and fix the grammar for the reviews (if necessary, just clean the reviews OR fix the grammar)
    - Note: The process to analyze and fix grammar for each review takes a long time. 
- Extract phrase structures for each review
    - Match aspect words in each reviews.
    - Find associated adjectives/nouns for each aspect word in the phrase or phrases


## How to run the program

- Install the requirements in *requirements.txt* file
- Simply run the *main.py* file with the following arguments 

| Argument        | Choices          | Description  |
| :-------------: |:-------------:| -----:|
| --industry    | [shipping, flashlight] | specify company type |
| --corpus    |   ./corpus  |   locate the corpus folder to use the corpus dataset |
| --data | ./data/[data_type_dir]/[\*.json, \*.csv]   |  data folder for data inputs. See examples inside the folder |
| --data_type | [csv, json]   |  data file type (ex: json file, csv file) |
| --output | [line_chart, heatmap, word_cloud, geomap]   | result output category. The results will produce a json file in order for the frontend to read the data and produce a visualization|

