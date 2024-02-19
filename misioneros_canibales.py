from collections import defaultdict
class Direction:
	OLD_TO_NEW = 1
	NEW_TO_OLD = 0


class CONST:
	def __init__(self):
		self.MAX_M = 3
		self.MAX_C = 3
		self.CAP_BOAT = 2

MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None


class State(object):

	def __init__(self, missionaries, cannibals, dir, missionariesPassed, cannibalsPassed, level, CONSTS,moves):
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.dir = dir
		self.action = ""
		self.level = level
		self.missionariesPassed = missionariesPassed
		self.cannibalsPassed = cannibalsPassed
		self.CONSTANTS = CONSTS
		self.moves = moves

	def successors(self):
		listChild = []
		if not self.isValid() or self.isGoalState():
			return listChild
		if self.dir == Direction.OLD_TO_NEW:
			sgn = -1
			direction = "a la nueva orilla"
		else:
			sgn = 1
			direction = "a la orilla inicial"
		for i in self.moves:
			(m, c) = i
			self.addValidSuccessors(listChild, m, c, sgn, direction)
		return listChild

	def addValidSuccessors(self, listChild, m, c, sgn, direction):
		newState = State(self.missionaries + sgn * m, self.cannibals + sgn * c, self.dir + sgn * 1,
							self.missionariesPassed - sgn * m, self.cannibalsPassed - sgn * c, self.level + 1,
							self.CONSTANTS,self.moves)
		if newState.isValid():
			listChild.append(newState)

	def isValid(self):
		if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > MAX_M or self.cannibals > MAX_C or (
				self.dir != 0 and self.dir != 1):
			return False

		if (self.cannibals > self.missionaries > 0) or (
				self.cannibalsPassed > self.missionariesPassed > 0):
			return False

		return True

	def isGoalState(self):
		return self.cannibals == 0 and self.missionaries == 0 and self.dir == Direction.NEW_TO_OLD

	def __repr__(self):
		direction = ""
		Lmission = "M" * self.missionaries
		Lcanibal = "C" * self.cannibals
		Rmission = "M" * self.missionariesPassed
		Rcanibal = "C" * self.cannibalsPassed

		if(self.dir == 1):
			direction = "-->"
		else:
			direction = "<--"

		return "Estado: %d = %s%s %s %s%s " % (self.level, Lmission, Lcanibal, direction, Rmission, Rcanibal)

	def __eq__(self, other):
		return self.missionaries == other.missionaries and self.cannibals == other.cannibals and self.dir == other.dir

	def __hash__(self):
		return hash((self.missionaries, self.cannibals, self.dir))

	def __ne__(self, other):
		return not (self == other)


TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0, CNST,None)


class Graph:

	def __init__(self):

		self.bfs_parent = {}
		self.expandedBFS = 0

	def BFS(self, s):
		self.expandedBFS = 0
		self.bfs_parent[s] = None
		visited = {(s.missionaries, s.cannibals, s.dir): True}
		s.level = 0

		queue = [s]
		while queue:
			self.expandedBFS += 1
			u = queue.pop(0)
			if u.isGoalState():
				queue.clear()
				self.bfs_parent[TERMINAL_STATE] = u
				return self.bfs_parent

			for v in reversed(u.successors()):
				if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
					self.bfs_parent[v] = u
					v.level = u.level + 1
					queue.append(v)
					visited[(v.missionaries, v.cannibals, v.dir)] = True

		return {}

	
	def printPath(self, parentList, tail):
		if tail is None:
			return
		if parentList == {} or parentList is None: 
			return
		if tail == TERMINAL_STATE: tail = parentList[tail]

		stack = []
		while tail is not None:
			stack.append(tail)
			tail = parentList[tail]

		while stack:
			print(stack.pop())

def genPossibleMoves():
	moves = []
	for m in range(3):
		for c in range(3):
			if 0 < m < c:
				continue
			if 1 <= m + c <= 2:
				moves.append((m, c))
	return moves

def runBFS(g, INITIAL_STATE):
	p = g.BFS(INITIAL_STATE)
	g.printPath(p, TERMINAL_STATE)

def main():
	print("misioneros = 3")
	print("canibales = 3")
	moves = genPossibleMoves()
	INITIAL_STATE = State(3, 3, Direction.OLD_TO_NEW, 0, 0, 0, CONST(), moves)
	g = Graph()
	print("Inicio del BFS: ")
	runBFS(g, INITIAL_STATE)
	print("Problema solucionado! :D")

if __name__ == '__main__':
	main()
