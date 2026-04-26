# News Retrieval and Conversational AI System

## Overview

This project implements a News Retrieval and Conversational Question Answering system that allows users to search and interact with news articles using natural language. It combines Information Retrieval techniques (BM25) with transformer-based AI models to provide accurate and meaningful responses.

## Features

* BM25-based document retrieval for relevant search results
* Transformer-based Question Answering (QA) system
* Named Entity Recognition (NER) fallback for implicit queries
* Flask-based web interface for user interaction
* Oracle database integration for data storage
* Query logging and response storage

## Tech Stack

* Python
* Flask
* Oracle SQL
* Hugging Face Transformers
* rank_bm25

## Project Structure

project/
│── main.py
│── app.py
│── mymodel.py
│── preprocess.py
│── requirements.txt
│── dataset_sample.csv
│── architecture_diagram.jpg
│── results_output.txt

## How It Works

1. User enters a search query through the web interface
2. BM25 retrieves top relevant news articles
3. User selects an article
4. QA model extracts answers from the article
5. NER model handles fallback cases (e.g., location, person)
6. Queries and answers are stored in the database

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   python main.py

3. Open browser:
   http://127.0.0.1:5000

## Sample Output

Query: tech
Selected Article: (retrieved article)
Question: which country?
Answer: US

## Limitations

* Limited semantic understanding
* Depends on dataset quality
* QA model may fail for vague or unclear questions

## Future Improvements

* Semantic search using embeddings
* Improved UI/UX design
* Real-time news integration
* User authentication and personalization


