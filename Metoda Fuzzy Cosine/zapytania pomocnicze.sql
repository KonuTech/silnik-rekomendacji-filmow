-- najciekawsze dane z updateowanych Pozycji
select p.tytul_pl, p.czas_trwania, a.nazwa_aktor, fk.DoM, p.typ from Pozycja as p left join FK_Aktor_Pozycja as fk on fk.id_pozycja = p.id_pozycja left join Aktor as a on a.id_aktor = fk.id_aktor group by p.tytul_pl, a.nazwa_aktor, fk.DoM, p.czas_trwania order by p.id_pozycja asc limit 0,50;

-- rozbudowane zapytanie z GATUNKIEM i AKTORAMI
 select p.tytul_pl, p.czas_trwania, a.nazwa_aktor, fk.DoM as "DoM Aktora", p.typ, g.nazwa_gatunek, fk_g.DoM as "DoM Gatunmku" from Pozycja as p left join FK_Aktor_Pozycja as fk on fk.id_pozycja = p.id_pozycja left join Aktor as a on a.id_aktor = fk.id_aktor left join FK_Gatunek_Pozycja as fk_g on fk_g.id_pozycja = p.id_pozycja left join Gatunek as g on g.id_gatunek = fk_g.id_gatunek group by p.tytul_pl, a.nazwa_aktor, fk.DoM, fk_g.Dom, g.nazwa_gatunek, p.czas_trwania order by p.id_pozycja asc limit 0,50;

-- tworzenie nowej tabeli Filmy - Filmy (wiele do wielu)
CREATE TABLE IF NOT EXISTS `FK_Filmy_Filmy` (
  `id_film` int(11) NOT NULL,
  `id_film2` int(11) NOT NULL,
  `Similarity` decimal(10,7) DEFAULT NULL,
  PRIMARY KEY (`id_film`,`id_film2`),
  FOREIGN KEY (`id_film`) REFERENCES `Filmy`(`id_film`),
  FOREIGN KEY (`id_film2`) REFERENCES `Filmy`(`id_film`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Przykładowe zapytanie do powyższej tabeli
select ff.Similarity
from Filmy as f
	inner join FK_Filmy_Filmy as ff on f.id_film = ff.id_film
WHERE (f.id_film = 1161 and ff.id_film2 = 1126) or (f.id_film = 1126 and ff.id_film2 = 1161);


-- Wyznaczanie rekomendowanych filmów dla użytkownika
select f.tytul_pl, f2.tytul_pl, ff.Similarity, ff.id_film, ff.id_film2
from Filmy as f
	inner join FK_Filmy_Filmy as ff on ff.id_film = f.id_film
	inner join Filmy as f2 on ff.id_film2 = f2.id_film
where ff.id_film = 5464 or ff.id_film2 = 5464
order by ff.Similarity desc
limit 0,10;


-- 
select LubianeFilmy.liked, LubianeFilmy sum(ff.Similarity) from
	(select f.id_film, f.tytul_pl, DoMLiked(uf.ocena) as 'liked'
	from Filmy as f
		inner join FK_Uzytkownicy_Filmy as uf on uf.id_film = f.id_film
		inner join Uzytkownicy as u on u.id_uzytkownik = uf.id_uzytkownik
	where u.login = "tosia" group by f.tytul_pl having liked > 0.5) as LubianeFilmy
	inner join FK_Filmy_Filmy as ff on ff.id_film = LubianeFilmy.id_film or ff.id_film2 = LubianeFilmy.id_film
	group by LubianeFilmy.liked;

	-- inner join FK_Filmy_Filmy as ff on f.id_film = ff.id_film


-- Delete błędnych pozycji
delete f.* from Filmy as f
	inner join FK_Aktorzy_Filmy as af on af.id_film = f.id_film
	inner join Aktorzy as a on af.id_aktor = a.id_aktor

	inner join FK_Filmy_Filmy as ff on ff.id_film = f.id_film

	inner join FK_Gatunki_Filmy as gf on gf.id_film = f.id_film
	inner join Gatunki as g on g.id_gatunek = gf.id_gatunek

	inner join FK_Jezyki_Filmy as jf on jf.id_film = f.id_film
	inner join Jezyki as j on j.id_jezyk = jf.id_jezyk

	inner join FK_Keywords_Filmy as kf on kf.id_film = f.id_film
	inner join Keywords as k on k.id_keyword = kf.id_keyword
	
	inner join FK_Panstwa_Filmy as pf on pf.id_film = f.id_film
	inner join Panstwa as p on p.id_panstwo = pf.id_panstwo

	inner join Rezyserzy as r on r.id_rezyser = f.id_rezyser

	inner join FK_Uzytkownicy_Filmy as uf on uf.id_film = f.id_film
	inner join Uzytkownicy as u on u.id_uzytkownik = uf.id_uzytkownik
where f.id_film = 5464;

-- Iloczyn kartezjański filmów
insert into FK_Filmy_Filmy(id_film, id_film2, Similarity) select f.id_film, f2.id_film, Similarity(f.id_film, f2.id_film) as Similarity from Filmy f join Filmy f2;

select f.id_film, f2.id_film, Similarity(f.id_film, f2.id_film) as Similarity from Filmy f join Filmy f2 limit 0,100






-- Rekomendowane filmy
select f.id_film, f2.id_film, DoMLiked(uf.ocena) as ocena, ff.Similarity
from Filmy f
	inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
	inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
	inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film or ff.id_film2 = f.id_film
	inner join Filmy as f2 on ff.id_film2 = f2.id_film
where u.login = "tosia" group by f.id_film, uf.ocena, f2.id_film, ff.Similarity;


-- Rekomendowane filmy
select sum(Similarity*Ocena) from
(select f.id_film as idFilm1, ff.id_film2 as idFilm2, ff.id_film as idFilm3, DoMLiked(uf.ocena) as 'Ocena', ff.Similarity
from Filmy f
	inner join FK_Uzytkownicy_Filmy uf on uf.id_film = f.id_film
	inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik
	inner join FK_Filmy_Filmy ff on ff.id_film = f.id_film or ff.id_film2 = f.id_film
where u.login = "tosia" and ((ff.id_film = 1126 and ff.id_film2 = f.id_film) or (ff.id_film2 = 1126 and ff.id_film = f.id_film))
group by f.id_film, ff.id_film2, ff.id_film, ff.Similarity 
having Ocena > 0.5) as LubianeFilmy;





-- Rekomendacje dla danego użytkownika spośród wszystkich filmów
select ff.id_film, ff.id_film2
from FK_Filmy_Filmy ff
group by ff.id_film, ff.id_film2;





