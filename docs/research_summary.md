Found 24 summary file(s):
  - battery_summary_dynamic_astar_apf_def.csv
  - battery_summary_dynamic_astar_dwa_def.csv
  - battery_summary_dynamic_dijkstra_apf_def.csv
  - battery_summary_dynamic_dijkstra_dwa_def.csv
  - battery_summary_dynamic_dstar_lite_apf_def.csv
  - battery_summary_dynamic_dstar_lite_dwa_def.csv
  - battery_summary_dynamic_hybrid_astar_apf_def.csv
  - battery_summary_dynamic_hybrid_astar_dwa_def.csv
  - battery_summary_dynamic_lazy_theta_star_apf_def.csv
  - battery_summary_dynamic_lazy_theta_star_dwa_def.csv
  - battery_summary_dynamic_rrt_apf_10..csv
  - battery_summary_dynamic_rrt_dwa_10..csv
  - battery_summary_static_astar_apf_def.csv
  - battery_summary_static_astar_dwa_def.csv
  - battery_summary_static_dijkstra_apf_def.csv
  - battery_summary_static_dijkstra_dwa_def.csv
  - battery_summary_static_dstar_lite_apf_def.csv
  - battery_summary_static_dstar_lite_dwa_def.csv
  - battery_summary_static_hybrid_astar_apf_def.csv
  - battery_summary_static_hybrid_astar_dwa_def.csv
  - battery_summary_static_lazy_theta_star_apf_def.csv
  - battery_summary_static_lazy_theta_star_dwa_def.csv
  - battery_summary_static_rrt_apf_10..csv
  - battery_summary_static_rrt_dwa_10..csv
  [WARN] Could not read battery_summary_static_astar_apf_def.csv: Error tokenizing data. C error: Expected 14 fields in line 30, saw 15
. Skipping.
  [WARN] Could not read battery_summary_static_astar_dwa_def.csv: Error tokenizing data. C error: Expected 14 fields in line 32, saw 15
. Skipping.
  [WARN] Could not read battery_summary_static_dijkstra_apf_def.csv: Error tokenizing data. C error: Expected 14 fields in line 31, saw 15
. Skipping.
  [WARN] Could not read battery_summary_static_dijkstra_dwa_def.csv: Error tokenizing data. C error: Expected 14 fields in line 31, saw 15
. Skipping.
  [WARN] Could not read battery_summary_static_hybrid_astar_apf_def.csv: Error tokenizing data. C error: Expected 14 fields in line 16, saw 15
. Skipping.
  [WARN] Could not read battery_summary_static_hybrid_astar_dwa_def.csv: Error tokenizing data. C error: Expected 14 fields in line 15, saw 15
. Skipping.

Total rows after merge: 3144
Identified 88 unique experimental conditions.

============================================================
  SUCCESS RATES (grouped by Algorithm)
============================================================

  astar-apf                                | 196/269 =  72.9%  CI: [67.3%, 77.8%]
  astar-dwa                                | 163/254 =  64.2%  CI: [58.1%, 69.8%]
  dijkstra-apf                             |  96/137 =  70.1%  CI: [61.9%, 77.1%]
  dijkstra-dwa                             |  90/135 =  66.7%  CI: [58.4%, 74.1%]
  dstar_lite-apf                           | 151/269 =  56.1%  CI: [50.2%, 61.9%]
  dstar_lite-dwa                           | 161/288 =  55.9%  CI: [50.1%, 61.5%]
  hybrid_astar-apf                         | 112/214 =  52.3%  CI: [45.7%, 58.9%]
  hybrid_astar-dwa                         | 116/251 =  46.2%  CI: [40.2%, 52.4%]
  lazy_theta_star-apf                      |   0/237 =   0.0%  CI: [0.0%, 1.6%]
  lazy_theta_star-dwa                      |   0/237 =   0.0%  CI: [0.0%, 1.6%]
  rrt-apf                                  | 253/445 =  56.9%  CI: [52.2%, 61.4%]
  rrt-dwa                                  | 217/408 =  53.2%  CI: [48.3%, 58.0%]

Successful runs: 1555 / 3144

============================================================
  METRIC: Time(s)
============================================================

--- Descriptive Statistics ---
                  count       mean        std      min        25%       50%        75%       max
Algorithm                                                                                       
astar-apf         196.0  50.699899  29.199546  15.6067  31.610450  44.36595  61.324625  174.8057
astar-dwa         163.0  66.257702  35.620320  14.6650  39.629900  56.49900  83.310400  174.8054
dijkstra-apf       96.0  47.447510  23.111274  17.7044  32.637275  43.59475  55.146325  140.8252
dijkstra-dwa       90.0  64.346668  35.269140  15.6975  37.938575  56.53715  77.731225  166.4947
dstar_lite-apf    151.0  39.917895  21.827585  11.0283  25.843900  36.33730  49.778900  173.4640
dstar_lite-dwa    161.0  59.961687  35.388377  12.9140  35.032600  51.21060  72.407800  176.2191
hybrid_astar-apf  112.0  70.460306  32.278149  21.6694  48.835550  64.03775  87.880700  170.1907
hybrid_astar-dwa  116.0  69.408578  27.821793  19.3397  47.745975  65.73245  87.258425  131.9084
rrt-apf           253.0  54.803647  28.458965  13.0131  34.647900  48.25430  71.777100  166.3584
rrt-dwa           217.0  54.378434  27.523226  14.5775  31.603800  50.19500  70.181300  143.7269

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar-apf                                | Mean=50.6999  95% CI: [46.8067, 54.8028]
  astar-dwa                                | Mean=66.2577  95% CI: [60.9868, 71.9802]
  dijkstra-apf                             | Mean=47.4475  95% CI: [42.9593, 52.2661]
  dijkstra-dwa                             | Mean=64.3467  95% CI: [57.4375, 71.8332]
  dstar_lite-apf                           | Mean=39.9179  95% CI: [36.6439, 43.5866]
  dstar_lite-dwa                           | Mean=59.9617  95% CI: [54.6284, 65.6302]
  hybrid_astar-apf                         | Mean=70.4603  95% CI: [64.6738, 76.3468]
  hybrid_astar-dwa                         | Mean=69.4086  95% CI: [64.4301, 74.4531]
  rrt-apf                                  | Mean=54.8036  95% CI: [51.2804, 58.3889]
  rrt-dwa                                  | Mean=54.3784  95% CI: [50.7809, 57.9830]

=== Shapiro-Wilk Normality Test (Time(s)) ===
H0: Data is normally distributed (p > 0.05)

  astar-apf                                | W=0.8195  p=0.000000  => NOT Normal
  astar-dwa                                | W=0.9059  p=0.000000  => NOT Normal
  dijkstra-apf                             | W=0.8620  p=0.000000  => NOT Normal
  dijkstra-dwa                             | W=0.8783  p=0.000000  => NOT Normal
  dstar_lite-apf                           | W=0.8346  p=0.000000  => NOT Normal
  dstar_lite-dwa                           | W=0.8762  p=0.000000  => NOT Normal
  hybrid_astar-apf                         | W=0.9386  p=0.000062  => NOT Normal
  hybrid_astar-dwa                         | W=0.9600  p=0.001593  => NOT Normal
  rrt-apf                                  | W=0.9298  p=0.000000  => NOT Normal
  rrt-dwa                                  | W=0.9407  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Time(s)) ===
  H=148.7972  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Time(s)) ---
  astar-apf            vs astar-dwa            | U=11385.0  p=0.000003  => DIFFERENT
  astar-apf            vs dijkstra-apf         | U=9740.0  p=0.624788  => similar
  astar-apf            vs dijkstra-dwa         | U=6524.0  p=0.000409  => DIFFERENT
  astar-apf            vs dstar_lite-apf       | U=18376.0  p=0.000113  => DIFFERENT
  astar-apf            vs dstar_lite-dwa       | U=13276.0  p=0.009933  => DIFFERENT
  astar-apf            vs hybrid_astar-apf     | U=6374.0  p=0.000000  => DIFFERENT
  astar-apf            vs hybrid_astar-dwa     | U=6464.0  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-apf              | U=22157.0  p=0.053186  => similar
  astar-apf            vs rrt-dwa              | U=19025.0  p=0.064371  => similar
  astar-dwa            vs dijkstra-apf         | U=10413.0  p=0.000009  => DIFFERENT
  astar-dwa            vs dijkstra-dwa         | U=7537.0  p=0.717648  => similar
  astar-dwa            vs dstar_lite-apf       | U=18448.0  p=0.000000  => DIFFERENT
  astar-dwa            vs dstar_lite-dwa       | U=14681.0  p=0.064426  => similar
  astar-dwa            vs hybrid_astar-apf     | U=8048.0  p=0.095728  => similar
  astar-dwa            vs hybrid_astar-dwa     | U=8290.0  p=0.079829  => similar
  astar-dwa            vs rrt-apf              | U=24298.0  p=0.002123  => DIFFERENT
  astar-dwa            vs rrt-dwa              | U=20914.0  p=0.002319  => DIFFERENT
  dijkstra-apf         vs dijkstra-dwa         | U=3007.0  p=0.000348  => DIFFERENT
  dijkstra-apf         vs dstar_lite-apf       | U=8874.0  p=0.002980  => DIFFERENT
  dijkstra-apf         vs dstar_lite-dwa       | U=6203.0  p=0.008179  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-apf     | U=2822.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-dwa     | U=2840.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs rrt-apf              | U=10348.0  p=0.032902  => DIFFERENT
  dijkstra-apf         vs rrt-dwa              | U=8854.0  p=0.034433  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-apf       | U=10062.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-dwa       | U=7861.0  p=0.264510  => similar
  dijkstra-dwa         vs hybrid_astar-apf     | U=4242.0  p=0.053450  => similar
  dijkstra-dwa         vs hybrid_astar-dwa     | U=4334.0  p=0.036922  => DIFFERENT
  dijkstra-dwa         vs rrt-apf              | U=13053.0  p=0.039024  => DIFFERENT
  dijkstra-dwa         vs rrt-dwa              | U=11200.0  p=0.042753  => DIFFERENT
  dstar_lite-apf       vs dstar_lite-dwa       | U=7552.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-apf     | U=3236.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-dwa     | U=3165.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-apf              | U=12739.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-dwa              | U=10985.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-apf     | U=6858.0  p=0.000773  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-dwa     | U=6985.0  p=0.000348  => DIFFERENT
  dstar_lite-dwa       vs rrt-apf              | U=21398.0  p=0.385031  => similar
  dstar_lite-dwa       vs rrt-dwa              | U=18466.0  p=0.342557  => similar
  hybrid_astar-apf     vs hybrid_astar-dwa     | U=6444.0  p=0.917623  => similar
  hybrid_astar-apf     vs rrt-apf              | U=18455.0  p=0.000004  => DIFFERENT
  hybrid_astar-apf     vs rrt-dwa              | U=15839.5  p=0.000006  => DIFFERENT
  hybrid_astar-dwa     vs rrt-apf              | U=19288.0  p=0.000001  => DIFFERENT
  hybrid_astar-dwa     vs rrt-dwa              | U=16558.0  p=0.000002  => DIFFERENT
  rrt-apf              vs rrt-dwa              | U=27441.0  p=0.995108  => similar

============================================================
  METRIC: Distance(m)
============================================================

--- Descriptive Statistics ---
                  count       mean        std     min        25%       50%        75%      max
Algorithm                                                                                     
astar-apf         196.0  16.717386   7.269632  5.7528  11.280625  16.10325  20.622150  45.5061
astar-dwa         163.0  15.697677   7.039651  5.5460  10.480400  14.53010  18.679600  38.8654
dijkstra-apf       96.0  17.123190   7.701392  6.3514  11.671375  16.62955  20.356350  48.6708
dijkstra-dwa       90.0  16.260530   7.194816  5.5349  10.667875  15.93210  18.873350  37.5067
dstar_lite-apf    151.0  15.705413   7.143174  5.0079  10.479750  14.62800  18.924750  51.5627
dstar_lite-dwa    161.0  15.308062   6.719436  5.1756  10.372100  14.29050  18.398200  45.4483
hybrid_astar-apf  112.0  20.696949   8.801566  7.3175  14.215800  19.47470  25.855325  42.4415
hybrid_astar-dwa  116.0  15.493449   5.654489  6.3412  11.341600  14.68385  18.970550  30.2006
rrt-apf           253.0  21.288214  10.957956  5.3545  12.809700  19.46150  27.158500  72.3356
rrt-dwa           217.0  18.210340   9.414126  5.2151  11.009300  17.20140  23.297700  60.6200

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar-apf                                | Mean=16.7174  95% CI: [15.7080, 17.7389]
  astar-dwa                                | Mean=15.6977  95% CI: [14.6405, 16.7882]
  dijkstra-apf                             | Mean=17.1232  95% CI: [15.6361, 18.7397]
  dijkstra-dwa                             | Mean=16.2605  95% CI: [14.8147, 17.7679]
  dstar_lite-apf                           | Mean=15.7054  95% CI: [14.6042, 16.8767]
  dstar_lite-dwa                           | Mean=15.3081  95% CI: [14.2926, 16.3742]
  hybrid_astar-apf                         | Mean=20.6969  95% CI: [19.0607, 22.3305]
  hybrid_astar-dwa                         | Mean=15.4934  95% CI: [14.4910, 16.5315]
  rrt-apf                                  | Mean=21.2882  95% CI: [19.9420, 22.6447]
  rrt-dwa                                  | Mean=18.2103  95% CI: [16.9752, 19.4560]

=== Shapiro-Wilk Normality Test (Distance(m)) ===
H0: Data is normally distributed (p > 0.05)

  astar-apf                                | W=0.9377  p=0.000000  => NOT Normal
  astar-dwa                                | W=0.9184  p=0.000000  => NOT Normal
  dijkstra-apf                             | W=0.8853  p=0.000000  => NOT Normal
  dijkstra-dwa                             | W=0.9191  p=0.000032  => NOT Normal
  dstar_lite-apf                           | W=0.9231  p=0.000000  => NOT Normal
  dstar_lite-dwa                           | W=0.9319  p=0.000001  => NOT Normal
  hybrid_astar-apf                         | W=0.9478  p=0.000257  => NOT Normal
  hybrid_astar-dwa                         | W=0.9661  p=0.004936  => NOT Normal
  rrt-apf                                  | W=0.9256  p=0.000000  => NOT Normal
  rrt-dwa                                  | W=0.9326  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Distance(m)) ===
  H=76.4418  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Distance(m)) ---
  astar-apf            vs astar-dwa            | U=17515.0  p=0.115593  => similar
  astar-apf            vs dijkstra-apf         | U=9136.0  p=0.688747  => similar
  astar-apf            vs dijkstra-dwa         | U=9251.0  p=0.507467  => similar
  astar-apf            vs dstar_lite-apf       | U=16081.5  p=0.166090  => similar
  astar-apf            vs dstar_lite-dwa       | U=17625.0  p=0.057030  => similar
  astar-apf            vs hybrid_astar-apf     | U=8033.0  p=0.000091  => DIFFERENT
  astar-apf            vs hybrid_astar-dwa     | U=12201.5  p=0.279386  => similar
  astar-apf            vs rrt-apf              | U=18846.0  p=0.000013  => DIFFERENT
  astar-apf            vs rrt-dwa              | U=19910.0  p=0.263138  => similar
  astar-dwa            vs dijkstra-apf         | U=6837.0  p=0.090222  => similar
  astar-dwa            vs dijkstra-dwa         | U=6957.0  p=0.498122  => similar
  astar-dwa            vs dstar_lite-apf       | U=12224.0  p=0.918744  => similar
  astar-dwa            vs dstar_lite-dwa       | U=13419.0  p=0.724622  => similar
  astar-dwa            vs hybrid_astar-apf     | U=5923.0  p=0.000001  => DIFFERENT
  astar-dwa            vs hybrid_astar-dwa     | U=9181.0  p=0.681618  => similar
  astar-dwa            vs rrt-apf              | U=14170.5  p=0.000000  => DIFFERENT
  astar-dwa            vs rrt-dwa              | U=15194.0  p=0.018743  => DIFFERENT
  dijkstra-apf         vs dijkstra-dwa         | U=4654.0  p=0.363411  => similar
  dijkstra-apf         vs dstar_lite-apf       | U=8088.0  p=0.125085  => similar
  dijkstra-apf         vs dstar_lite-dwa       | U=8864.0  p=0.048863  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-apf     | U=4068.0  p=0.002516  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-dwa     | U=6133.5  p=0.203792  => similar
  dijkstra-apf         vs rrt-apf              | U=9470.0  p=0.001491  => DIFFERENT
  dijkstra-apf         vs rrt-dwa              | U=9966.0  p=0.542643  => similar
  dijkstra-dwa         vs dstar_lite-apf       | U=7085.0  p=0.580266  => similar
  dijkstra-dwa         vs dstar_lite-dwa       | U=7778.0  p=0.334380  => similar
  dijkstra-dwa         vs hybrid_astar-apf     | U=3502.0  p=0.000197  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-dwa     | U=5348.0  p=0.763838  => similar
  dijkstra-dwa         vs rrt-apf              | U=8316.0  p=0.000146  => DIFFERENT
  dijkstra-dwa         vs rrt-dwa              | U=8775.0  p=0.162236  => similar
  dstar_lite-apf       vs dstar_lite-dwa       | U=12501.0  p=0.664835  => similar
  dstar_lite-apf       vs hybrid_astar-apf     | U=5562.0  p=0.000002  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-dwa     | U=8601.0  p=0.802418  => similar
  dstar_lite-apf       vs rrt-apf              | U=13221.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-dwa              | U=14110.0  p=0.023548  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-apf     | U=5678.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-dwa     | U=8849.0  p=0.457687  => similar
  dstar_lite-dwa       vs rrt-apf              | U=13585.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs rrt-dwa              | U=14647.0  p=0.007241  => DIFFERENT
  hybrid_astar-apf     vs hybrid_astar-dwa     | U=8740.0  p=0.000007  => DIFFERENT
  hybrid_astar-apf     vs rrt-apf              | U=14197.0  p=0.975543  => similar
  hybrid_astar-apf     vs rrt-dwa              | U=14317.0  p=0.008107  => DIFFERENT
  hybrid_astar-dwa     vs rrt-apf              | U=10124.5  p=0.000002  => DIFFERENT
  hybrid_astar-dwa     vs rrt-dwa              | U=11006.0  p=0.059157  => similar
  rrt-apf              vs rrt-dwa              | U=31965.0  p=0.002105  => DIFFERENT

============================================================
  METRIC: Smoothness(rad)
============================================================

--- Descriptive Statistics ---
                  count       mean         std     min        25%       50%        75%        max
Algorithm                                                                                        
astar-apf         196.0  40.877089   73.183909  2.3951  15.697700  25.35370  41.479000   760.5155
astar-dwa         163.0  79.034255  176.357866  2.8346  15.826150  31.76380  55.611350  1256.4033
dijkstra-apf       96.0  41.384857   75.077736  4.7734  19.628050  31.31535  43.804325   743.6382
dijkstra-dwa       90.0  70.256849  145.170785  3.3925  16.010975  30.53980  52.692550   875.8406
dstar_lite-apf    151.0  26.844194   26.001546  2.5204  12.286900  18.57360  34.987150   183.3694
dstar_lite-dwa    161.0  84.234130  199.135836  2.7883  10.028900  20.81270  47.690800  1366.5517
hybrid_astar-apf  112.0  46.756101   31.326302  6.4816  27.360925  40.48470  56.907150   204.3258
hybrid_astar-dwa  116.0  41.800879  126.137488  3.5316  10.926375  23.15610  38.528525  1354.8820
rrt-apf           253.0  60.369962   42.119066  8.8122  31.306600  49.34010  77.962300   292.2096
rrt-dwa           217.0  37.329171   31.232179  3.4433  16.173700  28.93570  49.449500   275.3321

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar-apf                                | Mean=40.8771  95% CI: [32.1708, 52.3651]
  astar-dwa                                | Mean=79.0343  95% CI: [53.8496, 108.2556]
  dijkstra-apf                             | Mean=41.3849  95% CI: [30.9877, 58.8784]
  dijkstra-dwa                             | Mean=70.2568  95% CI: [44.0378, 103.3305]
  dstar_lite-apf                           | Mean=26.8442  95% CI: [22.9568, 31.1935]
  dstar_lite-dwa                           | Mean=84.2341  95% CI: [56.5548, 116.3911]
  hybrid_astar-apf                         | Mean=46.7561  95% CI: [41.2288, 52.7543]
  hybrid_astar-dwa                         | Mean=41.8009  95% CI: [26.7147, 67.7972]
  rrt-apf                                  | Mean=60.3700  95% CI: [55.3905, 65.6259]
  rrt-dwa                                  | Mean=37.3292  95% CI: [33.3044, 41.6886]

=== Shapiro-Wilk Normality Test (Smoothness(rad)) ===
H0: Data is normally distributed (p > 0.05)

  astar-apf                                | W=0.3344  p=0.000000  => NOT Normal
  astar-dwa                                | W=0.3903  p=0.000000  => NOT Normal
  dijkstra-apf                             | W=0.2587  p=0.000000  => NOT Normal
  dijkstra-dwa                             | W=0.4118  p=0.000000  => NOT Normal
  dstar_lite-apf                           | W=0.7118  p=0.000000  => NOT Normal
  dstar_lite-dwa                           | W=0.4220  p=0.000000  => NOT Normal
  hybrid_astar-apf                         | W=0.8601  p=0.000000  => NOT Normal
  hybrid_astar-dwa                         | W=0.1876  p=0.000000  => NOT Normal
  rrt-apf                                  | W=0.8290  p=0.000000  => NOT Normal
  rrt-dwa                                  | W=0.7726  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Smoothness(rad)) ===
  H=175.0874  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Smoothness(rad)) ---
  astar-apf            vs astar-dwa            | U=14253.0  p=0.078849  => similar
  astar-apf            vs dijkstra-apf         | U=8402.0  p=0.137953  => similar
  astar-apf            vs dijkstra-dwa         | U=8049.0  p=0.235527  => similar
  astar-apf            vs dstar_lite-apf       | U=17948.0  p=0.000675  => DIFFERENT
  astar-apf            vs dstar_lite-dwa       | U=17535.0  p=0.070246  => similar
  astar-apf            vs hybrid_astar-apf     | U=7592.0  p=0.000007  => DIFFERENT
  astar-apf            vs hybrid_astar-dwa     | U=12669.0  p=0.091263  => similar
  astar-apf            vs rrt-apf              | U=12981.0  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-dwa              | U=19849.0  p=0.242258  => similar
  astar-dwa            vs dijkstra-apf         | U=8076.0  p=0.665793  => similar
  astar-dwa            vs dijkstra-dwa         | U=7489.0  p=0.782959  => similar
  astar-dwa            vs dstar_lite-apf       | U=15754.0  p=0.000018  => DIFFERENT
  astar-dwa            vs dstar_lite-dwa       | U=15392.0  p=0.007090  => DIFFERENT
  astar-dwa            vs hybrid_astar-apf     | U=7779.0  p=0.037429  => DIFFERENT
  astar-dwa            vs hybrid_astar-dwa     | U=11288.0  p=0.005773  => DIFFERENT
  astar-dwa            vs rrt-apf              | U=14429.0  p=0.000000  => DIFFERENT
  astar-dwa            vs rrt-dwa              | U=18608.0  p=0.384283  => similar
  dijkstra-apf         vs dijkstra-dwa         | U=4338.0  p=0.961961  => similar
  dijkstra-apf         vs dstar_lite-apf       | U=9523.0  p=0.000032  => DIFFERENT
  dijkstra-apf         vs dstar_lite-dwa       | U=9199.0  p=0.010744  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-apf     | U=4104.0  p=0.003301  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-dwa     | U=6670.0  p=0.013229  => DIFFERENT
  dijkstra-apf         vs rrt-apf              | U=6931.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs rrt-dwa              | U=10674.0  p=0.727263  => similar
  dijkstra-dwa         vs dstar_lite-apf       | U=8684.0  p=0.000309  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-dwa       | U=8469.0  p=0.026555  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-apf     | U=4119.0  p=0.025805  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-dwa     | U=6207.0  p=0.020092  => DIFFERENT
  dijkstra-dwa         vs rrt-apf              | U=7501.0  p=0.000002  => DIFFERENT
  dijkstra-dwa         vs rrt-dwa              | U=10040.0  p=0.698231  => similar
  dstar_lite-apf       vs dstar_lite-dwa       | U=11371.5  p=0.325159  => similar
  dstar_lite-apf       vs hybrid_astar-apf     | U=4334.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-dwa     | U=8030.0  p=0.244765  => similar
  dstar_lite-apf       vs rrt-apf              | U=7054.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-dwa              | U=11946.0  p=0.000010  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-apf     | U=6102.0  p=0.000006  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-dwa     | U=9239.0  p=0.880963  => similar
  dstar_lite-dwa       vs rrt-apf              | U=11335.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs rrt-dwa              | U=14838.0  p=0.012290  => DIFFERENT
  hybrid_astar-apf     vs hybrid_astar-dwa     | U=8974.0  p=0.000001  => DIFFERENT
  hybrid_astar-apf     vs rrt-apf              | U=11316.0  p=0.002160  => DIFFERENT
  hybrid_astar-apf     vs rrt-dwa              | U=14993.0  p=0.000512  => DIFFERENT
  hybrid_astar-dwa     vs rrt-apf              | U=6822.0  p=0.000000  => DIFFERENT
  hybrid_astar-dwa     vs rrt-dwa              | U=10402.0  p=0.009091  => DIFFERENT
  rrt-apf              vs rrt-dwa              | U=38750.0  p=0.000000  => DIFFERENT

============================================================
  METRIC: CPU(%)
============================================================

--- Descriptive Statistics ---
                  count       mean        std    min      25%     50%      75%     max
Algorithm                                                                             
astar-apf         196.0  11.909133   4.726379   5.77   8.8775  10.445  13.5325   30.21
astar-dwa         163.0  22.541656   5.325045   9.42  19.5900  22.110  24.6500   53.58
dijkstra-apf       96.0  31.347500  12.708774  10.08  22.1100  28.315  39.3050   66.50
dijkstra-dwa       90.0  41.124444  12.643698  15.69  31.8475  37.990  47.0575   80.10
dstar_lite-apf    151.0  40.925033  15.308133  14.29  28.5550  42.200  50.6350   77.34
dstar_lite-dwa    161.0  56.273851  15.729343  26.63  43.7000  56.650  67.4500  104.22
hybrid_astar-apf  112.0  45.502321  16.832523  22.07  33.1750  39.540  56.2825   83.97
hybrid_astar-dwa  116.0  51.699914  15.243898  22.86  40.9375  47.205  61.7925   88.25
rrt-apf           253.0  44.107905  34.032191   7.14   9.0400  39.950  76.2300  105.47
rrt-dwa           217.0  54.878111  36.321944  17.99  23.7500  30.500  87.1300  120.70

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar-apf                                | Mean=11.9091  95% CI: [11.2814, 12.5916]
  astar-dwa                                | Mean=22.5417  95% CI: [21.7480, 23.3669]
  dijkstra-apf                             | Mean=31.3475  95% CI: [28.8329, 33.8714]
  dijkstra-dwa                             | Mean=41.1244  95% CI: [38.6097, 43.7963]
  dstar_lite-apf                           | Mean=40.9250  95% CI: [38.5366, 43.3379]
  dstar_lite-dwa                           | Mean=56.2739  95% CI: [53.8327, 58.7152]
  hybrid_astar-apf                         | Mean=45.5023  95% CI: [42.4238, 48.7206]
  hybrid_astar-dwa                         | Mean=51.6999  95% CI: [49.0333, 54.4369]
  rrt-apf                                  | Mean=44.1079  95% CI: [40.0141, 48.2507]
  rrt-dwa                                  | Mean=54.8781  95% CI: [50.1065, 59.7419]

=== Shapiro-Wilk Normality Test (CPU(%)) ===
H0: Data is normally distributed (p > 0.05)

  astar-apf                                | W=0.8559  p=0.000000  => NOT Normal
  astar-dwa                                | W=0.8974  p=0.000000  => NOT Normal
  dijkstra-apf                             | W=0.9611  p=0.006099  => NOT Normal
  dijkstra-dwa                             | W=0.9574  p=0.004950  => NOT Normal
  dstar_lite-apf                           | W=0.9758  p=0.009162  => NOT Normal
  dstar_lite-dwa                           | W=0.9840  p=0.059842  => Normal
  hybrid_astar-apf                         | W=0.8961  p=0.000000  => NOT Normal
  hybrid_astar-dwa                         | W=0.9339  p=0.000023  => NOT Normal
  rrt-apf                                  | W=0.8614  p=0.000000  => NOT Normal
  rrt-dwa                                  | W=0.8033  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (CPU(%)) ===
  H=626.3648  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (CPU(%)) ---
  astar-apf            vs astar-dwa            | U=2280.5  p=0.000000  => DIFFERENT
  astar-apf            vs dijkstra-apf         | U= 960.0  p=0.000000  => DIFFERENT
  astar-apf            vs dijkstra-dwa         | U= 106.0  p=0.000000  => DIFFERENT
  astar-apf            vs dstar_lite-apf       | U= 594.0  p=0.000000  => DIFFERENT
  astar-apf            vs dstar_lite-dwa       | U=  12.0  p=0.000000  => DIFFERENT
  astar-apf            vs hybrid_astar-apf     | U=  62.0  p=0.000000  => DIFFERENT
  astar-apf            vs hybrid_astar-dwa     | U=  19.0  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-apf              | U=13694.0  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-dwa              | U= 865.5  p=0.000000  => DIFFERENT
  astar-dwa            vs dijkstra-apf         | U=4270.0  p=0.000000  => DIFFERENT
  astar-dwa            vs dijkstra-dwa         | U= 878.5  p=0.000000  => DIFFERENT
  astar-dwa            vs dstar_lite-apf       | U=3774.0  p=0.000000  => DIFFERENT
  astar-dwa            vs dstar_lite-dwa       | U= 232.0  p=0.000000  => DIFFERENT
  astar-dwa            vs hybrid_astar-apf     | U= 706.5  p=0.000000  => DIFFERENT
  astar-dwa            vs hybrid_astar-dwa     | U= 269.5  p=0.000000  => DIFFERENT
  astar-dwa            vs rrt-apf              | U=16710.0  p=0.001093  => DIFFERENT
  astar-dwa            vs rrt-dwa              | U=6652.5  p=0.000000  => DIFFERENT
  dijkstra-apf         vs dijkstra-dwa         | U=2431.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs dstar_lite-apf       | U=4660.5  p=0.000002  => DIFFERENT
  dijkstra-apf         vs dstar_lite-dwa       | U=1716.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-apf     | U=2664.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-dwa     | U=1690.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs rrt-apf              | U=11158.5  p=0.241880  => similar
  dijkstra-apf         vs rrt-dwa              | U=7690.5  p=0.000223  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-apf       | U=6696.0  p=0.850757  => similar
  dijkstra-dwa         vs dstar_lite-dwa       | U=3322.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-apf     | U=4561.0  p=0.246552  => similar
  dijkstra-dwa         vs hybrid_astar-dwa     | U=3000.5  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs rrt-apf              | U=11798.5  p=0.609220  => similar
  dijkstra-dwa         vs rrt-dwa              | U=10121.0  p=0.615586  => similar
  dstar_lite-apf       vs dstar_lite-dwa       | U=6147.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-apf     | U=7576.5  p=0.149569  => similar
  dstar_lite-apf       vs hybrid_astar-dwa     | U=5786.5  p=0.000002  => DIFFERENT
  dstar_lite-apf       vs rrt-apf              | U=19890.0  p=0.487701  => similar
  dstar_lite-apf       vs rrt-dwa              | U=14904.0  p=0.140637  => similar
  dstar_lite-dwa       vs hybrid_astar-apf     | U=12474.5  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-dwa     | U=10953.0  p=0.014108  => DIFFERENT
  dstar_lite-dwa       vs rrt-apf              | U=25037.5  p=0.000083  => DIFFERENT
  dstar_lite-dwa       vs rrt-dwa              | U=20494.0  p=0.003980  => DIFFERENT
  hybrid_astar-apf     vs hybrid_astar-dwa     | U=4612.0  p=0.000155  => DIFFERENT
  hybrid_astar-apf     vs rrt-apf              | U=15450.5  p=0.167890  => similar
  hybrid_astar-apf     vs rrt-dwa              | U=13156.5  p=0.219415  => similar
  hybrid_astar-dwa     vs rrt-apf              | U=17256.5  p=0.006642  => DIFFERENT
  hybrid_astar-dwa     vs rrt-dwa              | U=14353.0  p=0.034821  => DIFFERENT
  rrt-apf              vs rrt-dwa              | U=21119.0  p=0.000016  => DIFFERENT

============================================================
  METRIC: Memory(MiB)
============================================================

--- Descriptive Statistics ---
                  count       mean       std    min      25%     50%      75%    max
Algorithm                                                                           
astar-apf         196.0  43.749949  2.635474  40.70  41.8825  42.555  45.3650  51.32
astar-dwa         163.0  45.563742  2.859902  41.18  43.4750  44.080  47.3800  52.39
dijkstra-apf       96.0  46.146458  2.483940  41.16  44.6525  46.280  47.9300  51.09
dijkstra-dwa       90.0  47.669667  2.708304  40.13  45.6500  47.700  50.1325  52.37
dstar_lite-apf    151.0  60.730596  1.683486  56.70  59.9300  61.040  61.9800  64.25
dstar_lite-dwa    161.0  62.574845  1.423413  58.37  61.7500  62.700  63.6600  65.96
hybrid_astar-apf  112.0  46.569643  3.046922  35.64  45.3975  45.880  46.6975  61.77
hybrid_astar-dwa  116.0  47.543276  2.010532  39.12  46.7350  47.205  48.0000  55.79
rrt-apf           253.0  40.722213  0.477488  36.33  40.5300  40.770  41.0200  41.40
rrt-dwa           217.0  42.342074  0.345389  40.51  42.1500  42.360  42.5700  43.11

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar-apf                                | Mean=43.7499  95% CI: [43.3891, 44.1322]
  astar-dwa                                | Mean=45.5637  95% CI: [45.1298, 46.0016]
  dijkstra-apf                             | Mean=46.1465  95% CI: [45.6525, 46.6468]
  dijkstra-dwa                             | Mean=47.6697  95% CI: [47.1180, 48.2314]
  dstar_lite-apf                           | Mean=60.7306  95% CI: [60.4562, 60.9914]
  dstar_lite-dwa                           | Mean=62.5748  95% CI: [62.3552, 62.7901]
  hybrid_astar-apf                         | Mean=46.5696  95% CI: [46.0269, 47.1567]
  hybrid_astar-dwa                         | Mean=47.5433  95% CI: [47.1703, 47.9114]
  rrt-apf                                  | Mean=40.7222  95% CI: [40.6592, 40.7769]
  rrt-dwa                                  | Mean=42.3421  95% CI: [42.2956, 42.3863]

=== Shapiro-Wilk Normality Test (Memory(MiB)) ===
H0: Data is normally distributed (p > 0.05)

  astar-apf                                | W=0.8302  p=0.000000  => NOT Normal
  astar-dwa                                | W=0.8423  p=0.000000  => NOT Normal
  dijkstra-apf                             | W=0.9744  p=0.056702  => Normal
  dijkstra-dwa                             | W=0.9756  p=0.087754  => Normal
  dstar_lite-apf                           | W=0.9278  p=0.000001  => NOT Normal
  dstar_lite-dwa                           | W=0.9543  p=0.000041  => NOT Normal
  hybrid_astar-apf                         | W=0.6979  p=0.000000  => NOT Normal
  hybrid_astar-dwa                         | W=0.8092  p=0.000000  => NOT Normal
  rrt-apf                                  | W=0.7458  p=0.000000  => NOT Normal
  rrt-dwa                                  | W=0.9621  p=0.000015  => NOT Normal

=== Kruskal-Wallis H-Test (Memory(MiB)) ===
  H=1324.1313  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Memory(MiB)) ---
  astar-apf            vs astar-dwa            | U=8404.0  p=0.000000  => DIFFERENT
  astar-apf            vs dijkstra-apf         | U=4458.0  p=0.000000  => DIFFERENT
  astar-apf            vs dijkstra-dwa         | U=2627.0  p=0.000000  => DIFFERENT
  astar-apf            vs dstar_lite-apf       | U=   0.0  p=0.000000  => DIFFERENT
  astar-apf            vs dstar_lite-dwa       | U=   0.0  p=0.000000  => DIFFERENT
  astar-apf            vs hybrid_astar-apf     | U=4384.0  p=0.000000  => DIFFERENT
  astar-apf            vs hybrid_astar-dwa     | U=3047.5  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-apf              | U=48923.0  p=0.000000  => DIFFERENT
  astar-apf            vs rrt-dwa              | U=24814.0  p=0.003404  => DIFFERENT
  astar-dwa            vs dijkstra-apf         | U=6348.0  p=0.011275  => DIFFERENT
  astar-dwa            vs dijkstra-dwa         | U=4112.0  p=0.000000  => DIFFERENT
  astar-dwa            vs dstar_lite-apf       | U=   0.0  p=0.000000  => DIFFERENT
  astar-dwa            vs dstar_lite-dwa       | U=   0.0  p=0.000000  => DIFFERENT
  astar-dwa            vs hybrid_astar-apf     | U=5908.5  p=0.000001  => DIFFERENT
  astar-dwa            vs hybrid_astar-dwa     | U=5046.5  p=0.000000  => DIFFERENT
  astar-dwa            vs rrt-apf              | U=41209.0  p=0.000000  => DIFFERENT
  astar-dwa            vs rrt-dwa              | U=34801.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs dijkstra-dwa         | U=2893.5  p=0.000102  => DIFFERENT
  dijkstra-apf         vs dstar_lite-apf       | U=   0.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs dstar_lite-dwa       | U=   0.0  p=0.000000  => DIFFERENT
  dijkstra-apf         vs hybrid_astar-apf     | U=5308.0  p=0.876045  => similar
  dijkstra-apf         vs hybrid_astar-dwa     | U=3365.0  p=0.000001  => DIFFERENT
  dijkstra-apf         vs rrt-apf              | U=24246.5  p=0.000000  => DIFFERENT
  dijkstra-apf         vs rrt-dwa              | U=19043.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-apf       | U=   0.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs dstar_lite-dwa       | U=   0.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-apf     | U=6606.0  p=0.000150  => DIFFERENT
  dijkstra-dwa         vs hybrid_astar-dwa     | U=5580.0  p=0.396911  => similar
  dijkstra-dwa         vs rrt-apf              | U=22527.0  p=0.000000  => DIFFERENT
  dijkstra-dwa         vs rrt-dwa              | U=19221.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs dstar_lite-dwa       | U=4568.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-apf     | U=16761.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs hybrid_astar-dwa     | U=17516.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-apf              | U=38203.0  p=0.000000  => DIFFERENT
  dstar_lite-apf       vs rrt-dwa              | U=32767.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-apf     | U=17985.5  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs hybrid_astar-dwa     | U=18676.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs rrt-apf              | U=40733.0  p=0.000000  => DIFFERENT
  dstar_lite-dwa       vs rrt-dwa              | U=34937.0  p=0.000000  => DIFFERENT
  hybrid_astar-apf     vs hybrid_astar-dwa     | U=2978.5  p=0.000000  => DIFFERENT
  hybrid_astar-apf     vs rrt-apf              | U=27833.0  p=0.000000  => DIFFERENT
  hybrid_astar-apf     vs rrt-dwa              | U=23870.0  p=0.000000  => DIFFERENT
  hybrid_astar-dwa     vs rrt-apf              | U=28853.5  p=0.000000  => DIFFERENT
  hybrid_astar-dwa     vs rrt-dwa              | U=24712.5  p=0.000000  => DIFFERENT
  rrt-apf              vs rrt-dwa              | U= 204.0  p=0.000000  => DIFFERENT

Found 1589 failure cases. Generating report: results/seed_15257/failure_report.txt
Failure report generated successfully.
