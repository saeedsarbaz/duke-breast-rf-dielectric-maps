"""The study's seven-channel 2.5-D U-Net and checkpoint loader."""

from pathlib import Path

import torch
from torch import nn


class ConvBlock(nn.Module):
    def __init__(self, in_ch: int, out_ch: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class SmallUNet(nn.Module):
    def __init__(self, in_ch: int = 7, base: int = 24):
        super().__init__()
        self.e1 = ConvBlock(in_ch, base)
        self.e2 = ConvBlock(base, base * 2)
        self.e3 = ConvBlock(base * 2, base * 4)
        self.p = nn.MaxPool2d(2)
        self.u2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2)
        self.d2 = ConvBlock(base * 4, base * 2)
        self.u1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2)
        self.d1 = ConvBlock(base * 2, base)
        self.out = nn.Conv2d(base, 1, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e1 = self.e1(x)
        e2 = self.e2(self.p(e1))
        e3 = self.e3(self.p(e2))
        d2 = self.d2(torch.cat([self.u2(e3), e2], dim=1))
        d1 = self.d1(torch.cat([self.u1(d2), e1], dim=1))
        return self.out(d1)


def load_fold_checkpoint(checkpoint_path, device="cpu") -> SmallUNet:
    """Load an original fold checkpoint; returns an eval-mode logit model."""
    checkpoint = torch.load(Path(checkpoint_path), map_location="cpu", weights_only=True)
    if checkpoint["input_channels"] != 7 or checkpoint["out_size"] != 128:
        raise ValueError("Expected a study checkpoint with seven channels and 128 x 128 inputs")
    if checkpoint["fold"] not in range(1, 7):
        raise ValueError("Checkpoint fold must be between 1 and 6")
    model = SmallUNet(in_ch=7, base=24)
    model.load_state_dict(checkpoint["state_dict"], strict=True)
    return model.to(device).eval()
