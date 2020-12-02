-- TODO: Implement tagging/ratings/revisions
-- Goal for now is just to get Kemono working in SQL.

-- Posts
CREATE TABLE IF NOT EXISTS booru_posts (
  "id" varchar(255) NOT NULL,
  "user" varchar(255) NOT NULL,
  "service" varchar(20) NOT NULL,
  "title" text NOT NULL DEFAULT '',
  "content" text NOT NULL DEFAULT '',
  "embed" jsonb NOT NULL DEFAULT '{}',
  "shared_file" boolean NOT NULL DEFAULT '0',
  "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "published" timestamp,
  "edited" timestamp,
  "file" jsonb NOT NULL,
  "attachments" jsonb[] NOT NULL
);
CREATE INDEX IF NOT EXISTS id_idx ON booru_posts USING hash ("id");
CREATE INDEX IF NOT EXISTS user_idx ON booru_posts USING btree ("user");
CREATE INDEX IF NOT EXISTS service_idx ON booru_posts USING btree ("service");
CREATE INDEX IF NOT EXISTS added_idx ON booru_posts USING btree ("added");
CREATE INDEX IF NOT EXISTS published_idx ON booru_posts USING btree ("published");
CREATE INDEX IF NOT EXISTS updated_idx ON booru_posts USING btree ("user", "service", "added");

-- Booru bans
CREATE TABLE IF NOT EXISTS dnp (
  "id" varchar(255) NOT NULL,
  "service" varchar(20) NOT NULL
);

-- Posts (Discord)
CREATE TABLE IF NOT EXISTS discord_posts (
  "id" varchar(255) NOT NULL,
  "author" jsonb NOT NULL,
  "server" varchar(255) NOT NULL,
  "channel" varchar(255) NOT NULL,
  "content" text NOT NULL DEFAULT '',
  "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "published" timestamp,
  "edited" timestamp,
  "embeds" jsonb[] NOT NULL,
  "mentions" jsonb[] NOT NULL,
  "attachments" jsonb[] NOT NULL
);
CREATE INDEX IF NOT EXISTS discord_id_idx ON discord_posts USING hash ("id");
CREATE INDEX IF NOT EXISTS server_idx ON discord_posts USING hash ("server");
CREATE INDEX IF NOT EXISTS channel_idx ON discord_posts USING hash ("channel");

-- Flags
CREATE TABLE IF NOT EXISTS booru_flags (
  "id" varchar(255) NOT NULL,
  "user" varchar(255) NOT NULL,
  "service" varchar(20) NOT NULL
);

-- Lookup
CREATE TABLE IF NOT EXISTS lookup (
  "id" varchar(255) NOT NULL,
  "name" varchar(255) NOT NULL,
  "service" varchar(20) NOT NULL,
  "indexed" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS name_idx ON lookup USING btree ("name");
CREATE INDEX IF NOT EXISTS lookup_id_idx ON lookup USING btree ("id");
CREATE INDEX IF NOT EXISTS lookup_service_idx ON lookup USING btree ("service");
CREATE INDEX IF NOT EXISTS lookup_indexed_idx ON lookup USING btree ("indexed");

-- Board
CREATE TABLE IF NOT EXISTS board_replies (
  "reply" integer NOT NULL,
  "in" integer NOT NULL
);

-- Requests
DO $$ BEGIN
  CREATE TYPE request_status AS ENUM ('open', 'fulfilled', 'closed');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;
CREATE TABLE IF NOT EXISTS requests (
  "id" SERIAL PRIMARY KEY,
  "service" varchar(20) NOT NULL,
  "user" varchar(255) NOT NULL,
  "post_id" varchar(255),
  "title" text NOT NULL,
  "description" text NOT NULL DEFAULT '',
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "image" text,
  "price" numeric NOT NULL,
  "votes" integer NOT NULL DEFAULT 1,
  "ips" text[] NOT NULL,
  "status" request_status NOT NULL DEFAULT 'open'
);
CREATE INDEX IF NOT EXISTS request_title_idx ON requests USING btree ("title");
CREATE INDEX IF NOT EXISTS request_service_idx ON requests USING btree ("service");
CREATE INDEX IF NOT EXISTS request_votes_idx ON requests USING btree ("votes");
CREATE INDEX IF NOT EXISTS request_created_idx ON requests USING btree ("created");
CREATE INDEX IF NOT EXISTS request_price_idx ON requests USING btree ("price");
CREATE INDEX IF NOT EXISTS request_status_idx ON requests USING btree ("status");

-- Request Subscriptions
CREATE TABLE IF NOT EXISTS request_subscriptions (
  "request_id" numeric NOT NULL,
  "endpoint" text NOT NULL,
  "expirationTime" numeric,
  "keys" jsonb NOT NULL
);
CREATE INDEX IF NOT EXISTS request_id_idx ON request_subscriptions USING btree ("request_id");

-- Logs
CREATE TABLE IF NOT EXISTS logs (
  "log0" text NOT NULL,
  "log" text[] NOT NULL,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS log_idx ON logs USING GIN (to_tsvector('english', log0));