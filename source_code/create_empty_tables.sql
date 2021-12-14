drop table if exists cursors;
drop table if exists articles;
drop table if exists authors;
drop table if exists comments;
drop table if exists avatars;

create table articles (
	article_id VARCHAR(50) NOT NULL,
	article_name VARCHAR(10) default "",
	PRIMARY KEY (article_id)
);

create table cursors (
	cursor_id VARCHAR(50) NOT NULL,
	has_next VARCHAR(10),
	has_prev VARCHAR(10),
	cursor_more VARCHAR(10),
	next_cursor_id VARCHAR(50),
	prev_cursor_id VARCHAR(50),
	article_id VARCHAR(50) NOT NULL, 
	datetime VARCHAR(50),
	PRIMARY KEY (cursor_id),
	FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

create table authors (
	author_id VARCHAR(50) NOT NULL,
	username VARCHAR(50),
	about VARCHAR(10),
	author_name VARCHAR(50),
	disable_trackers VARCHAR(10),
	is_power_contributor VARCHAR(10),
	joined_at VARCHAR(50),
	profile_url VARCHAR(100), 
	is_private VARCHAR(10),
	is_primary VARCHAR(10),
	is_anonymous VARCHAR(10),
	url VARCHAR(100),
	location VARCHAR(50),
	PRIMARY KEY (author_id)
);

create table comments (
	comment_id VARCHAR(50) NOT NULL,
	comment_likes INT,
	comment_dislikes INT,
	num_reports INT,
	created_at VARCHAR(50),
	editable_until VARCHAR(50),
	message VARCHAR(500), 
	is_spam VARCHAR(10),
	is_deleted VARCHAR(10),
	is_deleted_by_author VARCHAR(10),
	is_approved VARCHAR(10),
	is_flagged VARCHAR(10),
	raw_message VARCHAR(500),
	is_highlighted VARCHAR(10),
	can_vote VARCHAR(10),
	points INT,
	is_edited VARCHAR(10),
	sb VARCHAR(50),
	forum VARCHAR(50),
	thread VARCHAR(50),
	cursor_id VARCHAR(50) NOT NULL,
	author_id VARCHAR(50) NOT NULL,
	parent_comment_id VARCHAR(50),
	PRIMARY KEY (comment_id),
	FOREIGN KEY (cursor_id) REFERENCES cursors(cursor_id),
	FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

create table avatars (
	author_id VARCHAR(50) NOT NULL,
	permalink VARCHAR(200),
	small_permalink VARCHAR(200),
	small_cache VARCHAR(50),
	large_permalink VARCHAR(200),
	large_cache VARCHAR(50),
	PRIMARY KEY (author_id)
);
