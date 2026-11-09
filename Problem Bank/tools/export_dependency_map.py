"""Project an audited offline dependency atlas into the public course asset."""

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path


EMBEDDED_DATA = re.compile(
    r'(<script type="application/json" id="([^"]+)">)(.*?)(</script>)', re.DOTALL
)
PRIVATE_FIELDS = {"provenance", "library_file_id", "local_path", "source_path"}
PRIVATE_MARKERS = re.compile(
    r"libfile_[a-zA-Z0-9]+|/workspace/|chat_files/|file://|chatgpt\.com/library"
)
TRANSIENT_REF = re.compile(r"\bturn\d+(?:view|search|find)\d+\b")
TRANSIENT_FIELDS = {
    "web_ref", "session3_web_ref", "session4_web_ref", "session3_root_verification_refs",
}
EDITORIAL_LABELS = {
    "regression_route_review.json": "the regression method review",
    "joint_probability_review.json": "the joint-probability review",
    "locator_corrections.json": "the source locator corrections",
    "curriculum_status_reviews.json": "Curriculum status review",
    "working/review_flags.json": "Editorial review notes",
    "campaign09_summary_route_patch.json": "the probability-summary route review",
}
HISTORICAL_LINK_LABEL = "Open current Fall 2026 replacement PDF ↗"
SCRIPT = re.compile(r"<script>(.*?)</script>", re.DOTALL)


def public_data(value):
    if isinstance(value, list):
        return [public_data(item) for item in value]
    if isinstance(value, dict):
        result = {
            key: public_data(item)
            for key, item in value.items()
            if key not in PRIVATE_FIELDS and key not in TRANSIENT_FIELDS
            and "probe" not in key and "sha256" not in key
        }
        if result.get("id") == "cb-ced-2020":
            result["link_label"] = HISTORICAL_LINK_LABEL
        return result
    if isinstance(value, str):
        for filename, label in EDITORIAL_LABELS.items():
            value = value.replace(filename, label)
        return re.sub(r"\s*" + TRANSIENT_REF.pattern, "", value)
    return value


def update_script_and_policy(output):
    scripts = list(SCRIPT.finditer(output))
    if len(scripts) != 1:
        raise ValueError("Expected one executable script")
    match = scripts[0]
    script = match[1]
    old_label = "Open public source ↗"
    if script.count(old_label) != 2:
        raise ValueError("Expected a source link in the evidence and references panels")
    script = script.replace(
        old_label,
        "${esc((url===safeURL(r?.url)&&r?.link_label)||'Open public source ↗')}",
        1,
    )
    reference_link = ">Open public source ↗</a>"
    if script.count(reference_link) != 1:
        raise ValueError("Expected one reference-list source link")
    script = script.replace(reference_link, ">${esc(r.link_label||'Open public source ↗')}</a>")
    script = script.replace(
        "Historical edition cited; this mutable URL can now serve Fall 2026. Verify the edition.",
        "Historical edition cited. The linked PDF is the current Fall 2026 replacement. "
        "An immutable Fall 2020 PDF was not verified.",
    )
    heading_end = "</span></div></div>`;" + "renderGraph();renderRelations();renderEvidence()}"
    if script.count(heading_end) != 1:
        raise ValueError("Expected one skill selection heading")
    practice_link = (
        "${n.node_type==='ap_skill'&&!n.origin?`"
        '<p><a href="expanded-bank.html?skill=${encodeURIComponent(n.id)}">'
        "Find practice for this skill</a></p>`:''}"
    )
    script = script.replace(heading_end, "</span></div>" + practice_link + "</div>`;"
                            "renderGraph();renderRelations();renderEvidence()}")
    digest = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
    output = output[:match.start(1)] + script + output[match.end(1):]
    old_policy = "script-src 'unsafe-inline';"
    if output.count(old_policy) != 1:
        raise ValueError("Expected one inline-script policy to replace")
    return output.replace(old_policy, f"script-src 'sha256-{digest}'; connect-src 'none';")


def project(source):
    graph_found = False

    def replace_data(match):
        nonlocal graph_found
        opening, script_id, content, closing = match.groups()
        data = public_data(json.loads(content))
        if script_id == "graph-data":
            graph_found = bool(data["nodes"] and data["edges"])
            # Added AP concepts carry an origin marker. Practice files use the original IDs.
            original_ids = {
                node["id"] for node in data["nodes"]
                if node.get("node_type") == "ap_skill" and not node.get("origin")
            }
            if len(original_ids) != 200:
                raise ValueError("Expected 200 original practice skill IDs")
        encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return opening + encoded.replace("</", "<\\/") + closing

    output = EMBEDDED_DATA.sub(replace_data, source)
    if not graph_found or PRIVATE_MARKERS.search(output) or TRANSIENT_REF.search(output):
        raise ValueError("Expected an atlas with a complete graph and public source links")

    output = output.replace("PRIVATE · WORKS OFFLINE", "EDITORIAL · WORKS OFFLINE")
    output = output.replace(
        "AP Statistics · Private dependency atlas",
        '<a href="../practice.html">Return to the Problem Bank</a>',
    )
    output = output.replace("are embedded without modification", "are included in this course copy")
    output = output.replace(
        "No diagnostic questions are shown in this interface. Canonical embedded graph metadata is preserved for exact-data audit.",
        "The course copy includes editorial learning links, public evidence, and original synthetic method comparisons.",
    )
    return update_script_and_policy(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Audited standalone atlas from the private project")
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "dependency-map.html",
    )
    args = parser.parse_args()
    args.output.write_text(project(args.source.read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
