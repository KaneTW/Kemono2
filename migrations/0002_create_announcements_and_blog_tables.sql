create sequence "public"."announcements_id_seq";

create sequence "public"."blog_posts_id_seq";

create table "public"."announcements" (
    "id" integer not null default nextval('announcements_id_seq'::regclass),
    "created_at" timestamp without time zone not null default CURRENT_TIMESTAMP,
    "content" text not null
);


create table "public"."blog_posts" (
    "id" integer not null default nextval('blog_posts_id_seq'::regclass),
    "author" character varying not null,
    "title" character varying not null,
    "content" text not null,
    "created_at" timestamp without time zone not null default CURRENT_TIMESTAMP,
    "cover_image" integer
);


create table "public"."file_blog_post_relationships" (
    "blog_post_id" integer not null,
    "file_id" integer not null
);


alter sequence "public"."announcements_id_seq" owned by "public"."announcements"."id";

alter sequence "public"."blog_posts_id_seq" owned by "public"."blog_posts"."id";

CREATE UNIQUE INDEX announcements_pkey ON public.announcements USING btree (id);

CREATE UNIQUE INDEX blog_posts_pkey ON public.blog_posts USING btree (id);

CREATE UNIQUE INDEX file_blog_post_relationships_pkey ON public.file_blog_post_relationships USING btree (file_id, blog_post_id);

alter table "public"."announcements" add constraint "announcements_pkey" PRIMARY KEY using index "announcements_pkey";

alter table "public"."blog_posts" add constraint "blog_posts_pkey" PRIMARY KEY using index "blog_posts_pkey";

alter table "public"."file_blog_post_relationships" add constraint "file_blog_post_relationships_pkey" PRIMARY KEY using index "file_blog_post_relationships_pkey";

alter table "public"."blog_posts" add constraint "blog_posts_cover_image_fkey" FOREIGN KEY (cover_image) REFERENCES files(id);

alter table "public"."file_blog_post_relationships" add constraint "file_blog_post_relationships_blog_post_id_fkey" FOREIGN KEY (blog_post_id) REFERENCES blog_posts(id);

alter table "public"."file_blog_post_relationships" add constraint "file_blog_post_relationships_file_id_fkey" FOREIGN KEY (file_id) REFERENCES files(id);

