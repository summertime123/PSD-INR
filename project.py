import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
import rdn
import mlp 

class ProjFun(nn.Module):
    def __init__(self):
        super(ProjFun, self).__init__()
        self.projac = nn.ReLU()

    def _Projection2D(self, local_feat, global_feat):
        b, c, w, h = global_feat.size()
        local_feat = local_feat.view(b, c, w * h)
        global_feat = global_feat.view(b, c, w * h)
        projection_1 = torch.sum((local_feat * global_feat), dim=-1, keepdim=True)
        projection_2 = torch.sum((global_feat * global_feat), dim=-1, keepdim=True)
        projection_3 = projection_1 * global_feat / (projection_2 + 1e-6)
        # utils.keshihuafeat(projection_3.view(b, c, w, h),'projection_feat')
        out = local_feat - projection_3
        out = out.view(b, c, w, h)
        # utils.keshihuafeat(out,'out_resulial')
        out = self.projac(out)
        return out

    def forward(self, X, H):
        residual = self._Projection2D(X, H)
        return residual
