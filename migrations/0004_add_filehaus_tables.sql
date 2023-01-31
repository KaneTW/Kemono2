create sequence "public"."shares_id_seq";


create table "public"."file_share_relationships" (
    "share_id" integer not null,
    "upload_url" character varying not null,
    "upload_id" character varying not null,
    "file_id" integer,
    "filename" character varying not null
);


create table "public"."lookup_share_relationships" (
    "share_id" integer not null,
    "service" character varying not null,
    "user_id" character varying not null
);


create table "public"."shares" (
    "id" integer not null default nextval('shares_id_seq'::regclass),
    "name" character varying not null,
    "description" character varying not null,
    "uploader" integer,
    "added" timestamp without time zone not null default CURRENT_TIMESTAMP
);


alter sequence "public"."shares_id_seq" owned by "public"."shares"."id";

CREATE INDEX file_share_id_idx ON public.file_share_relationships USING btree (share_id);

CREATE UNIQUE INDEX file_share_relationships_pkey ON public.file_share_relationships USING btree (share_id, upload_id);

CREATE UNIQUE INDEX lookup_share_relationships_pkey ON public.lookup_share_relationships USING btree (share_id, service, user_id);

CREATE INDEX shares_added_idx ON public.shares USING btree (added);

CREATE UNIQUE INDEX shares_pkey ON public.shares USING btree (id);

CREATE INDEX shares_uploader_idx ON public.shares USING btree (uploader);

alter table "public"."file_share_relationships" add constraint "file_share_relationships_pkey" PRIMARY KEY using index "file_share_relationships_pkey";

alter table "public"."lookup_share_relationships" add constraint "lookup_share_relationships_pkey" PRIMARY KEY using index "lookup_share_relationships_pkey";

alter table "public"."shares" add constraint "shares_pkey" PRIMARY KEY using index "shares_pkey";

alter table "public"."file_share_relationships" add constraint "file_share_relationships_file_id_fkey" FOREIGN KEY (file_id) REFERENCES files(id);

alter table "public"."file_share_relationships" add constraint "file_share_relationships_share_id_fkey" FOREIGN KEY (share_id) REFERENCES shares(id);

alter table "public"."lookup_share_relationships" add constraint "lookup_share_relationships_service_user_id_fkey" FOREIGN KEY (service, user_id) REFERENCES lookup(service, id);

alter table "public"."lookup_share_relationships" add constraint "lookup_share_relationships_share_id_fkey" FOREIGN KEY (share_id) REFERENCES shares(id);

alter table "public"."shares" add constraint "shares_uploader_fkey" FOREIGN KEY (uploader) REFERENCES account(id);

