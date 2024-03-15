
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    mysql_library_init(0, NULL, NULL);

    MYSQL *mysql = mysql_init(NULL);
    const char *host_name = "127.0.0.1"; // set your mysql host
    const char *user_name = "root";      // set your user_name
    const char *password = "";           // set your password
    const char *db_name = "test";        // set your databasename
    int port_num = 2883;                 // set your mysql port
    char *socket_name = NULL;
    MYSQL_RES *result;
    MYSQL_FIELD *fields;
    MYSQL_ROW row;
    int status = 0;
    /* connect to server with the CLIENT_MULTI_STATEMENTS option */
    if (mysql_real_connect(mysql, host_name, user_name, password, db_name,
                           port_num, socket_name,
                           CLIENT_MULTI_STATEMENTS) == NULL)
    {
        printf("mysql_real_connect() failed\n");
        mysql_close(mysql);
        exit(1);
    }
    /* execute multiple statements */
    status = mysql_query(mysql, "DROP TABLE IF EXISTS customer_t1;");
    if (status)
    {
        printf("Could not execute statement(s)");
        mysql_close(mysql);
        exit(0);
    }
    status = mysql_query(mysql, "CREATE TABLE customer_t1(c_customer_sk "
                                "integer, c_customer_name varchar(32));");
    status = mysql_query(
        mysql, "INSERT INTO customer_t1 VALUES(1,1),(20,'oceanbase');");
    status = mysql_query(
        mysql, "UPDATE customer_t1 SET c_customer_name='new data' WHERE id=1;");
    status = mysql_query(mysql, "SELECT * FROM customer_t1;");
    /* did current statement return data? */
    result = mysql_store_result(mysql);
    if (result)
    {
        /* yes; process rows and free the result set */
        // process_result_set(mysql, result);
        int num_fields = mysql_num_fields(result);
        int num_rows = mysql_num_rows(result);
        printf("result: %d rows %d fields\n", num_rows, num_fields);
        printf("---------------------\n");
        fields = mysql_fetch_fields(result);
        for (int i = 0; i < num_fields; ++i)
        {
            printf("%s\t", fields[i].name);
        }
        printf("\n---------------------\n");
        while ((row = mysql_fetch_row(result)))
        {
            for (int i = 0; i < num_fields; ++i)
            {
                printf("%s\t", row[i] ? row[i] : "NULL");
            }
            printf("\n");
        }
        printf("---------------------\n");
        mysql_free_result(result);
    }
    else /* no result set or error */
    {
        if (mysql_field_count(mysql) == 0)
        {
            printf("%lld rows affected\n", mysql_affected_rows(mysql));
        }
        else /* some error occurred */
        {
            printf("Could not retrieve result set\n");
        }
    }
    status = mysql_query(mysql, "DROP TABLE customer_t1;");
    mysql_close(mysql);
    return 0;
}

