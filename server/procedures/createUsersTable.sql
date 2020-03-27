DROP TABLE IF EXISTS users;
CREATE TABLE users(
  user_id   INT               NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
  user_name VARCHAR(33)       NOT NULL,
  email     VARCHAR(50)       NOT NULL,
  img_url   VARCHAR(250)      NULL        
);