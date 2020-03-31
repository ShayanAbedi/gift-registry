DELIMITER //
DROP PROCEDURE IF EXISTS getPresents //

CREATE PROCEDURE getPresents()
BEGIN
  SELECT presents.present_id, presents.present_name, presents.link, presents.img_url, presents.submission_date, presents.user_id, users.user_name
    FROM presents
    INNER JOIN users ON presents.user_id = users.user_id;
END //
DELIMITER ;