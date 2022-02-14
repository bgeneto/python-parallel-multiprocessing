# python-parallel-multiprocessing
Test python multiprocessing libraries performance under Linux and Windows
Parallel processing with Python 3 is very tricky.

| OS         | seq. time | map. time | opt joblib | auto joblib | ProcessPool | ThreadPool | ThreadPoolExecutor | ProcessPoolExecutor | mpire     |
|------------|-----------|-----------|------------|-------------|-------------|------------|--------------------|---------------------|-----------|
| Linux 5.15 | 0.2754851 | 0.3158627 | 1.3803515  | 1.6456630   | 0.1508692   | 0.3681457  | 18.8981458         | 0.2698220           | 1.5323328 |
| Windows 11 | 0.2727147 | 0.3233928 | 1.2181586  | 1.6349657   | 1.0570806   | 0.3281467  | 15.1203394         | 1.2328661           | 5.1917256 |

**Conclusion:** use process with Linux and threads with Windows.
