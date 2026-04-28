"""
Merge presentations at the OOXML (ZIP) level - v2.
Fixes: namespace consistency, notesSlide conflicts for example slides.
"""
import os
import re
import shutil
import zipfile
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent.parent.parent
    orig_path = base / ".tmp" / "ai-collaborative-dev-platform.pptx"
    ex_path = base / ".tmp" / "example-slides" / "examples.pptx"
    out_path = base / ".tmp" / "ai-collaborative-dev-platform-v2.pptx"

    # Insert example slides after these original slide numbers (1-based)
    insert_after = [3, 5, 6, 8, 11]

    work_dir = base / ".tmp" / "merge_work2"
    orig_dir = work_dir / "original"
    ex_dir = work_dir / "examples"
    out_dir = work_dir / "output"

    if work_dir.exists():
        shutil.rmtree(work_dir)

    # Extract both
    with zipfile.ZipFile(orig_path) as zf:
        zf.extractall(orig_dir)
    with zipfile.ZipFile(ex_path) as zf:
        zf.extractall(ex_dir)

    # Copy original as base
    shutil.copytree(orig_dir, out_dir)

    # Build new slide ordering
    orig_count = len([f for f in (orig_dir / "ppt/slides").iterdir()
                      if f.name.startswith("slide") and f.suffix == ".xml"])
    new_order = []  # (source, orig_slide_num_or_ex_idx)
    ex_idx = 0
    for i in range(1, orig_count + 1):
        new_order.append(("orig", i))
        if ex_idx < len(insert_after) and i == insert_after[ex_idx]:
            new_order.append(("ex", ex_idx + 1))
            ex_idx += 1

    total = len(new_order)
    print(f"Original: {orig_count}, Total: {total}")

    # Copy example media files with unique names
    ex_media = ex_dir / "ppt" / "media"
    out_media = out_dir / "ppt" / "media"
    out_media.mkdir(exist_ok=True)
    media_map = {}
    if ex_media.exists():
        existing = set(f.name for f in out_media.iterdir())
        for mf in ex_media.iterdir():
            new_name = mf.name
            if new_name in existing:
                stem, suf = mf.stem, mf.suffix
                c = 1
                while new_name in existing:
                    new_name = f"{stem}_ex{c}{suf}"
                    c += 1
            media_map[mf.name] = new_name
            shutil.copy2(mf, out_media / new_name)
            existing.add(new_name)

    # Clear existing slides and rels
    slides_dir = out_dir / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"
    for f in slides_dir.glob("slide*.xml"):
        f.unlink()
    for f in rels_dir.glob("slide*.xml.rels"):
        f.unlink()

    # Copy slides with new numbering
    for new_num, (source, idx) in enumerate(new_order, 1):
        if source == "orig":
            src_slide = orig_dir / "ppt" / "slides" / f"slide{idx}.xml"
            src_rels = orig_dir / "ppt" / "slides" / "_rels" / f"slide{idx}.xml.rels"
        else:
            src_slide = ex_dir / "ppt" / "slides" / f"slide{idx}.xml"
            src_rels = ex_dir / "ppt" / "slides" / "_rels" / f"slide{idx}.xml.rels"

        dst_slide = slides_dir / f"slide{new_num}.xml"
        dst_rels = rels_dir / f"slide{new_num}.xml.rels"

        shutil.copy2(src_slide, dst_slide)

        if src_rels.exists():
            content = src_rels.read_text(encoding='utf-8')

            if source == "ex":
                # Update media references
                for old_name, new_name in media_map.items():
                    content = content.replace(f"../media/{old_name}", f"../media/{new_name}")
                # Remove notesSlide references (they conflict with original notes)
                content = re.sub(
                    r'<[^>]*Relationship[^>]*notesSlide[^>]*/>', '', content
                )

            dst_rels.write_text(content, encoding='utf-8')

    # Update presentation.xml - rebuild sldIdLst
    pres_path = out_dir / "ppt" / "presentation.xml"
    pres_content = pres_path.read_text(encoding='utf-8')

    # Find max rId in presentation.xml.rels
    pres_rels_path = out_dir / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels = pres_rels_path.read_text(encoding='utf-8')

    max_rid = max(int(m.group(1)) for m in re.finditer(r'rId(\d+)', pres_rels))

    # Remove existing slide relationships
    pres_rels = re.sub(
        r'<Relationship\s[^>]*Target="slides/slide\d+\.xml"[^>]*/>', '', pres_rels
    )

    # Add new slide relationships before </Relationships>
    new_rels = ""
    for i in range(1, total + 1):
        rid = max_rid + i
        new_rels += (
            f'<Relationship Id="rId{rid}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
            f'Target="slides/slide{i}.xml" />'
        )

    # Ensure consistent namespace - use the original format
    pres_rels = pres_rels.replace('</Relationships>', new_rels + '</Relationships>')
    # Normalize: if original uses bare Relationships (no prefix), keep it
    # If it uses rel: prefix, keep that
    pres_rels_path.write_text(pres_rels, encoding='utf-8')

    # Update sldIdLst in presentation.xml
    # Find max sldId
    sld_ids = [int(m.group(1)) for m in re.finditer(r'<p:sldId id="(\d+)"', pres_content)]
    max_sld_id = max(sld_ids) if sld_ids else 256

    # Remove existing sldId entries
    pres_content = re.sub(r'<p:sldId\s[^>]*/>', '', pres_content)

    # Build new sldId entries
    new_sld_ids = ""
    for i in range(1, total + 1):
        rid = max_rid + i
        sid = max_sld_id + i
        new_sld_ids += f'<p:sldId id="{sid}" r:id="rId{rid}" />'

    # Insert into sldIdLst
    pres_content = pres_content.replace(
        '<p:sldIdLst>', f'<p:sldIdLst>{new_sld_ids}'
    )
    # Also handle empty sldIdLst
    pres_content = re.sub(
        r'<p:sldIdLst\s*/>', f'<p:sldIdLst>{new_sld_ids}</p:sldIdLst>',
        pres_content
    )
    pres_path.write_text(pres_content, encoding='utf-8')

    # Update [Content_Types].xml
    ct_path = out_dir / "[Content_Types].xml"
    ct_content = ct_path.read_text(encoding='utf-8')

    # Remove existing slide overrides (handle both /> and / > patterns)
    ct_content = re.sub(
        r'<Override\s+PartName="/ppt/slides/slide\d+\.xml"[^>]*/>', '', ct_content
    )

    # Add new slide overrides
    slide_ct = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
    new_overrides = ""
    for i in range(1, total + 1):
        new_overrides += f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="{slide_ct}" />'

    ct_content = ct_content.replace('</Types>', new_overrides + '</Types>')
    ct_path.write_text(ct_content, encoding='utf-8')

    # Create output PPTX
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_path, dirs, files in os.walk(out_dir):
            for file in files:
                fp = Path(root_path) / file
                arcname = fp.relative_to(out_dir).as_posix()
                zf.write(fp, arcname)

    print(f"Saved: {out_path}")
    shutil.rmtree(work_dir)
    print("Done!")


if __name__ == "__main__":
    main()
