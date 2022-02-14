# python-parallel-multiprocessing

Test python parallel libraries performance under Linux and Windows 
by calculating the Pi value via Monte Carlo algorithm. 

(Parallel processing with Python 3 is generally very tricky)

|                     | Linux 5.10 | Windows 11 |
|---------------------|------------|------------|
| seq. time           | 0.2754851  | 0.2727147  |
| map. time           | 0.3158627  | 0.3233928  |
| opt joblib          | 1.3803515  | 1.2181586  |
| auto joblib         | 1.6456630  | 1.6349657  |
| ProcessPool         | 0.1508692  | 1.0570806  |
| ThreadPool          | 0.3681457  | 0.3281467  |
| ThreadPoolExecutor  | 18.8981458 | 15.1203394 |
| ProcessPoolExecutor | 0.2698220  | 1.2328661  |
| mpire               | 1.5323328  | 5.1917256  |

For such small task, ThreadPool is better in Windows and ProcessPool in faster in Linux.

**Conclusion:** use process backend with Linux and threads backend with Windows.
