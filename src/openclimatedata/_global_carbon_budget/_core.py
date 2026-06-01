import re
import warnings

from dataclasses import dataclass
from typing import Optional, Literal

import pandas as pd
import pooch
import openpyxl

from ._countrynames import mappings

unit_values = Literal["GtC/yr", "MtC/yr", "tC/person/yr"]


class _Global_Carbon_Budget_Release(dict):
    def __init__(
        self,
        name: str,
        version: int,
        data_version: str,
        doi: str,
        doi_article: str,
        published: str,
        citation: str,
        citation_article: str,
        license: str,
        global_carbon_budget: dict,
        national_fossil_carbon_emissions: dict,
        national_landuse_change_emissions: Optional[dict] = None,
    ):
        self.name = name
        self.version = version
        self.data_version = data_version
        self.doi = doi
        self.doi_article = doi_article
        self.published = published
        self.citation = citation
        self.citation_article = citation_article
        self.license = license

        self.Global_Budget = _Global_Carbon_Budget_File(
            release=self,
            filename=global_carbon_budget["filename"],
            url=global_carbon_budget["url"],
            known_hash=global_carbon_budget["known_hash"],
            sheets=global_carbon_budget["sheets"],
        )

        self.National_Fossil_Emissions = _Global_Carbon_Budget_File(
            release=self,
            filename=national_fossil_carbon_emissions["filename"],
            url=national_fossil_carbon_emissions["url"],
            known_hash=national_fossil_carbon_emissions["known_hash"],
            sheets=national_fossil_carbon_emissions["sheets"],
        )

        if national_landuse_change_emissions:
            self.National_Landuse_Change_Emissions = _Global_Carbon_Budget_File(
                release=self,
                filename=national_landuse_change_emissions["filename"],
                url=national_landuse_change_emissions["url"],
                known_hash=national_landuse_change_emissions["known_hash"],
                sheets=national_landuse_change_emissions["sheets"],
            )

    def __repr__(self):
        repr = f"""{self.name}

Article: {self.citation_article}

Data: {self.citation}

License: {self.license}
https://doi.org/{self.doi}

Global_Carbon_Budget['{self.version}'].Global_Budget: `{self.Global_Budget.filename}`
Global_Carbon_Budget['{self.version}'].National_Fossil_Emissions: `{self.National_Fossil_Emissions.filename}`"""
        if hasattr(self, "National_Landuse_Change_Emissions"):
            repr += f"""
Global_Carbon_Budget['{self.version}'].National_Landuse_Change_Emissions: `{self.National_Landuse_Change_Emissions.filename}`
"""
        return repr


class _Global_Carbon_Budget_File(dict):
    def __init__(
        self, release: object, filename: str, url: str, known_hash: str, sheets: list
    ):
        self.release = release
        self.filename = filename
        self.url = url
        self.known_hash = known_hash
        self.sheets = sheets

        for sheet in sheets:
            self[sheet["sheet_name"]] = _Global_Carbon_Budget_Sheet(
                release=self.release, file=self, **sheet
            )

    def _get_file_path(self):
        return pooch.retrieve(
            path=pooch.os_cache("openclimatedata/global-carbon-budget"),
            fname=self.filename,
            url=self.url,
            known_hash=self.known_hash,
        )

    def __repr__(self):
        return f"""
{self.filename}

Sheets:
""" + "\n".join([sheet["sheet_name"] for sheet in self.sheets])


class _Global_Carbon_Budget_Sheet(dict):
    def __init__(
        self,
        release: object,
        file: object,
        sheet_name: str,
        skiprows: int,
        unit: unit_values = "GtC/yr",
        unit_overwrite: dict[str, unit_values] = {},
        nrows: Optional[int] = None,
        columns: Optional[str] = None,
        tables: Optional[list] = None,
    ):
        self.release = release
        self.file = file
        self.sheet_name = sheet_name
        self.skiprows = skiprows
        self.unit = unit
        self.unit_overwrite = unit_overwrite
        self.nrows = nrows
        self.columns = columns

        # Sheets with complex tables are handled as sub-tables
        if tables:
            for table in tables:
                self[table["table_name"]] = _Global_Carbon_Budget_Table(
                    sheet=self,
                    table_name=table["table_name"],
                    skiprows=table["skiprows"],
                    columns=table["columns"],
                    nrows=table.get("nrows", None),
                )
        else:
            self.to_dataframe = self._to_dataframe
            self.to_long_dataframe = self._to_long_dataframe
            self.to_ocd = self._to_ocd

    def __repr__(self):
        if not hasattr(self, "note"):
            file_path = self.file._get_file_path()
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            rows = [
                list(row)
                for row in list(
                    wb[self.sheet_name].iter_rows(
                        max_row=self.skiprows, values_only=True
                    )
                )
            ]
            note = ""
            for row in rows:
                line = ("\t".join([cell if cell else "\t" for cell in row])).strip()
                if not line.startswith("AFGHANISTAN"):
                    note += line
                note += "\n"

            self.note = note

        return f"""{self.release.name} — {self.file.filename}  — {self.sheet_name}

{self.note}
""".strip()

    def _to_dataframe(self):
        file_path = self.file._get_file_path()
        with warnings.catch_warnings(action="ignore", category=UserWarning):
            df = pd.read_excel(
                file_path,
                sheet_name=self.sheet_name,
                skiprows=self.skiprows,
                usecols=self.columns,
                index_col=0,
                nrows=self.nrows,
            )
        df.index.name = "Year"
        return df

    def _to_long_dataframe(self):
        df = self.to_dataframe()
        value_vars = df.columns
        var_name = "Country" if value_vars[0] == "Afghanistan" else "Category"

        qf = None
        if self.file.filename.startswith("National_LandUse") and "QF" in df.index:
            qf = df.loc["QF"].astype("Int64")
            df = df.drop("QF")

        with warnings.catch_warnings(
            action="ignore", category=pd.errors.PerformanceWarning
        ):
            df = df.reset_index().melt(
                id_vars=["Year"],
                value_vars=value_vars,
                var_name=var_name,
                value_name="Value",
            )
        df[var_name] = df[var_name].astype("category")

        if isinstance(qf, pd.Series):
            df = (
                df.set_index("Country")
                .merge(qf, left_index=True, right_index=True)
                .reset_index()
            )
            df["QF"] = df["QF"].astype("category")

        return df

    def _to_ocd(self):
        """Long DataFrame with all column names lower-cased."""
        df = self._to_long_dataframe()
        df.columns = df.columns.map(lambda x: x.lower())

        if "category" in df.columns:
            df["unit"] = df.apply(
                lambda x: (
                    self.unit_overwrite[x["category"]]
                    if x["category"] in self.unit_overwrite
                    else self.unit
                ),
                axis=1,
            )
        elif "country" in df.columns:
            # For national fossil and land-use emissions all columns should have the same unit, so no overwrite needed
            df["unit"] = self.unit

            df["code"] = df["country"].apply(lambda x: mappings.get(x, x))
            df = df.drop("country", axis=1)
            df = df[["code", "year", "value", "unit"]]

        return df


@dataclass
class _Global_Carbon_Budget_Table:
    sheet: object
    table_name: str
    skiprows: int
    columns: str
    nrows: Optional[int] = None

    def __repr__(self):
        return f"""{self.sheet.sheet_name} - {self.table_name} - {self.columns}"""

    def to_dataframe(self):
        file_path = self.sheet.file._get_file_path()
        df = pd.read_excel(
            file_path,
            sheet_name=self.sheet.sheet_name,
            skiprows=self.skiprows,
            usecols=self.columns,
            index_col=0,
            nrows=self.nrows,
        )
        # Remove suffixes `.1`, `.2`, etc. from duplicated columns names
        # (added by Pandas, see https://github.com/pandas-dev/pandas/issues/64198).
        # `CLM5.0` or `CLM6.0` needs to remain
        df.columns = df.columns.map(lambda x: re.sub(r"\.[1234]$", "", x))
        df.columns = df.columns.str.strip()
        df.name = self.table_name
        df.index.name = "Year"
        return df

    def to_long_dataframe(self):
        df = self.to_dataframe()
        value_vars = df.columns
        df = df.reset_index().melt(
            id_vars=["Year"],
            value_vars=value_vars,
            var_name="Category",
            value_name="Value",
        )
        df.Category = df.Category.astype("category")
        return df

    def to_ocd(self):
        """Long DataFrame with all column names lower-cased."""
        df = self.to_long_dataframe()
        df.columns = df.columns.map(lambda x: x.lower())
        df["unit"] = df.apply(
            lambda x: (
                self.sheet.unit_overwrite[x["category"]]
                if x["category"] in self.sheet.unit_overwrite
                else self.sheet.unit
            ),
            axis=1,
        )

        return df
