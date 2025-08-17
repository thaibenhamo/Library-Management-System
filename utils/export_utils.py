
from io import BytesIO
import pandas as pd
from sqlalchemy.inspection import inspect

def rows_to_dataframe(rows):
    """Convert SQLAlchemy rows to a DataFrame by reflecting columns (ignores relationships)."""
    if not rows:
        return pd.DataFrame()
    mapper = inspect(rows[0]).mapper
    cols = [c.key for c in mapper.columns]
    data = [{c: getattr(r, c) for c in cols} for r in rows]
    return pd.DataFrame(data, columns=cols)

def make_xlsx_bytes(sheets: dict[str, pd.DataFrame]) -> BytesIO:
    """Build an in-memory XLSX with one or more sheets."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        for sheet_name, df in sheets.items():
            # Excel sheet names max 31 chars
            safe = (sheet_name or "Sheet")[:31]
            (df if not df.empty else pd.DataFrame({"info": ["(no rows)"]})).to_excel(writer, index=False, sheet_name=safe)
    buf.seek(0)
    return buf
