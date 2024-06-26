# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen
# --------------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
import torchvision.models as models
from lib.model.da_faster_rcnn.faster_rcnn_Multi import _fasterRCNN
import copy
from model.utils.config import cfg
import pdb
import os.path as osp


class vgg16(_fasterRCNN):
    def __init__(self, classes, pretrained=False, class_agnostic=False):
        self.model_path = osp.abspath(osp.join(cfg.DATA_DIR, 'pretrained_model/vgg16_caffe.pth'))  # 加载预训练模型
        self.dout_base_model = 512
        self.pretrained = pretrained
        self.class_agnostic = class_agnostic

        _fasterRCNN.__init__(self, classes, class_agnostic)  ## 在子类中调用父类的方法：父类名.方法名称(参数)

    def _init_modules(self):
        vgg = models.vgg16()
        if self.pretrained:
            print("Loading pretrained weights from %s" % (self.model_path))
            state_dict = torch.load(self.model_path)
            vgg.load_state_dict({k: v for k, v in state_dict.items() if k in vgg.state_dict()})

        vgg.classifier = nn.Sequential(*list(vgg.classifier._modules.values())[:-1])

        # not using the last maxpool layer
        self.RCNN_base = nn.Sequential(*list(vgg.features._modules.values())[:-1])
        target_layer_list = []
        for i in range(10):
            target_layer_list.append(list(self.RCNN_base._modules.values())[i])
        for i in range(10, len(self.RCNN_base._modules.values())):
            target_layer_list.append(copy.deepcopy(list(self.RCNN_base._modules.values())[i]))
        self.RCNN_base_t = nn.Sequential(*target_layer_list)

        self.conv3_s = nn.Sequential(*list(vgg.features._modules.values())[:17])
        #self.conv3_t = nn.Sequential(*list(self.RCNN_base_t._modules.values())[:16])

        self.conv34_s = nn.Sequential(*list(vgg.features._modules.values())[17:24])
        #self.conv34_t = nn.Sequential(*list(self.RCNN_base_t._modules.values())[16:23])

        self.conv45_s = nn.Sequential(*list(vgg.features._modules.values())[24: -1])
        #self.conv45_t = nn.Sequential(*list(self.RCNN_base_t._modules.values())[23:])

        # Fix the layers before conv3:
        for layer in range(10):
            for p in self.RCNN_base[layer].parameters(): p.requires_grad = False
            #for p in self.RCNN_base_t[layer].parameters(): p.requires_grad = False

        self.RCNN_top = vgg.classifier
        self.RCNN_cls_score = nn.Linear(4096, self.n_classes)

        if self.class_agnostic:
            self.RCNN_bbox_pred = nn.Linear(4096, 4)
        else:
            self.RCNN_bbox_pred = nn.Linear(4096, 4 * self.n_classes)

    def _head_to_tail(self, pool5):

        pool5_flat = pool5.view(pool5.size(0), -1)
        fc7 = self.RCNN_top(pool5_flat)

        return fc7


'''
self.RCNN_base = nn.Sequential(*list(vgg.features._modules.values())[:14])
        self.RCNN_base2 = nn.Sequential(*list(vgg.features._modules.values())[14:21])
        self.RCNN_base3 = nn.Sequential(*list(vgg.features._modules.values())[21:-1])
'''