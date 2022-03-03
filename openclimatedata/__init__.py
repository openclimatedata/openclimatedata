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
    citation: str = """Gütschow, J.; Günther, A.; Pflüger, M. (2021): The PRIMAP-hist national historical emissions time series v2.3.1 (1850-2019). zenodo. doi:10.5281/zenodo.5494497.

Gütschow, J.; Jeffery, L.; Gieseke, R.; Gebel, R.; Stevens, D.; Krapp, M.; Rocha, M. (2016): The PRIMAP-hist national historical emissions time series, Earth Syst. Sci. Data, 8, 571-603, doi:10.5194/essd-8-571-2016"""

    def __repr__(self):
        return f"""{self.name}
'{self.filename}'
{self.note}

License: {self.license}
https://doi.org/{self.doi}

Recommended citation:
{self.citation}
        """

    def to_dataframe(self):
        full_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            url=f"doi:{self.doi}/{self.filename}",
            known_hash=self.known_hash,
            progressbar=True,
        )
        return pd.read_csv(full_path)

    def to_long_dataframe(self):
        df = self.to_dataframe()
        df = df.melt(
            id_vars=[
                "source",
                "scenario (PRIMAP-hist)",
                "area (ISO3)",
                "entity",
                "unit",
                "category (IPCC2006_PRIMAP)",
            ],
            var_name="year",
            value_name="value",
        )
        df.year = df.year.astype(int)
        return df


@dataclass
class _GCB:
    sheet_name: str
    skiprows: int
    note: str
    citation: str
    name: str = "Global Carbon Budget 2021 - v0.6"
    doi: str = "10.18160/gcp-2021"
    filename: str = "Global_Carbon_Budget_2021v0.6.xlsx"
    license: str = "CC BY 4.0"

    def __repr__(self):
        return f"""{self.name}
'{self.filename}' - '{self.sheet_name}'

License: {self.license}
https://doi.org/{self.doi}

{self.note}

{self.citation}"""

    def to_dataframe(self):
        file_path = pooch.retrieve(
            path=pooch.os_cache("openclimatedata"),
            fname=self.filename,
            url="https://data.icos-cp.eu/licence_accept?ids=%5B%220ST81nXCND5VfAQdOCSJDveT%22%5D",
            known_hash="d124fcd675c2343e557c041d3824890ef793840d1d0c78875dd1fb6d2e14e6a8",
        )
        return pd.read_excel(
            file_path, sheet_name=self.sheet_name, skiprows=self.skiprows, index_col=0
        )

    def to_long_dataframe(self):
        df = self.to_dataframe()
        return df.reset_index().melt(
            id_vars=["Year"],
            value_vars=[
                "fossil.emissions.excluding.carbonation",
                "Coal",
                "Oil",
                "Gas",
                "Cement.emission",
                "Flaring",
                "Other",
                "Per.Capita",
            ],
            var_name="Category",
            value_name="Value",
        )


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

GCB = {
    "2021_historical_budget": _GCB(
        sheet_name="Historical Budget",
        skiprows=15,
        note="""Historical CO2 budget
All values in billion tonnes of carbon per year (GtC/yr), for the globe. For values in billion tonnes of carbon dioxide (CO2) per year, multiply the numbers below by 3.664.
1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
Please note: The methods used to estimate the historical fluxes presented below differ from the carbon budget presented from 1959 onwards. For example, the atmospheric growth and ocean sink do not account for year-to-year variability before 1959.
Uncertainties: see the original papers for uncertainties""",
        citation="""Cite as:  Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)
Fossil fuel combustion and cement production emissions:  Friedlingstein et al. (2021)
Land-use change emissions:  As in Global Carbon Budget from 1959: average of three bookkeeping models: H&N (Houghton &Nassikas, 2017), BLUE (Hansis, et al., 2015) and OSCAR (Gasser et al., 2020). Cite as:  Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)
Atmospheric CO2 growth rate: Joos, F. and Spahni, R.: Rates of change in natural and anthropogenic radiative forcing over the past 20,000 years, Proceedings of the National Academy of Science, 105, 1425-1430, 2008.
The ocean CO2 sink prior to 1959 is the average of the two diagnostic ocean models: DeVries, T. et al., Global Biogeochemical Cycles, 28, 631-647, 2014; and Khatiwala, S et al., Biogeosciences, 10, 2169-2191, 2013.
The land sink is as in Global Carbon Budget from 1959: average of 17 dynamic global vegetation models that reproduce the observed mean total land sink of the 1990s.
Cement carbonation is the average of two estimates: Friedlingstein et al. (2021)
The budget imbalance is the sum of emissions (fossil fuel and industry + land-use change) minus (atmospheric growth + ocean sink + land sink + cement carbonation sink); it is a measure of our imperfect data and understanding of the contemporary carbon cycle.
""",
    ),
    "2021_fossil_emissions_by_category": _GCB(
        sheet_name="Fossil Emissions by Category",
        skiprows=8,
        note="""Fossil fuel and cement production emissions by fuel type
All values in million tonnes of carbon per year (MtC/yr), except the per capita emissions which are in tonnes of carbon per person per year (tC/person/yr). For values in million tonnes of CO2 per year, multiply the values below by 3.664
1MtC = 1 million tonne of carbon = 3.664 million tonnes of CO2
Methods: Full details of the method are described in Friedlingstein et al (2021) and Andrew and Peters (2021)
The uncertainty for the global estimates is about ±5 % for a ± 1 sigma confidence level.""",
        citation="""Cite as: Friedlingstein et al (2021; https://doi.org/10.5194/essd-2021-386)""",
    ),
}
