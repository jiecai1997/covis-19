# COVIS19

## Link
🌐[covis19.herokuapp.com](https://covis19.herokuapp.com)

---

## About
**COVIS19 = COVID19 + DATAVIS**

COVIS19 is an interactive data visualization web-app that showcases the health and financial effects of the coronavirus.

In the sea of information overload, I wanted to make something that is informative yet simple. I believe that well-presented numbers and visuals stick with people most, so I built COVIS19 with that in mind.

### 💊Health Information

This page contains information related to COVID-19 cases, tests, hospitalizations, ICU/ventilator usage, deaths and recovereies in the US. 

Users can visualize trends to answer questions such as *are we flattening the curve yet?* and *how do positive rates compare between states after normalizing for each state's population density?*

### 💵Financial Information

This page contains information related to 2020 YTD (year to date) performance of several stocks and indexes, highlighting the financial impact of the coronavirus on the US market. 

I show the performance of the average market via. major indices as a baseline, then display how other stock categories have proved to be risilient or vulnerable. I also allow the user to enter their own stock ticker to compare its YTD performance with the market average!

---
## Data Sources
All of the data sources used are open-source. Shoutout to the developers for making this information available for everyone.

### 💊Health Data
via [The COVID Tracking Project's API](https://covidtracking.com/api)

### 💵Financial Data
via [Yfinance Python Package](https://github.com/ranaroussi/yfinance)

---

## Tech Stack
I used [Dash by Plotly](https://plotly.com/dash/). This allowed me to develop my app entirely using Python - from setting up the app server, reading in external data to outputting data visusalization UI.