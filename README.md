# hnr_foodify

![flowchart](https://github.com/VibhuKrovvidi/hnr_foodify/blob/main/resources/foodify.png)
## Description
Foodify is an API tool that allows users slice and dice restaurant review data based on the categories or aspects that matter most to them. 
For example, if you are a student on a budget, the value-for-money that a restaurant offers is of most importance to you.
If you are trying to impress, the ambience is most critical.

We use aspect-based sentiment analysis to categorise and crowd-source a consensus on these different categories. 
Our hope is that users can use the API we provide to make better informed and data-driven decisions.
Ultimately, we hope to create tools to allow comparisons, rankings, trends and dashboards to help guide not only users, but also restaurants, thereby closing the feedback loop.

## How we made it
Flask + Python

![flowchart](https://github.com/VibhuKrovvidi/hnr_foodify/blob/main/resources/flow.png)

## How to use it

There are two endpoints, both supporting GET requests:

* `/restaurant/<restaurant_name>` - this returns the standard key aspects and their polarity scores. If given restaurant is not in the database, it will return a 404. 

* `/restaurant/<restaurant_name>/feature` - this returns the polarity score for custom aspect (feature) of given restaurant. In query params, foodify expects a `feature_name` and `corpus` (words that describe the feature). 

## Team
Vibhu, Raivat
