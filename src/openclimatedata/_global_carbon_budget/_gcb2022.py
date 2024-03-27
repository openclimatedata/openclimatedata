from ._core import _GCB_Global_Budget_Release

GCB2022 = _GCB_Global_Budget_Release(
    name="Global Carbon Budget 2022",
    version="1.0",
    doi="10.18160/gcp-2022",
    published="2022-11-11",
    citation="Global Carbon Project. (2022). Supplemental data of Global Carbon Budget 2022 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2022",
    license="CC BY 4.0",
    filename="Global_Carbon_Budget_2022v1.0.xlsx",
    url="https://data.icos-cp.eu/licence_accept?ids=%5B%221umMtgeUlhS2Y1YW_Qp94bu3%22%5D",
    known_hash="d6e98cb607949614b6635616fd0a7de1bbb790fccaeaa96b9ff183db216c2b4d",
    sheets=[
        {
            "sheet_name": "Global Carbon Budget",
            "skiprows": 20,
        },
        {
            "sheet_name": "Historical Budget",
            "skiprows": 15,
        },
        {"sheet_name": "Fossil Emissions by Category", "skiprows": 8},
        {
            "sheet_name": "Land-Use Change Emissions",
            "skiprows": 26,
            "tables": [
                {
                    "table_name": "GCB",
                    "skiprows": 29,
                    "columns": "A:D",
                },
                {
                    "table_name": "H&N",
                    "skiprows": 29,
                    "columns": "A,F:H",
                },
                {
                    "table_name": "BLUE",
                    "skiprows": 29,
                    "columns": "A,I:K",
                },
                {
                    "table_name": "OSCAR",
                    "skiprows": 29,
                    "columns": "A,L:N",
                },
                {
                    "table_name": "Individual models",
                    "skiprows": list(range(28)) + [29],
                    "columns": "A,P:AE,AG:AH",
                },
            ],
        },
        {
            "sheet_name": "Ocean Sink",
            "skiprows": 28,
            "tables": [
                {"table_name": "GCB", "skiprows": 30, "columns": "A:C"},
                {
                    "table_name": "Individual models",
                    "skiprows": 30,
                    "columns": "A,E:N,P:Q",
                },
                {
                    "table_name": "Data-based products",
                    "skiprows": 30,
                    "columns": "A,S:AB",
                },
            ],
        },
        {
            "sheet_name": "Terrestrial Sink",
            "skiprows": 21,
            "tables": [
                {"table_name": "GCB", "skiprows": 23, "columns": "A:B"},
                {
                    "table_name": "Individual models",
                    "skiprows": 23,
                    "columns": "A,D:S,U:V",
                },
            ],
        },
        {"sheet_name": "Cement Carbonation Sink", "skiprows": 9, "columns": "A,B,D,E"},
    ],
)
