import json
import time
import urllib.request

from threading import Thread, Lock


class Colors:
    RESET = "\033[0m"
    PURPLE = "\033[0;35m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"


class FetcherThread(Thread):

    # Class attribute.
    counter = {key: 0 for key in "abcdefghijklmnopqrstuvwxyz"}
    global_counter = {"counter": 0, "all": 0}
    # Control concurrent access to shared class attribute.
    # https://docs.python.org/3/library/threading.html?highlight=lock#threading.Lock
    counter_lock = Lock()

    def __init__(self, url):
        super().__init__()  # Initialize base class.
        self.url = url

    def run(self):
        print('{0}Starting Thread: {1} {2}'.format(
            Colors.PURPLE, self.name, Colors.RESET))
        response = urllib.request.urlopen(self.url)
        txt = str(response.read())
        for l in txt:
            letter = l.lower()
            with self.counter_lock:
                self.global_counter['all'] += 1
                if letter in self.counter:
                    self.counter[letter] += 1
                    self.global_counter['counter'] += 1

        print('{0}Execution of Thread: {1} is complete!{2}'.format(
            Colors.GREEN, self.name, Colors.RESET))


def main(code):
    ''' Create and start worker threads, then wait for them all to finish. '''
    n_threads = 20
    workers = [FetcherThread(
        url=f"https://www.rfc-editor.org/rfc/rfc{i}.txt") for i in range(code, code + n_threads)]

    for worker in workers:
        worker.start()

    # Wait for all treads to finish.
    start = time.time()
    for worker in workers:
        worker.join()
    end = time.time()
    print("\n{}Done, time taken: {}{}".format(
        Colors.YELLOW, end - start, Colors.RESET))


if __name__ == '__main__':

    import builtins
    import matplotlib.pyplot as plt

    def print(*args, **kwargs):
        ''' Redefine print to prevent concurrent printing. '''
        with print.lock:
            builtins.print(*args, **kwargs)

    print.lock = Lock()  # Function attribute.

    code = 1000  # 7813
    main(code)
    print()
    print('{0}Threads execution is complete!{1}'.format(
        Colors.GREEN, Colors.RESET))
    print('Final counter value:', json.dumps(FetcherThread.counter, indent=4))
    print('Total characters: ', FetcherThread.global_counter)
    # Data to plot
    labels = []
    sizes = []

    for x, y in FetcherThread.counter.items():
        labels.append(x)
        sizes.append(y)

    # Plot
    plt.pie(sizes,labels=labels, startangle=90, autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)

    plt.axis('equal')
    plt.show()
