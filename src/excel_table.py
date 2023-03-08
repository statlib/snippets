import pandas as pd


def write_table(
    df: pd.DataFrame,
    fpath: str,
    sheet_name="Data",
    col_width=15,
    h_align: str = "left",
    v_align: str = "top",
    reset_index: bool = True,
) -> None:
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
    d = df.shape
    nr = d[0]
    nc = d[1] - 1
    col_conf = [{"header": col} for col in df.columns]
    ws.add_table(0, 0, nr, nc, {"columns": col_conf})
    ws.set_column(0, nc, col_width)
    w.close()
