# Database connection setup

## Create database using your rdbms cli (**mysql recommended**)

- mysql

    ```shell
    mysql -u root -p
    ```
    you need to enter your password in opened prompt

- mycli
    ```shell
    mycli -u root -p <replace-your-password>
    ```

- after executing `mysql` or `mycli` (you can name database whatever you want)
    ```shell
    > create database transfermarkt;
    ```

## Create .env file

First at all we need to create `.env` file in project root because in `src/transfermarkt/db/schema.py` file we read database connection configuration from `.env` file. 

`.env` file should be like:


```
DB_USER="root"
DB_PASSWORD="<your-password>"
DB_HOST="localhost"
DB_PORT=3306
DB_NAME="transfermarkt"
```

## execute create_tables functions

execute python command in your terminal

```shell
python scripts/db_setup.py
```

**Done!** You can check tables created in given database