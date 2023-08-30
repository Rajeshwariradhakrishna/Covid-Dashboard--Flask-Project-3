-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE Countries (
    Country VARCHAR   NOT NULL,
    WHO_Region VARCHAR   NOT NULL,
    CONSTRAINT pk_Countries PRIMARY KEY (
        Country
     )
);

CREATE TABLE Cases (
    Country VARCHAR   NOT NULL,
    WHO_Region VARCHAR   NOT NULL,
    Cases_Cumulative_Total BIGINT   NOT NULL,
    New_Cases_Last_7_Days INT   NOT NULL,
    Deaths_Cumulative_Total BIGINT   NOT NULL,
    New_Deaths_Last_7_Days INT NOT NULL,
	Latitude DOUBLE PRECISION NOT NULL,
	Longitude DOUBLE PRECISION NOT NULL,
	CASE_ID SERIAL PRIMARY KEY
);

CREATE TABLE Vaccinations (
    Country VARCHAR   NOT NULL,
    WHO_Region VARCHAR   NOT NULL,
    Date_Updated DATE   NOT NULL,
    Total_Vaccinations BIGINT   NOT NULL,
    Persons_Vaccinated_Plus1_Dose INT   NOT NULL,
    First_Vaccine_Date DATE,
    Persons_Booster_Add_Dose INT,
	VAX_ID SERIAL PRIMARY KEY
);

ALTER TABLE Cases ADD CONSTRAINT fk_Cases_Country FOREIGN KEY(Country)
REFERENCES Countries (Country);

ALTER TABLE Vaccinations ADD CONSTRAINT fk_Vaccinations_Country FOREIGN KEY(Country)
REFERENCES Countries (Country);


-- Select Data from Tables --
SELECT * FROM Countries;
SELECT * FROM Cases;
SELECT * FROM Vaccinations;





