
> [!tip] Cities
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "cities")
> SORT file.name ASC
> ```

> [!info] Settlements
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "settlements")
> SORT file.name ASC
> ```

> [!abstract] Landmarks
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "landmarks")
> SORT file.name ASC
> ```

> [!note] Buildings & Sites
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "buildings_sites")
> SORT file.name ASC
> ```

> [!warning] Wilderness
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "wilderness")
> SORT file.name ASC
> ```

> [!danger] Planes & Other Realms
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "planes_other_realms")
> SORT file.name ASC
> ```

> [!example] Unsorted
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	placeType as "Type",
> 	region as "Region",
> 	controlledBy as "Controlled By"
> FROM "Whispers of the Umbral Abyss/Locations"
> WHERE type = "place" AND contains(tags, "unsorted")
> SORT file.name ASC
> ```