CREATE TABLE "User" (
	UserID SERIAL PRIMARY KEY NOT NULL,
	Email VARCHAR(100) UNIQUE NOT NULL,
	Firstname VARCHAR(100) NOT NULL,
	Lastname VARCHAR(100) NOT NULL,
	PasswordHash VARCHAR(512) NOT NULL,
	Points INT,
	Address TEXT,
	ProfilePictureLink Text
);

CREATE TABLE "Tags" (
	TagID SERIAL PRIMARY KEY,
	Word VARCHAR(30)
);

CREATE TABLE "Article" (
	ArticleID SERIAL PRIMARY KEY NOT NULL,
	Color VARCHAR(30) NOT NULL,
	TypeOfClothing VARCHAR(30) NOT NULL,
	PriceRange INT, --categorised to discrete integers
	Condition INT --categorised to discrete integers
);

CREATE TABLE "User_Has" (
	HasID SERIAL PRIMARY KEY NOT NULL,
	HasUserID INT REFERENCES "User"(UserID) ,
	ArticleID INT REFERENCES "Article"(ArticleID),
	ImageOfItem Text,
	Cotton BOOLEAN,
	LocationMade TEXT
);

CREATE TABLE "User_Wants" (
	WantsID SERIAL PRIMARY KEY NOT NULL,
	WantsUserID INT REFERENCES "User"(UserID) ,
	ArticleID INT REFERENCES "Article"(ArticleID) 
);

CREATE TABLE "Match_Article" (
	MatchArticleID SERIAL PRIMARY KEY NOT NULL,
	MatchID INT NOT NULL,
	HasID INT REFERENCES "User_Has"(HasID),
	WantsID INT REFERENCES "User_Wants"(WantsID) ,
	Status VARCHAR(10) NOT NULL 
);

CREATE TABLE "User_Has_Tag" (
	HasID INT REFERENCES "User_Has"(HasID),
	TagID INT REFERENCES "Tags"(TagID)
);





SELECT * FROM information_schema.tables WHERE table_schema = 'public';

