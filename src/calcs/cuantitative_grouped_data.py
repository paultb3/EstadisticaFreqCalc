import pandas as pd
import numpy as np
import os
import math

# =================== FUNCIONES ===================

def find_min(data):
    return np.min(data)

def find_max(data):
    return np.max(data)

def find_range(data):
    return np.max(data) - np.min(data)

def log_n(n):
    return math.log10(n)

def calculate_m(n):
    return 1 + (3.322 * log_n(n))

def round_m(m, ):
    return round(m)

def calculate_amplitude(rango, m_redondeado):
    return math.ceil(rango / m_redondeado)

def calc_intervals(vmin, amplitud, m):
    intervals = []
    lower = vmin
    for _ in range(m):
        upper = lower + amplitud
        intervals.append((lower, upper))
        lower = upper
    return intervals

def calc_fi(data, intervals):
    fi = []
    for lower, upper in intervals:
        count = sum(1 for x in data if lower <= x < upper)
        fi.append(count)
    return fi

def calc_fi_cumulative(fi):
    return np.cumsum(fi).tolist()

def calc_hi(fi, n):
    return [f / n for f in fi]

def calc_hi_cumulative(hi):
    return np.cumsum(hi).tolist()

def calc_pi_percent(hi):
    return [h * 100 for h in hi]

def calc_pi_cumulative(pi):
    return np.cumsum(pi).tolist()

def calc_midpoints(intervals):
    return [(l + u) / 2 for l, u in intervals]

def calc_mean(midpoints, fi, n):
    return sum([f * x for f, x in zip(fi, midpoints)]) / n

def calc_median(intervals, fi, n, amplitud):
    Fi = calc_fi_cumulative(fi)
    median_class_idx = next(i for i, F in enumerate(Fi) if F >= n / 2)
    L = intervals[median_class_idx][0]
    F_prev = Fi[median_class_idx - 1] if median_class_idx > 0 else 0
    f = fi[median_class_idx]
    return L + ((n / 2 - F_prev) / f) * amplitud

def calc_mode(intervals, fi, amplitud):
    modal_idx = np.argmax(fi)
    L = intervals[modal_idx][0]
    f1 = fi[modal_idx]
    f0 = fi[modal_idx - 1] if modal_idx > 0 else 0
    f2 = fi[modal_idx + 1] if modal_idx + 1 < len(fi) else 0
    if (2*f1 - f0 - f2) == 0:
        return L
    return L + ((f1 - f0) / (2*f1 - f0 - f2)) * amplitud


