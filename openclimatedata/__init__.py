from dataclasses import dataclass, field
import pooch
import pandas as pd


@dataclass
class _PRIMAPHIST_2_3_1:
    filename: str
    known_hash: str
    note: str
    name: str = "PRIMAP-hist 2.3.1"
    doi: str = "10.5281/zenodo.5494497"
    license: str = "CC BY 4.0"

    def __repr__(self):
        return f"""{self.name}
{self.filename}
{self.note}
License: {self.license}
https://doi.org/{self.doi}
        """

    def to_dataframe(self):
        full_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            url=f"doi:{self.doi}/{self.filename}",
            known_hash=self.known_hash,
            progressbar=True,
        )
        return pd.read_csv(full_path)


PRIMAPHIST = {
    "2.3.1": _PRIMAPHIST_2_3_1(
        filename="Guetschow-et-al-2021-PRIMAP-hist_v2.3.1_20-Sep_2021.csv",
        known_hash="md5:f4cb55a55e4d5e5dcfb1513b677ae318",
        note="The main dataset with numerical extrapolation of all time series to 2019 and three significant digits.",
    ),
    "2.3.1_no_extrap": _PRIMAPHIST_2_3_1(
        filename="Guetschow-et-al-2021-PRIMAP-hist_v2.3.1_no_extrap_20-Sep_2021.csv",
        known_hash="md5:870bf6d47e74f9245d9f9803d7be80ea",
        note="Variant without numerical extrapolation of missing values and not including country groups (three significant digits).",
    ),
    "2.3.1_no_extrap_no_rounding": _PRIMAPHIST_2_3_1(
        filename="Guetschow-et-al-2021-PRIMAP-hist_v2.3.1_no_extrap_no_rounding_20-Sep_2021.csv",
        known_hash="md5:f0b9afb73aefbf40693d475ea3dcc6ad",
        note="Variant without numerical extrapolation of missing values and not including country groups (eleven significant digits).",
    ),
}
