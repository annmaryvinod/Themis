-- +migrate Up
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    document_id UUID NOT NULL,
    chunk TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL
);

-- +migrate Down
DROP TABLE IF EXISTS embeddings;
