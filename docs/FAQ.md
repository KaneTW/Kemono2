## Frequently Asked Questions

### __My dump doesn't migrate.__
Assuming the running setup:

1. Enter into database container:
    ```sh
    docker exec --interactive --tty kemono-db psql --username=nano kemonodb
    ```
2. Check the contents of the `posts` table:
    ```sql
    SELECT * FROM posts;
    ```
    Most likely it has 0 rows.
3. Move contents of `booru_posts` to `posts`:
    ```sql
    INSERT INTO posts SELECT * FROM booru_posts ON CONFLICT DO NOTHING;
    ```
4. Restart the archiver:
    ```sh
    docker restart kemono-archiver
    ```
    If you see a bunch of log entries from `kemono-db`, then it means archiver is doing the job.
5. In case the frontend still doesn't show the artists/posts, clear redis cache:
    ```sh
    docker exec kemono-redis redis-cli FLUSHALL
    ```
### __How do I git modules?__
Assuming you haven't cloned the repo recursively for whatever reason:
1. Initiate the submodules
    ```sh
    git submodule init
    git submodule update --init --recursive
    ```
2. Switch to archiver folder and add your fork to the remotes list:
    ```sh
    cd archiver
    git remote add <remote_name> <your_fork_link>
    ```
3. Now you can interact with Kitsune repo the same way you do as if it was outside of project folder.

### __How do I import from db dump?__
1. Retrieve a database dump.
2. Run this command in the folder of said dump:
    ```sh
    cat db-filename.dump | gunzip | docker exec --interactive kemono-db psql --username=nano kemonodb
    ```
3. Restart the archiver to trigger migrations:
    ```sh
    docker restart kemono-archiver
    ```
    If that didn't start the migrations, refer to [FAQ section](#my-dump-doesnt-migrate) for manual instructions.

### __How do I put files into nginx container?__
1. Retrieve the files in required folder structure.
2. Copy them into nginx image:
    ```sh
    docker cp ./ kemono-nginx:/storage
    ```
3. Add required permissions to that folder:
    ```sh
    docker exec kemono-nginx chown --recursive nginx /storage
    ```
