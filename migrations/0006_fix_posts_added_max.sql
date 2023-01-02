set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.posts_added_max()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  INSERT INTO posts_added_max AS pam ("user", service, added)
    SELECT "user", service, max(added) AS added FROM posts
     WHERE posts.service = NEW.service
     AND posts."user" = NEW."user"
    GROUP BY "user", service
  ON CONFLICT (service, "user")
    DO UPDATE SET added = EXCLUDED.added
    WHERE EXCLUDED.added > pam.added;
  RETURN NULL;
END;
$function$
;
