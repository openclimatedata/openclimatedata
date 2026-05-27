from ._core import _Global_Carbon_Budget_Release

GCB2025 = _Global_Carbon_Budget_Release(
    name="Global Carbon Budget 2025",
    version="1.0",
    doi="10.18160/gcp-2025",
    doi_article="10.5194/essd-18-3211-2026",
    published="2026-05-13",
    citation="Global Carbon Project. (2025). Supplemental data of Global Carbon Budget 2025 (Version 1.0) [Data set]. Global Carbon Project. https://doi.org/10.18160/gcp-2025",
    citation_article="Friedlingstein, P., O'Sullivan, M., Jones, M. W., Andrew, R. M., Bakker, D. C. E., Hauck, J., Landschützer, P., Le Quéré, C., Li, H., Luijkx, I. T., Peters, G. P., Peters, W., Pongratz, J., Schwingshackl, C., Sitch, S., Canadell, J. G., Ciais, P., Aas, K., Alin, S. R., Anthoni, P., Barbero, L., Bates, N. R., Bellouin, N., Benoit-Cattin, A., Berghoff, C. F., Bernardello, R., Bopp, L., Brasika, I. B. M., Chamberlain, M. A., Chandra, N., Chevallier, F., Chini, L. P., Collier, N. O., Colligan, T. H., Cronin, M., Djeutchouang, L. M., Dou, X., Enright, M. P., Enyo, K., Erb, M., Evans, W., Feely, R. A., Feng, L., Ford, D. J., Foster, A., Fransner, F., Gasser, T., Gehlen, M., Gkritzalis, T., Goncalves De Souza, J., Grassi, G., Gregor, L., Gruber, N., Guenet, B., Gürses, Ö., Harrington, K., Harris, I., Heinke, J., Hurtt, G. C., Iida, Y., Ilyina, T., Ito, A., Jacobson, A. R., Jain, A. K., Jarníková, T., Jersild, A., Jiang, F., Jones, S. D., Kato, E., Keeling, R. F., Klein Goldewijk, K., Knauer, J., Kong, Y., Korsbakken, J. I., Koven, C., Kunimitsu, T., Lan, X., Liu, J., Liu, Z., Liu, Z., Lo Monaco, C., Ma, L., Marland, G., McGuire, P. C., McKinley, G. A., Melton, J. R., Monacci, N., Monier, E., Morgan, E. J., Munro, D. R., Müller, J. D., Nakaoka, S.-I., Nayagam, L. R., Niwa, Y., Nutzel, T., Olsen, A., Omar, A. M., Pan, N., Pandey, S., Pierrot, D., Qin, Z., Regnier, P., Rehder, G., Resplandy, L., Roobaert, A., Rosan, T. M., Rödenbeck, C., Schwinger, J., Skjelvan, I., Smallman, T. L., Spada, V., Sreeush, M. G., Sun, Q., Sutton, A. J., Sweeney, C., Swingedouw, D., Séférian, R., Takao, S., Tatebe, H., Tian, H., Tian, X., Tilbrook, B., Tsujino, H., Tubiello, F., van Ooijen, E., van der Werf, G. R., van de Velde, S. J., Walker, A. P., Wanninkhof, R., Yang, X., Yuan, W., Yue, X., and Zeng, J.: Global Carbon Budget 2025, Earth Syst. Sci. Data, 18, 3211–3288, https://doi.org/10.5194/essd-18-3211-2026, 2026.",
    license="CC BY 4.0",
    global_carbon_budget={
        "filename": "Global_Carbon_Budget_2025_v1.0.xlsx",
        "url": "https://data.icos-cp.eu/licence_accept?ids=%5B%22qSjPBsV1drZnYdH-yCJMmkGn%22%5D",
        "known_hash": "a928cf06c57576b66761d1fec8224c9a41a781eb63442afc03ba902858dd64a9",
        "sheets": [
            {
                "sheet_name": "Global Carbon Budget",
                "skiprows": 21,
            },
            {
                "sheet_name": "Historical Budget",
                "skiprows": 15,
            },
            {
                "sheet_name": "Fossil Emissions by Category",
                "skiprows": 8,
                "unit_overwrite": {"Per.Capita": "t/person/yr"},
            },
            {
                "sheet_name": "Land-Use Change Emissions",
                "skiprows": 36,
                "tables": [
                    {
                        "table_name": "GCB",
                        "skiprows": 39,
                        "columns": "A:G",
                    },
                    {
                        "table_name": "BLUE",
                        "skiprows": 39,
                        "columns": "A,I:M",
                    },
                    {
                        "table_name": "OSCAR",
                        "skiprows": 39,
                        "columns": "A,N:R",
                    },
                    {
                        "table_name": "LUCE",
                        "skiprows": 39,
                        "columns": "A,S:W",
                    },
                    {
                        "table_name": "Peat Drainage & Peat Fires",
                        "skiprows": list(range(38)) + [39],
                        "columns": "A,Y:AA",
                    },
                    {
                        "table_name": "Individual models (NET) - Does not include peat emissions",
                        "skiprows": list(range(38)) + [39],
                        "columns": "A,AC:AX,AZ:BA",
                    },
                ],
            },
            {
                "sheet_name": "Atmospheric Growth",
                "skiprows": 8,
                "tables": [
                    {"table_name": "GCB", "skiprows": 8, "columns": "A:D"},
                    {
                        "table_name": "Individual Inversions",
                        "skiprows": 8,
                        "columns": "A,F:S",
                    },
                ],
            },
            # nrows needed in Ocean Sink sheet, otherwise years get read as floats
            {
                "sheet_name": "Ocean Sink",
                "skiprows": 29,
                "tables": [
                    {
                        "table_name": "GCB",
                        "skiprows": 31,
                        "columns": "A:C",
                        "nrows": 98,
                    },
                    {
                        "table_name": "Individual models",
                        "skiprows": 31,
                        "columns": "A,E:N,P:Q",
                        "nrows": 98,
                    },
                    {
                        "table_name": "fCO2-products",
                        "skiprows": 31,
                        "columns": "A,S:AC",
                        "nrows": 98,
                    },
                ],
            },
            {
                "sheet_name": "Terrestrial Sink",
                "skiprows": 29,
                "tables": [
                    {
                        "table_name": "GCB",
                        "skiprows": 29,
                        "columns": "A:C",
                        "nrows": 66,
                    },
                    {
                        "table_name": "Individual models",
                        "skiprows": 29,
                        "columns": "A,E:Z,AB:AC",
                        "nrows": 66,
                    },
                ],
            },
            {
                "sheet_name": "Cement Carbonation Sink",
                "skiprows": 9,
                "columns": "A,B,D,E",
            },
        ],
    },
    national_fossil_carbon_emissions={
        "filename": "National_Fossil_Carbon_Emissions_2025_v1.0.xlsx",
        "url": "https://data.icos-cp.eu/licence_accept?ids=%5B%22loCXyssaalv6DPdO6Qdj90qQ%22%5D",
        "known_hash": "968097cacb1a6a5bfa0cf74ee90763f74a90ef10499e060ab43d1a74c671d46b",
        "sheets": [
            {
                "sheet_name": "Territorial Emissions",
                "skiprows": 11,
                "unit": "MtC/yr",
            },
            {"sheet_name": "Consumption Emissions", "skiprows": 8, "unit": "MtC/yr"},
            {"sheet_name": "Emissions Transfers", "skiprows": 8, "unit": "MtC/yr"},
        ],
    },
    national_landuse_change_emissions={
        "filename": "National_LandUseChange_Carbon_Emissions_2025_v1.0.xlsx",
        "url": "https://data.icos-cp.eu/licence_accept?ids=%5B%22milTbWkl0G-MSpdYG3IBIfzy%22%5D",
        "known_hash": "9a29536d6925d06f8c4a97581b720121fcf219732c240e970bc24167d74e38d1",
        "sheets": [
            {"sheet_name": "BLUE", "skiprows": 7, "unit": "TgC/yr"},
            {"sheet_name": "OSCAR", "skiprows": 7, "unit": "TgC/yr"},
            {"sheet_name": "LUCE", "skiprows": 7, "unit": "TgC/yr"},
        ],
    },
)
