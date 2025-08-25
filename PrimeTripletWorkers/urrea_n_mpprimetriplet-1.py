# Name: Nicolas Urrea
# Date: October 14, 2024
# Assignment: Assignment 3
# Due Date: October 14, 2024, 11:59 PM
# About this project: This program finds the smallest prime triplet starting from a number the user gives. It checks for prime numbers and looks for three in a row with the right gaps.
# Assumptions: Pretty much assuming the user is putting in a valid number.
# All work below was performed solely by Nicolas Urrea.
# Execution times for N=1,000,000,000,000 with 1, 2, 4, 8, 16 workers:
# 1 worker: 3.54 seconds
# 2 workers: 1.99 seconds
# 4 workers: 1.38 seconds
# 8 workers: 0.86 seconds

# Execution times for N=3,000,000,000,000 with 1, 2, 4, 8, 16 workers:
# 1 worker: 4.66 seconds
# 2 workers: 3.08 seconds
# 4 workers: 2.28 seconds
# 8 workers: 1.31 seconds

import sys
import math
import time
from multiprocessing import Process, Queue, cpu_count


def sieve_of_eratosthenes(limit):
    """Generate a list of primes up to the given limit using the Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [x for x in range(limit + 1) if is_prime[x]]


def is_prime(n, small_primes):
    """Check if a number is prime using precomputed small primes."""
    if n < 2:
        return False
    for prime in small_primes:
        if prime * prime > n:
            break
        if n % prime == 0:
            return False
    return True


def find_primes_in_range(start, end, small_primes, result_queue):
    """Worker function to find all primes in a given range."""
    primes = [x for x in range(start, end) if is_prime(x, small_primes)]
    result_queue.put(primes)


def find_prime_triplet(primes):
    """Check for a prime triplet in a sorted list of primes."""
    for i in range(len(primes) - 2):
        if primes[i + 2] - primes[i] == 6:
            return primes[i], primes[i + 1], primes[i + 2]
    return None


def main():
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 urrea_n_mpprimetriplet.py <workers>")
        sys.exit(1)

    try:
        nprocs = int(sys.argv[1])
        if nprocs < 1:
            raise ValueError
    except ValueError:
        print("Error: Number of workers must be a positive integer.")
        sys.exit(1)

    # Dynamically limit workers to system capacity
    max_workers = min(nprocs, cpu_count())
    if nprocs > max_workers:
        print(f"Limiting workers to {max_workers} (system capacity).")
        nprocs = max_workers

    try:
        number = int(input("Enter an integer: "))
    except ValueError:
        print("Error: Input must be an integer.")
        sys.exit(1)

    if number < 2:
        number = 2

    print(f"Finding prime triplet starting from {number} using {nprocs} worker(s)...")

    # Start time measurement
    start_time = time.time()

    # Precompute small primes
    largest_prime_needed = int(math.sqrt(number + 100000)) + 1
    small_primes = sieve_of_eratosthenes(largest_prime_needed)

    # Initialize search variables
    cur = number
    chunk_size = 1000  # Size of each chunk to be processed by workers

    result_queue = Queue()

    while True:
        # Assign ranges to workers
        processes = []
        for i in range(nprocs):
            start = cur + i * chunk_size
            end = start + chunk_size
            p = Process(target=find_primes_in_range, args=(start, end, small_primes, result_queue))
            processes.append(p)
            p.start()

        # Collect results from workers
        all_primes = []
        for _ in range(nprocs):
            all_primes.extend(result_queue.get())

        # Terminate all worker processes
        for p in processes:
            p.join()

        # Sort the primes found in this chunk
        all_primes.sort()

        # Check for a prime triplet
        triplet = find_prime_triplet(all_primes)
        if triplet:
            print(f"Smallest prime triplet: {triplet}")
            break

        # Move to the next chunk
        cur += nprocs * chunk_size

    print(f"Execution time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
