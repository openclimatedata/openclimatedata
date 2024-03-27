from ._core import _GCB_Global_Budget_Release

GCB2023 = _GCB_Global_Budget_Release(
    name="Global Carbon Budget 2023",
    version="1.1",
    doi="10.18160/GCP-2023",
    published="2023-12-05",
    citation="Global Carbon Project, 2023. Supplemental data of Global Carbon Budget 2023. https://doi.org/10.18160/GCP-2023",
    license="CC BY 4.0",
    filename="Global_Carbon_Budget_2023v1.1.xlsx",
    url="https://data.icos-cp.eu/licence_accept?ids=%5B%22NMvAsIKjrLx4KUeha_ckfVPP%22%5D",
    known_hash="34cbc0b082a3acbc782947a16bf7247d53cf867ab4a0cd241e8491f2d00842b9",
    sheets=[
        {
            "sheet_name": "Global Carbon Budget",
            "skiprows": 21,
        },
        {
            "sheet_name": "Historical Budget",
            "skiprows": 15,
        },
        {"sheet_name": "Fossil Emissions by Category", "skiprows": 8},
        {
            "sheet_name": "Land-Use Change Emissions",
            "skiprows": 34,
            "tables": [
                {
                    "table_name": "GCB",
                    "skiprows": 37,
                    "columns": "A:G",
                },
                {
                    "table_name": "BLUE",
                    "skiprows": 37,
                    "columns": "A,I:M",
                },
                {
                    "table_name": "H&C2023",
                    "skiprows": 37,
                    "columns": "A,N:R",
                },
                {
                    "table_name": "OSCAR",
                    "skiprows": 37,
                    "columns": "A,S:W",
                },
                {
                    "table_name": "Peat Drainage & Peat Fires",
                    "skiprows": list(range(36)) + [37],
                    "columns": "A,Y:AA",
                },
                {
                    "table_name": "Individual models (NET) - Does not include peat emissions",
                    "skiprows": list(range(36)) + [37],
                    "columns": "A,AC:AV,AX:AY",
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
            "skiprows": 26,
            "tables": [
                {"table_name": "GCB", "skiprows": 27, "columns": "A:B"},
                {
                    "table_name": "Individual models",
                    "skiprows": 27,
                    "columns": "A,D:W,Y:Z",
                },
            ],
        },
        {"sheet_name": "Cement Carbonation Sink", "skiprows": 9, "columns": "A,B,D,E"},
    ],
)
