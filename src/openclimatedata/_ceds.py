import re

from dataclasses import dataclass
from zipfile import ZipFile
import pooch
import pandas as pd
import pyarrow as pa
import numpy as np

_dtype_category = pd.ArrowDtype(pa.dictionary(pa.int16(), pa.string()))


@dataclass
class _CedsRelease(dict):

    name: str
    citation: str
    doi: str
    published: str
    filename: str
    url: str
    hash: str
    license: str
    table_patterns: dict

    def __repr__(self):
        newline = "\n"

        return f"""{self.name}
'{self.filename}'

License: {self.license}
https://doi.org/{self.doi}

Citation:
{self.citation}

{len(self.entities)} entities:
{newline.join([f'- "{k}"' for k in self.entities])}"""

    def __post_init__(self):

        file_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename,
            url=self.url,
            known_hash=self.hash,
        )
        with ZipFile(file_path) as zip_file:
            filelist = zip_file.infolist()
            csv_files = [
                re.sub(
                    r"^CEDS_", "", f.filename.rsplit("/")[-1]
                )  # replace leading 'CEDS' for 2019 files which are in a subdirectory
                for f in filelist
                if ".csv" in f.filename and not f.filename.startswith("_")
            ]
        self.entities = sorted(
            list(set([f.split("_", maxsplit=1)[0] for f in csv_files]))
        )

        for entity in self.entities:
            if entity not in self.keys():
                self[entity] = {}
            for key, value in self.table_patterns.items():
                self[entity][key] = _CedsTable(
                    entity=entity,
                    filename=self.filename,
                    url=self.url,
                    hash=self.hash,
                    path_pattern=value,
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
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename,
            url=self.url,
            known_hash=self.hash,
        )

    def _load_csv_from_zip(self, path_pattern):
        file_path = self._get_file_path()
        with ZipFile(file_path) as zip_file:
            df = pd.read_csv(
                zip_file.open(self.path_pattern.format(entity=self.entity)),
                engine="pyarrow",
            )

        _dtype_category = pd.ArrowDtype(pa.dictionary(pa.int16(), pa.string()))
        if "country" in df.columns:
            df["country"] = df["country"].astype(_dtype_category)
        elif "iso" in df.columns:
            df["iso"] = df["iso"].astype(_dtype_category)
        df["em"] = df["em"].astype(_dtype_category)
        df["units"] = df["units"].astype(_dtype_category)
        if "sector" in self.path_pattern:
            df["sector"] = df["sector"].astype(_dtype_category)
        elif "fuel" in self.path_pattern:
            df["fuel"] = df["fuel"].astype(_dtype_category)
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
        df["year"] = df["year"].astype("uint16[pyarrow]")
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
            df["code"] = df["code"].astype("category")
            df["code"] = df["code"].cat.rename_categories(
                {"global": "BUNKERS", "srb (kosovo)": "XKX"}
            )
            df["code"] = df["code"].cat.rename_categories(str.upper)
            df["code"] = df["code"].astype(_dtype_category)
        return df


CEDS = {
    "v_2021_04_21": _CedsRelease(
        **{
            "name": "CEDS v_2021_04_21 Release Emission Data",
            "doi": "10.5281/zenodo.4741285",
            "published": "2021-04-06",
            "filename": "CEDS_v2021-04-21_emissions.zip",
            "url": "https://zenodo.org/records/4741285/files/CEDS_v2021-04-21_emissions.zip",
            "hash": "md5:01659c651754a66ddf3d79715a2ba841",
            # TODO fix the citation with the correct version number? see https://github.com/JGCRI/CEDS/issues/48
            "citation": """O'Rourke, P. R., Smith, S. J., Mott, A., Ahsan, H., McDuffie, E. E., Crippa, M., Klimont, Z., McDonald, B., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2021). CEDS v_2021_04_21 Release Emission Data (v_2021_02_05) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4741285""",
            "license": "CC BY 4.0",
            "table_patterns": {
                "by_country": "{entity}_CEDS_emissions_by_country_2021_04_21.csv",
                "by_sector_country": "{entity}_CEDS_emissions_by_sector_country_2021_04_21.csv",
                "by_country_fuel": "{entity}_CEDS_emissions_by_country_fuel_2021_04_21.csv",
            },
        }
    ),
    "v_2021_02_05": _CedsRelease(
        **{
            "name": "CEDS v_2021_02_05 Release Emission Data",
            "doi": "10.5281/zenodo.4509372",
            "published": "2021-02-05",
            "filename": "CEDS_v2021-02-05_emissions.zip",
            "url": "https://zenodo.org/records/4509372/files/CEDS_v2021-02-05_emissions.zip",
            "hash": "md5:7054c1e1ca510015a37d6c1bb5934c9b",
            "citation": """O'Rourke, P. R., Smith, S. J., Mott, A., Ahsan, H., McDuffie, E. E., Crippa, M., Klimont, Z., McDonald, B., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2021). CEDS v_2021_02_05 Release Emission Data (v_2021_02_05) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4509372""",
            "license": "CC BY 4.0",
            "table_patterns": {
                "by_country": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_country_2021_02_05.csv",
                "by_sector_country": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_sector_country_2021_02_05.csv",
                "by_country_fuel": "CEDS_v2021-02-05_emissions/{entity}_CEDS_emissions_by_country_fuel_2021_02_05.csv",
            },
        }
    ),
    "v_2020_09_11": _CedsRelease(
        **{
            "name": "CEDS v_2020_09_11 Pre-Release Emission Data",
            "doi": "10.5281/zenodo.4025316",
            "published": "2020-09-11",
            "filename": "CEDS_v_2020_09_11_emissions.zip",
            "url": "https://zenodo.org/records/4025316/files/CEDS_v_2020_09_11_emissions.zip",
            "hash": "md5:0c7f4bfc5eafcd7510920fd0b8bbdd16",
            "citation": """O'Rourke, P. R., Smith, S. J., McDuffie, E. E., Klimont, Z., Crippa, M., Mott, A., Wang, S., Nicholson, M. B., Feng, L., & Hoesly, R. M. (2020). CEDS v_2020_09_11 Pre-Release Emission Data (v_2020_09_11) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4025316""",
            "license": "CC BY 4.0",
            "table_patterns": {
                "by_country": "{entity}_CEDS_emissions_by_country_2020_09_11.csv",
                "by_sector_country": "{entity}_CEDS_emissions_by_sector_country_2020_09_11.csv",
                "by_country_fuel": "{entity}_CEDS_emissions_by_country_fuel_2020_09_11.csv",
            },
        }
    ),
    "v_2019_12_23": _CedsRelease(
        **{
            "name": "CEDS v_2019_12_23 Emission Data",
            "doi": "10.5281/zenodo.3606753",
            "published": "2020-01-13",
            "filename": "CEDS_v_2019_12_23-final_emissions.zip",
            "url": "https://zenodo.org/records/3606753/files/CEDS_v_2019_12_23-final_emissions.zip",
            "hash": "md5:830ac6fbc5ba24885acecf1aa6567db8",
            "citation": """Hoesly, R. M., O'Rourke, P. R., Smith, S. J., Feng, L., Klimont, Z., Janssens-Maenhout, G., Pitkanen, T., Seibert, J. J., Vu, L., Andres, R. J., Bolt, R. M., Bond, T. C., Dawidowski, L., Kholod, N., Kurokawa, J.-. ichi ., Li, M., Liu, L., Lu, Z., Moura, M. C. P., Zhang, Q., Goldstein, B., Muwan, P. (2020). CEDS v_2019_12_23 Emission Data (v_2019_12_23) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.3606753""",
            "license": "CC BY 4.0",
            "table_patterns": {
                "by_country": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_emissions_by_country_v_2019_12_23.csv",
                "by_sector_country": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_emissions_by_country_CEDS_sector_v_2019_12_23.csv",
                "global_by_fuel": "CEDS_v_2019_12_23-final_emissions/CEDS_{entity}_global_emissions_by_fuel_v_2019_12_23.csv",
            },
        }
    ),
}
