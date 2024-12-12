-- +migrate Up
CREATE TABLE webscraper_contents (
    id SERIAL PRIMARY KEY,
    document_id UUID NOT NULL UNIQUE,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL
);

-- +migrate Down
DROP TABLE IF EXISTS webscraper_contents;
