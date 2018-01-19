import math, sys, random

# If you'd like to change the granularity of the probability ranges, change only this value.  
# This value determines that the lowest "granularity" is currently 1/10000, or 0.0001.
# If it were replaced by 5000, the lowest granularity would be 1/5000, or 0.0002.
PROB_RANGE = 10000

# This value represents the megaball for MegaMillions mode, determining the range, between 1 and MEGABALL, of the final slot in that mode.
MEGABALL = 25

# All modes MUST be listed here.  If more are needed, add them here.  Additional mode groups can be added, following the example of the lottery_modes.
# "D_" represents any dice-rolling mode.
supported_modes = ["CoinFlip", "D_", "LocalTriple", "Take5", "MegaMillions", "MarkovStep"]
lottery_modes = ["LocalTriple", "Take5", "MegaMillions"]



if len(sys.argv) < 6:
	print "usage: python monte_carlo.py <mode> <trials> <batches> <outputfile> <analysisfile>"
	sys.exit()

mode = sys.argv[1]
trials = int(sys.argv[2])
batches = int(sys.argv[3])
output_file = sys.argv[4]
analsys_file = sys.argv[5]

if mode not in supported_modes:
	if (mode[0] != "D") or not (mode[1:].isdigit()):
		print "Supported modes are CoinFlip, Dice, LocalTriple, Take5, MegaMillions"
		sys.exit()

# This section of code takes in your preferred starting probability, increase in probability after a success, and decrease in probability after a failure.
# All input is divided by the PROB_RANGE to actually develop the probabilities desired.  For instance, if PROB_RANGE = 10000, and startProb = 5000, then 
# the actual likelihood of the event is 1/2.
if mode == "MarkovStep":
	startProb = int(input("Define the starting probability, as an integer between 0 and " + str(PROB_RANGE) + ".\n"))
	while (startProb < 0) or (startProb > PROB_RANGE):
		startProb = int(input("Please enter an integer between 0 and " + str(PROB_RANGE) + ".\n"))
	stepUp = int(input("Define the change in probability per victory, as an integer between -" + str(PROB_RANGE) + " and " + str(PROB_RANGE) + ".\n"))
	while (stepUp < -PROB_RANGE) or (stepUp > PROB_RANGE):
		stepUp = int(input("Please enter an integer between -" + str(PROB_RANGE) + " and " + str(PROB_RANGE) + ".\n"))
	stepDown = int(input("Define the change in probability per defeat, as an integer between -" + str(PROB_RANGE) + " and " + str(PROB_RANGE) + ".\n"))
	while (stepDown < -PROB_RANGE) or (stepDown > PROB_RANGE):
		stepDown = int(input("Please enter an integer between -" + str(PROB_RANGE) + " and " + str(PROB_RANGE) + ".\n"))


if (trials < 1):
	if trials < 1:
		print "You need to run trials."
		sys.exit()
	

if (batches < 1):
	if batches < 1:
		print "You need at least 1 batch."
		sys.exit()
	

output = open(output_file, 'w')
analysis = open(analsys_file, 'w')

analysis.write("Mode: " + mode + "\n")
analysis.write("Size of each batch: " + str(trials) + "\n")
analysis.write("Number of batches: " + str(batches) + "\n\n")

if mode == "MarkovStep":
	analysis.write("Initial Probability: " + str(startProb/PROB_RANGE) + "\n")
	analysis.write("Step Up: " + str(stepUp/PROB_RANGE) + "\n")
	analysis.write("Step Down: " + str(stepDown/PROB_RANGE) + "\n")

# The following functions run a single batch, each consisting of a specified number of trials.  
# They are reliant upon the random library to generate random numbers within specified distributions.

# coinFlip simply randomly selects 0 or 1 over and over. Nothing crazy.
def coinFlip():
	val = 0
	result_array = []
	for i in range(0, int(trials)):
		val = random.randint(0, 1)
		result_array.append(val)
	return result_array

# diceRoll takes in the number of sides specified in the mode selection, and selects an int val, where 1 <= val <= sides.
def diceRoll(sides):
	val = 0
	result_array = []
	for i in range(0, int(trials)):
		val = random.randint(1, sides)
		result_array.append(val)
	return result_array

# lotteryPull generates a short array of integers, each between 1 and size, of length slots when millions is false, or of length slots + 1 when millions is true.
# in the case that millions is true, The final number, representing the Megaball, is between 1 and 25.  That value can be changed at the top of the file.
def lotteryPull(slots, size, millions):
	val = []
	result_array = []
	for i in range(0, int(trials)):
		for j in range(0, slots):
			val.append(random.randint(1, size))
		if millions:
			val.append(random.randint(1, MEGABALL))
		result_array.append(val)
		val = []
	return result_array

# markovRun runs the specified number of trials, at starting probability currentProb, where currentProb = startProb / PROB_RANGE, and increasing or decreasing currentProb by 
# stepUp / PROB_RANGE or stepDown / PROB_RANGE on successes and failures, respectively.
def markovRun():
	currentProb = startProb
	val = 0
	result_array = []
	for i in range(0, int(trials)):
		val = random.randint(1, PROB_RANGE)
		if val < (currentProb):
			result_array.append(1)
			currentProb = currentProb + stepUp
			if currentProb > PROB_RANGE:
				currentProb = PROB_RANGE
			if currentProb < -PROB_RANGE:
				currentProb = -PROB_RANGE
		else:
			result_array.append(0)
			currentProb = currentProb + stepDown
			if currentProb > PROB_RANGE:
				currentProb = PROB_RANGE
			if currentProb < -PROB_RANGE:
				currentProb = -PROB_RANGE
	return result_array



# batch_run manages one batch, selecting the necessary mode and returning the results of that batch.
# Any additional mode functions should be written above here, and the mode should be added to the list of if statements below, where that function should be called.
def batch_run():
	if mode == "CoinFlip":
		b_results = coinFlip()
	elif mode == "MarkovStep":
		b_results = markovRun()
	elif mode in lottery_modes:
		if mode == "LocalTriple":
			b_results = lotteryPull(3, 10, False)
		if mode == "Take5":
			b_results = lotteryPull(5, 39, False)
		if mode == "MegaMillions":
			b_results = lotteryPull(5, 70, True)
	elif mode[0] == "D":
		sides = int(mode[1:])
		b_results = diceRoll(sides)
	else:
		print("HERESY")
	return b_results

batches_results = []

# This loop calls batch_run the specified number of times, and writes the results to output.
for i in range(0, int(batches)):
	output.write("Batch " + str(i + 1) + ":\n")
	results = batch_run()

	batches_results.append(results)

	if mode in lottery_modes:
		for x in results:
			output.write(" ".join(str(p) for p in x))
			output.write("\n")
		output.write("\n\n")

	else:
		output.write("\n".join(str(y) for y in results))
		output.write("\n\n")


average_array = []

# If a new mode is added, the expected means should be added here.  Either calculate it by hand, as done for CoinFlip, or calculate it through an algorithm, as done for dice.
if mode == "CoinFlip":
	expected_mean = .5
	possible_values = [0, 1]
elif mode == "MarkovStep":
	expected_mean = .5
	possible_values = [0, 1]
elif mode in lottery_modes:
	if mode == "LocalTriple":
		expected_mean = 5.5
	if mode == "Take5":
		expected_mean = 20
	if mode == "MegaMillions":
		expected_mean = (5 * 70 + MEGABALL) / 12.0
else:
	sides = int(mode[1:])
	expected_mean = (1 + sides) / 2.0
	possible_values = []
	for x in range(1, sides + 1):
		possible_values.append(x)


#This section of code writes the expected mean of any given batch, the actual mean of each batch, and the total mean of all batches.
analysis.write("Expected mean: " + str(expected_mean) + ".\nMeans:\n")

for bat in range(0, len(batches_results)):
	if mode not in lottery_modes:
		average = sum(batches_results[bat])/(float(trials))
	else:
		average = 0
		for tri in batches_results[bat]:
			average = average + sum(tri)
		if mode == "LocalTriple":
			average = average / (3.0 * (float(trials)))
		elif mode == "Take5":
			average = average / (5.0 * (float(trials)))
		elif mode == "MegaMillions":
			average = average / (6.0 * (float(trials)))

	average_array.append(average)
	analysis.write("Batch " + str(bat + 1) + " mean: " + str(average) + "\n")

average = sum(average_array) / float(batches)
analysis.write("Total mean: " + str(average) + "\n\n")


# Calculates the expected variance given an expected mean and all possible values, assuming uniform distributions.
def variance_expected(exp_mean, pos_values):
	return sum([(x - exp_mean) ** 2 for x in pos_values]) / len(pos_values)

#Calculates the actual variance, given the actual mean and the list of actual values.
def variance_actual(act_mean, act_values):
	return sum([(x - act_mean) ** 2 for x in act_values]) / len(act_values)

all_results = []

# This section of code writes out the expected variance, actual variance of each batch, and the actual overall variance,
# as well as the expected and actual standard deviations, for all but lottery modes.
if mode not in lottery_modes:
	for bat in batches_results:
		for item in bat:
			all_results.append(item)

	exp_var = variance_expected(expected_mean, possible_values)
	analysis.write("Expected Variance: " + str(exp_var) + "\n")
	analysis.write("Expected Standard Deviation: " + str(math.sqrt(exp_var)) + "\n")
	for x in range(1, len(batches_results) + 1):
		act_var = variance_actual(average_array[x - 1], batches_results[x - 1])
		analysis.write("Actual Variance of Batch " + str(x) + ": " + str(act_var) + "\n")
		analysis.write("Actual Standard Deviation of Batch " + str(x) + ": " + str(math.sqrt(act_var)) + "\n")
		
	tot_var = variance_actual(average, all_results)
	analysis.write("Overall Variance: " + str(tot_var) + "\n")
	analysis.write("Overall Standard Deviation: " + str(math.sqrt(tot_var)) + "\n")

analysis.close()
output.close()