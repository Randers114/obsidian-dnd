```dataview
TABLE 
status AS "Status",
race AS "Race",
occupation AS "Job",
location AS "Location",
party_relationship AS "Relation"
FROM "People"
WHERE contains(tags, "#person")
SORT status ASC, file.name ASC
```
