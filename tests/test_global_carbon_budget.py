import os

import pandas as pd
import pytest
from pytest import approx

from openclimatedata import Global_Carbon_Budget

from openclimatedata._global_carbon_budget._countrynames import mappings

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


versions = Global_Carbon_Budget.keys()


def test_gcb():
    for version in versions:
        assert Global_Carbon_Budget[version].__repr__()
        assert Global_Carbon_Budget[version].name
        assert Global_Carbon_Budget[version].doi
        assert Global_Carbon_Budget[version].doi_article
        if "[preprint]" not in Global_Carbon_Budget[version].citation_article:
            assert Global_Carbon_Budget[version].published


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_dfs():
    # Index should be integer years
    # No column should be unnamed
    for version in versions:
        excel_files = [
            Global_Carbon_Budget[version].Global_Budget,
            Global_Carbon_Budget[version].National_Fossil_Emissions,
        ]
        if version >= "2022":
            excel_files += [
                Global_Carbon_Budget[version].National_Landuse_Change_Emissions
            ]
        for excel_file in excel_files:
            sheet_names = excel_file.keys()

            for sheet_name in sheet_names:
                if len(excel_file[sheet_name].keys()) > 0:
                    for subtable in excel_file[sheet_name].keys():
                        df = excel_file[sheet_name][subtable].to_dataframe()
                        assert type(df.index) is pd.RangeIndex
                        assert all([not i.startswith("Unnamed") for i in df.columns])
                else:
                    df = excel_file[sheet_name].to_dataframe()
                    if "QF" in df.index:  # early National Landuse data has a QF row
                        assert type(df.index) is pd.Index
                    else:
                        assert type(df.index) is pd.RangeIndex
                    assert all([not i.startswith("Unnamed") for i in df.columns])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_global_units():
    for version in versions:
        excel_file = Global_Carbon_Budget[version].Global_Budget
        sheet_names = excel_file.keys()
        for sheet_name in sheet_names:
            if len(excel_file[sheet_name].keys()) > 0:
                for subtable in excel_file[sheet_name].keys():
                    df = excel_file[sheet_name][subtable].to_ocd()
                    # Sheets with subtables all have GtC/yr
                    assert df.iloc[0].unit == "GtC/yr"
                    assert "GtC/yr" in excel_file[sheet_name].__repr__()
            else:
                df = excel_file[sheet_name].to_ocd()
                if version < "2025" and sheet_name.startswith(("Fossil", "Cement")):
                    assert df.iloc[0].unit == "MtC/yr"
                    assert "MtC/yr" in excel_file[sheet_name].__repr__()
                    if sheet_name.startswith("Fossil"):
                        assert df.iloc[-1].unit == "tC/person/yr"
                        assert "tC/person/yr" in excel_file[sheet_name].__repr__()
                else:
                    assert df.iloc[0].unit == "GtC/yr"
                    assert "GtC/yr" in excel_file[sheet_name].__repr__()


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_national_fossil_units():
    for version in versions:
        excel_file = Global_Carbon_Budget[version].National_Fossil_Emissions
        sheet_names = excel_file.keys()
        for sheet_name in sheet_names:
            df = excel_file[sheet_name].to_ocd()
            assert df.iloc[0].unit == "MtC/yr"
            assert "MtC/yr" in excel_file[sheet_name].__repr__()


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_national_landuse_change_units():
    for version in versions:
        if version < "2022":
            continue
        excel_file = Global_Carbon_Budget[version].National_Landuse_Change_Emissions
        sheet_names = excel_file.keys()
        for sheet_name in sheet_names:
            df = excel_file[sheet_name].to_ocd()
            assert df.iloc[0].unit in {"TgC/yr", "MtC/yr"}
            assert "MtC" in excel_file[sheet_name].__repr__()


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_national_fossil_emissions():
    for version in versions:
        excel_file = Global_Carbon_Budget[version].National_Fossil_Emissions

        territorial_emissions = excel_file["Territorial Emissions"]
        consumption_emissions = excel_file["Consumption Emissions"]
        emissions_transfer = excel_file["Emissions Transfers"]

        te_df = territorial_emissions.to_dataframe()
        te_ocd = territorial_emissions.to_ocd()

        assert te_df.index[-1] == int(version) - 1
        assert te_df.iloc[-1].World == te_ocd.iloc[-1].value

        ce_df = consumption_emissions.to_dataframe()
        ce_ocd = consumption_emissions.to_ocd()

        assert ce_df.index[-1] == int(version) - 1
        assert ce_df.iloc[-1].World == ce_ocd.iloc[-1].value

        et_df = emissions_transfer.to_dataframe()
        et_ocd = emissions_transfer.to_ocd()

        assert et_df.index[-1] == int(version) - 1
        assert et_df.iloc[-1].World == et_ocd.iloc[-1].value


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_national_landuse_change_emissions():
    for version in versions:
        if version < "2022":
            continue
        excel_file = Global_Carbon_Budget[version].National_Landuse_Change_Emissions

        for model in excel_file.keys():
            df = excel_file[model].to_dataframe()
            ocdf = excel_file[model].to_ocd()

            assert df.loc[1850].Afghanistan == ocdf.iloc[0].value
            assert df.iloc[-1, -1] == ocdf.iloc[-1].value


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_sheet_names():
    for version in versions:
        global_carbon_budget_sheet_names = Global_Carbon_Budget[
            version
        ].Global_Budget.keys()

        assert "Global Carbon Budget" in global_carbon_budget_sheet_names
        assert "Historical Budget" in global_carbon_budget_sheet_names
        if version >= "2025":
            assert "Atmospheric Growth" in global_carbon_budget_sheet_names
        if version > "2019":
            assert "Fossil Emissions by Category" in global_carbon_budget_sheet_names
            assert "Cement Carbonation Sink" in global_carbon_budget_sheet_names
        else:
            assert "Fossil Emissions by Fuel Type" in global_carbon_budget_sheet_names
        assert "Land-Use Change Emissions" in global_carbon_budget_sheet_names
        assert "Ocean Sink" in global_carbon_budget_sheet_names
        assert "Terrestrial Sink" in global_carbon_budget_sheet_names

        national_fossil_sheet_names = Global_Carbon_Budget[
            version
        ].National_Fossil_Emissions.keys()

        assert "Territorial Emissions" in national_fossil_sheet_names
        assert "Consumption Emissions" in national_fossil_sheet_names
        assert "Emissions Transfers" in national_fossil_sheet_names


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_countrynames():
    countrynames = set()
    special_codes = set(
        [
            "Africa",
            "Asia",
            "Bunkers",
            "Central America",
            "EU27",
            "EU28",
            "Europe",
            "KP Annex B",
            "Middle East",
            "Non KP Annex B",
            "Non-OECD",
            "North America",
            "Oceania",
            "OECD",
            "South America",
            "Statistical Difference",
            "DISPUTED",
            "OTHER",
            "TOTAL",
        ]
    )

    for version in versions:
        territorial_emissions = (
            Global_Carbon_Budget[version]
            .National_Fossil_Emissions["Territorial Emissions"]
            .to_dataframe()
        )
        for name in territorial_emissions.columns:
            countrynames.add(name)

        if version >= "2022":
            luc_emissions = (
                Global_Carbon_Budget[version]
                .National_Landuse_Change_Emissions[
                    list(
                        Global_Carbon_Budget[
                            version
                        ].National_Landuse_Change_Emissions.keys()
                    )[0]
                ]
                .to_dataframe()
            )
            for name in luc_emissions.columns:
                countrynames.add(name)

        ocd_codes = (
            Global_Carbon_Budget[version]
            .National_Fossil_Emissions["Territorial Emissions"]
            .to_ocd()
            .code.unique()
        )
        assert set([i for i in ocd_codes if len(i) > 3]).issubset(special_codes)

    special_codes.remove("TOTAL")
    assert countrynames.difference(set(mappings.keys())) == special_codes


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_dataframes_for_subtables_only():
    # In sheets with subtables, `to_dataframe` etc. should only be available
    # for tables, not on the main sheet.
    for version in versions:
        sheet_names = Global_Carbon_Budget[version].Global_Budget.keys()

        for sheet_name in sheet_names:
            if (
                len(
                    Global_Carbon_Budget[version]
                    .Global_Budget[sheet_name]
                    .keys()
                )
                > 0
            ):
                assert "to_dataframe" not in dir(
                    Global_Carbon_Budget[version].Global_Budget[sheet_name]
                )
                assert "to_long_dataframe" not in dir(
                    Global_Carbon_Budget[version].Global_Budget[sheet_name]
                )


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2025():
    year = "2025"
    gcb = Global_Carbon_Budget[year].Global_Budget
    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()
    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()

    luc_emissions_blue = gcb["Land-Use Change Emissions"]["BLUE"].to_dataframe()

    luc_emissions_luce = gcb["Land-Use Change Emissions"]["LUCE"].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    assert list(luc_emissions_luce.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models (NET) - Does not include peat emissions"
    ].to_dataframe()

    assert "CLM6.0" in luc_emisssions_individual_models.columns

    atmospheric_growth = gcb["Atmospheric Growth"]["GCB"].to_dataframe()
    atmospheric_growth_individual_inversions = gcb["Atmospheric Growth"][
        "Individual Inversions"
    ].to_dataframe()

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"]["fCO2-products"].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = gcb["Cement Carbonation Sink"].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.41678824533062)
    assert global_carbon_budget["budget imbalance"].loc[2024] == approx(
        -1.69186306041634
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1750
    ] == approx(0.00253982996724891)
    assert historical_budget["budget imbalance"].loc[2024] == approx(-1.69186306041634)

    assert fossil_emissions_by_category["fossil.emissions.excluding.carbonation"].loc[
        1850
    ] == approx(0.0537247802539048)
    assert fossil_emissions_by_category["Per.Capita"].loc[2024] == approx(
        1.29068632776699
    )

    assert luc_emissions_gcb.Net.loc[1959] == approx(2.37248)
    assert luc_emisssions_individual_models["Model Spread (sd)"].loc[2024] == approx(
        0.543991273730604
    )

    assert atmospheric_growth.GCB.loc[1959] == approx(2.03904)
    assert atmospheric_growth_individual_inversions["THU"].loc[2024] == approx(
        7.22531823174002
    )

    assert ocean_sink_gcb.GCB.loc[1959] == approx(1.11508070269876)
    assert ocean_sink_data_based_products["sd fCO2-product"].loc[2024] == approx(
        0.542323029491313
    )

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.453344829624502)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2024] == approx(
        1.10504513145914
    )
    assert terrestrial_sink_individual_models["Model Spread (sd)"].iloc[-1] == approx(
        1.10504513145914
    )

    assert cement_carbonation_sink.GCB.loc[1959] == approx(0.013422795)
    assert cement_carbonation_sink.GCB.loc[2024] == approx(0.224290503)
    assert pd.isna(cement_carbonation_sink.Huang[2024])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2024():
    year = "2024"
    gcb = Global_Carbon_Budget[year].Global_Budget
    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()
    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()

    luc_emissions_blue = gcb["Land-Use Change Emissions"]["BLUE"].to_dataframe()

    luc_emissions_luce = gcb["Land-Use Change Emissions"]["LUCE"].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    assert list(luc_emissions_luce.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models (NET) - Does not include peat emissions"
    ].to_dataframe()

    assert "CLM6.0" in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = gcb["Cement Carbonation Sink"].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.41667280224566)
    assert global_carbon_budget["budget imbalance"].loc[2023] == approx(
        -0.01914941811923
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1750
    ] == approx(0.00253982996724891)
    assert historical_budget["budget imbalance"].loc[2023] == approx(
        -0.0191494181192304
    )

    assert fossil_emissions_by_category["fossil.emissions.excluding.carbonation"].loc[
        1850
    ] == approx(53.7247802539048)
    assert fossil_emissions_by_category["Per.Capita"].loc[2023] == approx(
        1.2820252936662
    )

    assert luc_emissions_gcb.Net.loc[1959] == approx(2.1134525)
    assert luc_emisssions_individual_models["Model Spread (sd)"].loc[2023] == approx(
        0.734649181145946
    )

    assert ocean_sink_gcb.GCB.loc[1959] == approx(1.00844107356389)
    assert ocean_sink_data_based_products["sd fCO2-products (excl. UExP-FFN-U)"].loc[
        2023
    ] == approx(0.5477927075966)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.368378445686921)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2023] == approx(
        1.01471911105563
    )

    assert cement_carbonation_sink.GCB.loc[1959] == approx(12.542147)
    assert cement_carbonation_sink.GCB.loc[2023] == approx(214.049113)
    assert pd.isna(cement_carbonation_sink.Huang[2023])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2023():
    year = "2023"
    gcb = Global_Carbon_Budget[year].Global_Budget

    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()
    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()

    luc_emissions_blue = gcb["Land-Use Change Emissions"]["BLUE"].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models (NET) - Does not include peat emissions"
    ].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPX-Bern" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = gcb["Cement Carbonation Sink"].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.41666545551985)
    assert global_carbon_budget["budget imbalance"].loc[2022] == approx(
        -0.0921741721108096
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1750
    ] == approx(0.00253982996724891)
    assert historical_budget["budget imbalance"].loc[2022] == approx(
        -0.0921741721108091
    )

    assert fossil_emissions_by_category["fossil.emissions.excluding.carbonation"].loc[
        1850
    ] == approx(53.6986807874229)
    assert fossil_emissions_by_category["Per.Capita"].loc[2022] == approx(
        1.27134792448779
    )

    assert luc_emissions_gcb.Net.loc[1959] == approx(2.12152666666667)
    assert luc_emisssions_individual_models["Model Spread (sd)"].loc[2022] == approx(
        0.607291045665856
    )

    assert ocean_sink_gcb.GCB.loc[1959] == approx(0.992419800030039)
    assert ocean_sink_data_based_products["sd data-products (excl. Watson.)"].loc[
        2022
    ] == approx(0.31727790009081)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.430358951653902)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2022] == approx(
        0.829692166272794
    )

    assert cement_carbonation_sink.GCB.loc[1959] == approx(12.542147)
    assert cement_carbonation_sink.GCB.loc[2022] == approx(217.464615)
    assert pd.isna(cement_carbonation_sink.Huang[2022])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2022():
    year = "2022"
    gcb = Global_Carbon_Budget[year].Global_Budget

    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()
    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()

    luc_emissions_blue = gcb["Land-Use Change Emissions"]["BLUE"].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "Gross Sink",
        "Gross Source",
    ]

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models"
    ].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = gcb["Cement Carbonation Sink"].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.41709093103705)
    assert global_carbon_budget["budget imbalance"].loc[2021] == approx(
        -0.57757145051883
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1750
    ] == approx(0.002552)
    assert historical_budget["budget imbalance"].loc[2021] == approx(-0.57757145051883)

    assert fossil_emissions_by_category["fossil.emissions.excluding.carbonation"].loc[
        1850
    ] == approx(53.738)
    assert fossil_emissions_by_category["Per.Capita"].loc[2021] == approx(
        1.28103137304945
    )

    assert luc_emissions_gcb.Net.loc[1959] == approx(1.93893333333333)
    assert luc_emisssions_individual_models["Model Spread (sd)"].loc[2021] == approx(
        0.488150134956261
    )

    assert ocean_sink_gcb.GCB.loc[1959] == approx(0.975005218749614)
    assert ocean_sink_data_based_products["sd data-products (excl. Watson.)"].loc[
        2021
    ] == approx(0.24795776316279)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.401805228689998)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2021] == approx(
        0.888433352902292
    )

    assert cement_carbonation_sink.GCB.loc[1959] == approx(12.684256)
    assert cement_carbonation_sink.GCB.loc[2021] == approx(229.794956)
    assert pd.isna(cement_carbonation_sink.Guo[2021])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2021():
    year = "2021"
    gcb = Global_Carbon_Budget[year].Global_Budget

    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()
    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()

    luc_emissions_blue = gcb["Land-Use Change Emissions"]["BLUE"].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "Gross Sink",
        "Gross Source",
    ]

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models"
    ].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = gcb["Cement Carbonation Sink"].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.41713282396274)
    assert global_carbon_budget["budget imbalance"].loc[2020] == approx(
        -0.775025676533141
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1750
    ] == approx(0.002552)
    assert historical_budget["budget imbalance"].loc[2020] == approx(-0.775025676531002)

    assert fossil_emissions_by_category["fossil.emissions.excluding.carbonation"].loc[
        1959
    ] == approx(2417.13282396274)
    assert fossil_emissions_by_category["Per.Capita"].loc[2020] == approx(
        1.21875600594367
    )

    assert luc_emissions_gcb.Net.loc[1959] == approx(1.84551880806033)
    assert luc_emisssions_individual_models["Model Spread (sd)"].loc[2020] == approx(
        0.730856668977054
    )

    assert ocean_sink_gcb.GCB.loc[1959] == approx(0.918022208427885)
    assert ocean_sink_data_based_products["sd data-products (excl. Watson.)"].loc[
        2020
    ] == approx(0.33545744617825)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.395882352941176)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2020] == approx(
        0.989381862876127
    )

    assert cement_carbonation_sink.GCB.loc[1959] == approx(12.68373)
    assert cement_carbonation_sink.GCB.loc[2020] == approx(218.796424)
    assert pd.isna(cement_carbonation_sink.Guo[2020])


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2020():
    year = "2020"
    gcb = Global_Carbon_Budget[year].Global_Budget

    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()

    assert global_carbon_budget.loc[1959][
        "fossil emissions excluding carbonation"
    ] == approx(2.415)

    # Excel sheets contains proxy-based projections for 2020, we don't include them in the data
    assert global_carbon_budget.index[-1] == 2019

    historical_budget = gcb["Historical Budget"].to_dataframe()
    # Excel sheets contains proxy-based projections for 2020, we don't include them in the data
    assert historical_budget.index[-1] == 2019

    fossil_emissions_by_category = gcb["Fossil Emissions by Category"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()
    luc_emissions_bookkeeping = gcb["Land-Use Change Emissions"][
        "Bookkeeping Models"
    ].to_dataframe()
    assert "BLUE" in luc_emissions_bookkeeping.columns
    assert "H&N" in luc_emissions_bookkeeping.columns

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models"
    ].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()

    assert global_carbon_budget["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2.415)
    assert global_carbon_budget["budget imbalance"].loc[2019] == approx(
        0.3434082821477872
    )

    assert historical_budget["fossil emissions excluding carbonation"].loc[
        1751
    ] == approx(0.002552)
    assert historical_budget["budget imbalance"].loc[2019] == approx(
        0.34317149434110444
    )

    assert fossil_emissions_by_category["fossil emissions excluding carbonation"].loc[
        1959
    ] == approx(2415.0)
    assert fossil_emissions_by_category["Per Capita"].loc[2019] == approx(
        1.28938398227429
    )

    assert luc_emissions_gcb.GCB.loc[1959] == approx(1.8041998730239868)
    assert luc_emisssions_individual_models["MMM (multi-model mean)"].loc[
        2019
    ] == approx(2.1597810111764706)

    assert ocean_sink_gcb.GCB.loc[1959] == approx(0.8613677600284719)
    assert ocean_sink_data_based_products["mean data-products (excl. Watson.)"].loc[
        2019
    ] == approx(2.764190868690535)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.6774448472352941)
    assert terrestrial_sink_individual_models["Model Spread (sd)"].loc[2019] == approx(
        1.231594161674994
    )


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
@pytest.mark.filterwarnings(
    "ignore:Unknown extension is not supported and will be removed"
)
def test_gcb_2019():
    year = "2019"
    gcb = Global_Carbon_Budget[year].Global_Budget

    global_carbon_budget = gcb["Global Carbon Budget"].to_dataframe()

    assert global_carbon_budget.loc[1959]["fossil fuel and industry"] == approx(
        2.41724007382511
    )

    historical_budget = gcb["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = gcb["Fossil Emissions by Fuel Type"].to_dataframe()
    luc_emissions_gcb = gcb["Land-Use Change Emissions"]["GCB"].to_dataframe()
    luc_emissions_bookkeeping = gcb["Land-Use Change Emissions"][
        "Bookkeeping Models"
    ].to_dataframe()
    assert "BLUE" in luc_emissions_bookkeeping.columns
    assert "H&N" in luc_emissions_bookkeeping.columns

    luc_emisssions_individual_models = gcb["Land-Use Change Emissions"][
        "Individual models"
    ].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = gcb["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = gcb["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = gcb["Terrestrial Sink"]["GCB"].to_dataframe()
    terrestrial_sink_individual_models = gcb["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()

    assert global_carbon_budget["fossil fuel and industry"].loc[1959] == approx(
        2.41724007382511
    )
    assert global_carbon_budget["budget imbalance"].loc[2018] == approx(
        0.253417818912503
    )

    assert historical_budget["fossil fuel and industry"].loc[1751] == approx(0.003)
    assert historical_budget["budget imbalance"].loc[2018] == approx(0.238817818912503)

    assert fossil_emissions_by_category.Total.loc[1959] == approx(2417.24007382511)
    assert fossil_emissions_by_category["Per Capita"].loc[2018] == approx(
        1.30802356331913
    )

    assert luc_emissions_gcb.GCB.loc[1959] == approx(1.81036466770172)
    assert luc_emisssions_individual_models["MMM (multi-model mean)"].loc[
        2018
    ] == approx(2.32947129546408)

    assert ocean_sink_gcb.GCB.loc[1959] == approx(0.756759356352744)
    assert ocean_sink_data_based_products["MPM (multi-product mean)"].loc[
        2018
    ] == approx(2.668920)

    assert terrestrial_sink_gcb.GCB.loc[1959] == approx(0.528027347983859)
    assert terrestrial_sink_individual_models["MMM (multi-model mean)"].loc[
        2018
    ] == approx(3.46882836308954)
