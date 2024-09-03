CREATE TABLE kbu_bot.sound (
	id_sound INT auto_increment NOT NULL,
	name_sound TEXT NOT NULL,
	CONSTRAINT sound_pk PRIMARY KEY (id_sound)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;