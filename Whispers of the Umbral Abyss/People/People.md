

> [!tip] Wayfarers Accord
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "wayfarers_accord")
> SORT file.name ASC
> ```

> [!info] Allies
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "allies")
> SORT file.name ASC
> ```

> [!warning] Antagonists
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "antagonists")
> SORT file.name ASC
> ```

> [!abstract] Faction Figures
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "faction_figures")
> SORT file.name ASC
> ```

> [!note] Local Contacts
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "local_contacts")
> SORT file.name ASC
> ```

> [!danger] Supernatural
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "supernatural")
> SORT file.name ASC
> ```

> [!example] Unsorted
> ```dataview
> TABLE WITHOUT ID
> 	file.link as "Name",
> 	race as "Race",
> 	occupation as "Occupation",
> 	status as "Status",
> 	locations as "Locations",
> 	organizations as "Organizations"
> FROM "Whispers of the Umbral Abyss/People"
> WHERE type = "person" AND contains(tags, "unsorted")
> SORT file.name ASC
> ```