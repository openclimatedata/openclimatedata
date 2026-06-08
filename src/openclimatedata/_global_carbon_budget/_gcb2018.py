from ._core import _Global_Carbon_Budget_Release

GCB2018 = _Global_Carbon_Budget_Release(
    name="Global Carbon Budget 2018",
    version=2018,
    data_version="1.0",
    doi="10.18160/gcp-2018 ",
    doi_article="10.5194/essd-10-2141-2018",
    published="2018-12-05",
    citation="Global Carbon Project. (2018). Supplemental data of Global Carbon Budget 2018 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2018",
    citation_article="Le Quéré, C., Andrew, R. M., Friedlingstein, P., Sitch, S., Hauck, J., Pongratz, J., Pickers, P. A., Korsbakken, J. I., Peters, G. P., Canadell, J. G., Arneth, A., Arora, V. K., Barbero, L., Bastos, A., Bopp, L., Chevallier, F., Chini, L. P., Ciais, P., Doney, S. C., Gkritzalis, T., Goll, D. S., Harris, I., Haverd, V., Hoffman, F. M., Hoppema, M., Houghton, R. A., Hurtt, G., Ilyina, T., Jain, A. K., Johannessen, T., Jones, C. D., Kato, E., Keeling, R. F., Goldewijk, K. K., Landschützer, P., Lefèvre, N., Lienert, S., Liu, Z., Lombardozzi, D., Metzl, N., Munro, D. R., Nabel, J. E. M. S., Nakaoka, S., Neill, C., Olsen, A., Ono, T., Patra, P., Peregon, A., Peters, W., Peylin, P., Pfeil, B., Pierrot, D., Poulter, B., Rehder, G., Resplandy, L., Robertson, E., Rocher, M., Rödenbeck, C., Schuster, U., Schwinger, J., Séférian, R., Skjelvan, I., Steinhoff, T., Sutton, A., Tans, P. P., Tian, H., Tilbrook, B., Tubiello, F. N., van der Laan-Luijkx, I. T., van der Werf, G. R., Viovy, N., Walker, A. P., Wiltshire, A. J., Wright, R., Zaehle, S., and Zheng, B.: Global Carbon Budget 2018, Earth Syst. Sci. Data, 10, 2141–2194, https://doi.org/10.5194/essd-10-2141-2018, 2018.",
    license="CC BY 4.0",
    global_carbon_budget={
        "filename": "Global_Carbon_Budget_2018v1.0.xlsx",
        "url": "https://data.icos-cp.eu/licence_accept?ids=%5B%22OT_YY6iORypk2yAcwjMpUQpo%22%5D",
        "known_hash": "393fd863a88e472a64db201cc23329510a68b5d84d26201880d3c845c631fffe",
        "sheets": [
            {
                "sheet_name": "Global Carbon Budget",
                "columns": "A:G",
                "skiprows": 19,
            },
            {"sheet_name": "Historical Budget", "skiprows": 14},
            {
                "sheet_name": "Fossil Emissions by Fuel Type",
                "skiprows": 12,
                "unit": "MtC/yr",
                "unit_overwrite": {"Per Capita": "tC/person/yr"},
            },
            {
                "sheet_name": "Land-Use Change Emissions",
                "skiprows": 25,
                "tables": [
                    {
                        "table_name": "GCB",
                        "skiprows": 27,
                        "columns": "A:B",
                    },
                    {
                        "table_name": "Bookkeeping Models",
                        "skiprows": 27,
                        "columns": "A,D:E",
                    },
                    {
                        "table_name": "Individual models",
                        "skiprows": 27,
                        "columns": "A,G:V,X",
                    },
                ],
            },
            {
                "sheet_name": "Ocean Sink",
                "skiprows": 17,
                "tables": [
                    {
                        "table_name": "GCB",
                        "skiprows": 19,
                        "columns": "A:B",
                        "nrows": 59,
                    },
                    {
                        "table_name": "Individual models",
                        "skiprows": 19,
                        "columns": "A,D:J",
                        "nrows": 59,
                    },
                    {
                        "table_name": "Data-based products",
                        "skiprows": 19,
                        "columns": "A,L:M",
                        "nrows": 59,
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
                        "columns": "A,D:T",
                    },
                ],
            },
        ],
    },
    national_fossil_carbon_emissions={
        "filename": "National_Carbon_Emissions_2018v1.0.xlsx",
        "url": "https://data.icos-cp.eu/licence_accept?ids=%5B%22zLixg_KdbUFw2cRvRJ2GMGZh%22%5D",
        "known_hash": "ccb8b183f29d6d4170d9c46f449d863066614cb6ee4b39155bcc7048ed29e7e9",
        "sheets": [
            {"sheet_name": "Territorial Emissions", "skiprows": 16, "unit": "MtC/yr"},
            {"sheet_name": "Consumption Emissions", "skiprows": 8, "unit": "MtC/yr"},
            {"sheet_name": "Emissions Transfers", "skiprows": 8, "unit": "MtC/yr"},
        ],
    },
)
