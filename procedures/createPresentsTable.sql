DROP TABLE IF EXISTS presents;
CREATE TABLE presents(
  present_id    INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
  present_name  VARCHAR(33)   NOT NULL,
  link          VARCHAR(250)  NOT NULL,
  img_url       VARCHAR(250)  NULL        ,
  submission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id       INT           NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);