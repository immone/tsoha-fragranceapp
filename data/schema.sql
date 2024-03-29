CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE fragrances (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER references users,
    name TEXT,
    designer TEXT,
    nose TEXT,
    description TEXT,
    notes TEXT,
    created_in INTEGER,
    visible BOOLEAN
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    fragrance_id INTEGER references fragrances,
    visible BOOLEAN
);

CREATE TABLE designers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN
);

CREATE TABLE perfumers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN
);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER references users,
    fragrance_id INTEGER references fragrances
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    rating INTEGER,
    sent_at TIMESTAMP,
    fragrance_id INTEGER references fragrances,
    user_id INTEGER references users,
    visible BOOLEAN
);
