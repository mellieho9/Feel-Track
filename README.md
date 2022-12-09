# Feel-track
An online visualization tool you can count on to travel safely

# Background
Summer vacations are just around the corner, and the hottest thing to do is travel. Ever since the advent of the coronavirus, however, the prevalence of safety from infectious diseases is at its highest. Even today, when borders have opened, the fear of catching such infectious diseases is present. We aim to ease this concern by developing **Feel-Track**. **Feel-Track** allows users to keep track of the rate of infectious illnesses both around them and wherever they want to travel to. When users wish to travel to a place, they can search and obtain information on the illness safety in those areas based on illness scores, and make conscious decisions on where to go. 

## Current progress 
- [x] Created login/register authentication system
- [x] Created machine learning model to detect illnesses based on symptoms
- [x] Created chloropleth graphs visualizing real-time regional illness exposure rates of 5 most prevalent diseases in the US (Ongoing*: Have to manually download data from CDC to visualize due to time constraints)
- [x] Created a NFT gallery to incentivize filling out health survey
- [ ] Created a SMS notification to fill out health survey with Twilio API (Ongoing)
- [ ] Created a graph that tracks user's health and visualizes it via a graph
- [ ] Created a frontend framework to deploy the above features (Incomplete because had to launch the app via Framer due to time contraints)

## What's next
- Expand visualization to visualize all illnesses across the world 
- Include settings to filter views for specific illnesses
- Add a search bar to zoom into 
- Build a CMS that tabulates results from health survey and recalculates the regional exposure rate when combining user data with CDC data
- Create an algorithm that automatically scrapes updated regional illness exposure data from the CDC

# What we used 
## For frontend
Figma, Framer, and DeCathlon's Vitamin UI kit
## For backend
Twilio SMS and Studio, Flask, PostgreSQL
## For visualizing regional illness exposure data
