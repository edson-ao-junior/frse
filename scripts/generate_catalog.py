#!/usr/bin/env python3
"""Validate metadata and render public research catalogs using the standard library."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name, collection, fields):
    payload = json.loads((ROOT / 'metadata' / name).read_text(encoding='utf-8'))
    if not isinstance(payload.get('as_of'), str):
        raise ValueError(f'{name}: missing as_of')
    items = payload.get(collection)
    if not isinstance(items, list):
        raise ValueError(f'{name}: missing list {collection}')
    seen = set()
    for item in items:
        if not isinstance(item, dict) or any(field not in item for field in fields):
            raise ValueError(f'{name}: invalid item {item!r}')
        if item['id'] in seen:
            raise ValueError(f'{name}: duplicate id {item["id"]}')
        seen.add(item['id'])
    return payload, items


def safe(value):
    if value is None or value == '':
        return 'Not available'
    return str(value).replace('|', r'\|').replace('\n',' ').strip()


def save(path, lines):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')


def main(check=False):
    sp, studies = read('studies.json', 'studies', ['id', 'title', 'wp', 'research_status', 'publication_status', 'artifact_status', 'url', 'detail'])
    pp, pubs = read('publications.json', 'publications', ['id', 'title', 'study', 'status', 'venue', 'type'])
    study_ids = {s['id'] for s in studies}
    for pub in pubs:
        if pub['study'] not in study_ids:
            raise ValueError(f'{pub["id"]}: unknown study reference {pub["study"]}')
    for study in studies:
        if not (ROOT / 'docs' / 'studies' / study['url'] / 'index.md').exists():
            raise ValueError(f'{study["id"]}: missing study page')
    if check:
        print(f'Metadata validated: {len(studies)} studies, {len(pubs)} publications')
        return

    lines = ['# Research Studies', '',
        'This catalog is maintained from `metadata/studies.json`. Research, publication, and public release statuses are tracked **independently**.', '',
        '| Study | Work package | Research status | Publication status |', '| --- | --- | --- | --- |']
    for s in studies:
        lines.append(f'| [{safe(s["id"])} · {safe(s["title"])}]({safe(s["url"])}) | {safe(s["wp"])} | {safe(s["research_status"])} | {safe(s["publication_status"])} |')
    lines += ['', '## Study summaries', '']
    for s in studies:
        lines.extend([f'### [{s["id"]}: {s["title"]}]({s["url"]})', '', safe(s['detail']), '', f'**Artifact release:** {safe(s["artifact_status"])}.', ''])
    lines += [f'*Metadata reviewed: {safe(sp["as_of"])}.*', '',
              'For proposed follow-up studies that are not yet formalized, see [Future Research Directions](future-studies.md).']
    save('docs/studies/index.md', lines)

    lines = ['# Current Research Status', '',
       'The table below is generated from the study metadata. A research milestone does not imply peer-reviewed publication or public release.', '',
       '| Study | Research | Paper | Public artifact package |', '| --- | --- | --- | --- |']
    for s in studies:
        lines.append(f'| [{s["id"]}](../studies/{s["url"]}) | {safe(s["research_status"])} | {safe(s["publication_status"])} | {safe(s["artifact_status"])} |')
    lines += ['', f'**Status last reviewed:** {safe(sp["as_of"])}.', '',
              'To update this page, edit `metadata/studies.json` and push to `main`. The publishing workflow regenerates the table.', '',
              'See the [roadmap](../roadmap/) for intended research sequencing.']
    save('docs/progress/status.md', lines)

    lines = ['# Publications', '',
        'This publication tracker describes actual or prospective scientific manuscripts. Working titles are not final bibliographic citations; no DOI, submission, acceptance, or publication is implied unless explicitly recorded.', '',
        '| ID | Working title | Related study | Manuscript status | Venue |', '| --- | --- | --- | --- | --- |']
    for p in pubs:
        lines.append(f'| {safe(p["id"])} | {safe(p["title"])} | {safe(p["study"])} | {safe(p["status"])} | {safe(p["venue"])} |')
    lines += ['', f'**Status last reviewed:** {safe(pp["as_of"])}.', '',
         'The published papers and datasets will be added with verified DOI, citation, source code, preprint, and material links when available and permitted.', '',
         'For updates, edit `metadata/publications.json` and push to `main`.' ]
    save('docs/research-outputs/publications.md', lines)
    print(f'Catalogs generated: {len(studies)} studies, {len(pubs)} publication records')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='validate without generating pages')
    main(check=parser.parse_args().check)
