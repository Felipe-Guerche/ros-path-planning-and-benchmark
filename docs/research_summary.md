Analyzing single file: results/seed_15257/merges/final_summary_seed_15257.csv

============================================================
  SUCCESS RATES (grouped by Config_Tag)
============================================================

  astar                                    | 513/763 =  67.2%  CI: [63.8%, 70.5%]
  dijkstra                                 | 346/512 =  67.6%  CI: [63.4%, 71.5%]
  dstar_lite                               | 312/557 =  56.0%  CI: [51.9%, 60.1%]
  hybrid_astar                             | 249/960 =  25.9%  CI: [23.3%, 28.8%]
  lazy_theta_star                          | 153/960 =  15.9%  CI: [13.8%, 18.4%]
  rrt                                      | 470/853 =  55.1%  CI: [51.7%, 58.4%]

Successful runs: 2043 / 4605

============================================================
  METRIC: Time(s)
============================================================

--- Descriptive Statistics ---
                 count       mean        std      min        25%       50%        75%       max
Config_Tag                                                                                     
astar            513.0  52.023520  30.905365  11.0882  30.803400  45.01800  64.121500  174.8057
dijkstra         346.0  49.040466  28.879206  11.0915  29.755325  42.83370  59.776650  166.4947
dstar_lite       312.0  50.261006  31.220874  11.0283  29.886450  41.54295  62.241150  176.2191
hybrid_astar     249.0  64.253288  33.785633  17.6130  39.588900  56.09290  76.458900  177.7670
lazy_theta_star  153.0  59.193360  27.796715  19.6873  40.573700  53.82850  67.582300  155.2580
rrt              470.0  54.607325  28.001872  13.0131  32.911050  49.20525  71.455425  166.3584

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar                                    | Mean=52.0235  95% CI: [49.4487, 54.7401]
  dijkstra                                 | Mean=49.0405  95% CI: [46.0586, 52.1307]
  dstar_lite                               | Mean=50.2610  95% CI: [46.8378, 53.8264]
  hybrid_astar                             | Mean=64.2533  95% CI: [60.1912, 68.6073]
  lazy_theta_star                          | Mean=59.1934  95% CI: [55.0127, 63.7608]
  rrt                                      | Mean=54.6073  95% CI: [52.1273, 57.1580]

=== Shapiro-Wilk Normality Test (Time(s)) ===
H0: Data is normally distributed (p > 0.05)

  astar                                    | W=0.8541  p=0.000000  => NOT Normal
  dijkstra                                 | W=0.8422  p=0.000000  => NOT Normal
  dstar_lite                               | W=0.8394  p=0.000000  => NOT Normal
  hybrid_astar                             | W=0.8829  p=0.000000  => NOT Normal
  lazy_theta_star                          | W=0.8792  p=0.000000  => NOT Normal
  rrt                                      | W=0.9367  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Time(s)) ===
  H=68.7441  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Time(s)) ---
  astar                vs dijkstra             | U=93455.5  p=0.187015  => similar
  astar                vs dstar_lite           | U=83472.0  p=0.299529  => similar
  astar                vs hybrid_astar         | U=47556.0  p=0.000000  => DIFFERENT
  astar                vs lazy_theta_star      | U=30990.0  p=0.000078  => DIFFERENT
  astar                vs rrt                  | U=109741.0  p=0.015018  => DIFFERENT
  dijkstra             vs dstar_lite           | U=53455.0  p=0.830724  => similar
  dijkstra             vs hybrid_astar         | U=29500.0  p=0.000000  => DIFFERENT
  dijkstra             vs lazy_theta_star      | U=19224.0  p=0.000001  => DIFFERENT
  dijkstra             vs rrt                  | U=69394.0  p=0.000342  => DIFFERENT
  dstar_lite           vs hybrid_astar         | U=27336.5  p=0.000000  => DIFFERENT
  dstar_lite           vs lazy_theta_star      | U=17856.0  p=0.000010  => DIFFERENT
  dstar_lite           vs rrt                  | U=63588.0  p=0.001655  => DIFFERENT
  hybrid_astar         vs lazy_theta_star      | U=20336.0  p=0.255198  => similar
  hybrid_astar         vs rrt                  | U=67799.0  p=0.000459  => DIFFERENT
  lazy_theta_star      vs rrt                  | U=39648.0  p=0.056195  => similar

============================================================
  METRIC: Distance(m)
============================================================

--- Descriptive Statistics ---
                 count       mean        std     min        25%       50%        75%      max
Config_Tag                                                                                   
astar            513.0  15.941921   7.149325  5.2389  10.467400  14.60400  19.902900  45.5061
dijkstra         346.0  16.102367   7.440617  5.2246  10.545650  14.72745  19.865125  48.6708
dstar_lite       312.0  15.500370   6.919420  5.0079  10.363375  14.55485  18.785475  51.5627
hybrid_astar     249.0  16.270011   7.148991  5.3050  10.987200  15.30280  19.924800  40.2343
lazy_theta_star  153.0  15.381531   6.390071  5.3561  10.975600  14.46170  18.470800  38.5971
rrt              470.0  19.867153  10.377635  5.2151  11.739200  17.87200  24.922875  72.3356

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar                                    | Mean=15.9419  95% CI: [15.3197, 16.5566]
  dijkstra                                 | Mean=16.1024  95% CI: [15.3194, 16.8855]
  dstar_lite                               | Mean=15.5004  95% CI: [14.7319, 16.2834]
  hybrid_astar                             | Mean=16.2700  95% CI: [15.3961, 17.1525]
  lazy_theta_star                          | Mean=15.3815  95% CI: [14.3891, 16.3801]
  rrt                                      | Mean=19.8672  95% CI: [18.9602, 20.8161]

=== Shapiro-Wilk Normality Test (Distance(m)) ===
H0: Data is normally distributed (p > 0.05)

  astar                                    | W=0.9373  p=0.000000  => NOT Normal
  dijkstra                                 | W=0.9262  p=0.000000  => NOT Normal
  dstar_lite                               | W=0.9280  p=0.000000  => NOT Normal
  hybrid_astar                             | W=0.9373  p=0.000000  => NOT Normal
  lazy_theta_star                          | W=0.9454  p=0.000012  => NOT Normal
  rrt                                      | W=0.9266  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Distance(m)) ===
  H=52.7617  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Distance(m)) ---
  astar                vs dijkstra             | U=88147.5  p=0.866184  => similar
  astar                vs dstar_lite           | U=82353.5  p=0.483636  => similar
  astar                vs hybrid_astar         | U=61888.0  p=0.487205  => similar
  astar                vs lazy_theta_star      | U=40456.0  p=0.562059  => similar
  astar                vs rrt                  | U=94797.5  p=0.000000  => DIFFERENT
  dijkstra             vs dstar_lite           | U=55869.0  p=0.437003  => similar
  dijkstra             vs hybrid_astar         | U=41990.0  p=0.599415  => similar
  dijkstra             vs lazy_theta_star      | U=27471.0  p=0.500101  => similar
  dijkstra             vs rrt                  | U=64585.0  p=0.000001  => DIFFERENT
  dstar_lite           vs hybrid_astar         | U=36435.0  p=0.206705  => similar
  dstar_lite           vs lazy_theta_star      | U=23963.0  p=0.944665  => similar
  dstar_lite           vs rrt                  | U=55563.0  p=0.000000  => DIFFERENT
  hybrid_astar         vs lazy_theta_star      | U=20257.0  p=0.285533  => similar
  hybrid_astar         vs rrt                  | U=47482.5  p=0.000031  => DIFFERENT
  lazy_theta_star      vs rrt                  | U=27216.5  p=0.000006  => DIFFERENT

============================================================
  METRIC: Smoothness(rad)
============================================================

--- Descriptive Statistics ---
                 count       mean         std     min       25%       50%       75%        max
Config_Tag                                                                                    
astar            513.0  51.207123  123.956559  2.3951  13.97320  23.31960  41.21190  1256.4033
dijkstra         346.0  46.762423  105.162564  2.6532  14.45870  23.00860  39.75940   875.8406
dstar_lite       312.0  56.458873  146.808078  2.5204  11.30810  19.82930  38.66215  1366.5517
hybrid_astar     249.0  38.842984   49.997724  2.8936  13.95040  28.65950  47.06680   537.1284
lazy_theta_star  153.0  42.466780   73.174443  3.6925  13.97590  24.33470  42.35120   611.5258
rrt              470.0  49.731980   39.174889  3.4433  23.27845  39.16645  65.75355   292.2096

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar                                    | Mean=51.2071  95% CI: [41.2565, 62.6837]
  dijkstra                                 | Mean=46.7624  95% CI: [36.6160, 58.6273]
  dstar_lite                               | Mean=56.4589  95% CI: [41.5856, 74.1715]
  hybrid_astar                             | Mean=38.8430  95% CI: [33.3297, 45.6575]
  lazy_theta_star                          | Mean=42.4668  95% CI: [32.2532, 54.9187]
  rrt                                      | Mean=49.7320  95% CI: [46.2086, 53.3526]

=== Shapiro-Wilk Normality Test (Smoothness(rad)) ===
H0: Data is normally distributed (p > 0.05)

  astar                                    | W=0.3076  p=0.000000  => NOT Normal
  dijkstra                                 | W=0.3210  p=0.000000  => NOT Normal
  dstar_lite                               | W=0.3305  p=0.000000  => NOT Normal
  hybrid_astar                             | W=0.5093  p=0.000000  => NOT Normal
  lazy_theta_star                          | W=0.4202  p=0.000000  => NOT Normal
  rrt                                      | W=0.8125  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Smoothness(rad)) ===
  H=125.9917  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Smoothness(rad)) ---
  astar                vs dijkstra             | U=89827.0  p=0.762570  => similar
  astar                vs dstar_lite           | U=87944.0  p=0.017091  => DIFFERENT
  astar                vs hybrid_astar         | U=59869.0  p=0.160555  => similar
  astar                vs lazy_theta_star      | U=38878.0  p=0.860900  => similar
  astar                vs rrt                  | U=82103.0  p=0.000000  => DIFFERENT
  dijkstra             vs dstar_lite           | U=58858.0  p=0.044977  => DIFFERENT
  dijkstra             vs hybrid_astar         | U=39693.0  p=0.101908  => similar
  dijkstra             vs lazy_theta_star      | U=25905.5  p=0.704629  => similar
  dijkstra             vs rrt                  | U=53545.0  p=0.000000  => DIFFERENT
  dstar_lite           vs hybrid_astar         | U=33014.5  p=0.002244  => DIFFERENT
  dstar_lite           vs lazy_theta_star      | U=21309.0  p=0.060225  => similar
  dstar_lite           vs rrt                  | U=45173.0  p=0.000000  => DIFFERENT
  hybrid_astar         vs lazy_theta_star      | U=20120.0  p=0.343714  => similar
  hybrid_astar         vs rrt                  | U=43342.0  p=0.000000  => DIFFERENT
  lazy_theta_star      vs rrt                  | U=24693.0  p=0.000000  => DIFFERENT

============================================================
  METRIC: CPU(%)
============================================================

--- Descriptive Statistics ---
                 count       mean        std    min      25%     50%      75%     max
Config_Tag                                                                           
astar            513.0  18.130604   8.405990   5.77  10.6900  18.070  23.5000   62.62
dijkstra         346.0  38.240173  15.314017  10.08  27.5650  36.565  48.0150   83.95
dstar_lite       312.0  48.845417  17.301343  14.29  36.3850  48.140  61.9275  104.22
hybrid_astar     249.0  26.461446  12.019722   7.74  21.3100  22.730  25.9800   84.71
lazy_theta_star  153.0  26.855359  11.446584   9.50  21.4800  23.340  26.5800   88.07
rrt              470.0  49.080532  35.479622   7.14  21.4075  36.095  80.9175  120.70

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar                                    | Mean=18.1306  95% CI: [17.4222, 18.8781]
  dijkstra                                 | Mean=38.2402  95% CI: [36.6409, 39.8426]
  dstar_lite                               | Mean=48.8454  95% CI: [46.9268, 50.7321]
  hybrid_astar                             | Mean=26.4614  95% CI: [25.0280, 28.0074]
  lazy_theta_star                          | Mean=26.8554  95% CI: [25.1647, 28.7621]
  rrt                                      | Mean=49.0805  95% CI: [45.8783, 52.3554]

=== Shapiro-Wilk Normality Test (CPU(%)) ===
H0: Data is normally distributed (p > 0.05)

  astar                                    | W=0.9244  p=0.000000  => NOT Normal
  dijkstra                                 | W=0.9736  p=0.000006  => NOT Normal
  dstar_lite                               | W=0.9907  p=0.045269  => NOT Normal
  hybrid_astar                             | W=0.6707  p=0.000000  => NOT Normal
  lazy_theta_star                          | W=0.6095  p=0.000000  => NOT Normal
  rrt                                      | W=0.8899  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (CPU(%)) ===
  H=666.0422  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (CPU(%)) ---
  astar                vs dijkstra             | U=19992.5  p=0.000000  => DIFFERENT
  astar                vs dstar_lite           | U=8765.5  p=0.000000  => DIFFERENT
  astar                vs hybrid_astar         | U=34975.5  p=0.000000  => DIFFERENT
  astar                vs lazy_theta_star      | U=19631.0  p=0.000000  => DIFFERENT
  astar                vs rrt                  | U=60140.0  p=0.000000  => DIFFERENT
  dijkstra             vs dstar_lite           | U=34632.0  p=0.000000  => DIFFERENT
  dijkstra             vs hybrid_astar         | U=65763.5  p=0.000000  => DIFFERENT
  dijkstra             vs lazy_theta_star      | U=40230.0  p=0.000000  => DIFFERENT
  dijkstra             vs rrt                  | U=77796.0  p=0.291003  => similar
  dstar_lite           vs hybrid_astar         | U=66949.5  p=0.000000  => DIFFERENT
  dstar_lite           vs lazy_theta_star      | U=41129.0  p=0.000000  => DIFFERENT
  dstar_lite           vs rrt                  | U=80325.5  p=0.023537  => DIFFERENT
  hybrid_astar         vs lazy_theta_star      | U=17704.5  p=0.234924  => similar
  hybrid_astar         vs rrt                  | U=39739.5  p=0.000000  => DIFFERENT
  lazy_theta_star      vs rrt                  | U=25155.5  p=0.000000  => DIFFERENT

============================================================
  METRIC: Memory(MiB)
============================================================

--- Descriptive Statistics ---
                 count       mean        std    min      25%     50%      75%     max
Config_Tag                                                                           
astar            513.0  44.305712   2.795338  40.62  42.3600  43.410  45.6100   52.39
dijkstra         346.0  46.740318   2.785544  40.13  44.8350  46.760  48.7725   52.93
dstar_lite       312.0  61.682276   1.805957  56.70  60.8175  61.905  62.8850   65.96
hybrid_astar     249.0  47.399639  20.043299  22.14  41.5800  42.230  44.0000  178.86
lazy_theta_star  153.0  49.337059  23.731076  21.36  41.7100  42.320  44.1800  181.10
rrt              470.0  41.470106   0.911578  36.33  40.7400  41.230  42.3175   43.11

--- 95% Bootstrap Confidence Intervals (Mean) ---
  astar                                    | Mean=44.3057  95% CI: [44.0672, 44.5422]
  dijkstra                                 | Mean=46.7403  95% CI: [46.4494, 47.0385]
  dstar_lite                               | Mean=61.6823  95% CI: [61.4793, 61.8744]
  hybrid_astar                             | Mean=47.3996  95% CI: [45.0779, 50.0699]
  lazy_theta_star                          | Mean=49.3371  95% CI: [45.8923, 53.3041]
  rrt                                      | Mean=41.4701  95% CI: [41.3862, 41.5512]

=== Shapiro-Wilk Normality Test (Memory(MiB)) ===
H0: Data is normally distributed (p > 0.05)

  astar                                    | W=0.8701  p=0.000000  => NOT Normal
  dijkstra                                 | W=0.9843  p=0.000811  => NOT Normal
  dstar_lite                               | W=0.9604  p=0.000000  => NOT Normal
  hybrid_astar                             | W=0.4474  p=0.000000  => NOT Normal
  lazy_theta_star                          | W=0.4628  p=0.000000  => NOT Normal
  rrt                                      | W=0.9163  p=0.000000  => NOT Normal

=== Kruskal-Wallis H-Test (Memory(MiB)) ===
  H=1236.1947  p=0.000000
  => Statistically significant difference between groups.

  --- Pairwise Mann-Whitney U (Memory(MiB)) ---
  astar                vs dijkstra             | U=44777.5  p=0.000000  => DIFFERENT
  astar                vs dstar_lite           | U=   0.0  p=0.000000  => DIFFERENT
  astar                vs hybrid_astar         | U=82416.0  p=0.000000  => DIFFERENT
  astar                vs lazy_theta_star      | U=49933.0  p=0.000000  => DIFFERENT
  astar                vs rrt                  | U=210752.0  p=0.000000  => DIFFERENT
  dijkstra             vs dstar_lite           | U=   0.0  p=0.000000  => DIFFERENT
  dijkstra             vs hybrid_astar         | U=69159.5  p=0.000000  => DIFFERENT
  dijkstra             vs lazy_theta_star      | U=42340.5  p=0.000000  => DIFFERENT
  dijkstra             vs rrt                  | U=157714.0  p=0.000000  => DIFFERENT
  dstar_lite           vs hybrid_astar         | U=70313.0  p=0.000000  => DIFFERENT
  dstar_lite           vs lazy_theta_star      | U=42688.0  p=0.000000  => DIFFERENT
  dstar_lite           vs rrt                  | U=146640.0  p=0.000000  => DIFFERENT
  hybrid_astar         vs lazy_theta_star      | U=18525.0  p=0.643809  => similar
  hybrid_astar         vs rrt                  | U=82828.5  p=0.000000  => DIFFERENT
  lazy_theta_star      vs rrt                  | U=51936.0  p=0.000000  => DIFFERENT

Found 2562 failure cases. Generating report: /home/felipe/github/ros_motion_planning-master/results/seed_15257/merges/failure_report.txt
Failure report generated successfully.
