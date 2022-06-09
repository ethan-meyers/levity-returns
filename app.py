import pandas as pd
from redshift_credentials import database, username, password, host, port, schema
from datetime import datetime
from sql.sql_commands import Monthly_Returns, Weekly_Returns
from resources import g_drive_cred, workbook
from functions import sql_con, pd_to_gsheets, clear_data_range, update_range

def main():
    # Define connection.
    conn = sql_con(username, password, host, port, database, schema)

    # Create dict of queries.
    queries = {
        'Monthly_Returns': Monthly_Returns,
        'Weekly_Returns': Weekly_Returns
    }

    for query in queries:
        # Query all records from feedback_view_trends
        df = pd.read_sql(queries[query], conn)

        df.fillna('', inplace=True)

        # CLEAR RANGE AND LOAD DATA!!!
        print(f'Now loading data to {query}!')
        clear_data_range(workbook, query, 'A1')
        try:
            pd_to_gsheets(workbook, query, df, 1, 1)
        except:
            print(f"Failed to update {query}")
            print()
        print()

    ##########
    
    # create timestamp to note when program ran
    datetime_stamp = datetime.now().strftime("%m/%d/%Y %I:%M %p")

    datetime_stamp = [datetime_stamp]

    datetime_df = pd.DataFrame(data=datetime_stamp, columns=['Last update:'])

    pd_to_gsheets(workbook_name=workbook, sheet_name='Updates', df=datetime_df, row_num=1, col_num=1)

    print(datetime_stamp)

    return

if __name__ == "__main__":
    main()