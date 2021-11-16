# News Aggregator
## Description
This repository contains the solution for [https://bitbucket.org/hamzamasroor/news-aggregator/src/master/](https://bitbucket.org/hamzamasroor/news-aggregator/src/master/)

A Django application that aggregates news from two different APIs. The APIs you’ll be using are Reddit and News API. The application runs on your localhost and serve the result in JSON format from an endpoint whenever it gets a request.

## Getting Started
### Installation
To install all the requirements run the following command: 
`pip install -r requirements.txt`
### Pre-StartUp commands
run the following commands (in respective order) to set up the database:
- `python manage.py makemigrations`
- `python manage.py migrate`
### Starting the application
run the following command to start the application:
`python manage.py runserver`

The Application will now run on `localhost:8000`
## USAGE
### Create a user
To create a user make a **POST** request to the following URL, passing you username as a parameter:

`localhost:8000/news/create/?user=<your_username>`

### Search and List
Make a request to the following URL:
`localhost:8000`

You can also add a query with the URL as:
`localhost:8000/news?query=<your_query>`
#### Examples

```
> Request
GET /news   HTTP/1.1
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ
Accept: application/json

> Response
[
  {
    "headline": "Human organs can be stored for three times as long in major breakthrough for transplants",  // Headline of the article
    "link": "https://www.telegraph.co.uk/science/2019/09/09/human-organs-can-stored-three-times-long-major-breakthrough/",  // Link of the article
    "source": "reddit" // Source that you retrieved this news from
  },
  {
    "headline": "Depth of Field: The Shared Memory of One World Trade Center",
    "link": "https://www.wired.com/story/one-world-trade-center-history-future/",
    "source": "newsapi"
  },
]
```
Pass a query parameter
```
> Request
GET /news?query=bitcoin   HTTP/1.1
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ
Accept: application/json

> Response
[
  {
    "headline": "IRS goes after cryptocurrency owners for unpaid taxes",
    "link": "https://www.cbsnews.com/news/own-bitcoin-irs-pursues-cryptocurrency-owners-for-unpaid-taxes/",
    "source": "reddit"
  },
  {
    "headline": "Skirting US sanctions, Cubans flock to cryptocurrency to shop online, send funds",
    "link": "https://www.channelnewsasia.com/news/business/skirting-us-sanctions--cubans-flock-to-cryptocurrency-to-shop-online--send-funds-11901148",
    "source": "newsapi"
  },
]
```
### List and mark/unmark Favourite
To list the favourite articles of a user, make a **GET** request to the following URL and pass username as a parameter:

`localhost:8000/news/favourite?user=<username>`

#### Example

```
> Request
GET /news/favourite?user=mpopatia   HTTP/1.1
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ
Accept: application/json

> Response
[
  {
    "id": 42,
    "headline": "IRS goes after cryptocurrency owners for unpaid taxes",
    "link": "https://www.cbsnews.com/news/own-bitcoin-irs-pursues-cryptocurrency-owners-for-unpaid-taxes/",
    "source": "reddit"
  },
  {
    "id": 57,
    "headline": "Skirting US sanctions, Cubans flock to cryptocurrency to shop online, send funds",
    "link": "https://www.channelnewsasia.com/news/business/skirting-us-sanctions--cubans-flock-to-cryptocurrency-to-shop-online--send-funds-11901148",
    "source": "newsapi"
  },
]
```

To add or remove from favourites, make a **POST** request to the following URL, and pass username and artile id as parameters:

`localhost:8000/news/favourite/?user=<username>&id=<article_id>`

#### Examples

mark favourite
```
> Request
POST /news/favourite/?user=mpopatia&id=5  HTTP/1.1
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ
Accept: application/json

> Response
[
  {
    "user": "mpopatia",
    "favorite": true,
    "id": 21,
    "headline": "Human organs can be stored for three times as long in major breakthrough for transplants",
    "link": "https://www.telegraph.co.uk/science/2019/09/09/human-organs-can-stored-three-times-long-major-breakthrough/",
    "source": "reddit"
  },
]
```
unmark favourites

```
> Request
POST /news/favourite/?user=mpopatia&id=5  HTTP/1.1
Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ
Accept: application/json

> Response
[
  {
    "user": "mpopatia",
    "favorite": false,
    "id": 21,
    "headline": "Human organs can be stored for three times as long in major breakthrough for transplants",
    "link": "https://www.telegraph.co.uk/science/2019/09/09/human-organs-can-stored-three-times-long-major-breakthrough/",
    "source": "reddit"
  },
]
```
## Documentation
Access `index.html` file in `docs\_build\html\` to access documentatiom


