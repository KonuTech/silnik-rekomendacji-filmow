-- Pierwsza wersja funkcji
DROP FUNCTION `SumDoM`;
CREATE DEFINER=`glebels_root`@`localhost` FUNCTION `SumDoM`(`uzytkownikId` INT, `filmId` INT) RETURNS DECIMAL(10,7) NOT DETERMINISTIC NO SQL SQL SECURITY DEFINER return (select round(sum(Similarity*Ocena),7) from
    (select f.id_film as idFilm1, ff.id_film2 as idFilm2, ff.id_film as idFilm3, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
    from Filmy f
            inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
            inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
            inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film or ff.id_film2 = f.id_film
    where u.id_uzytkownik = uzytkownikId and ((ff.id_film = filmId and ff.id_film2 = f.id_film) or (ff.id_film2 = filmId and ff.id_film = f.id_film))
    group by f.id_film, ff.id_film2, ff.id_film, ff.Similarity 
    having Ocena > 0.5) as tmp)




-- Wszystkie filmy użytkownika
select f.tytul_pl, uf.ocena 
from FK_Uzytkownicy_Filmy uf 
	inner join Filmy f on f.id_film = uf.id_film 
	inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik 
where u.id_uzytkownik=1;

-- Zmienione zapytanie na potrzeby nowej tabeli z pełnym iloczynek kartezjańskim
select f.id_film as idFilm1, ff.id_film2 as idFilm2, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
    from Filmy f
            inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
            inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
            inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film
    where u.id_uzytkownik = 1 and ff.id_film2 = 437 and ff.id_film2 != f.id_film
    group by f.id_film, ff.id_film2, ff.Similarity 
    having Ocena > 0.5


-- NOWA FUNKCJA
-- Nowa funkcja sumująca iloczyny podobieństw i ocen
DROP FUNCTION `SumDoM2`;
CREATE DEFINER=`glebels_root`@`localhost` FUNCTION `SumDoM2`(`uzytkownikId` INT, `filmId` INT) RETURNS DECIMAL(10,7) DETERMINISTIC NO SQL SQL SECURITY DEFINER return (select round(sum(Similarity*Ocena),7) from
    (select f.id_film as idFilm1, ff.id_film2 as idFilm2, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
    from Filmy f
            inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
            inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
            inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film
    where u.id_uzytkownik = uzytkownikId and ff.id_film2 = filmId
    group by f.id_film, ff.id_film2, ff.Similarity 
    having Ocena > 0.5) as tmp)

-- Wersja z sumą ważoną
DROP FUNCTION `SumDoM2`;
CREATE DEFINER=`glebels_root`@`localhost` FUNCTION `SumDoM2`(`uzytkownikId` INT, `filmId` INT) RETURNS DECIMAL(10,7) DETERMINISTIC NO SQL SQL SECURITY DEFINER return (select round((sum(Similarity*Ocena)/count(tmp.idFilm1)),7) from
    (select f.id_film as idFilm1, ff.id_film2 as idFilm2, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
    from Filmy f
            inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
            inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
            inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film
    where u.id_uzytkownik = uzytkownikId and ff.id_film2 = filmId
    group by f.id_film, ff.id_film2, ff.Similarity 
    having Ocena > 0.5) as tmp)








-- Zapytanie do funkcji przy tabeli FK_Filmy_Filmy z pełnym iloczynem kartezjańskim
select id_film, tytul_pl, f.ocena, sumDoM2(1,id_film) 
From Filmy f 
where id_film not in (select f.id_film from FK_Uzytkownicy_Filmy uf inner join Filmy f on f.id_film = uf.id_film inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik where u.id_uzytkownik=1) 
group by id_film, tytul_pl 
order by sumDoM2(1,id_film) desc, f.ocena desc, f.popularnosc desc
limit 0,20;






-- Pierwiastek iloczynu stopni przynależności
select sqrt(DoMReleaseYear(346,348)*DoMReleaseYear(348,346));

select Year(rok_produkcji) from Filmy where id_film = 1161
select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) desc limit 0,1;
select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) asc limit 0,1;

-- When year1 < year2
select (1964-(select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) asc limit 0,1))/(1971-(select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) asc limit 0,1)) as DoM

-- When year1 > year2
select ((select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) desc limit 0,1)-1971)/((select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) desc limit 0,1)-1964) as DoM



-- Ciało funkcji zwracającej przynależność roku produkcji jednego filmu do roku produkcji drugiego filmu
return (select if((select Year(rok_produkcji) from Filmy where id_film = idFilm1)<(select Year(rok_produkcji) from Filmy where id_film = idFilm2), 
    (select ((select Year(rok_produkcji) from Filmy where id_film = idFilm1)+1-(select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) asc limit 0,1))/((select Year(rok_produkcji) from Filmy where id_film = idFilm2)+1-(select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) asc limit 0,1)) as DoM), 
    (select ((select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) desc limit 0,1)+1-(select Year(rok_produkcji) from Filmy where id_film = idFilm1))/((select Year(rok_produkcji) from Filmy order by Year(rok_produkcji) desc limit 0,1)+1-(select Year(rok_produkcji) from Filmy where id_film = idFilm2)) as DoM)) as DoM)



select ff.id_film, f.rok_produkcji, ff.id_film2, f2.rok_produkcji, sqrt(DoMReleaseYear(ff.id_film,ff.id_film2)*DoMReleaseYear(ff.id_film2,ff.id_film)) 
from FK_Filmy_Filmy ff
inner join Filmy f on f.id_film = ff.id_film
inner join Filmy f2 on f2.id_film = ff.id_film2
limit 0,100;