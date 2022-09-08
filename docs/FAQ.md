
# Frequently Asked Questions

<br>

### My dump doesn't migrate.

*This assumes a running setup.*

<br>

1.  Enter into database container:

    ```sh
    docker exec                 \
        --interactive           \
        --username=nano         \
        --tty kemono-db psql    \
        kemonodb
    ```

    <br>

2.  Check the contents of the  `posts`  table.
    
    ```sql
    SELECT * FROM posts;
    ```
    
    *Most likely it has  `0`  rows.*

    <br>

3.  Move contents of  `booru_posts`  ➞  `posts`
    
    ```sql
    INSERT INTO posts SELECT * FROM booru_posts ON CONFLICT DO NOTHING;
    ```

    <br>

4.  Restart the archiver.
    
    ```sh
    docker restart kemono-archiver
    ```
    
    If you see a bunch of log entries from  `kemono-db` , <br>
    then this indicates that the archiver is doing it's job.

    <br>

5.  In case the frontend still doesn't show <br>
    the artists / posts, clear the redis cache.
    
    ```sh
    docker exec         \
        kemono-redis    \
        redis-cli       \
        FLUSHALL
    ```

<br>
<br>

### How do I git modules?

*This assumes you haven't cloned the repository recursively.*

<br>

1.  Initiate the submodules

    ```sh
    git submodule init
    git submodule update    \
        --recursive         \
        --init 
    ```

    <br>

2.  Switch to the archiver folder and <br>
    add your fork to the remotes list.
    
    ```sh
    cd archiver
    git remote add <remote_name> <your_fork_link>
    ```
    <br>
    
3.  Now you can interact with Kitsune repo the same <br>
    way you do as if it was outside of project folder.

<br>
<br>

### How do I import from db dump?

<br>

1.  Retrieve a database dump.

    <br>

2.  Run the following in the folder of said dump.
    
    ```sh
    cat db-filename.dump                \
        | gunzip                        \
        | docker exec                   \
        --interactive kemono-db psql    \
        --username=nano kemonodb
    ```
    
    <br>
    
3.  Restart the archiver to trigger migrations.
    
    ```sh
    docker restart kemono-archiver
    ```
    
    <br>
    
    If that didn't start the migrations, refer <br>
    to  [`My Dump Doesn't Migrate`]  section.

<br>
<br>

### How do I put files into nginx container?

<br>

1.  Retrieve the files in required folder structure.

    <br>

2.  Copy them into nginx image.
    
    ```sh
    docker \
        cp ./ kemono-nginx:/storage
    ```
    
    <br>
    
3.  Add required permissions to that folder.
    
    ```sh
    docker                  \
        exec kemono-nginx   \
        chown --recursive   \
        nginx /storage
    ```
    
<br>


<!----------------------------------------------------------------------------->

[`My Dump Doesn't Migrate`]: #my-dump-doesnt-migrate

