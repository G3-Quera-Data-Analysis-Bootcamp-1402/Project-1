# Database Connection Setup

## Install EdgeDB cli

please follow [EdgeDB](https://www.edgedb.com)'s installation instructions 

## Run `migration` and `migrate` commands

After cloning the project please go to `src/transfermarkt/db` directory, then execute these commands

1.
    ```shell
    edgedb project init
    ```
2. 
    ```shell
    edgedb migration create
    ```

3.
    ```shell
    edgedb migrate
    ```
4.
    if you didn't got errors you can check types created in your database by running
    
    ```shell
    edgedb ui
    ```
