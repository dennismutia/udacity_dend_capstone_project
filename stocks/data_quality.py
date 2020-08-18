import pandas as pd

db_connection_string = f"mssql+pyodbc://findata"

class DataQualityTests:
    '''
    Checks whether data was staged and date dim table was created correctly

    Parameters;
    db_connection_string: ODBC connection string to sql server
    '''
    
    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string

    def test_staging(self):
        print("Testing that records were inserted in the staging table started...")
        test_query = '''
        select count(*) as record_count from daily_trading_data
        '''    
        record_count = pd.read_sql(test_query, self.db_connection_string)

        if record_count.record_count[0] < 1:
            raise ValueError("Data quality test failed. 0 records staged")
        else:
            print("Data quality test passed.")

    def test_date_dim_completeness(self):
        print("Date dim table date range test started...")
        dim_date_range_query = '''
        select 
	        datediff(DAY, min([Date]), max([Date])) as date_range
        from d_Dates
        '''
        staging_date_range_query = '''
        select
            datediff(DAY, min(price_date), max(price_date)) as date_range
        from daily_trading_data
        '''

        date_dim_range = pd.read_sql(dim_date_range_query, self.db_connection_string).date_range[0]
        staging_date_range = pd.read_sql(staging_date_range_query, self.db_connection_string).date_range[0]

        if date_dim_range != staging_date_range:
            raise ValueError("Date dim table not complete. Date range between staged data and date dim is different.")
        else:
            print("Data quality test passed.")


