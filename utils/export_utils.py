from io import BytesIO
import pandas as pd
from sqlalchemy.inspection import inspect


def rows_to_dataframe(rows):
    """
    Convert SQLAlchemy rows to a pandas DataFrame by reflecting columns.

    Dynamically inspects SQLAlchemy model instances to extract column names
    and values, creating a DataFrame with only the database columns (ignores
    relationships and other non-column attributes).

    Args:
        rows (list): List of SQLAlchemy model instances (e.g., [User, User, ...]).

    Returns:
        pd.DataFrame: DataFrame with columns matching the SQLAlchemy model's
                     database columns. Returns empty DataFrame if no rows provided.
    """
    if not rows:
        return pd.DataFrame()
    mapper = inspect(rows[0]).mapper
    cols = [c.key for c in mapper.columns]
    data = [{c: getattr(r, c) for c in cols} for r in rows]
    return pd.DataFrame(data, columns=cols)


def make_xlsx_bytes(sheets: dict[str, pd.DataFrame]) -> BytesIO:
    """
    Build an in-memory Excel (.xlsx) file with one or more sheets.

    Creates an Excel workbook in memory from a dictionary of sheet names and
    DataFrames. Handles empty DataFrames by inserting a placeholder message.
    Truncates sheet names to Excel's 31-character limit.

    Args:
        sheets (dict[str, pd.DataFrame]): Dictionary mapping sheet names to DataFrames.
                                        Example: {"users": user_df, "books": book_df}

    Returns:
        BytesIO: In-memory Excel file as bytes stream, ready for download or further processing.
    """
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        for sheet_name, df in sheets.items():
            # Excel sheet names max 31 chars
            safe = (sheet_name or "Sheet")[:31]
            (df if not df.empty else pd.DataFrame({"info": ["(no rows)"]})).to_excel(writer, index=False, sheet_name=safe)
    buf.seek(0)
    return buf
