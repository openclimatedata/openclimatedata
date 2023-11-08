from dataclasses import dataclass, field
import pooch
import pandas as pd


@dataclass
class _GCB_Fossil:
    name: str
    citation: str
    doi: str
    filename: str
    url: str
    hash: str
    filename_sources: str
    url_sources: str
    hash_sources: str
    license: str

    def __repr__(self):
        return f"""{self.name}
'{self.filename}'

License: {self.license}
https://doi.org/{self.doi}

{self.citation}"""

    def to_dataframe(self):
        file_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename,
            url=self.url,
            known_hash=self.hash,
        )
        return pd.read_csv(file_path, encoding="latin-1")

    def to_long_dataframe(self):
        df = self.to_dataframe()
        value_vars = df.columns[2:]
        df = df.reset_index().melt(
            id_vars=["Year", "ISO 3166-1 alpha-3"],
            value_vars=value_vars,
            var_name="Category",
            value_name="Value",
        )
        df = df.rename(columns={"ISO 3166-1 alpha-3": "Code"})

        file_path_sources = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename_sources,
            url=self.url_sources,
            known_hash=self.hash_sources,
        )
        df_sources = pd.read_csv(file_path_sources, encoding="latin-1")
        value_vars = df_sources.columns[2:]
        df_sources = df_sources.reset_index().melt(
            id_vars=["Year", "ISO 3166-1 alpha-3"],
            value_vars=value_vars,
            var_name="Category",
            value_name="Source",
        )
        df_sources = df_sources.rename(columns={"ISO 3166-1 alpha-3": "Code"})

        df = df.set_index(["Year", "Code", "Category"])
        df_sources = df_sources.set_index(["Year", "Code", "Category"])
        return pd.concat([df, df_sources], axis="columns").reset_index()


GCB_Fossil_Emissions = {
    "2023": _GCB_Fossil(
        name="The Global Carbon Project's fossil CO2 emissions dataset",
        doi="10.5281/zenodo.10065794",
        filename="GCB2023v28_MtCO2_flat.csv",
        url="https://zenodo.org/records/10065794/files/GCB2023v28_MtCO2_flat.csv",
        hash="md5:23d6f3f0a7e88281d41f6eaf8aa68c37",
        filename_sources="GCB2023v28_sources_flat.csv",
        url_sources="https://zenodo.org/records/10065794/files/GCB2023v28_sources_flat.csv?download=1",
        hash_sources="md5:f2a5e14d1562f9be80ab8b59c607b9a2",
        citation="""Andrew, R. M., & Peters, G. P. (2023). The Global Carbon Project's fossil CO2 emissions dataset (2023v28) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10065794""",
        license="CC BY 4.0",
    ),
    "2022": _GCB_Fossil(
        name="The Global Carbon Project's fossil CO2 emissions dataset",
        doi="10.5281/zenodo.7215364",
        filename="GCB2022v27_MtCO2_flat.csv",
        url="https://zenodo.org/record/7215364/files/GCB2022v27_MtCO2_flat.csv",
        hash="md5:251ce1c5f07d5d28128fa84df856b2f9",
        filename_sources="GCB2022v27_sources_flat.csv",
        url_sources="https://zenodo.org/record/7215364/files/GCB2022v27_sources_flat.csv",
        hash_sources="md5:7ad24d6ec981b55404b0308ed5158d6e",
        citation="""Andrew, Robbie M., & Peters, Glen P. (2022). The Global Carbon Project's fossil CO2 emissions dataset (2022v27) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7215364""",
        license="CC BY 4.0",
    ),
    "2021": _GCB_Fossil(
        name="The Global Carbon Project's fossil CO2 emissions dataset",
        doi="10.5281/zenodo.5569235",
        filename="GCB2021v34_MtCO2_flat.csv",
        url="https://zenodo.org/record/5569235/files/GCB2021v34_MtCO2_flat.csv",
        hash="md5:00d432500752936a2c95f6feeb599a51",
        filename_sources="GCB2021v34_sources_flat.csv",
        url_sources="https://zenodo.org/record/5569235/files/GCB2021v34_sources_flat.csv",
        hash_sources="md5:ae185160899541fc4bef08fa869cbde2",
        citation="""Andrew, Robbie M., & Peters, Glen P. (2021). The Global Carbon Project's fossil CO2 emissions dataset (2021v34) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5569235""",
        license="CC BY 4.0",
    )

}
