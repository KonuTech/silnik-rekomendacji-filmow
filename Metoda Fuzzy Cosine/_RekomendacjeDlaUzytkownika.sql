-- Zapytanie do funkcji przy tabeli FK_Filmy_Filmy z pełnym iloczynem kartezjańskim
select id_film, tytul_pl, sumDoM2(45,id_film) as Prognoza
From Filmy f 
where id_film not in (select f.id_film from FK_Uzytkownicy_Filmy uf inner join Filmy f on f.id_film = uf.id_film inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik where u.id_uzytkownik=45 and uf.ocena != -1) 
group by id_film, tytul_pl 
order by Prognoza desc, f.ocena desc, f.popularnosc desc
limit 0,50;	



-- Zapytanie do funkcji przy tabeli FK_Filmy_Filmy z pełnym iloczynem kartezjańskim Z UWZGLĘDNIENIEM OCENY FILMU
select id_film, tytul_pl, ((sumDoM2(45,id_film)*75/100)+(f.ocena/10*25/100)) as Prognoza
From Filmy f 
where id_film not in (select f.id_film from FK_Uzytkownicy_Filmy uf inner join Filmy f on f.id_film = uf.id_film inner join Uzytkownicy u on u.id_uzytkownik = uf.id_uzytkownik where u.id_uzytkownik=45 and uf.ocena != -1) 
group by id_film, tytul_pl 
order by Prognoza desc, f.ocena desc, f.popularnosc desc
limit 0,50;	