import math
import ray
from dask.distributed import Client
from joblib import Parallel, delayed
from mpire import WorkerPool
from timeit import default_timer as timer

def some_function(x: float, y: float, z: float) -> float:
    return (x * y)**2 / math.sqrt(abs(z+0.0625))

from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool

def main():
    data = [(x, y, z) for x, y, z in zip(range(1, 10000), range(42, 420000), range(23, 230000))]

    # Serial processing
    start = timer()
    results = [some_function(x, y, z) for x, y, z in data]
    end = timer()
    print(f"Serial time: {(end-start):.4f}")

    # Multiprocessing
    start = timer()
    with Pool(processes=5) as pool:
        results = pool.starmap(some_function, data)
    end = timer()
    print(f"Multiprocessing time: {(end-start):.4f}")

    # MPIRE
    start = timer()
    with WorkerPool(n_jobs=5) as pool:
        results = pool.map(some_function, data)
    end = timer()
    print(f"MPIRE time: {(end-start):.4f}")

    # Joblib
    start = timer()
    results = Parallel(n_jobs=5)(delayed(some_function)(x, y, z) for x, y, z in data)
    end = timer()
    print(f"Joblib time: {(end-start):.4f}")

    # ProcessPoolExecutor
    start = timer()
    with ProcessPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(some_function, x, y, z) for x, y, z in data]
        results = [future.result() for future in as_completed(futures)]
    end = timer()
    print(f"ProcessPoolExecutor time: {(end-start):.4f}")

    # Dask
    start = timer()
    client = Client(n_workers=5)
    results = client.gather([client.submit(some_function, x, y, z) for x, y, z in data])
    client.close()
    end = timer()
    print(f"Dask time: {(end-start):.4f}")

    # Ray
    start = timer()
    ray.init(num_cpus=5)
    remote_function = ray.remote(some_function)
    results = ray.get([remote_function.remote(x, y, z) for x, y, z in data])
    ray.shutdown()
    end = timer()
    print(f"Ray time: {(end-start):.4f}")



if __name__ == "__main__":
    main()