# Agora

A web application that provides users with news posts based on their preferences.

Users will select various preferences upon creating an account and can adjust their preferences as they wish.

The application will then fetch news articles from our news database and display them on the main page in a post format with each post having a description of the article, a link to the article, and certain statistics about the article (read time, sentiment, etc).

The user will also have the option to click on each post to get a more detailed view of the post as well as interact with the comment and like features for each post. These metrics will also be taken into account when recommending news posts to the user in the future.

This application is divided into multiple services, each with their own purpose within the application.

## Services

### Aggregator

This service pulls news data from News API. This data contains metadata (such as link, title, description) for news articles from various sources. This service acts as a Publisher to which Bundler service is subscribed to, so it sends data to Bundler whenever it receives new data.

### DB-Service

This service provides API calls to push and pull data into our database. All other services depend on this service to circulate data as necessary. We are using MongoDB noSQL database for all our data, hosted through MongoAtlas.

### Bundler

This service is responsible for creating the posts to display in our application. It first receives metadata about news articles from the aggregator. After that, the service uses the BERT model to figure our similar news articles together and then bundles them into a post. It then hands over the bundled source web links to scrapper to get the actual content of the news article and then calls the LLM service to create a title and a description for the post. It then sends over these posts to the recommender to decide what to send to the user side.

### Scraper

This service performs web scraping on the web links provided to it by the Bundler to get all the content from the source link and sends this data back to the Bundler service.

### LLM

This service uses `Gemma` LLM by Google, hosted locally, to generate a holistic and unbiased summary as well as a title for the bundled content it receives from the bundler and then sends the title and the summary back to the bundler.

### Recommender

This service uses user information and post information to decide what posts to show to the current user. It looks at user preferences and performs topic modelling to find similar posts and also looks at what other posts similar users are liking (collaborative filtering).

### Frontend

This service is the client-side user interface made using React and Tailwind CSS for users to interact with our application. It provides all our functionalities and a clear user flow for a stable user experience.

## Installation & Configuration

First, clone all required repositories:

```bash
git clone --recurse git@github.com:CS520-news-aggregator/agora.git
```

### .env files

With respect to configuration, we have `.env` files in the following directories:

1. `db-service/.env`

```
ATLAS_URI=URI
ATLAS_DB=DB_NAME
```

2. `bundler/.env`

```
IMGUR_CLIENT_ID=CLIENT_ID
```

3. `aggregator/.env`

```
NEWS_API_KEY=KEY
```

### Docker

```bash
# Copy docker-compose to base directory
ln -s news-aggregator/docker-compose.yml .

# Run all services
docker-compose up --build
```

### Local

```bash
python -m venv env
source env/bin/activate

# For each directory, do the following:
cd db-service
pip install -r requirements.txt

# To start each service
python main.py
```

## Models & Datasets

### Topic Clustering

For building various sources in order to create posts, we are using [BertTopic](https://maartengr.github.io/BERTopic/index.html). We trained it on a collection of news articles aggregator through the past few years from the following datasets:

1. [All The News](https://components.one/datasets/all-the-news-articles-dataset/): 200K news articles and essays from 2013 to early 2018
2. [Social Animal](https://www.kaggle.com/datasets/socialanimal/social-animal-10k-articles-with-text-and-nlp-data/data?select=articles.csv): 10K articles from 2023

We are evaluating our model through [topic coherence score](https://www.baeldung.com/cs/topic-modeling-coherence-score). This quantifies how interpretable the topics generated from the model are to humans. Higher coherence scores usually correlates with higher model performance. In our case, we observed a topic coherence score of **NaN**.
TODO - Arnav

### Gemma

We hosted the `gemma` LLM locally and queried it through [Ollama](https://github.com/ollama/ollama) API calls. This was used for generating titles and summaries for our posts. Through prompt engineering and parsing responses, we get acceptable results with current news articles as inputs.

### Topic Similarity

As part of our recommender service, we curate news posts tailored to each user's specific interests. One method we employ is leveraging topic similarity, which ensures that users are presented with content closely aligned with their preferences. By analyzing the topics users express interest in and those associated with each post, we recommend articles that discuss subjects most similar to the user's preferences. To achieve this, we utilize a `spacy` transformer model, which calculates distances between topics based on their semantic similarities.

### Collaborative Filtering

To enhance personalized news recommendations even further, we implemented collaborative filtering in our Recommender service. Our collaborative filtering service tracks the interactions and preferences of the users across the platfrom, which allows us to identify and track similar users' behavior. By combining and analyzing the interactions, comments, upvotes and downvotes of various users, our collabortive filtering service is able to identify users with similar interests. Using this logic helps our Recommender service to recommend posts that were positively interacted by one user, to another user with similar behavior, which helps us in suggesting potentially interesting posts to all the users. This builds on top of the hypothesis that users who have had common preferences and behaviors in the past will mostly like enjoy similar topics in the future as well.

## Testing

### Docker

```bash
# For each service, do the following:
docker exec -it news-aggregator_db-service_1 /bin/bash
pytest -s --cov=routers --cov-report term-missing tests/
```

### Local

```bash
# For each directory, do the following:
cd db-service
pytest -s --cov=routers --cov-report term-missing tests/
```

## Demo

[![Demo Video](https://i.imgur.com/ZrmpF9u.png)](https://drive.google.com/file/d/1MQTEs_0nSMLMqmA0ZQL6wOnkciDhMp0w/preview)
