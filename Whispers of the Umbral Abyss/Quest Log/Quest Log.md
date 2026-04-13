> [!info] Quest Summary
> ```dataview
> TABLE WITHOUT ID
> 	status as "Status",
> 	length(rows) as "Count"
> FROM "Whispers of the Umbral Abyss"
> WHERE type = "quest"
> GROUP BY status
> SORT status ASC
> ```

> [!abstract] Active Quests
> ```dataview
> TABLE
> 	title as "Quest",
> 	priority as "Priority",
> 	locations as "Locations",
> 	assignedBy as "Assigned By"
> FROM "Whispers of the Umbral Abyss"
> WHERE type = "quest" AND status = "active"
> SORT priority ASC, title ASC
> ```

> [!success] Completed Quests
> ```dataview
> TABLE
> 	title as "Quest",
> 	priority as "Priority",
> 	assignedBy as "Assigned By"
> FROM "Whispers of the Umbral Abyss"
> WHERE type = "quest" AND status = "completed"
> SORT title ASC
> ```

