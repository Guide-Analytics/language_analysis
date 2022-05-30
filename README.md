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

