from ._core import _Global_Carbon_Budget_Release

GCB2019 = _Global_Carbon_Budget_Release(
    name="Global Carbon Budget 2019",
    version="1.0",
    doi="10.18160/gcp-2019 ",
    doi_article="10.5194/essd-11-1783-2019",
    published="2019-12-04",
    citation="Global Carbon Project. (2019). Supplemental data of Global Carbon Budget 2019 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2019",
    citation_article="Friedlingstein, P., Jones, M. W., O'Sullivan, M., Andrew, R. M., Hauck, J., Peters, G. P., Peters, W., Pongratz, J., Sitch, S., Le Quéré, C., Bakker, D. C. E., Canadell, J. G., Ciais, P., Jackson, R. B., Anthoni, P., Barbero, L., Bastos, A., Bastrikov, V., Becker, M., Bopp, L., Buitenhuis, E., Chandra, N., Chevallier, F., Chini, L. P., Currie, K. I., Feely, R. A., Gehlen, M., Gilfillan, D., Gkritzalis, T., Goll, D. S., Gruber, N., Gutekunst, S., Harris, I., Haverd, V., Houghton, R. A., Hurtt, G., Ilyina, T., Jain, A. K., Joetzjer, E., Kaplan, J. O., Kato, E., Klein Goldewijk, K., Korsbakken, J. I., Landschützer, P., Lauvset, S. K., Lefèvre, N., Lenton, A., Lienert, S., Lombardozzi, D., Marland, G., McGuire, P. C., Melton, J. R., Metzl, N., Munro, D. R., Nabel, J. E. M. S., Nakaoka, S.-I., Neill, C., Omar, A. M., Ono, T., Peregon, A., Pierrot, D., Poulter, B., Rehder, G., Resplandy, L., Robertson, E., Rödenbeck, C., Séférian, R., Schwinger, J., Smith, N., Tans, P. P., Tian, H., Tilbrook, B., Tubiello, F. N., van der Werf, G. R., Wiltshire, A. J., and Zaehle, S.: Global Carbon Budget 2019, Earth Syst. Sci. Data, 11, 1783–1838, https://doi.org/10.5194/essd-11-1783-2019, 2019.",
    license="CC BY 4.0",
    filename="Global_Carbon_Budget_2019v1.0.xlsx",
    url="https://data.icos-cp.eu/licence_accept?ids=%5B%22Z6S-dJJHB4RCe07mcmhMYxwx%22%5D",
    known_hash="67a4be7492470784427b4ee672684c631c313d89772e6247c69a8058cfb4cd1f",
    sheets=[
        {
            "sheet_name": "Global Carbon Budget",
            "columns": "B:H",
            "skiprows": 18,
        },
        {"sheet_name": "Historical Budget", "skiprows": 14},
        {"sheet_name": "Fossil Emissions by Fuel Type", "skiprows": 12},
        {
            "sheet_name": "Land-Use Change Emissions",
            "skiprows": 24,
            "tables": [
                {
                    "table_name": "GCB",
                    "skiprows": 25,
                    "columns": "A:B",
                },
                {
                    "table_name": "Bookkeeping Models",
                    "skiprows": 25,
                    "columns": "A,D:E",
                },
                {
                    "table_name": "Individual models",
                    "skiprows": 25,
                    "columns": "A,G:V,X",
                },
            ],
        },
        {
            "sheet_name": "Ocean Sink",
            "skiprows": 21,
            "tables": [
                {"table_name": "GCB", "skiprows": 22, "columns": "A:B"},
                {
                    "table_name": "Individual models",
                    "skiprows": 22,
                    "columns": "A,D:L,N",
                },
                {
                    "table_name": "Data-based products",
                    "skiprows": 22,
                    "columns": "A,P:R,T",
                },
            ],
        },
        {
            "sheet_name": "Terrestrial Sink",
            "skiprows": 23,
            "tables": [
                {"table_name": "GCB", "skiprows": 23, "columns": "A:B"},
                {
                    "table_name": "Individual models",
                    "skiprows": 23,
                    "columns": "A,D:S,U",
                },
            ],
        },
    ],
)
