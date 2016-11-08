

DELIMITER $$ 
DROP PROCEDURE IF EXISTS Proc$$
CREATE PROCEDURE Proc()
	BEGIN
		DECLARE x,y INT;
		DECLARE var1, var2 INT;
		DECLARE cur1 CURSOR FOR SELECT id_film from Filmy order by id_film asc limit 0,5;
		DECLARE cur2 CURSOR FOR SELECT id_film from Filmy order by id_film asc limit 0,5;

		open cur1;
		open cur2;

		SET x = 1;
		set y = 1;

		WHILE (x  <= 5) DO
			fetch cur1 into var1;

			WHILE (y <= 5) DO 
				fetch cur2 into var2;
				if var2 != var1 then insert into FK_Filmy_Filmy VALUES(var1,var2, 1.1);
				end if;
				SET  y = y + 1;
			END WHILE;
			SET  x = x + 1;
		END WHILE;
	END$$
DELIMITER ;


delete from FK_Filmy_Filmy;
call Proc();
select * from FK_Filmy_Filmy;