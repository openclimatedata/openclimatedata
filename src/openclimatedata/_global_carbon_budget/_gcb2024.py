from ._core import _Global_Carbon_Budget_Release

GCB2024 = _Global_Carbon_Budget_Release(
    name="Global Carbon Budget 2024",
    version="1.1",
    doi="10.18160/gcp-2024",
    doi_article="10.5194/essd-17-965-2025",
    published="2025-03-14",
    citation="Global Carbon Project. (2024). Supplemental data of Global Carbon Budget 2024 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2024",
    citation_article="Friedlingstein, P., O'Sullivan, M., Jones, M. W., Andrew, R. M., Hauck, J., Landschützer, P., Le Quéré, C., Li, H., Luijkx, I. T., Olsen, A., Peters, G. P., Peters, W., Pongratz, J., Schwingshackl, C., Sitch, S., Canadell, J. G., Ciais, P., Jackson, R. B., Alin, S. R., Arneth, A., Arora, V., Bates, N. R., Becker, M., Bellouin, N., Berghoff, C. F., Bittig, H. C., Bopp, L., Cadule, P., Campbell, K., Chamberlain, M. A., Chandra, N., Chevallier, F., Chini, L. P., Colligan, T., Decayeux, J., Djeutchouang, L. M., Dou, X., Duran Rojas, C., Enyo, K., Evans, W., Fay, A. R., Feely, R. A., Ford, D. J., Foster, A., Gasser, T., Gehlen, M., Gkritzalis, T., Grassi, G., Gregor, L., Gruber, N., Gürses, Ö., Harris, I., Hefner, M., Heinke, J., Hurtt, G. C., Iida, Y., Ilyina, T., Jacobson, A. R., Jain, A. K., Jarníková, T., Jersild, A., Jiang, F., Jin, Z., Kato, E., Keeling, R. F., Klein Goldewijk, K., Knauer, J., Korsbakken, J. I., Lan, X., Lauvset, S. K., Lefèvre, N., Liu, Z., Liu, J., Ma, L., Maksyutov, S., Marland, G., Mayot, N., McGuire, P. C., Metzl, N., Monacci, N. M., Morgan, E. J., Nakaoka, S.-I., Neill, C., Niwa, Y., Nützel, T., Olivier, L., Ono, T., Palmer, P. I., Pierrot, D., Qin, Z., Resplandy, L., Roobaert, A., Rosan, T. M., Rödenbeck, C., Schwinger, J., Smallman, T. L., Smith, S. M., Sospedra-Alfonso, R., Steinhoff, T., Sun, Q., Sutton, A. J., Séférian, R., Takao, S., Tatebe, H., Tian, H., Tilbrook, B., Torres, O., Tourigny, E., Tsujino, H., Tubiello, F., van der Werf, G., Wanninkhof, R., Wang, X., Yang, D., Yang, X., Yu, Z., Yuan, W., Yue, X., Zaehle, S., Zeng, N., and Zeng, J.: Global Carbon Budget 2024, Earth Syst. Sci. Data, 17, 965–1039, https://doi.org/10.5194/essd-17-965-2025, 2025.",
    license="CC BY 4.0",
    filename="Global_Carbon_Budget_2024_v1.1.xlsx",
    url="https://data.icos-cp.eu/licence_accept?ids=%5B%223ouh1IWooae1ZhCym8El-C35%22%5D",
    known_hash="de8ba1d485a8a1a7b56610b29bc125f82df998e51e1e4a8d59613c4ae6478498",
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
            "skiprows": 35,
            "tables": [
                {
                    "table_name": "GCB",
                    "skiprows": 38,
                    "columns": "A:G",
                },
                {
                    "table_name": "BLUE",
                    "skiprows": 38,
                    "columns": "A,I:M",
                },
                {
                    "table_name": "H&C2023",
                    "skiprows": 38,
                    "columns": "A,N:R",
                },
                {
                    "table_name": "OSCAR",
                    "skiprows": 38,
                    "columns": "A,S:W",
                },
                {
                    "table_name": "LUCE",
                    "skiprows": 38,
                    "columns": "A,X:AB",
                },
                {
                    "table_name": "Peat Drainage & Peat Fires",
                    "skiprows": list(range(37)) + [38],
                    "columns": "A,AD:AF",
                },
                {
                    "table_name": "Individual models (NET) - Does not include peat emissions",
                    "skiprows": list(range(37)) + [38],
                    "columns": "A,AH:BA,BC:BD",
                },
            ],
        },
        # nrows needed in Ocean Sink sheet, otherwise years get read as floats
        {
            "sheet_name": "Ocean Sink",
            "skiprows": 29,
            "tables": [
                {"table_name": "GCB", "skiprows": 31, "columns": "A:B", "nrows": 91},
                {
                    "table_name": "Individual models",
                    "skiprows": 31,
                    "columns": "A,D:M,O:P",
                    "nrows": 91,
                },
                {
                    "table_name": "Data-based products",
                    "skiprows": 31,
                    "columns": "A,R:AB",
                    "nrows": 91,
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
