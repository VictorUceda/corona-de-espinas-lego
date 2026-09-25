import numpy as np, laspy
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
CX, CY = 437677.50, 4476982.68
fig, ax = plt.subplots(figsize=(14, 8))
for f, col in [('refs/geo/lidar_clip.laz', 'k'), ('refs/geo/lidar_clip_2016.laz', 'r')]:
    L = laspy.read(f); x, y, z, c = map(np.asarray, (L.x, L.y, L.z, L.classification))
    r = np.hypot(x - CX, y - CY); az = np.degrees(np.arctan2(x - CX, y - CY)) % 360
    g = np.median(z[(c == 2) & (r > 42) & (r < 60)])
    m = (r < 46) & ~np.isin(c, [3, 4, 5, 7]) & ((az < 160) | (az > 215))
    ax.scatter(r[m], z[m] - g, s=.3, c=col, alpha=.25)
    # facade points: at r 37-44, heights 0.5..14, building classes
    fm = m & (r > 36) & (z - g > 0.5) & (z - g < 16)
    print(f, 'ground', round(g, 2), 'facade-ish pts', fm.sum())
    for h0 in np.arange(0, 16, 1):
        mm = fm & (z - g >= h0) & (z - g < h0 + 1)
        if mm.sum() > 5: print(f'  h {h0:4.1f}: n={mm.sum():4d} r p50={np.median(r[mm]):.2f} p90={np.percentile(r[mm],90):.2f} max={r[mm].max():.2f}')
ax.set_xlim(0, 46); ax.set_ylim(-1, 31); ax.set_aspect('equal'); ax.grid(True, lw=.3); ax.set_xticks(range(0, 47, 2)); ax.set_yticks(range(0, 32, 2))
ax.set_xlabel('r (m)'); ax.set_ylabel('h (m)'); plt.savefig('work/section_lidar.png', dpi=110, bbox_inches='tight')
