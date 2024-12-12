CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE query_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- +migrate Down
DROP TABLE IF EXISTS query_history;

CREATE INDEX query_history_embedding_idx ON query_history USING ivfflat (embedding) WITH (lists = 100);

