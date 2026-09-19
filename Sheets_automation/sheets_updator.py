import gspread

gc = gspread.oauth(credentials_filename='./credentials.json')

def fetch_headers(url_str:str,worksheet:str) -> list:
    sh = gc.open_by_url(url_str)
    worksht = sh.worksheet(worksheet)
    return worksht.row_values(1)

def fetch_sheets(url_str:str) -> list:
    sh = gc.open_by_url(url_str)
    worksheet_list = sh.worksheets()
    return [sheet.title for sheet in worksheet_list]

def fetch_part_rownumber(url_str:str,worksheet:str,partnumber:str) -> int:
    sh = gc.open_by_url(url_str)
    print(partnumber)
    worksht = sh.worksheet(worksheet)
    part_col_list = worksht.col_values(3)
    return part_col_list.index(partnumber)

def fetch_cellvalues(url_str:str,worksheet:str,row_no:int,col_no:int):
    sh = gc.open_by_url(url_str)
    worksht = sh.worksheet(worksheet)
    val = worksht.cell(row_no,col_no)
    return val

def update_cell(url_str:str,worksheet:str,row_no:int,col_no:int,value):
    sh = gc.open_by_url(url_str)
    worksht = sh.worksheet(worksheet)
    worksht.update_cell(row_no,col_no,value)

    
    
    