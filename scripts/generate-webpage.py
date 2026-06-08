# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "openclimatedata==0.40.1",
#     "pyarrow>=23.0.1",
# ]
# ///

from pathlib import Path

import openclimatedata as ocd
import pandas as pd

from tqdm import tqdm

root = Path(__file__).parents[1]

html = f"""<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<meta name="robots" content="noindex">
<title>Openclimatedata - Downloads</title>
</head>
<body>
<h1>Openclimatedata Downloads - Version {ocd.__version__}</h1>
<p><a href="https://github.com/openclimatedata/openclimatedata">GitHub Repo</a></p>
"""

global_carbon_budget_versions = ocd.Global_Carbon_Budget.keys()

html += """<h2>Global Carbon Budget</h2>"""


print("Global Carbon Budget")
for gcb_version in tqdm(global_carbon_budget_versions):
    html += """<ul>\n"""
    for sheet in ocd.Global_Carbon_Budget[gcb_version].Global_Budget.keys():
        sheetslug = sheet.lower().replace(" ", "-")
        if sheet not in [
            "Atmospheric Growth",
            "Land-Use Change Emissions",
            "Ocean Sink",
            "Terrestrial Sink",
        ]:
            filename = f"global-carbon-budget-{gcb_version}-{sheetslug}.parquet"
            filepath = Path(root / "scripts" / filename)

            html += f"""<li><a href="{filename}">{filename}</a> ({ocd.Global_Carbon_Budget[gcb_version].license})</li>\n"""
            if not filepath.exists():
                df = ocd.Global_Carbon_Budget[gcb_version].Global_Budget[sheet].to_ocd()
                df.to_parquet(filepath, index=False)

        else:
            filename = f"global-carbon-budget-{gcb_version}-{sheetslug}.parquet"
            filepath = Path(root / "scripts" / filename)
            html += f"""<li><a href="{filename}">{filename}</a> ({ocd.Global_Carbon_Budget[gcb_version].license})</li>\n"""
            if not filepath.exists():
                dfs = []
                for subtable in (
                    ocd.Global_Carbon_Budget[gcb_version].Global_Budget[sheet].keys()
                ):
                    df = (
                        ocd.Global_Carbon_Budget[gcb_version]
                        .Global_Budget[sheet][subtable]
                        .to_ocd()
                    )
                    df.insert(1, "subtable", subtable)
                    dfs.append(df)
                pd.concat(dfs).to_parquet(filepath, index=False)

    for sheet in ocd.Global_Carbon_Budget[gcb_version].National_Fossil_Emissions.keys():
        sheetslug = sheet.lower().replace(" ", "-")
        filename = f"global-carbon-budget-{gcb_version}-{sheetslug}.parquet"
        filepath = Path(root / "scripts" / filename)

        html += f"""<li><a href="{filename}">{filename}</a> ({ocd.Global_Carbon_Budget[gcb_version].license})</li>\n"""
        if not filepath.exists():
            df = (
                ocd.Global_Carbon_Budget[gcb_version]
                .National_Fossil_Emissions[sheet]
                .to_ocd()
            )
            df.to_parquet(filepath, index=False)

    if gcb_version >= "2022":
        for sheet in ocd.Global_Carbon_Budget[
            gcb_version
        ].National_Landuse_Change_Emissions.keys():
            sheetslug = sheet.lower().replace(" ", "-").replace("&", "")
            filename = f"global-carbon-budget-{gcb_version}-{sheetslug}.parquet"
            filepath = Path(root / "scripts" / filename)

            html += f"""<li><a href="{filename}">{filename}</a> ({ocd.Global_Carbon_Budget[gcb_version].license})</li>\n"""
            if not filepath.exists():
                df = (
                    ocd.Global_Carbon_Budget[gcb_version]
                    .National_Landuse_Change_Emissions[sheet]
                    .to_ocd()
                )
                df.to_parquet(filepath, index=False)

    html += f"""</ul><small>{ocd.Global_Carbon_Budget[gcb_version].citation}</small>"""


gcb_versions = ocd.GCB_Fossil_Emissions.keys()

html += """<h2>GCB Fossil</h2>
<ul>"""

print("GCB Fossil")
for gcb_version in tqdm(gcb_versions):
    filename = f"gcb-fossil-{gcb_version}.parquet"
    filepath = root / "scripts" / filename
    html += f"""<li><a href="{filename}">{filename}</a> ({ocd.GCB_Fossil_Emissions[gcb_version].license})</br>
    <small>{ocd.GCB_Fossil_Emissions[gcb_version].citation}</small>
    </li>\n"""
    if not filepath.exists():
        df = ocd.GCB_Fossil_Emissions[gcb_version].to_ocd()
        df.to_parquet(filepath)


primaphist_versions = ocd.PRIMAPHIST.keys()

html += """</ul>
<h2>PRIMAP-hist</h2>
<ul>"""

print("PRIMAP-hist")
for primaphist_version in tqdm(primaphist_versions):
    filename = f"primap-hist-{primaphist_version.replace('.', '-')}.parquet"
    filepath = Path(root / "scripts" / filename)
    html += f"""<li><a href="{filename}">{filename}</a> ({ocd.PRIMAPHIST[primaphist_version].license})</br></li>\n
    <small>{ocd.PRIMAPHIST[primaphist_version].citation}</small>
    """
    if not filepath.exists():
        df = ocd.PRIMAPHIST[primaphist_version]["main"].to_ocd()
        df.to_parquet(filepath)

ceds_versions = ocd.CEDS.keys()

html += """</ul>
<h2>CEDS</h2>
"""

print("CEDS")
for ceds_version in tqdm(ceds_versions):
    html += f"""<p><strong>{ceds_version}</strong></p>
    <ul>"""

    for entity in ocd.CEDS[ceds_version].entities:
        filename = (
            f"ceds-{entity.lower()}-by-sector-{ceds_version.replace('.', '-')}.parquet"
        )
        filepath = Path(root / "scripts" / filename)
        html += f"""<li><a href="{filename}">{filename}</a> ({ocd.CEDS[ceds_version].license})</br></li>\n
        """
        if not filepath.exists():
            df = ocd.CEDS[ceds_version][entity]["by_sector"].to_ocd()
            df.to_parquet(filepath, index=False)

        if "by_sector_fuel" in ocd.CEDS[ceds_version][entity]:
            filename = f"ceds-{entity.lower()}-by-sector-fuel-{ceds_version.replace('.', '-')}.parquet"
            filepath = Path(root / "scripts" / filename)
            html += f"""<li><a href="{filename}">{filename}</a> ({ocd.CEDS[ceds_version].license})</br></li>\n
            """
            if not filepath.exists():
                df = ocd.CEDS[ceds_version][entity]["by_sector_fuel"].to_ocd()
                df.to_parquet(filepath, index=False)

        if "bunkers" in ocd.CEDS[ceds_version][entity]:
            filename = f"ceds-{entity.lower()}-bunkers-{ceds_version.replace('.', '-')}.parquet"
            filepath = Path(root / "scripts" / filename)
            html += f"""<li><a href="{filename}">{filename}</a> ({ocd.CEDS[ceds_version].license})</br></li>\n
            """
            if not filepath.exists():
                df = ocd.CEDS[ceds_version][entity]["bunkers"].to_ocd()
                df.to_parquet(root / "scripts" / filename, index=False)

    html += f"""</ul><small>{ocd.CEDS[ceds_version].citation}</small>
    """


html += """
</body>
</html>
"""

with open(root / "scripts/index.html", "w") as f:
    f.write(html)
