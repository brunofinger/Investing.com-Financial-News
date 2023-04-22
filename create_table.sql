CREATE TABLE dados_commodities (
    id INT NOT NULL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    tag VARCHAR(50) NOT NULL,
    image VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    text TEXT NOT NULL
);
