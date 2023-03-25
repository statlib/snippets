import pandas as pd

def write_table(
    df: pd.DataFrame,
    fpath: str,
    sheet_name="Data",
    max_width=60,
    col_margin=3,
    h_align: str = "left",
    v_align: str = "top",
    reset_index: bool = True,
) -> None:
    """
    TODO: Text wrap
    
    > df = pd.DataFrame(
        {"A": "a" * 10, "B": "b" * 40, "C": "c" * 60, "D": "c" * 110}, index=[0]
    )
    > write_table(df, "test.xlsx")
    """
    assert fpath.endswith(".xlsx"), "'fpath' must be an .xlsx file"
    assert isinstance(df, pd.DataFrame), "'df' must be a Pandas DataFrame"
    if reset_index:
        df = df.reset_index(drop=True)
    w = pd.ExcelWriter(fpath, engine="xlsxwriter")
    (
        df.style.set_properties(
            **{"text-align": h_align, "vertical-align": v_align}
        ).to_excel(w, sheet_name=sheet_name, startrow=1, header=False, index=False)
    )
    wb = w.book
    ws = w.sheets[sheet_name]
    # cell_format = wb.add_format({"text_wrap": True})

    d = df.shape
    nr = d[0]
    nc = d[1] - 1
    col_conf = []
    for i, col in enumerate(df.columns):
        col_conf.append({"header": col})
        col_width = min(max_width, df[col].astype(str).map(len).max()) + col_margin
        ws.set_column(i, i, col_width)
    ws.add_table(0, 0, nr, nc, {"columns": col_conf})
    # ws.set_column(0, nc, col_width)
    w.close()
