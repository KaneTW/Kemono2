create table account (
    id serial primary key,
    username varchar not null,
    password_hash varchar not null,
    created_at timestamp without time zone not null default CURRENT_TIMESTAMP,
    role varchar default 'consumer',
    unique (username)
);

create table account_artist_favorite (
    id serial primary key,
    account_id int not null references account(id),
    service varchar not null,
    artist_id varchar not null,
    unique (account_id, service, artist_id)
);

create table account_post_favorite (
    id serial primary key,
    account_id int not null references account(id),
    service varchar not null,
    artist_id varchar not null,
    post_id varchar not null,
    unique (account_id, service, artist_id, post_id)
);

create table booru_flags (
    id varchar not null,
    "user" varchar not null,
    service varchar not null
);

create table comments (
    id varchar not null,
    post_id varchar not null,
    parent_id varchar,
    commenter varchar not null,
    service varchar not null,
    content text not null default '',
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    primary key (id, service)
);

create table discord_posts (
    id varchar not null,
    author jsonb not null,
    server varchar not null,
    channel varchar not null,
    content text not null default '',
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    edited timestamp without time zone,
    embeds jsonb[] not null,
    mentions jsonb[] not null,
    attachments jsonb[] not null,
    primary key (id, server, channel)
);

create table dms (
    id varchar not null,
    "user" varchar not null,
    service varchar not null,
    content text not null default '',
    embed jsonb not null default '{}',
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    file jsonb not null,
    primary key (id, service)
);

create table dnp (
    id varchar not null,
    service varchar not null,
    import boolean not null default false
);

create table files (
    id serial primary key,
    hash varchar not null,
    mtime timestamp without time zone not null,
    ctime timestamp without time zone not null,
    mime varchar,
    ext varchar,
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    size bigint,
    ihash varchar,
    unique (hash)
);

create table file_discord_message_relationships (
    file_id int not null references files(id),
    filename varchar not null,
    server varchar not null,
    channel varchar not null,
    id varchar not null,
    contributor_id int,
    primary key (file_id, server, channel, id)
);

create table file_post_relationships (
    file_id int not null references files(id),
    filename varchar not null,
    service varchar not null,
    "user" varchar not null,
    post varchar not null,
    contributor_id int references account(id),
    inline boolean not null default false,
    primary key (file_id, service, "user", post)
);

create table file_server_relationships (
    file_id int not null references files(id),
    remote_path character varying not null
);


create table lookup (
    id varchar not null,
    name varchar not null,
    service varchar not null,
    indexed timestamp without time zone not null default CURRENT_TIMESTAMP,
    updated timestamp without time zone not null default CURRENT_TIMESTAMP,
    primary key (id, service)
);

create table notifications (
    id bigserial primary key,
    account_id int not null,
    type smallint not null,
    extra_info jsonb,
    created_at timestamp without time zone not null default CURRENT_TIMESTAMP,
    is_seen boolean not null default false,
    foreign key (account_id) references account(id)
);

create table posts (
    id varchar not null,
    "user" varchar not null,
    service varchar not null,
    title text not null default '',
    content text not null default '',
    embed jsonb not null default '{}',
    shared_file boolean not null default false,
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    edited timestamp without time zone,
    file jsonb not null,
    attachments jsonb[] not null,
    primary key (id, service)
);

create table revisions (
    revision_id serial primary key,
    id varchar not null,
    "user" varchar not null,
    service varchar not null,
    title text not null default '',
    content text not null default '',
    embed jsonb not null default '{}',
    shared_file boolean not null default false,
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    edited timestamp without time zone,
    file jsonb not null,
    attachments jsonb[] not null
);

create table saved_session_key_import_ids (
    key_id integer not null,
    import_id character varying not null,
    unique (key_id, import_id)
);

create table saved_session_keys_with_hashes (
    id serial primary key,
    service varchar not null,
    discord_channel_ids varchar,
    encrypted_key varchar not null,
    hash varchar not null,
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    dead boolean not null default false,
    contributor_id int,
    unique (service, hash)
);

create table unapproved_dms (
    import_id varchar not null,
    id varchar not null,
    "user" varchar not null,
    service varchar not null,
    content text not null default ''::text,
    embed jsonb not null default '{}'::jsonb,
    added timestamp without time zone not null default CURRENT_TIMESTAMP,
    published timestamp without time zone,
    file jsonb not null,
    contributor_id varchar,
    primary key (id, service)
);

create table posts_added_max (
    "user" varchar not null,
    service varchar not null,
    added timestamp without time zone not null,
    primary key ("user", service)
);

create index account_artist_favorite_service_artist_id_idx on account_artist_favorite using btree (service, artist_id);

create index account_idx on account using btree (username, created_at, role);

create index account_post_favorite_service_artist_id_post_id_idx on account_post_favorite using btree (service, artist_id, post_id);

create index added_idx on posts using btree (added);

create index channel_idx on discord_posts using hash (channel);

create index comment_idx on comments using btree (post_id);

create index discord_id_idx on discord_posts using hash (id);

create index dm_idx on dms using btree ("user");

create index dm_search_idx on dms using gin (to_tsvector('english'::regconfig, content));

create index file_discord_id_idx on file_discord_message_relationships using btree (file_id);

create index file_discord_message_channel_idx on file_discord_message_relationships using btree (channel);

create index file_discord_message_contributor_id_idx on file_discord_message_relationships using btree (contributor_id);

create index file_discord_message_id_idx on file_discord_message_relationships using btree (id);

create index file_discord_message_server_idx on file_discord_message_relationships using btree (server);

create index file_id_idx on file_post_relationships using btree (file_id);

create index file_post_contributor_id_idx on file_post_relationships using btree (contributor_id);

create index file_post_id_idx on file_post_relationships using btree (post);

create index file_post_service_idx on file_post_relationships using btree (service);

create index file_post_user_idx on file_post_relationships using btree ("user");

create index flag_id_idx on booru_flags using btree (id);

create index flag_service_idx on booru_flags using btree (service);

create index flag_user_idx on booru_flags using btree ("user");

create index id_idx on posts using hash (id);

create index notifications_account_id_idx on notifications using btree (account_id);

create index notifications_created_at_idx on notifications using btree (created_at);

create index notifications_type_idx on notifications using btree (type);

create index published_idx on posts using btree (published);

create index saved_session_keys_with_hashes_contributor_idx on saved_session_keys_with_hashes using btree (contributor_id);

create index saved_session_keys_with_hashes_dead_idx on saved_session_keys_with_hashes using btree (dead);

create index search_idx on posts using gin (to_tsvector('english'::regconfig, ((content || ' '::text) || title)));

create index server_idx on discord_posts using hash (server);

create index service_idx on posts using btree (service);

create index unapproved_dm_idx on unapproved_dms using btree (import_id);

create index updated_idx on lookup using btree (updated);

create index user_idx on posts using btree ("user");

CREATE OR REPLACE FUNCTION POSTS_ADDED_MAX()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO posts_added_max (service, "user", added)
  VALUES(NEW.service, NEW."user", NEW.added)
  ON CONFLICT (service, "user") DO
    UPDATE SET added = NEW.added WHERE NEW.added > OLD.added;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER POSTS_ADDED_MAX AFTER UPDATE OR INSERT
ON posts FOR EACH ROW EXECUTE PROCEDURE POSTS_ADDED_MAX();
