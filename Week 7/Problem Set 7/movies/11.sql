SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN ratings ON movies.id = ratings.movie_id
WHERE stars.person_id = (
    SELECT id
    FROM people
    WHERE name = 'Chadwick Boseman'
)
ORDER BY rating DESC
LIMIT 5;
