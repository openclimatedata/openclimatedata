import re
from dataclasses import dataclass
from zipfile import ZipFile

import numpy as np
import pandas as pd
import pooch


@dataclass
class _CedsRelease(dict):
    name: str
    citation: str
    doi: str
    published: str
    license: str
    entities: list[str]
    tables: list[dict]

    def __repr__(self):
        newline = "\n"

        return f"""{self.name}

License: {self.license}
https://doi.org/{self.doi}

Citation:
{self.citation}

{len(self.entities)} entities:
{newline.join([f'- "{k}"' for k in self.entities])}"""

    def __post_init__(self):
        for entity in self.entities:
            if entity not in self.keys():
                self[entity] = {}

            for table in self.tables:
                for key, path_pattern in table["patterns"].items():
                    self[entity][key] = _CedsTable(
                        entity=entity,
                        filename=table["zipfile"]["filename"],
                        url=table["zipfile"]["url"],
                        hash=table["zipfile"]["hash"],
                        path_pattern=(
                            path_pattern(entity)
                            if callable(path_pattern)
                            else path_pattern
                        ),
                    )


@dataclass
class _CedsTable:
    entity: str
    filename: str
    url: str
    hash: str
    path_pattern: str

    def __repr__(self):
        return f"""<Data from: {self.path_pattern.format(entity=self.entity)}>"""

    def _get_file_path(self):
        return pooch.retrieve(
            path=pooch.os_cache("openclimatedata/ceds"),
            fname=self.filename,
            url=self.url,
            known_hash=self.hash,
        )

    def _load_csv_from_zip(self, path_pattern):
        file_path = self._get_file_path()
        with ZipFile(file_path) as zip_file:
            dtype = {
                "country": "category",
                "iso": "category",
                "em": "category",
                "units": "category",
                "sector": "category",
                "fuel": "category",
            }

            path = self.path_pattern.format(entity=self.entity)
            # Workaround: in v_2025_03_18 NMVOC file is named as `emissions`, others `estimates`
            if path.endswith(
                "NMVOC_CEDS_estimates_by_country_CEDS_sector_fuel_v_2025_03_18.csv"
            ):
                path = path.replace("estimates", "emissions")
            df = pd.read_csv(
                zip_file.open(path),
                dtype=dtype,
            )

        return df

    def to_dataframe(self):
        return self._load_csv_from_zip(self.path_pattern)

    def to_long_dataframe(self):
        """
        Turn CEDS data into a long dataframe.
        """
        df = self.to_dataframe()

        id_vars = [c for c in df.columns if not c.startswith("X")]

        df.columns = [int(c[1:]) if c.startswith("X") else c for c in df.columns]

        df = df.melt(
            id_vars=id_vars,
            var_name="year",
            value_name="value",
        )
        df["year"] = df["year"].astype("int32")
        return df

    def to_ocd(self):
        """Return a long DataFrame with standardized codes and column names."""
        df = self.to_long_dataframe()
        column_names = {
            "em": "entity",
            "units": "unit",
        }
        if "iso" in df.columns:
            column_names["iso"] = "code"
        elif "country" in df.columns:
            column_names["country"] = "code"
        df = df.rename(columns=column_names)

        if "code" in df.columns:
            df["code"] = df["code"].cat.rename_categories(
                {"global": "BUNKERS", "srb (kosovo)": "XKX"}
            )
            df["code"] = df["code"].cat.rename_categories(str.upper)
        return df


CEDS = {
    "v_2025_03_18": _CedsRelease(
        name="CEDS v_2025_03_18 Aggregate Data",
        doi="10.5281/zenodo.15059443",
        published="2025-03-18",
        citation="""Hoesly, R., Smith, S. J., Ahsan, H., Prime, N., O'Rourke, P., Crippa, M., Klimont, Z., Guizzardi, D., Feng, L., Harkins, C., MCDONALD, B., & Wang, S. (2025). CEDS v_2025_03_18 Aggregate Data (v_2025_03_18) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.15059443""",
        license="CC BY 4.0",
        entities=[
            "BC",
            "CH4",
            "CO",
            "CO2",
            "N2O",
            "NH3",
            "NMVOC",
            "NOx",
            "OC",
            "SO2",
        ],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v_2025_03_18_aggregate.zip",
                    "url": "https://zenodo.org/records/15059443/files/CEDS_v_2025_03_18_aggregate.zip",
                    "hash": "md5:262b30b8f88708d6a567dbb58ec623a5",
                },
                "patterns": {
                    "by_country": "CEDS_v_2025_03_18_aggregate/{entity}_CEDS_estimates_by_country_v_2025_03_18.csv",
                    "by_sector": "CEDS_v_2025_03_18_aggregate/{entity}_CEDS_estimates_by_country_sector_v_2025_03_18.csv",
                    "global_by_sector": "CEDS_v_2025_03_18_aggregate/{entity}_CEDS_global_estimates_by_sector_v_2025_03_18.csv",
                    "global_by_sector_fuel": "CEDS_v_2025_03_18_aggregate/{entity}_CEDS_global_estimates_by_sector_fuel_v_2025_03_18.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2025_03_18_detailed.zip",
                    "url": "https://zenodo.org/records/15059443/files/CEDS_v_2025_03_18_detailed.zip",
                    "hash": "md5:ee40a44dfca8b9c4751119c3d9daf22f",
                },
                "patterns": {
                    "by_sector_fuel": "CEDS_v_2025_03_18_detailed/{entity}_CEDS_estimates_by_country_CEDS_sector_fuel_v_2025_03_18.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2025_03_18_supplementary_bunkers.zip",
                    "url": "https://zenodo.org/records/15059443/files/CEDS_v_2025_03_18_supplementary_bunkers.zip",
                    "hash": "md5:6fc40fdccb1482768887141de20a1da6",
                },
                "patterns": {
                    "bunkers": "CEDS_v_2025_03_18_supplementary_bunkers/S.{entity}_bunker_estimates_v_2025_03_18.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2025_03_18_supplementary_extension.zip",
                    "url": "https://zenodo.org/records/15059443/files/CEDS_v_2025_03_18_supplementary_extension.zip",
                    "hash": "md5:5c2f99d3f18dbd896bb240f8a6c770ce",
                },
                "patterns": {
                    "extension_by_fuel": "CEDS_v_2025_03_18_supplementary_extension/{entity}_Extension_CEDS_global_estimates_by_fuel_v_2025_03_18.csv",
                    "extension_by_sector_fuel": "CEDS_v_2025_03_18_supplementary_extension/{entity}_Extension_CEDS_global_estimates_by_sector_fuel_v_2025_03_18.csv",
                    "extension_by_sector": "CEDS_v_2025_03_18_supplementary_extension/{entity}_Extension_CEDS_global_estimates_by_sector_v_2025_03_18.csv",
                },
            },
        ],
    ),
    "v_2024_07_08": _CedsRelease(
        name="CEDS v_2024_07_08 Release Emission Data",
        doi="10.5281/zenodo.12803197",
        published="2024-07-24",
        citation="""Hoesly, R., Smith, S. J., Prime, N., Ahsan, H., Suchyta, H., O'Rourke, P., Crippa, M., Klimont, Z., Guizzardi, D., Behrendt, J., Feng, L., Harkins, C., McDonald, B., Mott, A., McDuffie, A., Nicholson, M., & Wang, S. (2024). CEDS v_2024_07_08 Release Emission Data (v_2024_07_08) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.12803197""",
        license="CC BY 4.0",
        entities=[
            "BC",
            "CH4",
            "CO",
            "CO2",
            "N2O",
            "NH3",
            "NMVOC",
            "NOx",
            "OC",
            "SO2",
        ],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_07_08_aggregate.zip",
                    "url": "https://zenodo.org/records/12803197/files/CEDS_v_2024_07_08_aggregate.zip",
                    "hash": "md5:4ad029d409b8a66ed6f3d85319c66964",
                },
                "patterns": {
                    "by_country": "{entity}_CEDS_emissions_by_country_v2024_07_08.csv",
                    "by_sector": "{entity}_CEDS_emissions_by_country_sector_v2024_07_08.csv",
                    "global_by_sector": "{entity}_CEDS_global_emissions_by_sector_v2024_07_08.csv",
                    "global_by_sector_fuel": "{entity}_CEDS_global_emissions_by_sector_fuel_v2024_07_08.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_07_08_detailed.zip",
                    "url": "https://zenodo.org/records/12803197/files/CEDS_v_2024_07_08_detailed.zip",
                    "hash": "md5:558811c1a1c8e6997dcb266c18f9c093",
                },
                "patterns": {
                    "by_sector_fuel": "{entity}_CEDS_emissions_by_country_CEDS_sector_fuel_v2024_07_08.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_07_08_supplementary_bunkers.zip",
                    "url": "https://zenodo.org/records/12803197/files/CEDS_v_2024_07_08_supplementary_bunkers.zip",
                    "hash": "md5:8b90232036c5aea8ba1376c7450d23a4",
                },
                "patterns": {
                    "bunkers": "S.{entity}_bunker_emissions_v2024_07_08.csv",
                },
            },
        ],
    ),
    "v_2024_04_01": _CedsRelease(
        name="CEDS v_2024_04_01 Release Emission Data",
        doi="10.5281/zenodo.10904361",
        published="2024-04-01",
        citation="""Hoesly, R., & Smith, S. (2024). CEDS v_2024_04_01 Release Emission Data (v_2024_04_01) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10904361""",
        license="CC BY 4.0",
        entities=[
            "BC",
            "CH4",
            "CO",
            "CO2",
            "N2O",
            "NH3",
            "NMVOC",
            "NOx",
            "OC",
            "SO2",
        ],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_04_01_aggregate.zip",
                    "url": "https://zenodo.org/records/10904361/files/CEDS_v_2024_04_01_aggregate.zip",
                    "hash": "md5:636752881e915244bb96b4793d9fb121",
                },
                "patterns": {
                    "by_country": "CEDS_v_2024_04_01_aggregate/{entity}_CEDS_emissions_by_country_v2024_04_01.csv",
                    "by_sector": "CEDS_v_2024_04_01_aggregate/{entity}_CEDS_emissions_by_country_sector_v2024_04_01.csv",
                    "global_by_sector": "CEDS_v_2024_04_01_aggregate/{entity}_CEDS_global_emissions_by_sector_v2024_04_01.csv",
                    "global_by_sector_fuel": "CEDS_v_2024_04_01_aggregate/{entity}_CEDS_global_emissions_by_sector_fuel_v2024_04_01.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_04_01_detailed.zip",
                    "url": "https://zenodo.org/records/10904361/files/CEDS_v_2024_04_01_detailed.zip",
                    "hash": "md5:8310c3c9ad0da67c11f61168ca7d265d",
                },
                "patterns": {
                    "by_sector_fuel": "CEDS_v_2024_04_01_detailed/{entity}_CEDS_emissions_by_country_CEDS_sector_fuel_v2024_04_01.csv",
                },
            },
            {
                "zipfile": {
                    "filename": "CEDS_v_2024_04_01_supplementary_bunkers.zip",
                    "url": "https://zenodo.org/records/10904361/files/CEDS_v_2024_04_01_supplementary_bunkers.zip",
                    "hash": "md5:49d6bbe523409ca61cc84854fe4a27b2",
                },
                "patterns": {
                    "bunkers": "CEDS_v_2024_04_01_supplementary_bunkers/S.{entity}_bunker_emissions_v2024_04_01.csv",
                },
            },
        ],
    ),
    "v_2021_04_21": _CedsRelease(
        name="CEDS v_2021_04_21 Release Emission Data",
        doi="10.5281/zenodo.4741285",
        published="2021-04-06",
        # TODO fix the citation with the correct version number? see https://github.com/JGCRI/CEDS/issues/48
        citation="""O'Rourke, P. R., Smith, S. J., Mott, A., Ahsan, H., McDuffie, E. E., Crippa, M., Klimont, Z., McDonald, B., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2021). CEDS v_2021_04_21 Release Emission Data (v_2021_02_05) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4741285""",
        license="CC BY 4.0",
        entities=[
            "BC",
            "CH4",
            "CO",
            "CO2",
            "N2O",
            "NH3",
            "NMVOC",
            "NOx",
            "OC",
            "SO2",
        ],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v2021-04-21_emissions.zip",
                    "url": "https://zenodo.org/records/4741285/files/CEDS_v2021-04-21_emissions.zip",
                    "hash": "md5:01659c651754a66ddf3d79715a2ba841",
                },
                "patterns": {
                    "by_country": "{entity}_CEDS_emissions_by_country_2021_04_21.csv",
                    "by_sector": "{entity}_CEDS_emissions_by_sector_country_2021_04_21.csv",
                    "by_fuel": "{entity}_CEDS_emissions_by_country_fuel_2021_04_21.csv",
                },
            },
        ],
    ),
    "v_2021_02_05": _CedsRelease(
        name="CEDS v_2021_02_05 Release Emission Data",
        doi="10.5281/zenodo.4509372",
        published="2021-02-05",
        citation="""O'Rourke, P. R., Smith, S. J., Mott, A., Ahsan, H., McDuffie, E. E., Crippa, M., Klimont, Z., McDonald, B., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2021). CEDS v_2021_02_05 Release Emission Data (v_2021_02_05) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4509372""",
        license="CC BY 4.0",
        entities=[
            "BC",
            "CH4",
            "CO",
            "CO2",
            "N2O",
            "NH3",
            "NMVOC",
            "NOx",
            "OC",
            "SO2",
        ],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v2021-02-05_emissions.zip",
                    "url": "https://zenodo.org/records/4509372/files/CEDS_v2021-02-05_emissions.zip",
                    "hash": "md5:7054c1e1ca510015a37d6c1bb5934c9b",
                },
                "patterns": {
                    "by_country": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_country_2021_02_05.csv",
                    "by_sector": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_sector_country_2021_02_05.csv",
                    "by_fuel": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_country_fuel_2021_02_05.csv",
                },
            },
        ],
    ),
    "v_2020_09_11": _CedsRelease(
        name="CEDS v_2020_09_11 Pre-Release Emission Data",
        doi="10.5281/zenodo.4025316",
        published="2020-09-11",
        citation="""O'Rourke, P. R., Smith, S. J., McDuffie, E. E., Klimont, Z., Crippa, M., Mott, A., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2020). CEDS v_2020_09_11 Pre-Release Emission Data (v_2020_09_11) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4025316""",
        license="CC BY 4.0",
        entities=["BC", "CO", "NH3", "NMVOC", "NOx", "OC", "SO2"],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v_2020_09_11_emissions.zip",
                    "url": "https://zenodo.org/records/4025316/files/CEDS_v_2020_09_11_emissions.zip",
                    "hash": "md5:0c7f4bfc5eafcd7510920fd0b8bbdd16",
                },
                "patterns": {
                    "by_country": "{entity}_CEDS_emissions_by_country_2020_09_11.csv",
                    "by_sector": "{entity}_CEDS_emissions_by_sector_country_2020_09_11.csv",
                    "by_fuel": "{entity}_CEDS_emissions_by_country_fuel_2020_09_11.csv",
                },
            },
        ],
    ),
    "v_2019_12_23": _CedsRelease(
        name="CEDS v_2019_12_23 Emission Data",
        doi="10.5281/zenodo.3606753",
        published="2020-01-13",
        citation="""Hoesly, R. M., O'Rourke, P. R., Smith, S. J., Feng, L., Klimont, Z., Janssens-Maenhout, G., Pitkanen, T., Seibert, J. J., Vu, L., Andres, R. J., Bolt, R. M., Bond, T. C., Dawidowski, L., Kholod, N., Kurokawa, J.-. ichi ., Li, M., Liu, L., Lu, Z., Moura, M. C. P., Zhang, Q., Goldstein, B., Muwan, P. (2020). CEDS v_2019_12_23 Emission Data (v_2019_12_23) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.3606753""",
        license="CC BY 4.0",
        entities=["BC", "CH4", "CO", "CO2", "NH3", "NMVOC", "NOx", "OC", "SO2"],
        tables=[
            {
                "zipfile": {
                    "filename": "CEDS_v_2019_12_23-final_emissions.zip",
                    "url": "https://zenodo.org/records/3606753/files/CEDS_v_2019_12_23-final_emissions.zip",
                    "hash": "md5:830ac6fbc5ba24885acecf1aa6567db8",
                },
                "patterns": {
                    "by_country": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_emissions_by_country_v_2019_12_23.csv",
                    "by_sector": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_emissions_by_country_CEDS_sector_v_2019_12_23.csv",
                    "global_by_fuel": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_global_emissions_by_fuel_v_2019_12_23.csv",
                },
            },
        ],
    ),
    # "As of 2 August 2018, a corrected supplement is available for download,
    # which now includes missing data files, most notably, CO2 and CH4 emissions." (Corrected Supplement Explanation.docx)
    # The data supplementary zip file contains file with filenames starting with 2017_05_18 and 2016_07_26
    # The CH4_Extension files (by region) are not included below
    "v_2018_08_02": _CedsRelease(
        name="CEDS Corrected Supplemental Data",
        doi="https://doi.org/10.5194/gmd-11-369-2018",
        published="2018-08-02",
        citation="""Hoesly, R. M., Smith, S. J., Feng, L., Klimont, Z., Janssens-Maenhout, G., Pitkanen, T., Seibert, J. J., Vu, L., Andres, R. J., Bolt, R. M., Bond, T. C., Dawidowski, L., Kholod, N., Kurokawa, J.-I., Li, M., Liu, L., Lu, Z., Moura, M. C. P., O'Rourke, P. R., and Zhang, Q.: Historical (1750–2014) anthropogenic emissions of reactive gases and aerosols from the Community Emissions Data System (CEDS), Geosci. Model Dev., 11, 369-408, https://doi.org/10.5194/gmd-11-369-2018, 2018.""",
        license="CC BY 3.0",
        entities=["SO2", "NOx", "BC", "OC", "NH3", "NMVOC", "CO", "CO2", "CH4"],
        tables=[
            {
                "zipfile": {
                    "filename": "gmd-11-369-2018-supplement.zip",
                    "url": "https://doi.org/10.5194/gmd-11-369-2018-supplement",
                    "hash": "md5:af7e686222c2c98cd3a38f2b9a5dbd24",
                },
                "patterns": {
                    "by_country": lambda entity: (
                        "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_country_v2016_07_26.csv"
                        if entity not in ["CO2", "CH4"]
                        else "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_country_v2017_05_18.csv"
                    ),
                    "by_sector": lambda entity: (
                        "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_sector_country_v2016_07_26.csv"
                        if entity not in ["CO2", "CH4"]
                        else "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_sector_country_v2017_05_18.csv"
                    ),
                    "global_by_sector": lambda entity: (
                        "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_sector_v2016_07_26.csv"
                        if entity not in ["CO2", "CH4"]
                        else "Supplemental_Data_Correction/Data Supplement/{entity}_CEDS_emissions_by_sector_v2017_05_18.csv"
                    ),
                },
            }
        ],
    ),
}
