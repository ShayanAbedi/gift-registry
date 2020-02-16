DELIMITER //
DROP PROCEDURE IF EXISTS updatePresentLink //

CREATE PROCEDURE updatePresentLink(IN id INT, IN present_link VARCHAR(100))
BEGIN
    UPDATE presents
    SET link = present_link
    WHERE present_id = id;
END //
DELIMITER ;