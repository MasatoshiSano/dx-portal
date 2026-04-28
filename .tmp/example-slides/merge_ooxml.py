"""
Merge presentations at the OOXML (ZIP/XML) level.
Inserts example slides from examples.pptx into ai-collaborative-dev-platform.pptx.
"""
import copy
import os
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# Namespaces
NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}

for prefix, uri in NSMAP.items():
    ET.register_namespace(prefix, uri)

# Additional namespaces commonly found in PPTX
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('p14', 'http://schemas.microsoft.com/office/powerpoint/2010/main')
ET.register_namespace('p15', 'http://schemas.microsoft.com/office/powerpoint/2012/main')


def get_max_slide_num(zf):
    """Get the highest slide number in the archive."""
    max_num = 0
    for name in zf.namelist():
        m = re.match(r'ppt/slides/slide(\d+)\.xml', name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num


def get_max_rid(rels_xml):
    """Get the highest rId number from a .rels XML string."""
    root = ET.fromstring(rels_xml)
    max_rid = 0
    for rel in root:
        rid = rel.get('Id', '')
        m = re.match(r'rId(\d+)', rid)
        if m:
            max_rid = max(max_rid, int(m.group(1)))
    return max_rid


def main():
    base = Path(__file__).resolve().parent.parent.parent
    orig_path = base / ".tmp" / "ai-collaborative-dev-platform.pptx"
    ex_path = base / ".tmp" / "example-slides" / "examples.pptx"
    out_path = base / ".tmp" / "ai-collaborative-dev-platform-v2.pptx"

    # Insert example slides after these original slide numbers (1-based)
    # ex1 after slide 3, ex2 after slide 5, ex3 after slide 6, ex4 after slide 8, ex5 after slide 11
    insert_after = [3, 5, 6, 8, 11]

    # Work in a temp directory
    work_dir = base / ".tmp" / "merge_work"
    orig_dir = work_dir / "original"
    ex_dir = work_dir / "examples"

    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)

    # Extract both archives
    with zipfile.ZipFile(orig_path) as zf:
        zf.extractall(orig_dir)

    with zipfile.ZipFile(ex_path) as zf:
        zf.extractall(ex_dir)

    # Get original slide count
    orig_slides = sorted(
        [f for f in (orig_dir / "ppt" / "slides").iterdir() if f.name.startswith("slide") and f.suffix == ".xml"],
        key=lambda f: int(re.search(r'\d+', f.name).group())
    )
    orig_count = len(orig_slides)
    print(f"Original slides: {orig_count}")

    # Example slides
    ex_slides = sorted(
        [f for f in (ex_dir / "ppt" / "slides").iterdir() if f.name.startswith("slide") and f.suffix == ".xml"],
        key=lambda f: int(re.search(r'\d+', f.name).group())
    )
    print(f"Example slides: {len(ex_slides)}")

    # Build new slide ordering: original slides with examples inserted
    # Each item is (source_dir, slide_filename, rels_filename)
    new_order = []
    ex_idx = 0
    for orig_num in range(1, orig_count + 1):
        new_order.append(("original", f"slide{orig_num}.xml"))
        if ex_idx < len(insert_after) and orig_num == insert_after[ex_idx]:
            new_order.append(("example", f"slide{ex_idx + 1}.xml"))
            ex_idx += 1

    total = len(new_order)
    print(f"Total slides after merge: {total}")

    # Create output directory structure
    out_dir = work_dir / "output"
    shutil.copytree(orig_dir, out_dir)

    # Copy example slide media files
    ex_media = ex_dir / "ppt" / "media"
    out_media = out_dir / "ppt" / "media"
    out_media.mkdir(exist_ok=True)

    media_mapping = {}  # old_name -> new_name for example media
    if ex_media.exists():
        existing_media = set(f.name for f in out_media.iterdir()) if out_media.exists() else set()
        for media_file in ex_media.iterdir():
            new_name = media_file.name
            # Avoid conflicts
            if new_name in existing_media:
                stem = media_file.stem
                suffix = media_file.suffix
                counter = 1
                while new_name in existing_media:
                    new_name = f"{stem}_ex{counter}{suffix}"
                    counter += 1
            media_mapping[media_file.name] = new_name
            shutil.copy2(media_file, out_media / new_name)
            existing_media.add(new_name)

    # Remove old slides from output
    out_slides_dir = out_dir / "ppt" / "slides"
    out_rels_dir = out_slides_dir / "_rels"
    for f in out_slides_dir.glob("slide*.xml"):
        f.unlink()
    for f in out_rels_dir.glob("slide*.xml.rels"):
        f.unlink()

    # Copy slides in new order with new numbering
    for new_num, (source, filename) in enumerate(new_order, 1):
        if source == "original":
            src_dir = orig_dir
        else:
            src_dir = ex_dir

        src_slide = src_dir / "ppt" / "slides" / filename
        dst_slide = out_slides_dir / f"slide{new_num}.xml"
        shutil.copy2(src_slide, dst_slide)

        # Copy rels
        src_rels = src_dir / "ppt" / "slides" / "_rels" / f"{filename}.rels"
        dst_rels = out_rels_dir / f"slide{new_num}.xml.rels"
        if src_rels.exists():
            if source == "example" and media_mapping:
                # Update media references in rels
                rels_content = src_rels.read_text(encoding='utf-8')
                for old_name, new_name in media_mapping.items():
                    rels_content = rels_content.replace(f"../media/{old_name}", f"../media/{new_name}")
                dst_rels.write_text(rels_content, encoding='utf-8')
            else:
                shutil.copy2(src_rels, dst_rels)

            # For example slides, fix slideLayout reference to point to original layout
            if source == "example":
                rels_tree = ET.parse(dst_rels)
                rels_root = rels_tree.getroot()
                for rel in rels_root:
                    target = rel.get('Target', '')
                    if 'slideLayout' in target:
                        # Point to the first slide layout in original
                        rel.set('Target', '../slideLayouts/slideLayout1.xml')
                rels_tree.write(dst_rels, xml_declaration=True, encoding='UTF-8')

    # Update presentation.xml - slide list
    pres_xml = out_dir / "ppt" / "presentation.xml"
    pres_tree = ET.parse(pres_xml)
    pres_root = pres_tree.getroot()

    ns_p = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
    ns_r = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

    sld_id_lst = pres_root.find(f'{ns_p}sldIdLst')

    # Read existing presentation.xml.rels
    pres_rels_path = out_dir / "ppt" / "_rels" / "presentation.xml.rels"
    pres_rels_tree = ET.parse(pres_rels_path)
    pres_rels_root = pres_rels_tree.getroot()

    # Find max rId and sldId
    max_rid = 0
    for rel in pres_rels_root:
        m = re.match(r'rId(\d+)', rel.get('Id', ''))
        if m:
            max_rid = max(max_rid, int(m.group(1)))

    max_sld_id = 0
    for sld_id in sld_id_lst:
        sid = int(sld_id.get('id', '0'))
        max_sld_id = max(max_sld_id, sid)

    # Remove existing slide references from rels and sldIdLst
    to_remove_rels = []
    for rel in pres_rels_root:
        if 'slides/slide' in rel.get('Target', ''):
            to_remove_rels.append(rel)
    for r in to_remove_rels:
        pres_rels_root.remove(r)

    for child in list(sld_id_lst):
        sld_id_lst.remove(child)

    # Add new slide references
    ns_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'

    for i in range(1, total + 1):
        rid = f"rId{max_rid + i}"
        sid = max_sld_id + i

        # Add to presentation.xml.rels
        rel_elem = ET.SubElement(pres_rels_root, 'Relationship')
        rel_elem.set('Id', rid)
        rel_elem.set('Type', ns_rel_type)
        rel_elem.set('Target', f'slides/slide{i}.xml')

        # Add to sldIdLst
        sld_elem = ET.SubElement(sld_id_lst, f'{ns_p}sldId')
        sld_elem.set('id', str(sid))
        sld_elem.set(f'{ns_r}id', rid)

    # Save updated XML files
    pres_tree.write(pres_xml, xml_declaration=True, encoding='UTF-8')
    pres_rels_tree.write(pres_rels_path, xml_declaration=True, encoding='UTF-8')

    # Update [Content_Types].xml
    ct_path = out_dir / "[Content_Types].xml"
    ct_tree = ET.parse(ct_path)
    ct_root = ct_tree.getroot()
    ns_ct = '{http://schemas.openxmlformats.org/package/2006/content-types}'

    # Remove existing slide overrides
    to_remove = [elem for elem in ct_root if 'slides/slide' in elem.get('PartName', '')]
    for elem in to_remove:
        ct_root.remove(elem)

    # Add new slide overrides
    slide_ct = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
    for i in range(1, total + 1):
        override = ET.SubElement(ct_root, f'{ns_ct}Override')
        override.set('PartName', f'/ppt/slides/slide{i}.xml')
        override.set('ContentType', slide_ct)

    ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8')

    # Create output PPTX
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_path, dirs, files in os.walk(out_dir):
            for file in files:
                file_path = Path(root_path) / file
                arcname = file_path.relative_to(out_dir).as_posix()
                zf.write(file_path, arcname)

    print(f"Output saved to: {out_path}")

    # Cleanup
    shutil.rmtree(work_dir)
    print("Done!")


if __name__ == "__main__":
    main()
