#!/usr/bin/env python3
# Copyright: Harald Schilly <hsy@sagemath.com>
# License: Apache 2.0
from pprint import pprint
import yaml
import json
import os
import itertools as it
# to make all "src" absolute paths!
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

ID = it.count(0)

# TODO this is silly code, fix it

def update_meta(meta, new_meta):
    '''
    A simple dict update would overwrite/remove entries.
    '''
    if 'tags' in new_meta:
        meta['tags'].update(new_meta['tags'])
    if 'licenses' in new_meta:
        meta['licenses'].update(new_meta['licenses'])

def init_doc(docs, prefix):
    for doc in docs:
        doc['src'] = os.path.join(prefix, doc['src'])
        assert 'id' not in doc
        doc['id'] = 'doc-{}'.format(next(ID))

# prefix is the path to prefix
def resolve_references(meta, docs, prefix=''):
    # append new documents and merge meta
    if 'references' in meta:
        for ref in meta['references']:
            prefix = os.path.join(prefix, os.path.dirname(ref))
            print("resolve_references prefix={}".format(prefix))
            new_meta, *new_docs = yaml.load_all(open(ref))
            init_doc(new_docs, prefix)
            resolve_references(new_meta, new_docs, prefix=prefix)
            update_meta(meta, new_meta)
            docs.extend(new_docs)
        del meta['references']
    return meta, docs

def debug(meta, docs):
    print("META:")
    pprint(meta)
    print("DOCS:")
    for doc in docs:
        pprint(doc)

def export_json(meta, docs):
    with open('index.json', 'w') as out:
        json.dump({'metadata': meta, 'documents': docs}, out, indent=1)

def main(index_fn):
    meta, *docs = yaml.load_all(open(index_fn))
    init_doc(docs, ROOT)
    resolve_references(meta, docs, prefix=ROOT)
    debug(meta, docs)
    export_json(meta, docs)

if __name__ == '__main__':
    main(index_fn = 'index.yaml')