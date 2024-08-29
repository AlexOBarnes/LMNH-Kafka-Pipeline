-- Code for creating databases and seeding tables

DROP TABLE IF EXISTS exhibition CASCADE;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS museum_floor;
DROP TABLE IF EXISTS rating CASCADE;
DROP TABLE IF EXISTS rating_interaction;
DROP TABLE IF EXISTS request CASCADE;
DROP TABLE IF EXISTS request_interaction;

CREATE TABLE department(
    department_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE museum_floor(
    floor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    floor_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE request(
    request_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    request_value INT UNIQUE NOT NULL,
    request_description VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE rating(
    rating_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rating_value INT UNIQUE NOT NULL,
    rating_description VARCHAR(100) UNIQUE NOT NULL 
);

CREATE TABLE exhibition(
    exhibition_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    public_id TEXT UNIQUE NOT NULL,
    exhibition_name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    floor_id INT NOT NULL,
    exhibit_start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    exhibit_description TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (floor_id) REFERENCES museum_floor(floor_id)
);

CREATE TABLE request_interaction(
    request_interaction_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    request_id INT NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id),
    CONSTRAINT invalid_date CHECK (created_at <= CURRENT_TIMESTAMP)
);

CREATE TABLE rating_interaction(
    rating_interaction_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rating_id INT NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id),
    CONSTRAINT invalid_date CHECK (created_at <= CURRENT_TIMESTAMP)
);

INSERT INTO rating(rating_value, rating_description) VALUES
(0,'Terrible'),
(1,'Bad'),
(2,'Neutral'),
(3,'Good'),
(4,'Amazing');

INSERT INTO department(department_name) VALUES
('Entomology'),
('Ecology'),
('Zoology'),
('Paleontology'),
('Geology');

INSERT INTO museum_floor(floor_name) VALUES
('1'),
('2'),
('3'),
('Vault');

INSERT INTO request(request_value, request_description) VALUES
(0,'Assistance'),
(1,'Emergency');

INSERT INTO exhibition(public_id, exhibition_name, department_id, floor_id, exhibit_start_date, exhibit_description) VALUES
('EXH_00','Measureless to Man',5,1,'2021/08/23','An immersive 3D experience: delve deep into a previously-inaccessible cave system.'),
('EXH_01', 'Adaptation', 1,4,'2019/07/01','How insect evolution has kept pace with an industrialised world'),
('EXH_02','The Crenshaw Collection',3,2, '2021/03/03','An exhibition of 18th Century watercolours, mostly focused on South American wildlife.'),
('EXH_03','Cetacean Sensations',3,1,'2019/07/01','Whales: from ancient myth to critically endangered.'),
('EXH_04','Our Polluted World',2,3,'2021/05/12','A hard-hitting exploration of humanity''s impact on the environment.'),
('EXH_05','Thunder Lizards',4,1,'2023/02/01','How new research is making scientists rethink what dinosaurs really looked like.');