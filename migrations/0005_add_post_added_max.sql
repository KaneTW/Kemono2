create table "public"."posts_added_max" (
    "user" character varying not null,
    "service" character varying not null,
    "added" timestamp without time zone not null
);

CREATE UNIQUE INDEX posts_added_max_pkey ON public.posts_added_max USING btree ("user", service);

alter table "public"."posts_added_max" add constraint "posts_added_max_pkey" PRIMARY KEY using index "posts_added_max_pkey";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.posts_added_max()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  INSERT INTO posts_added_max (service, "user", added)
  VALUES(NEW.service, NEW."user", NEW.added)
  ON CONFLICT (service, "user") DO
    UPDATE SET added = NEW.added WHERE NEW.added > OLD.added;
  RETURN NULL;
END;
$function$
;

CREATE TRIGGER posts_added_max AFTER INSERT OR UPDATE ON public.posts FOR EACH ROW EXECUTE FUNCTION posts_added_max();

INSERT INTO posts_added_max ("user", service, added) SELECT "user", service, max(added) AS added FROM posts GROUP BY "user", service ORDER BY added;
