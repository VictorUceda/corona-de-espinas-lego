import json, numpy as np, laspy
from PIL import Image
CX, CY = 437677.50, 4476982.68
las = laspy.read('refs/geo/lidar_clip.laz')
x, y, z, c = np.asarray(las.x), np.asarray(las.y), np.asarray(las.z), np.asarray(las.classification)
dx, dy = x - CX, y - CY
r = np.hypot(dx, dy); th = np.degrees(np.arctan2(dx, dy)) % 360  # azimuth from north, clockwise
g = np.median(z[(c == 2) & (r > 42) & (r < 60)]); print('ground', round(g, 2))
b = (c == 6) | (c == 1)
print('radial profile (r, n, p10, p50, p90, max) heights above ground:')
for r0 in np.arange(0, 44, 1.0):
    m = b & (r >= r0) & (r < r0 + 1)
    if m.sum() > 3:
        h = z[m] - g
        print(f'{r0:4.0f} {m.sum():5d} {np.percentile(h,10):6.2f} {np.median(h):6.2f} {np.percentile(h,90):6.2f} {h.max():6.2f}')
np.savez('work/lidar_polar.npz', r=r, th=th, h=z - g, c=c)
# ortho polar unwrap
meta = json.load(open('refs/geo/pnoa_ma_010m.json')); print(meta)
