DROP FUNCTION `SumDoM`;
CREATE DEFINER=`glebels_root`@`localhost` FUNCTION `SumDoM`(`uzytkownikId` INT, `filmId` INT) RETURNS DECIMAL(10,7) DETERMINISTIC NO SQL SQL SECURITY DEFINER return (select round(sum(Similarity*Ocena),7) from
    (select f.id_film as idFilm1, ff.id_film2 as idFilm2, ff.id_film as idFilm3, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
    from Filmy f
            inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
            inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
            inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film or ff.id_film2 = f.id_film
    where u.id_uzytkownik = uzytkownikId and ((ff.id_film = filmId and ff.id_film2 = f.id_film) or (ff.id_film2 = filmId and ff.id_film = f.id_film))
    group by f.id_film, ff.id_film2, ff.id_film, ff.Similarity 
    having Ocena > 0.5) as tmp)