from itertools import chain, combinations
import sys

def getAttributeClosure(X, FDS):
  '''
  Computes the attribute colsure given a set of attribute and functional dependencies.
  X: key attributes
  FDS: list of functional dependencies
  '''
  retval = set(X)
  
  breaks = False

  while not breaks:
    breaks = True
    for fd in FDS:
      lhs = fd[0]
      rhs = fd[1]

      if lhs.issubset(retval) and not rhs.issubset(retval):
        breaks = False
        retval.update(rhs)

  return retval

def getSuperKeys(R, FDS):
  '''
  Computes the super keys
  '''
  s = list(R)
  subsets = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

  supers = []

  for subset in subsets:
    closure = getAttributeClosure(set(subset), FDS)
    if closure == R:
      supers.append( set(subset) )

  return supers


def getCandidateKeys(R, FDS):
  '''
  Computes the candidate keys, given a relation and functional dependencies.
  '''
  # Try every subset of R as the key, and find the shortest one
  s = list(R)
  subsets = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

  best_length = len(R)
  candidates = []

  for subset in subsets:
    closure = getAttributeClosure(set(subset), FDS)
    if closure == R and len(subset) < best_length:
      candidates = [set(subset)]
      best_length = len(subset)
    elif closure == R and len(subset) == best_length:
      candidates.append(set(subset))

  return candidates

def getPrimeAttributes(R, FDS):
  '''
  Computes the prime attributes, given a relation and functional dependencies
  '''
  retset = set([])

  candidates = getCandidateKeys(R, FDS)
  for key in candidates:
    for a in key:
      retset.add( a )
  return retset

def getNonPrimeAttributes(R, FDS):
  '''
  Computes the prime attributes, given a relation and functional dependencies
  '''
  primes = getPrimeAttributes(R, FDS)
  return set(R) - set(primes)

def is2NF(R, FDS):
  '''
  Checks if a relation is in 2NF
  Relation schema R is in 2NF if it is in 1NF and it does not have any 
  non-prime attributes that are functionally dependent on a part of a 
  candidate key
  '''

  candidates = getCandidateKeys(R, FDS)
  primes = getPrimeAttributes(R, FDS)
  non_primes = getNonPrimeAttributes(R, FDS)

  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]

    # We're only interesting in parts of candidate keys
    if lhs in candidates or len(lhs & non_primes):
      continue

    for att in non_primes:
      if att in rhs:
        print("\t", lhs, "->", rhs, "breaks 2NF requirements (", att, "is non-prime )")
        return False

  return True

def is3NF(R, FDS):
  '''
  Checks if a relation is in 3NF
  '''
  
  superkeys = getSuperKeys(R, FDS)
  primes = getPrimeAttributes(R, FDS)
  non_primes = getNonPrimeAttributes(R, FDS)

  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]

    if lhs in superkeys:
      continue

    for att in non_primes:
      if att in rhs:
        print("\t", lhs, "->", rhs, "breaks 2NF requirements (", att, "is non-prime )")
        return False

  return True

def isBCNF(R, FDS):
  '''
  Checks if a relation is in BCNF
  '''

  superkeys = getSuperKeys(R, FDS)

  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]

    if lhs not in superkeys:
      print("\t", lhs, "->", rhs, "breaks 2NF requirements (", lhs, "is non-superkey )")
      return False

  return True


def doChecks(name, R, FDS):

  print("***********************************")
  print("\t\t",name)
  print("***********************************")

  # Calculate candidate keys
  candidate_keys = getCandidateKeys(R, FDS)
  print("Candidate keys:")
  for key in candidate_keys:
    print("\t", key)
  print("")

  # Calculate prime attributes
  prime_attributes = getPrimeAttributes(R, FDS)
  print("Prime attributes:\n\t", prime_attributes)
  print("")

  non_prime_attributes = getNonPrimeAttributes(R, FDS)
  print("Non-prime attributes:\n\t", non_prime_attributes)
  print("")


  # Check if the relation is normalized
  print("2NF status:")
  is_2NF = is2NF(R, FDS)
  if is_2NF:
    print("\tThe relation is in 2NF")
  print("")

  print("3NF status:")
  is_3NF = is3NF(R, FDS)
  if is_3NF:
    print("\tThe relation is in 3NF")
  print("") 

  print("BCNF status:")
  is_BCNF = isBCNF(R, FDS)
  if is_BCNF:
    print("\tThe relation is in BCNF")
  print("") 



def main():
  # Read the data
  lines = []
  for line in sys.stdin:
    if line.strip() != "":
      lines.append(line.strip())
  
  name = ""
  R = -1  
  FDS = []
  for line in lines:

    # If we've found a new relation, do the calculations for the old one
    if line.find('(') != -1:

      if R != -1:
        doChecks(name, R, FDS)

      # Reset the relation and the FDs
      name = line[:line.find('(')]
      line = line[ line.find('(')+1 : line.find(')') ]
      R = set( [ x.strip() for x in line.split(',')] )
      FDS = []
      continue

    lhs = line.split('->')[0]
    rhs = line.split('->')[1]
    lhs = set([ x.strip() for x in lhs.split(',')])
    rhs = set([ x.strip() for x in rhs.split(',')])
  
    FD = (lhs, rhs)
    FDS.append( FD )

  # Do the calculations for the last relation
  if R != -1:
    doChecks(name, R, FDS)
  
  


if __name__ == "__main__":
  main()
