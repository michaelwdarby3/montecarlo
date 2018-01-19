# montecarlo
A simple implementation of monte carlo methods for flipping a coin, rolling a die, playing the lottery, and a simple 1-dimensional markov chain.

I built this implementation primarily for personal use, and experimentation with large datasets.

If the specified granularity, of up to 1/10000, is insufficient, change the PROB_RANGE value near the top of monte_carlo.py

On use, the outputfile will contain all samples, grouped by batches, with a trial on each line.  The analysisfile will contain data concerning the results, including the mode, number of trials, number of batches, and both the expected and actual means, variances, and standard deviations.

USAGE: python monte_carlo.py <mode> <trials> <batches> <outputfile> <analysisfile>
