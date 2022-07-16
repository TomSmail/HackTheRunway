CREATE TABLE User(
	UserID INT AUTOINCREMENT PRIMARY_KEY,
	Email VARCHAR(100),
	PasswordHash VARCHAR(512),
	Address TEXT,
	ProfilePictureLink Text
);

CREATE TABLE Article(
	ArticleID INT AUTOINCREMENT PRIMARY_KEY,
	Color VARCHAR(30),
	TypeOfClothing VARCHAR(30),
	PriceRange INT, --categorised to discrete integers
	Condition INT, --categorised to discrete integers
);

CREATE TABLE User_Has(
	HasID INT AUTOINCREMENT PRIMARY_KEY,
	HasUserID INT,
	ArticleID INT,
	FOREIGN KEY HasUserID REFERENCES Users(UserID),
	FOREIGN KEY ArticleID REFERENCES Articles(ArticleID)
);

CREATE TABLE User_Wants(
	WantsID INT AUTOINCREMENT PRIMARY_KEY,
	WantsUserID INT,
	ArticleID INT,
	FOREIGN KEY WantsUserID REFERENCES Users(UserID),
	FOREIGN KEY ArticleID REFERENCES Articles(ArticleID)
);

CREATE TABLE MatchArticle(
	MatchID INT,
	HasID INT,
	WantsID INT,
	Status VARCHAR(10)
	FOREIGN KEY HasID REFERENCES User_Has(HasID),
	FOREIGN KEY WantsID REFERENCES User_Wants(WantsID)
);


#ActiveMatches(MatchID,Status)
MatchArticle(MatchID,HasID,WantsID,Status) #Status Agreed by both parties etc.
