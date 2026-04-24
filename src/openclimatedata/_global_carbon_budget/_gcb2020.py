from ._core import _Global_Carbon_Budget_Release

GCB2020 = _Global_Carbon_Budget_Release(
    name="Global Carbon Budget 2020",
    version="1.0",
    doi="10.18160/gcp-2020",
    doi_article="10.5194/essd-12-3269-2020",
    published="2020-12-11",
    citation="Global Carbon Project. (2020). Supplemental data of Global Carbon Budget 2020 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2020",
    citation_article="Friedlingstein, P., O'Sullivan, M., Jones, M. W., Andrew, R. M., Hauck, J., Olsen, A., Peters, G. P., Peters, W., Pongratz, J., Sitch, S., Le Quéré, C., Canadell, J. G., Ciais, P., Jackson, R. B., Alin, S., Aragão, L. E. O. C., Arneth, A., Arora, V., Bates, N. R., Becker, M., Benoit-Cattin, A., Bittig, H. C., Bopp, L., Bultan, S., Chandra, N., Chevallier, F., Chini, L. P., Evans, W., Florentie, L., Forster, P. M., Gasser, T., Gehlen, M., Gilfillan, D., Gkritzalis, T., Gregor, L., Gruber, N., Harris, I., Hartung, K., Haverd, V., Houghton, R. A., Ilyina, T., Jain, A. K., Joetzjer, E., Kadono, K., Kato, E., Kitidis, V., Korsbakken, J. I., Landschützer, P., Lefèvre, N., Lenton, A., Lienert, S., Liu, Z., Lombardozzi, D., Marland, G., Metzl, N., Munro, D. R., Nabel, J. E. M. S., Nakaoka, S.-I., Niwa, Y., O'Brien, K., Ono, T., Palmer, P. I., Pierrot, D., Poulter, B., Resplandy, L., Robertson, E., Rödenbeck, C., Schwinger, J., Séférian, R., Skjelvan, I., Smith, A. J. P., Sutton, A. J., Tanhua, T., Tans, P. P., Tian, H., Tilbrook, B., van der Werf, G., Vuichard, N., Walker, A. P., Wanninkhof, R., Watson, A. J., Willis, D., Wiltshire, A. J., Yuan, W., Yue, X., and Zaehle, S.: Global Carbon Budget 2020, Earth Syst. Sci. Data, 12, 3269–3340, https://doi.org/10.5194/essd-12-3269-2020, 2020.",
    license="CC BY 4.0",
    filename="Global_Carbon_Budget_2020v1.0.xlsx",
    url="https://data.icos-cp.eu/licence_accept?ids=%5B%226QlPjfn_7uuJtAeuGGFXuPwz%22%5D",
    known_hash="e9094f8df9ffeeeb89b407ae186157b8fc339aa22662d7b514e85aa1553cfc81",
    sheets=[
        {
            "sheet_name": "Global Carbon Budget",
            "columns": "A:H",
            "skiprows": 20,
            "nrows": 62,
        },
        {"sheet_name": "Historical Budget", "skiprows": 15, "nrows": 271},
        {"sheet_name": "Fossil Emissions by Category", "skiprows": 8},
        {
            "sheet_name": "Land-Use Change Emissions",
            "skiprows": 27,
            "tables": [
                {
                    "table_name": "GCB",
                    "skiprows": 28,
                    "columns": "A:B",
                },
                {
                    "table_name": "Bookkeeping Models",
                    "skiprows": 28,
                    "columns": "A,D:F",
                },
                {
                    "table_name": "Individual models",
                    "skiprows": 28,
                    "columns": "A,H:X,Z:AA",
                },
            ],
        },
        {
            "sheet_name": "Ocean Sink",
            "skiprows": 22,
            "tables": [
                {"table_name": "GCB", "skiprows": 24, "columns": "A:C"},
                {
                    "table_name": "Individual models",
                    "skiprows": 24,
                    "columns": "A,E:M,O:P",
                },
                {
                    "table_name": "Data-based products",
                    "skiprows": 24,
                    "columns": "A,R:W",
                },
            ],
        },
        {
            "sheet_name": "Terrestrial Sink",
            "skiprows": 22,
            "tables": [
                {"table_name": "GCB", "skiprows": 24, "columns": "A:B"},
                {
                    "table_name": "Individual models",
                    "skiprows": 24,
                    "columns": "A,D:T,V:W",
                },
            ],
        },
        {"sheet_name": "Cement Carbonation Sink", "skiprows": 9, "columns": "A,B,D:E"},
    ],
)
