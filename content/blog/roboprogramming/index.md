# Robotics and Programming Projects

[< Back Home](/)

![Glorfindel image](/images/glorfindel.png)

The page hold various projects I've worked on related to Robotics and general Programming. I have the most experience with Python but working knowledge of Golang and exposure to C/C++

## IAQ Sensor Network

### Description

After doing the project above, I learned it I don't like using other people's sensors. They tend to dissuade the users (me) from trying to fix the sensors in lieu of buying brand new ones for a lot of money. The monitors used also required a subscription to access the data. And even though you play them a lot of money, their dashboards kinda stink and its hard to pull data from their site. THEY DON'T EVEN HAVE AN API (at least when I was doing the project). So, I decided to figure something else out. After a long search I came across an open source IAQ monitor from AirGradient. A Diy kit was ordered. Code was written to connect it to a server (Prometheus) being hosted on a embedded system (RaspberryPi). More code was written to automate the process of pulling data and sending it to my email. 

### Skills:

Technical: Embedded Systems (RaspberryPi), Python, Time-series Database (Prometheus), Real-time Visualizations (Grafana)  
Soft: Researching, Technical Writing

### Proof:

[Github Repo](https://github.com/zdelk/IAQ_Pi_network)  
[Grafana Dashboard](https://zdelk.grafana.net/public-dashboards/ea14be1063c647dabec262c3f1ddec0f)

## Anomaly Detection using Unsupervised Machine Learning

### Description

This was the final project of an Automation class. The idea behind it was to train a neural network that could detected anomalies in a manufacturing process by the cycle time at various points in the line. Generally automated lines have controllers that will throw issues that cause large problems or if something is really broken but these systems don't watch for small time losses from A to B. While not inherently a big issue, over time this can lead to a reduction in productivity and generally indicates a larger issue that the controller can't detect. While we did not have a large factory with multiple automated lines to play with, we did have a marble run machine that was fitted with a sorting device that would report sensor states over an Arduino IOT device. This was initially a pretty promising project, but we learned towards the end that the Arduino had a rate limit for publishing data to the cloud that skewed our measurements. I would be possible to implement a different embedded system without this rate limit but due to time and cost concerns we were not able to implement it.

### Skills

**Technical:** Embedded Systems (RaspberryPi and Arduino), Python (Pytorch), Time-Series Data Handling, Iterative Testing and Tuning  
**Soft:** Report Generation, Teamwork, Time-management

### Proof

[Final Report](https://link.com/anomaly)

## Command Line BlackJack (IN PROGRESS)

### Description

This is a personal project I've been working on just to get better at Object Oriented Programming. The end goal is to be able to play blackjack (21) on the command line. Was also thinking about integrating CPUs or a way of tracking the "count" of the table as a learning device inspired by the 2008 movie 21. It's still a work in progress but has been a fun experience.

### Skills

**Technical:** Python, Object Oriented Programming (OOP), Decision Tree
**Soft:** Project Design, Documentation