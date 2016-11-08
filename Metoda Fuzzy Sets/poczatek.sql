-- Podobieństwo według gatunków
select g1.nazwa_gatunek, g2.nazwa_gatunek, g1.DoM, g2.DoM,
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 left join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek
UNION
select g1.nazwa_gatunek, g2.nazwa_gatunek, g1.DoM, g2.DoM,
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 right join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek;



 -- Podobieństwo według gatunków bez zbędnych danych
select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 left join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek
UNION
select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 right join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek;


 -- Wyliczona suma minimów i maksimów
 select sum(minimum) as sumMin, sum(maksimum) as sumMax from
 (select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 left join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek
UNION
select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 right join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek) as maks_min;


-- Podobieństwo na przykładzie gatunków zgodnie z ideą zbiorów rozmytych
 select sum(minimum)/sum(maksimum) as genresSimilarity from
 (select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 left join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek
UNION
select
 CASE
 	WHEN g1.DoM is NULL THEN least(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN least(g1.DoM, 0)
 	ELSE LEAST(g1.DoM, g2.DoM)
 END as minimum,
 CASE
 	WHEN g1.DoM is NULL THEN greatest(0, g2.DoM)
 	WHEN g2.DoM is NULL THEN greatest(g1.DoM, 0)
 	ELSE greatest(g1.DoM, g2.DoM)
 END as maksimum from (select fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1161) as g1 right join (select nazwa_gatunek, fk.id_gatunek, DoM from Gatunki as g inner join FK_Gatunki_Filmy as fk on fk.id_gatunek = g.id_gatunek inner join Filmy as f on f.id_film = fk.id_film where f.id_film = 1126) as g2 on g2.id_gatunek = g1.id_gatunek) as maks_min;