# Origin Finder

A OSINT tool to navigate through relevant posts,to find the origin of misleading, rumour spreading posts.

This Application is made in the MANTHAN India wide Hackathon 2021(https://manthan.mic.gov.in/)

[![Origin Finder V1](.\assets\video.jpg)]( https://www.youtube.com/watch?v=WYCq_Jw-KLw "Origin Finder V1")



## Pipeline

<img src=".\assets\basic_pipeline.png" alt="pipeline" style="zoom: 50%;" />

<img src=".\assets\flowchart.png" alt="flowchart" style="zoom: 33%;" />

​																																**Old version**

## Features:

- Automatic Keywords extraction from the content of the posts
- Find Relevant posts with a single click of button
- Retrieve various metadata embedded in the posts
- Fetch Account Details of the users
- Experimental Social Graph Mode

## Social Media Sites Supported:

- Twitter
- Reddit

##  Installation:

Install all python dependencies:

​	`pip install -r requirements`

The frontend part can be hosted by using "serve". To install serve:

​	`npm install -g serve`

## Running:

Start The Backend:

​	`python main.py --backend`

Start The MITM (Man in the Middle):

​	`python main.py --mitm`

Start the Frontend:

​	`serve -s frontend/build`

## Team Members:

- Harish Raja 
- Monish Kumar GS
- me

## Credits:

- [searx](https://github.com/searx/searx)
  - we have used a custom implementation whose architecture is inspired by searx (we call it searz).
- [fake-news](https://github.com/FavioVazquez/fake-news)
  - Fake News Detection AI model is from this.

