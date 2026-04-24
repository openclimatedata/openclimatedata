import os

import pandas as pd
import pytest
from pytest import approx

from openclimatedata import Global_Carbon_Budget

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


versions = Global_Carbon_Budget.keys()


def test_gcb():
    for version in versions:
        assert Global_Carbon_Budget[version].__repr__()
        assert Global_Carbon_Budget[version].name
        assert Global_Carbon_Budget[version].doi
        assert Global_Carbon_Budget[version].published


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_sheet_names():
    for version in versions:
        sheet_names = Global_Carbon_Budget[version].keys()

        assert "Global Carbon Budget" in sheet_names
        assert "Historical Budget" in sheet_names
        if version > "2019":
            assert "Fossil Emissions by Category" in sheet_names
            assert "Cement Carbonation Sink" in sheet_names
        else:
            assert "Fossil Emissions by Fuel Type" in sheet_names
        assert "Land-Use Change Emissions" in sheet_names
        assert "Ocean Sink" in sheet_names
        assert "Terrestrial Sink" in sheet_names


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_dataframes_for_subtables_only():
    # In sheets with subtables, `to_dataframe` etc. should only be available
    # for tables, not on the main sheet.
    for version in versions:
        sheet_names = Global_Carbon_Budget[version].keys()

        for sheet_name in sheet_names:
            if len(Global_Carbon_Budget[version][sheet_name].keys()) > 0:
                assert "to_dataframe" not in dir(
                    Global_Carbon_Budget[version][sheet_name]
                )
                assert "to_long_dataframe" not in dir(
                    Global_Carbon_Budget[version][sheet_name]
                )


@pytest.mark.skipif(GITHUB_ACTIONS, reason="Test requires downloading.")
def test_gcb_2024():
    year = "2024"
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()
    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Category"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()

    luc_emissions_blue = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "BLUE"
    ].to_dataframe()

    luc_emissions_luce = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "LUCE"
    ].to_dataframe()

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

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models (NET) - Does not include peat emissions"].to_dataframe()

    assert "CLM6.0" in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = Global_Carbon_Budget[year][
        "Cement Carbonation Sink"
    ].to_dataframe()

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
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()
    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Category"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()

    luc_emissions_blue = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "BLUE"
    ].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "deforestation (total)",
        "forest regrowth (total)",
        "other transitions",
        "wood harvest & other forest management",
    ]

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models (NET) - Does not include peat emissions"].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPX-Bern" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = Global_Carbon_Budget[year][
        "Cement Carbonation Sink"
    ].to_dataframe()

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
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()
    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Category"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()

    luc_emissions_blue = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "BLUE"
    ].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "Gross Sink",
        "Gross Source",
    ]

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models"].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = Global_Carbon_Budget[year][
        "Cement Carbonation Sink"
    ].to_dataframe()

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
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()
    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Category"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()

    luc_emissions_blue = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "BLUE"
    ].to_dataframe()

    assert list(luc_emissions_blue.columns) == [
        "Net",
        "Gross Sink",
        "Gross Source",
    ]

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models"].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "Individual models"
    ].to_dataframe()
    cement_carbonation_sink = Global_Carbon_Budget[year][
        "Cement Carbonation Sink"
    ].to_dataframe()

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
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()

    assert global_carbon_budget.loc[1959][
        "fossil emissions excluding carbonation"
    ] == approx(2.415)

    # Excel sheets contains proxy-based projections for 2020, we don't include them in the data
    assert global_carbon_budget.index[-1] == 2019

    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    # Excel sheets contains proxy-based projections for 2020, we don't include them in the data
    assert historical_budget.index[-1] == 2019

    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Category"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()
    luc_emissions_bookkeeping = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "Bookkeeping Models"
    ].to_dataframe()
    assert "BLUE" in luc_emissions_bookkeeping.columns
    assert "H&N" in luc_emissions_bookkeeping.columns

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models"].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
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
def test_gcb_2019():
    year = "2019"
    global_carbon_budget = Global_Carbon_Budget[year][
        "Global Carbon Budget"
    ].to_dataframe()

    assert global_carbon_budget.loc[1959]["fossil fuel and industry"] == approx(
        2.41724007382511
    )

    historical_budget = Global_Carbon_Budget[year]["Historical Budget"].to_dataframe()
    fossil_emissions_by_category = Global_Carbon_Budget[year][
        "Fossil Emissions by Fuel Type"
    ].to_dataframe()
    luc_emissions_gcb = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "GCB"
    ].to_dataframe()
    luc_emissions_bookkeeping = Global_Carbon_Budget[year]["Land-Use Change Emissions"][
        "Bookkeeping Models"
    ].to_dataframe()
    assert "BLUE" in luc_emissions_bookkeeping.columns
    assert "H&N" in luc_emissions_bookkeeping.columns

    luc_emisssions_individual_models = Global_Carbon_Budget[year][
        "Land-Use Change Emissions"
    ]["Individual models"].to_dataframe()

    assert "CLM5.0" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS" in luc_emisssions_individual_models.columns
    assert "LPJ-GUESS " not in luc_emisssions_individual_models.columns

    ocean_sink_gcb = Global_Carbon_Budget[year]["Ocean Sink"]["GCB"].to_dataframe()
    ocean_sink_data_based_products = Global_Carbon_Budget[year]["Ocean Sink"][
        "Data-based products"
    ].to_dataframe()
    terrestrial_sink_gcb = Global_Carbon_Budget[year]["Terrestrial Sink"][
        "GCB"
    ].to_dataframe()
    terrestrial_sink_individual_models = Global_Carbon_Budget[year]["Terrestrial Sink"][
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
