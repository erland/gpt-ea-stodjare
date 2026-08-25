#!/usr/bin/env python3
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
obj=yaml.safe_load((ROOT/'schemas/object-types.yaml').read_text())['object_types']
p=obj['product']
assert p['id_prefix']=='PRD-'
assert p['category']=='supporting'
assert 'application_product' in p['allowed_values']['product_kind']
assert 'platform_product' in p['allowed_values']['product_kind']
fmt=yaml.safe_load((ROOT/'schemas/model-format.yaml').read_text())
assert fmt['file_structure']['object_files']['products.yaml']=='product'
assert (ROOT/'model/products.yaml').exists()
legacy=yaml.safe_load((ROOT/'compatibility/ea-stodjare-v1/schemas/object-types.yaml').read_text())
assert 'product' not in legacy['object_types']
mig=yaml.safe_load((ROOT/'compatibility/migration-rules/v1-to-v2-product-object.yaml').read_text())['migration_rule']
assert mig['automatic'] is False
print('OK: v2 Product object and legacy separation verified')
