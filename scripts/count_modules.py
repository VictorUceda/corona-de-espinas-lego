import numpy as np
from scipy.signal import find_peaks
from scipy import ndimage
d = np.load('work/lidar_polar.npz'); r, th, h, c = d['r'], d['th'], d['h'], d['c']
b = (c == 6) | (c == 1)
# max height per 1-degree bin in spike ring
for lo, hi in [(28, 34), (29.5, 32.5)]:
    m = b & (r > lo) & (r < hi)
    bins = np.full(720, np.nan); idx = (th[m] * 2).astype(int)
    np.fmax.at(bins, idx, h[m])
    bins = np.nan_to_num(bins, nan=0)
    sm = ndimage.uniform_filter1d(bins, 3, mode='wrap')
    pk, _ = find_peaks(np.r_[sm, sm[:20]], height=26, distance=5, prominence=1.0)
    pk = pk[pk < 720]
    print(f'ring {lo}-{hi}: peaks={len(pk)}')
    az = pk / 2; dif = np.diff(np.r_[az, az[0] + 360])
    print(' azimuths', np.round(az, 1).tolist()); print(' spacing', np.round(dif, 1).tolist())
    print(' median spacing', np.median(dif))
# entrance gap: angular coverage of building points at r 30-40 with h>17
m = b & (r > 30) & (r < 40) & (h > 17)
hist = np.bincount((th[m]).astype(int), minlength=360)
empty = np.where(hist == 0)[0]; print('empty az bins at r30-40,h>17:', empty.tolist())
for rr in (36, 39, 41, 42):
    m = b & (r > rr - 1) & (r < rr) & (h > 8)
    hist = np.bincount((th[m]).astype(int), minlength=360); print('r', rr, 'empty', np.where(hist == 0)[0].tolist())
