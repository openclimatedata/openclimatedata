# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "openclimatedata",
#     "pyarrow>=23.0.1",
# ]
#
# [tool.uv.sources]
# openclimatedata = { path = "../", editable = true}
# ///

from pathlib import Path

import openclimatedata as ocd

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

gcb_versions = ocd.GCB_Fossil_Emissions.keys()

html += """<h2>GCB Fossil</h2>
<ul>"""

print("GCB Fossil")
for gcb_version in tqdm(gcb_versions):
    df = ocd.GCB_Fossil_Emissions[gcb_version].to_ocd()
    filename = f"gcb-fossil-{gcb_version}.parquet"
    df.to_parquet(root / "scripts" / filename)
    html += f"""<li><a href="{filename}">{filename}</a> ({ocd.GCB_Fossil_Emissions[gcb_version].license})</br>
    <small>{ocd.GCB_Fossil_Emissions[gcb_version].citation}</small>
    </li>\n"""

primaphist_versions = ocd.PRIMAPHIST.keys()

html += """</ul>
<h2>PRIMAP-hist</h2>
<ul>"""

print("PRIMAP-hist")
for primaphist_version in tqdm(primaphist_versions):
    df = ocd.PRIMAPHIST[primaphist_version]["main"].to_ocd()
    filename = f"primap-hist-{primaphist_version.replace('.', '-')}.parquet"
    df.to_parquet(root / "scripts" / filename)
    html += f"""<li><a href="{filename}">{filename}</a> ({ocd.PRIMAPHIST[primaphist_version].license})</br></li>\n
    <small>{ocd.PRIMAPHIST[primaphist_version].citation}</small>
    """

ceds_versions = ocd.CEDS.keys()

html += """</ul>
<h2>CEDS</h2>
"""

print("CEDS")
for ceds_version in tqdm(ceds_versions):
    html += f"""<p><strong>{ceds_version}</strong></p>
    <ul>"""
    for entity in ocd.CEDS[ceds_version].entities:
        df = ocd.CEDS[ceds_version][entity]["by_sector"].to_ocd()
        filename = (
            f"ceds-{entity.lower()}-by-sector-{ceds_version.replace('.', '-')}.parquet"
        )
        df.to_parquet(root / "scripts" / filename, index=False)
        html += f"""<li><a href="{filename}">{filename}</a> ({ocd.CEDS[ceds_version].license})</br></li>\n
        """
    html += f"""</ul><small>{ocd.CEDS[ceds_version].citation}</small>
    """


html += """
</body>
</html>
"""

with open(root / "scripts/index.html", "w") as f:
    f.write(html)
