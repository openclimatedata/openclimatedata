# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "openclimatedata",
# ]
#
# [tool.uv.sources]
# openclimatedata = { path = "../", editable = true}
# ///

from pathlib import Path

import openclimatedata as ocd

root = Path(__file__).parents[1]

html = """<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>Openclimatedata - Downloads</title>
</head>
<body>
<ul>
<h1>Openclimatedata Downloads</h1>
<p><a href="https://github.com/openclimatedata/openclimatedata">GitHub Repo</a></p>
"""

gcb_versions = ocd.GCB_Fossil_Emissions.keys()

html += """<h2>GCB Fossil</h2>"""

for gcb_version in gcb_versions:
    df = ocd.GCB_Fossil_Emissions[gcb_version].to_ocd()
    filename = f"gcb-fossil-{gcb_version}.parquet"
    df.to_parquet(root / "scripts" / filename)
    html += f'<li><a href="{filename}">{filename}</a></li>\n'

html += """</ul>
</body>
</html>
"""

with open(root / "scripts/index.html", "w") as f:
    f.write(html)
