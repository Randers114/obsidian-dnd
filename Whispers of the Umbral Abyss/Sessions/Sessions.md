
> [!info] Session Summary
> ```dataview
TABLE WITHOUT ID  
rows.date[0].year as "Year",  
length(rows) as "Sessions"  
FROM "Whispers of the Umbral Abyss/Sessions"  
WHERE type = "session"  
GROUP BY date.year  
SORT key ASC
> ```

> [!tip] Recent Sessions
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Session",
> 	sessionNumber as "#",
> 	date as "Date",
> 	locations as "Locations",
> 	quests as "Quests"
> FROM "Whispers of the Umbral Abyss/Sessions"
> WHERE type = "session"
> SORT date DESC
> LIMIT 4
> ```

> [!abstract] Full Timeline
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Session",
> 	sessionNumber as "#",
> 	date as "Date",
> 	people as "People",
> 	locations as "Locations",
> 	quests as "Quests"
> FROM "Whispers of the Umbral Abyss/Sessions"
> WHERE type = "session"
> SORT date ASC
> ```



