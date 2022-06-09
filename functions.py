import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import pygsheets as pygs

# Google Drive Credentials Path
g_drive_cred = r'C:\Users\ethan.meyers\Documents\Repos\levity_return_kpi\credentials.json'
# g_drive_cred = r'C:\Users\darius kay\Dev\gitlab\test\python\credentials.json'

def sql_con(in_username, in_password, in_host, in_port, in_database, in_schema):
    '''Create connection function'''
    connection = "redshift+psycopg2://%s:%s@%s:%s/%s" % (in_username, in_password, in_host, str(in_port), in_database)
    engine = sa.create_engine(connection)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    setpath = "SET search_path TO %s" % in_schema
    s.execute(setpath)
    print("Connection Established!")
    return engine

# Function to clear data range.
def clear_data_range(workbook_name, tab_name, cell):
#     print(g_drive_cred)
    # authorization
    gc = pygs.authorize(client_secret=g_drive_cred)
    # open the google spreadsheet
    ws = gc.open_by_url(workbook_name)
    # select the first sheet
    wks = ws.worksheet_by_title(tab_name)
#     print(ws.id)
    wks.clear(start=cell)
    print(f"{workbook_name} - {tab_name}: Cleared")
    return

def update_range(workbook_name, tab_name, cell, data):
    # authorization
    gc = pygs.authorize(client_secret=g_drive_cred)
    # open the google spreadsheet
    ws = gc.open_by_url(workbook_name)
    # select the first sheet
    wks = ws.worksheet_by_title(tab_name)
    # Update value
    wks.update_value(cell, data)
    print("Update Complete!")
    return

def pd_to_gsheets(workbook_name, sheet_name, df, row_num, col_num):
    # authorization
    gc = pygs.authorize(client_secret=g_drive_cred)

    # open the google spreadsheet
    ws = gc.open_by_url(workbook_name)

    # select the first sheet
    wks = ws.worksheet_by_title(sheet_name)
    
    # Determine row count
    row_count = wks.rows
    print(f"Rows available in WS: {row_count}")
    # Determine length of DF.
    new_row_count = len(df)
    print(f"Rows in DF: {new_row_count}")
    # Determine if we need more rows.
    if new_row_count > row_count:
        diff = new_row_count - row_count
        # Add additional rows if needed.
        try:
            wks.add_rows(diff)
        except:
            pass
        print(f"{diff} rows added to WS")
    
    # update the designated sheet with df, starting at cell B2.
    wks.set_dataframe(df, (row_num, col_num))
    print("Update Complete!")

    return