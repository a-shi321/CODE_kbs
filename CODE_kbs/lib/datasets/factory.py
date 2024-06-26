# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__sets = {}
from datasets.pascal_voc_clipart import clipart

from datasets.pascal_voc import pascal_voc
from datasets.cityscape import cityscape
from datasets.myself import myself
from datasets.coco import coco
from datasets.imagenet import imagenet
from datasets.vg import vg
from datasets.water import water
from datasets.uda_pascal_voc import uda_pascal_voc
import numpy as np
from datasets.vg import vg

# Set up voc_<year>_<split>
# for year in ['2007', '2012']:
#   for split in ['train', 'val', 'trainval', 'test']:
#     name = 'voc_{}_{}'.format(year, split)
#     __sets[name] = (lambda split=split, year=year: pascal_voc(split, year))
for year in ['2007', '2012']:
  for split in ['train']:
    name = 'clipart_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: clipart(split, year))
# for year in ['2007', '2012']:
#   for split in [ 'test']:
#     name = 'clipart_{}_{}'.format(year, split)
#     __sets[name] = (lambda split=split, year=year: clipart_test(split, year))

for year in ['2007', '2012']:
  for split in ['train_s', 'train_t', 'train_all', 'test_s', 'test_t','test_all']:
    name = 'cityscape_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: cityscape(split, year))
# Set up voc_<year>_<split>

for year in ['2007', '2012']:
  for split in ['train_trainval', 'test']:
    name = 'VOC_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: pascal_voc(split, year))

for year in ['2007', '2012']:
  for split in ['test']:
    name = 'VOC_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: uda_pascal_voc(split, year))


for year in ['2007', '2012']:
  for split in ['train', 'val', 'train_all', 'test']:
    name = 'watercolor_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year:water(split, year))

def get_imdb(name):
  """Get an imdb (image database) by name."""
  #print("这个命名集合是个啥factory",__sets)
  if name not in __sets:
    raise KeyError('Unknown dataset: {}'.format(name))
  return __sets[name]()


def list_imdbs():
  """List all registered imdbs."""
  return list(__sets.keys())
