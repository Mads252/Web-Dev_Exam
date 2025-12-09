
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;



CREATE TABLE IF NOT EXISTS users (
  user_id           CHAR(32)      NOT NULL,
  email             VARCHAR(255)  NOT NULL,
  password_hash     VARCHAR(255)  NOT NULL,
  username          VARCHAR(50)   NOT NULL,
  display_name      VARCHAR(100)  NULL,
  bio               VARCHAR(160)  NULL,
  avatar_filename   VARCHAR(255)  NULL,
  is_admin          TINYINT(1)    NOT NULL DEFAULT 0,
  is_blocked        TINYINT(1)    NOT NULL DEFAULT 0,
  is_deleted        TINYINT(1)    NOT NULL DEFAULT 0,
  email_verified_at int(11)      NULL,
  created_at        int(11)      NOT NULL,
  updated_at        int(11)      NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY uq_users_email (email),
  UNIQUE KEY uq_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS posts (
  post_id      CHAR(32)      NOT NULL,
  user_id_fk   CHAR(32)      NOT NULL,
  content      VARCHAR(280)  NOT NULL,
  is_blocked   TINYINT(1)    NOT NULL DEFAULT 0,
  is_deleted   TINYINT(1)    NOT NULL DEFAULT 0,
  created_at   int(11)      NOT NULL,
  updated_at   int(11)      NULL,
  PRIMARY KEY (post_id),
  KEY idx_posts_user (user_id_fk),
  KEY idx_posts_created_at (created_at),
  CONSTRAINT fk_posts_users
    FOREIGN KEY (user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS post_media (
  media_id     CHAR(32)      NOT NULL,
  post_id_fk   CHAR(32)      NOT NULL,
  file_path    VARCHAR(255)  NOT NULL,
  media_type   ENUM('image','video') NOT NULL,
  created_at   int(11)      NOT NULL,
  PRIMARY KEY (media_id),
  KEY idx_media_post (post_id_fk),
  CONSTRAINT fk_media_posts
    FOREIGN KEY (post_id_fk) REFERENCES posts(post_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS follows (
  follower_user_id_fk   CHAR(32)   NOT NULL, -- den der følger
  followee_user_id_fk   CHAR(32)   NOT NULL, -- den der bliver fulgt
  created_at            int(11)   NOT NULL,
  PRIMARY KEY (follower_user_id_fk, followee_user_id_fk),
  KEY idx_follows_followee (followee_user_id_fk),
  CONSTRAINT fk_follows_follower
    FOREIGN KEY (follower_user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_follows_followee
    FOREIGN KEY (followee_user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS likes (
  user_id_fk   CHAR(32)   NOT NULL,
  post_id_fk   CHAR(32)   NOT NULL,
  created_at   int(11)   NOT NULL,
  PRIMARY KEY (user_id_fk, post_id_fk),
  KEY idx_likes_post (post_id_fk),
  CONSTRAINT fk_likes_users
    FOREIGN KEY (user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_likes_posts
    FOREIGN KEY (post_id_fk) REFERENCES posts(post_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS comments (
  comment_id   CHAR(32)      NOT NULL,
  post_id_fk   CHAR(32)      NOT NULL,
  user_id_fk   CHAR(32)      NOT NULL,
  content      VARCHAR(280)  NOT NULL,
  is_blocked   TINYINT(1)    NOT NULL DEFAULT 0,
  is_deleted   TINYINT(1)    NOT NULL DEFAULT 0,
  created_at   int(11)      NOT NULL,
  updated_at   int(11)      NULL,
  PRIMARY KEY (comment_id),
  KEY idx_comments_post (post_id_fk),
  KEY idx_comments_user (user_id_fk),
  CONSTRAINT fk_comments_posts
    FOREIGN KEY (post_id_fk) REFERENCES posts(post_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_comments_users
    FOREIGN KEY (user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS password_resets (
  reset_id     CHAR(32)    NOT NULL,
  user_id_fk   CHAR(32)    NOT NULL,
  token        CHAR(64)    NOT NULL,
  expires_at   int(11)    NOT NULL,
  used_at      int(11)    NULL,
  created_at   int(11)    NOT NULL,
  PRIMARY KEY (reset_id),
  UNIQUE KEY uq_password_resets_token (token),
  KEY idx_password_resets_user (user_id_fk),
  CONSTRAINT fk_password_resets_users
    FOREIGN KEY (user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS email_verifications (
  verification_id  CHAR(32)   NOT NULL,
  user_id_fk       CHAR(32)   NOT NULL,
  token            CHAR(64)   NOT NULL,
  expires_at       int(11)   NOT NULL,
  verified_at      int(11)   NULL,
  created_at       int(11)   NOT NULL,
  PRIMARY KEY (verification_id),
  UNIQUE KEY uq_email_verifications_token (token),
  KEY idx_email_verifications_user (user_id_fk),
  CONSTRAINT fk_email_verifications_users
    FOREIGN KEY (user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS admin_logs (
  log_id            CHAR(32)     NOT NULL,
  admin_user_id_fk  CHAR(32)     NOT NULL,
  target_user_id_fk CHAR(32)     NULL,
  target_post_id_fk CHAR(32)     NULL,
  action_type       VARCHAR(50)  NOT NULL,
  reason            VARCHAR(255) NULL,
  created_at        int(11)     NOT NULL,
  PRIMARY KEY (log_id),
  KEY idx_admin_logs_admin (admin_user_id_fk),
  KEY idx_admin_logs_target_user (target_user_id_fk),
  KEY idx_admin_logs_target_post (target_post_id_fk),
  CONSTRAINT fk_admin_logs_admin_users
    FOREIGN KEY (admin_user_id_fk) REFERENCES users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_admin_logs_target_users
    FOREIGN KEY (target_user_id_fk) REFERENCES users(user_id)
    ON DELETE SET NULL,
  CONSTRAINT fk_admin_logs_target_posts
    FOREIGN KEY (target_post_id_fk) REFERENCES posts(post_id)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
