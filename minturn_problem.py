from typing import Tuple, List, Set

import itertools

DistanceVector = Tuple[int, int, int, int, int, int]
PossibleDomain = List[int]
PDSubset = Tuple[int, int, int] # Possible Domain Subset
DPDSubset = Tuple[int, int, int] # Directional Possible Domain Subset
Points = Tuple[int, int, int, int] # points

def distance(x, y):
	d = x - y
	if d < 0:
		d = abs(d)
	if d > 6:
		d = 12 - d
	return d

distance_vector = (3, 2, 1, 0, 0, 0)

def distance_vector_to_possible_domain(dv: DistanceVector) -> PossibleDomain:
	ret: PossibleDomain = []
	for i, freq in enumerate(dv):
		for j in range(freq):
			ret.append(i+1)
	return ret

def valid_pd_subset(pds: PDSubset) -> bool:
	for i in pds:
		if pds.count(i) > 2:
			return False
		if not 1 <= i <= 6:
			return False
	return True

def Tr(x: int) -> int:
	return x*(x+1)//2

def Tr_inv(x: int) -> int:
	for i in range(x+1):
		if x == Tr(i):
			return i
		elif x < Tr(i):
			return -1
	raise AAAAAAAAA

def dv_to_pd_subsets(dv: DistanceVector) -> Set[PDSubset]:
	tr_n = sum(dv)
	n = Tr_inv(tr_n)
	pdss = set(itertools.combinations(distance_vector_to_possible_domain(dv),n))
	return {pds for pds in pdss if valid_pd_subset(pds)}

A=dv_to_pd_subsets(distance_vector)

def is_dpds_valid(dpds: DPDSubset) -> bool:
	if len(set(dpds)) < len(dpds):
		return False
	if -6 in dpds:
		return False
	return True

def pds_to_direction_pds(pds: PDSubset) -> Set[DPDSubset]:
	dpdss = set()
	for i in pds:
		if pds.count(i) > 2:
			return dpdss
	if pds.count(6) > 1:
		return dpdss
	for bitmask in range(2**len(pds)):
		dpds = tuple((-1)**bool(bitmask & 2**i) * e for i, e in enumerate(pds))
		if is_dpds_valid(dpds) and tuple(sorted(dpds)) not in dpdss:
			dpdss |= {tuple(sorted(dpds))}
	return dpdss

def dpds_to_points(dpds: DPDSubset) -> Points:
	return tuple(sorted([0] + [i % 12 for i in dpds]))

def points_to_dv(points: Points) -> DistanceVector:
	if len(points) == 0:
		raise ValueError("0 Points cannot be encoded in a DistanceVector")
	dv = [0]*6
	for i in range(len(points)):
		for j in range(i+1, len(points)):
			dv[distance(points[i], points[j])-1] += 1
	return tuple(dv)

def get_points_possibilities(dv: DistanceVector) -> List[Points]:
	possible_points_es = []
	pdss = dv_to_pd_subsets(dv)
	dpdsss = [pds_to_direction_pds(pds) for pds in pdss]
	dpdss = [dpds for dpdss in dpdsss for dpds in dpdss]
	points_es = [dpds_to_points(dpds) for dpds in dpdss]
	for i in range(len(points_es)):
		if dv == points_to_dv(points_es[i]):
			possible_points_es.append(points_es[i])
	return possible_points_es

#def up_distance(x: int, y: int) -> int:
#	if x < y:
#		return y - x
#	else: 

def are_points_same(pa: Points, pb: Points) -> bool:
	for i in range(12):
		if pa == tuple(sorted((p+i)%12 for p in pb)):
			return True
		elif pa == tuple(sorted((i-p)%12 for p in pb)):
			return True
	return False

def reduce_points_es(points_es: List[Points]) -> List[Points]:
	unique = []
	for ps in points_es:
		is_unique = True
		for ps_test in unique:
			if are_points_same(ps, ps_test):
				is_unique = False
		if is_unique:
			unique.append(ps)
	return unique

def all_liner_with_zero(ps: Points) -> List[Points]:
	same_direction_points = []
	opposite_direction_points = []
	for i in range(12):
		sdp = tuple(sorted((p+i)%12 for p in ps))
		odp = tuple(sorted((i-p)%12 for p in ps))
		if 0 in sdp:
			same_direction_points.append(sdp)
		if 0 in odp:
			opposite_direction_points.append(odp)
	return same_direction_points + opposite_direction_points

def minimum_equivalent_points(ps: Points) -> Points:
	return min(all_liner_with_zero(ps), key=sum)


def minturn(dv: DistanceVector) -> List[Points]:
	dv_ = dv
	n = Tr_inv(sum(dv))+1
	print(n)
	if n == 0:
		print("Special case: 0 points")
		return [()]
	if n == 12:
		print("Special case: 12 points")
		return [(*range(12),)]
	if n > 6:
		print("Inverting using pattern")
		new_dv = tuple((6-n)*2 + i for i in dv[:-1]) + tuple(6-n+ i for i in dv[-1:])
		dv = new_dv
	points_poss = get_points_possibilities(dv)
	reduced_points = reduce_points_es(points_poss)
	min_points = [minimum_equivalent_points(ps) for ps in reduced_points]
	if n > 6: # un-invert
		new_points = [tuple(i for i in range(12) if i not in points) for points in min_points]
		min_points = [minimum_equivalent_points(ps) for ps in new_points]
	return min_points

if __name__ == "__main__":
	while True:
		try:
			dv_str = input("Please input your interval vector: ")
			dv = tuple(int(i) for i in dv_str.split(','))
			if len(dv) != 6:
				raise ValueError("Please input 6 integers separated by commas")
			print(minturn(dv))
			if input("Continue? (y/n) ") != "y":
				break
		except ValueError as e:
			print(e)
		except EOFError:
			print("Could not read input")

