# Agora

Central repository for Agora - News Aggregator Platform

A web application that provides users with news posts based on their preferences.

Users will select various preferences upon creating an account and can adjust their
preferences as they wish.

The application will then fetch news articles from our news database and display them on the main page in a post format with each post having a description of the article, a link to the article, and certain statistics about the article (read time, sentiment, etc).
The user will also have the option to click on each post to get a more detailed view of the post as well as interact with the comment and like features for each post. These metrics will also be taken into account when recommending news posts to the user in
the future.

This application is divided into multiple services, each with their own purpose within the application. These services are:

### Aggregator 

This service pulls news data from News API. This data contains metadata (such as link, title, description) for news articles from various sources. This service acts as a Publisher to which Bundler service is subscribed to, so it sends data to Bundler whenever it receives new data.

### Db-Service

This service provides API calls to push and pull data into our database. All other services depend on this service to circulate data as necessary.

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






