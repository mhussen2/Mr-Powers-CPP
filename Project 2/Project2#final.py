import multiprocessing
import threading
import asyncio
import time
from math import factorial

def is_prime(n):
  if n < 2:
    return False
  for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
      return False
  return True

def search_primes(start):
  num = start
  largest = None
  t_end = time.time() + 180

  while time.time() < t_end:
    if is_prime(num):
      largest = num
    num += 1

  return largest

def get_fib(n):
  a = 0
  b = 1
  for i in range(n):
    a, b = b, a + b
  return a

async def get_fact(n):
  return factorial(n)

def save_to_file(text):
  with open("results.txt", "a") as file:
    file.write(text + "\n")

if __name__ == '__main__':
  print("== Prime Finder ==")

  try:
    start_point = int(input("Start number (e.g. 0): "))
  except:
    print("Invalid input, using 0")
    start_point = 0

  print("Searching for the biggest prime... (3 mins max)")
  start_time = time.time()

  with multiprocessing.Pool(1) as pool:
    result = pool.apply(search_primes, args=(start_point,))

  end_time = time.time()
  duration = round(end_time - start_time, 2)

  if result:
    print("Found prime:", result)
    print(f"Search time: {duration} seconds")
    save_to_file(f"Prime found from {start_point}: {result} in {duration}s")
  else:
    print("No prime found.")
    exit()

  print("\nPick calculation:")
  print("1. Fibonacci")
  print("2. Factorial")
  print("3. Both")
  choice = input("Your choice: ").strip()

  def fib_thread():
    f = get_fib(result)
    print(f"Fibonacci of {result} = {f}")
    save_to_file(f"Fibonacci({result}) = {f}")

  if choice == "1":
    t = threading.Thread(target=fib_thread)
    t.start()
    t.join()
  elif choice == "2":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fact = loop.run_until_complete(get_fact(result))
    print(f"Factorial of {result} = {fact}")
    save_to_file(f"Factorial({result}) = {fact}")
  elif choice == "3":
    t = threading.Thread(target=fib_thread)
    t.start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fact = loop.run_until_complete(get_fact(result))
    print(f"Factorial of {result} = {fact}")
    save_to_file(f"Factorial({result}) = {fact}")
    t.join()
  else:
    print("Invalid option.")
