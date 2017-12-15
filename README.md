# Summary
“Meetup is a social networking website that aims to brings people together to do, explore, teach and learn the things
that help them come alive.”

Meetup allows members to find and join groups unified by a common interest. As of 2017, there are 32 million users with
280 thousand groups available across 182 countries.

A member needs to be able to identify groups and activities which interest them the most to be able to use this platform
to network effectively.

The aim of our team was to use this dataset to build a recommender system which will identify and suggest groups and activities to a member based on their interest and additional interests of similar members. Furthermore, a social network analysis was done to identify the relationship between groups and people.

# Database EER diagram
![EER diagram][1]

# Data Collection Method
* Data was collected using Meetup API.   
* Python script was used to ping meetup API and collect responses as JSON objects.  
* Logical chunks of data were exported and saved as csv files.  

# Data Cleaning
* Data is filtered to include only 3 cities' information (New York, San Francisco, Chicago).
* Character encoding is normalized to ASCII characters across tables.

# Data Analysis and Machine Learning
## Suggest Groups to a Member
**AIM:** Identify users most similar to a given user in terms of interests in topics, search their group affiliations and suggest the same to the use    
**ALGORITHM:** Content Based Collaborative Filtering using K-Nearest Neighbors Algorithm  
The algorithm uses euclidean distances between the set point [User Vector] and all other points in the dataset, then sorts them to find the five nearest neighbors. Since our matrix is sparse, we use Brute force.
![Results](https://i.imgur.com/o4TuzGt.png)
## Suggest members to a Group Organizer
**AIM:** Identify groups similar to a particular group and recommend top 100 members to the group's organizer  
**ALGORITHM:** Model Based Collaborative Filtering using SVD Matrix Factorization  
The challenges related to sparsity of the matrix and growing nature of data for collaborative filtering is overcome by Matrix Factorization  
![Results](https://i.imgur.com/RT9OoOG.png)
## Discovering Best Venues  
**AIM:** Propose the top 10 meetup venues in the vicinity of given co-ordinates.  
**Method:** Taking co-ordinates as inputs, the algorithm plots ten of the highest rated meetup venues in the vicinity on an interactive map. Venue ratings were first normalised taking into account individual ratings and their count for each venue. The map was plotted using the Folium package on Python.  
![Results](https://i.imgur.com/XJCS6TY.png)

# Data Visualizations (using Tableau and Gephi)
![Popularity of topics][2]
![Trends within top topics][3]
![Popularity of Groups][4]
![Venue locations][5]
![Social network analysis using gephi][6]


  [1]: https://i.imgur.com/LquWsuq.png
  [2]: https://i.imgur.com/Nrzbgqa.png
  [3]: https://i.imgur.com/OLfuQLm.png
  [4]: https://i.imgur.com/O6VTATS.png
  [5]: https://i.imgur.com/BM1rg0d.png
  [6]: https://i.imgur.com/N7UtoyG.png
