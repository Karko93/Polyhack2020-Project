import pandas as pd

def html_table(table):
    return pd.DataFrame(data=table).to_html()
