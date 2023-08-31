game_by_region = 'query games "Playstation Games" { fields name,platforms.name,genres.name,first_release_date; where first_release_date > 1514771342000 & platforms != null & genres != null ; limit 500; };'

genre_query = 'query genres "Genre" { fields name; };'

plataform = 'query platforms "Plataform" { fields name;  where id = (8,39,6);};'