import numpy as np
from PIL import Image
from scipy import ndimage
d = np.load('work/lidar_polar.npz'); r, th, h, c = d['r'], d['th'], d['h'], d['c']
CX, CY = 437677.50, 4476982.68
# DSM raster 0.4 m, max z per cell, 100x100 m
res, half = 0.4, 50
dx = r * np.sin(np.radians(th)); dy = r * np.cos(np.radians(th))
m = (np.abs(dx) < half) & (np.abs(dy) < half) & (c != 7)
ix = ((dx[m] + half) / res).astype(int); iy = ((half - dy[m]) / res).astype(int)
n = int(2 * half / res); dsm = np.full((n, n), np.nan)
np.fmax.at(dsm, (iy, ix), h[m])
dsm = np.where(np.isnan(dsm), ndimage.generic_filter(np.nan_to_num(dsm, nan=-1), np.max, 3), dsm)
v = np.clip(dsm / 30, 0, 1)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10)); plt.imshow(dsm, cmap='turbo', vmin=0, vmax=30, extent=[-half, half, -half, half]); plt.colorbar(shrink=.7)
for rr in (10, 20, 30, 38, 41.5): plt.gca().add_patch(plt.Circle((0, 0), rr, fill=False, color='w', lw=.5))
plt.title('DSM LiDAR 2024 (m sobre suelo)'); plt.savefig('work/dsm.png', dpi=90); np.save('work/dsm.npy', dsm)
# ortho polar unwrap: theta 0..360 (azimuth from N clockwise) x r 0..45
im = np.asarray(Image.open('refs/geo/pnoa_ma_010m.png').convert('RGB')).astype(float)
TH = np.radians(np.arange(0, 360, 0.1)); R = np.arange(0, 45, 0.05)
tt, rr = np.meshgrid(TH, R)
px = (80 + rr * np.sin(tt)) / 0.1; py = (80 - rr * np.cos(tt)) / 0.1
out = np.stack([ndimage.map_coordinates(im[..., k], [py, px], order=1) for k in range(3)], -1)
Image.fromarray(out[::-1].clip(0, 255).astype(np.uint8)).save('work/ortho_polar.png')
