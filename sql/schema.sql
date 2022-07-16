CREATE TABLE "User" (
	UserID SERIAL PRIMARY KEY NOT NULL,
	Email VARCHAR(100),
	PasswordHash VARCHAR(512),
	Address TEXT,
	ProfilePictureLink Text
);

CREATE TABLE "Article" (
	ArticleID SERIAL PRIMARY KEY,
	Color VARCHAR(30),
	TypeOfClothing VARCHAR(30),
	PriceRange INT, --categorised to discrete integers
	Condition INT --categorised to discrete integers
);

CREATE TABLE "User_Has" (
	HasID SERIAL PRIMARY KEY,
	HasUserID INT REFERENCES "User"(UserID),
	ArticleID INT REFERENCES "Article"(ArticleID),
);

CREATE TABLE "User_Wants" (
	WantsID SERIAL PRIMARY KEY,
	WantsUserID INT REFERENCES "User"(UserID),
	ArticleID INT REFERENCES "Article"(ArticleID)
);

CREATE TABLE "Match_Article" (
	MatchArticleID SERIAL PRIMARY KEY,
	MatchID INT,
	HasID INT REFERENCES "User_Has"(HasID),
	WantsID INT REFERENCES "User_Wants"(WantsID),
	Status VARCHAR(10) 
);

CREATE TABLE "User_Has_Tag" (
	HasID INT REFERENCES "User_Has"(HasID),
	TagID INT REFERENCES "Tags"(TagID)
);


CREATE TABLE "Tags" (
	TagID SERIAL PRIMARY KEY,
	Word VARCHAR(30)
);


SELECT * FROM information_schema.tables WHERE table_schema = 'public';

