-- Tables for the TodoApp
CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	email TEXT UNIQUE,
	first_name TEXT,
	last_name TEXT,
	hashed_password TEXT,
	is_active INTEGER DEFAULT 1,
	role TEXT);
	
CREATE TABLE todos (
	id INTEGER PRIMARY KEY,
	title TEXT,
	description TEXT,
	priority INTEGER,
	complete INTEGER DEFAULT 0,
	owner_id INTEGER,
	FOREIGN KEY(owner_id) REFERENCES users(id));