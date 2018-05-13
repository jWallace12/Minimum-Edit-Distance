# Names: Dustin Conley and Jonah Wallace
# Assignment: CSCI 404 - Winter 2018 - Assignment #2
# File: distance.py - Built off of starting point from Dr. Yudong
# Purpose: To calculate the minimum edit distance of converting a source word
# 	   into a target word, along with printing out their alignments



# global var counting remaining alignments
alignCount = 0
limit = 0

# function to increment the alignment count
def incrementAligns():
	global alignCount
	alignCount = alignCount + 1

# function to recursively find and print all alignments
def distanceRecursive(dist, target, source, insertcost, deletecost, replacecost, xIndex, yIndex, sourceStr, pipeStr, targetStr):

    # Base Case 1:
    # Alignment limit has been reached
    if (alignCount == limit):
        return
   
    # Base Case 2:
    # Print the alignment
    if ((xIndex == 0) and (yIndex == 0)):
        targetStr = targetStr[:-1]
	pipeStr = pipeStr[:-1]
	sourceStr = sourceStr[:-1]
	incrementAligns()
	print "Alignment #" + str(alignCount) + ":"
	print targetStr[::-1]
	print pipeStr[::-1]
	print sourceStr[::-1]
	print ""
	return
    	
    # get the value for the left, down, and diagonal values, and find the min
    left = 0
    down = 0
    diag = 0
    diagonalSub = True
    if (xIndex > 0):
	left = dist[xIndex-1][yIndex] + insertcost
    else:
	left = 1000
    if (yIndex > 0):
	down = dist[xIndex][yIndex-1] + deletecost
    else:
	down = 1000
    if ((xIndex != 0) and (yIndex != 0)):
        diag = dist[xIndex-1][yIndex-1]
        if (target[-1] != source[-1]):
            diag = diag + replacecost
            diagonalSub = False
    else:
	diag = 1000
    minimum = min(left, down, diag)
    

    # Recurse on each value that is equal to the minimum

    # Substitution
    if (minimum == diag):
	if (diagonalSub):
		distanceRecursive(dist, target[:-1], source[:-1], insertcost, deletecost, 
				  replacecost, xIndex-1, yIndex-1, (sourceStr + source[-1] + " "), 
				  (pipeStr + "| "), (targetStr + target[-1] + " "))
	else:
		distanceRecursive(dist, target[:-1], source[:-1], insertcost, deletecost, 
				  replacecost, xIndex-1, yIndex-1, (sourceStr + source[-1] + " "), 
				  (pipeStr + "  "), (targetStr + target[-1] + " "))
            
    # Insertion
    if (minimum == left):
	if (target != ""):
            distanceRecursive(dist, target[:-1], source, insertcost, deletecost, 
			      replacecost, xIndex-1, yIndex, (sourceStr + "_ "), 
			      (pipeStr + "  "), (targetStr + target[-1] + " "))
	else:
	    distanceRecursive(dist, target[:-1], source, insertcost, deletecost, 
			      replacecost, xIndex-1, yIndex, (sourceStr + "_ "), 
			      (pipeStr + "  "), targetStr)

        
    # Deletion
    if (minimum == down):
	if (source != ""):
            distanceRecursive(dist, target, source[:-1], insertcost, deletecost, 
			      replacecost, xIndex, yIndex-1, (sourceStr + source[-1] + " "), 
			      (pipeStr + "  "), (targetStr + "_ "))
        else:
            distanceRecursive(dist, target, source[:-1], insertcost, deletecost, 
			      replacecost, xIndex, yIndex-1, sourceStr, (pipeStr + "  "), 
			      (targetStr + "_ "))
		
# function to compute the minimum edit distance
def distance(target, source, N, insertcost, deletecost, replacecost):
	global limit
	limit = int(N)
	n = len(target)+1
	m = len(source)+1

	# set up dist and initialize values
	dist = [ [0 for j in range(m)] for i in range(n) ]
	for i in range(1,n):
		dist[i][0] = dist[i-1][0] + insertcost
	for j in range(1,m):
		dist[0][j] = dist[0][j-1] + deletecost

	# align source and target strings
	for j in range(1, m):
		for i in range(1,n):
			inscost = insertcost + dist[i-1][j]
			delcost = deletecost + dist[i][j-1]
			if (source[j-1] == target[i-1]):
		        	add = 0
			else:
                        	add = replacecost

			substcost = add + dist[i-1][j-1]
			minimum = min(inscost, delcost, substcost)
			dist[i][j] = minimum

	# initialize backtrace variables
	xIndex = n-1
	yIndex = m-1
	sourceStr = ""
        pipeStr = ""
        targetStr = ""
	print("Levenshtein distance = " + str(dist[n-1][m-1]))
	distanceRecursive(dist, target, source, insertcost, deletecost, 
			  replacecost, xIndex, yIndex, sourceStr, pipeStr, targetStr)
        return

		
if __name__=="__main__":
	from sys import argv
	if len(argv) == 5:
		if ((argv[3] == "-n") and (int(argv[4]) > 0)):
			distance(argv[1], argv[2], argv[4], 1, 1, 2)
		else:
			print("Error: Syntax -- Use: distance.py target source [-n numAligns]")
	elif len(argv) == 3:
		distance(argv[1], argv[2], 1, 1, 1, 2)
	else:
		print("Error: Syntax -- Use: distance.py target source [-n numAligns]")
