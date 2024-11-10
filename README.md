# NBA Analysis
======================================================
A Tutorial on using Graphs with react + microservices
======================================================

Teach me how to make a graph and microservices project. Let's make an NBA team performance project. Treat me
like I'm an analyst for a basketball team and I want to make a visual aid on the team performance from the last 10 games

Steps:
1. Installation (vite react18 typescript project with react-hook-form, zod, redux)
2. Setting up react-hook-form and zod
3. Setting up redux
4. Setting up react-hook-form, and show how the setup can be mixed with RTK
5. Show how to create an Add Player modal. The modal should contain:
	- Name - player name (note, that a player id should be generated each time)
	- checkbox - Is Two-Way
	- a number box to indicate jersey number
	- a validation that appears if the form entries are not filled
	- A dropdown which initially has a placeholder "Select a position", where the category is PG, SG, SF, PF, C
	- a rich text area. Show how to use react-quill and add a rich text area in the modal that allows the user to put in notes about the player
6. Show how to create a main page, which shows a line chart using Nivo. This will draw player performances from the last 10 games. This data will come from a microservice.
7. Show how to use MWS to initially mock the responses
8. Show how to create a BFF asp.net web API. This web api will use refit to send a http request to another microservice called PlayerProfile.
9. Show how to create a player profile microservice using fastapi. This microservice will store the data in a mongodb. Ensure it only uses the free version.
10. Show how to deploy the bff, the react app and the microservice to railway.app
11. Show how to create another microservice written in asp.net. It will be called PlayerPerformance. It will hold data to each player in a postgres DB. This will contain player stats and limited to only 10 entries per player. If another entry is added, the oldest entry will be deleted.

