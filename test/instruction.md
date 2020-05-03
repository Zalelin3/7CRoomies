# Loading Local Test Files onto MySQL Database

*Disclaimer: I use Windows and I do everything in command prompts.*

1. Run the server (may need to run command line as admin):
`"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --console --local_infile=ON`
Replace path with wherever you installed MySQL.

2. Make sure the database is set up & has the schema we want. Follow Shihao’s instructions (the flask db init, migrate, upgrade part). If the schema doesn't match, the files won't load.

3. In the command line, we’ll modify the database as a client with all permissions.
    * `"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" --local-infile=1 -u root -p` and enter whatever password you chose for MySQL initially.
    * `mysql> SET GLOBAL local_infile=1;`
    * `use dreamteam_db` to work with our database.
    * `show tables` and make sure the tables are all there.
    * Load the data from local files I’ve pushed to github within this order:
    * `load data local infile 'C:/Users/Lin/7CRoomies/test/test/posts.txt' into table posts lines terminated by '\r\n';`
    * The rest can be loaded in any order. Just replace the name of txt file with the right file and the replace table name with the corresponding table.
Note: There may be a few warnings raised. If it’s 1-2, it’s fine. If it’s like a hundred, it’s not reading the data in properly. You can use show warnings to see what’s going wrong.

4. The data should be in the tables and ready to be used. You can copy and paste the following SQL commands. They should return 3 and 2 respectively, and their sum is the number of spots already taken in a post.

```
select count(ghost_user.email)
from user, ghost_user, lives
where lives.user_id = user.id
and lives.post_id = 3
and lives.status = 3
and ghost_user.representer_id = user.id;

select count(user.id)
from user, lives
where lives.user_id = user.id
and lives.post_id = 3
and lives.status = 3;
```

Food for thought: Is there a way to combine these two queries into one? Ideally, we want to have a pair of each post and the sum of these two results.
