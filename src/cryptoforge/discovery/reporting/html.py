"""
=========================================================
CryptoForge HTML Reporter
=========================================================
"""

from __future__ import annotations

from pathlib import Path

from cryptoforge.discovery.reporting.base import BaseReporter


class HtmlReporter(BaseReporter):

    REPORT_NAME = "Dataset_Report.html"

    def generate(self) -> Path:

        output = self.output_directory / self.REPORT_NAME

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>CryptoForge Discovery Report</title>
<style>

body {{
    font-family: Arial;
    margin:40px;
}}

table {{
    border-collapse:collapse;
    width:100%;
}}

td,th {{
    border:1px solid #cccccc;
    padding:8px;
}}

th {{
    background:#f2f2f2;
}}

</style>
</head>

<body>

<h1>CryptoForge Discovery Report</h1>

<pre>{self.result}</pre>

</body>
</html>
"""

        output.write_text(
            html,
            encoding="utf-8",
        )

        return output