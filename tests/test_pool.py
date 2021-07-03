from multiprocessing import Pool
import numpy
if __name__ == '__main__':
 pool = Pool()
 results = [pool.apply_async(numpy.sqrt, (x,))
 for x in range(100)]
 roots = [r.get() for r in results]
 print(roots)