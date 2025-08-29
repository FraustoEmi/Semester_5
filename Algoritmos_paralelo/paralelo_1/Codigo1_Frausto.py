import threading
import time
import random
import multiprocessing
import os
import concurrent.futures
import Codigo01a as CA
import Codigo01b as CB
import Codigo01c as CC


def main():
    salonA = CA.main_threading()
    salonB = CB.main_multiprocessing()
    salonC = CC.main_concurrent_futures()
    return salonA, salonB, salonC
    
if __name__ == '__main__':
    salonA, salonB, salonC = main()
    for i in salonA:
        print(i)
    for i in salonB:
        print(i)
    for i in salonC:
        print(i)