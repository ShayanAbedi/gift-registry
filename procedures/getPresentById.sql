DELIMITER //
DROP PROCEDURE IF EXISTS getPresentById //

CREATE PROCEDURE getPresentById(IN presentIdIn int)
BEGIN
   SELECT *
      FROM presents
      WHERE present_id = PresentIdIn;
END//
DELIMITER ;
