import operator
import os
import random
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import reduce
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from timeit import default_timer as timer

import ray
from dask import compute, delayed
from joblib import Parallel, delayed
from mpire import WorkerPool


def seq_pi(npts):
    inside_pts = 0

    # Total Random numbers generated = x_values * y_values
    for _ in range(npts):

        # Randomly generated x and y values from a uniform distribution
        # Range of x and y values is -1 to 1
        rand_x = random.uniform(-1, 1)
        rand_y = random.uniform(-1, 1)

        # Distance between (x, y) from the origin
        d = rand_x**2 + rand_y**2

        # Checking if (x, y) lies inside the circle
        if d <= 1:
            inside_pts += 1

        # Estimating value of pi,
        # pi= 4*(no. of points generated inside the
        # circle) / (no. of points generated inside the square)
    pi = 4 * inside_pts / npts

    return pi


def map_pi(r):
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-1, 1)
    return int(rand_x**2 + rand_y**2 <= 1)


@delayed
def delayed_pi(r):
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-1, 1)
    return int(rand_x**2 + rand_y**2 <= 1)


def main():
    # number of points generated
    npts = 2**19

    # sequence for map function
    r = range(npts)

    # use all threads avail
    nthreads = os.cpu_count()

    # classical single threaded function
    start = timer()
    pi = seq_pi(npts)
    end = timer()
    print(f"sequential pi estimation = {pi}")
    print(f"seq. time = {end-start:.7f}\n")

    # single threaded map function
    start = timer()
    results = map(map_pi, r)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"sequential pi estimation (map) = {pi}")
    print(f"map. time = {end-start:.7f}\n")

    # joblib with manual optimization
    start = timer()
    results = Parallel(n_jobs=nthreads,
                       batch_size=1024*nthreads,
                       prefer='threads'
                       )(delayed(map_pi)(r) for r in range(npts))
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (joblib - opt) = {pi}")
    print(f"opt joblib time = {end-start:.7f}\n")

    # joblib auto backend and chunksize
    start = timer()
    results = Parallel(n_jobs=nthreads
                       )(delayed(map_pi)(r) for r in range(npts))
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (joblib) = {pi}")
    print(f"joblib time = {end-start:.7f}\n")

    # multiprocessing Pool map
    start = timer()
    with Pool(processes=nthreads) as pool:
        results = pool.map(map_pi, r, chunksize=1024*nthreads)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (ProcessPool map) = {pi}")
    print(f"ProcessPool map time = {end-start:.7f}\n")

    # multiprocessing ThreadPool map
    start = timer()
    with ThreadPool(processes=nthreads) as pool:
        results = pool.map(map_pi, r, chunksize=1024*nthreads)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (ThreadPool map) = {pi}")
    print(f"ThreadPool map time = {end-start:.7f}\n")

    # ThreadPoolExecutor
    start = timer()
    with ThreadPoolExecutor(nthreads) as pool:
        results = pool.map(map_pi, r, chunksize=1024*nthreads)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (ThreadPoolExecutor) = {pi}")
    print(f"ThreadPoolExecutor time = {end-start:.7f}\n")

    # ProcessPoolExecutor
    start = timer()
    with ProcessPoolExecutor(nthreads) as pool:
        results = pool.map(map_pi, r, chunksize=1024*nthreads)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (ProcessPoolExecutor) = {pi}")
    print(f"ProcessPoolExecutor time = {end-start:.7f}\n")

    # mpire
    start = timer()
    with WorkerPool(n_jobs=nthreads) as pool:
        results = pool.map(map_pi, r)
    pi = 4 * reduce(operator.add, results) / npts
    end = timer()
    print(f"parallel pi estimation (mpire) = {pi}")
    print(f"mpire map time = {end-start:.7f}\n")

    # Dask
    #start = timer()
    #l = []
    # for r in range(npts):
    #    l.append(delayed_pi(r))
    #results = compute(*l)
    #pi = 4 * reduce(operator.add, results) / npts
    #end = timer()
    #print(f"parallel pi estimation (dask) = {pi}")
    #print(f"Dask time: {(end-start):.7f}")

    # Ray
    # start = timer()
    # ray.init(num_cpus=nthreads)
    # remote_function = ray.remote(map_pi)
    # results = ray.get([remote_function.remote(r) for r in range(npts)])
    # ray.shutdown()
    # pi = 4 * reduce(operator.add, results) / npts
    # end = timer()
    # print(f"parallel pi estimation (ray) = {pi}")
    # print(f"Ray time: {(end-start):.7f}")


if __name__ == "__main__":
    main()
