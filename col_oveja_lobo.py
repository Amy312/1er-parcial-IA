from enum import Enum
from collections import namedtuple
from functools import partial

visited = []
cola = []
State = namedtuple("State", ["man", "cabbage", "sheep", "wolf"])
Location = ["Left", "Right"]

start_state = State(
    man=Location[1],
    cabbage=Location[1],
    sheep=Location[1],
    wolf=Location[1],
)

goal_state = State(
    man=Location[0],
    cabbage=Location[0],
    sheep=Location[0],
    wolf=Location[0],
)

def bfs(graph, start, finish):
  visited.append(start)
  cola.append(start)
  actual=start
  parents=dict()
  parents[actual]=None

  while cola:
    actual = cola.pop(0)

    if finish.__eq__(actual):
        camino=[]
        parent=actual
        while parent is not None:
            camino.insert(0,parent)
            parent=parents.get(parent)
        return camino

    for vecino in graph(actual):
      if vecino not in visited:
        visited.append(vecino)
        parents[vecino]=actual
        cola.append(vecino)

def is_valid(state):
    sheep_eats_cabbage = (
        state.sheep == state.cabbage
        and state.man != state.sheep
    )
    wolf_eats_sheep = (
        state.wolf == state.sheep and state.man != state.wolf
    )
    invalid = sheep_eats_cabbage or wolf_eats_sheep
    return not invalid

def next_states(state):
    if state.man == Location[1]:
        other_side = Location[0]
    else:
        other_side = Location[1]

    move = partial(state._replace, man=other_side)

    candidates = [move()]

    for object in ["cabbage", "sheep", "wolf"]:
        if getattr(state, object) == state.man:
            candidates.append(move(**{object: other_side}))

    yield from filter(is_valid, candidates)

def describe_solution(path):
    print(Location[0]+":", [agent for agent in ["man", "cabbage", "sheep", "wolf"] if getattr(path[0],agent)==Location[0]],
          Location[1]+":", [agent for agent in ["man", "cabbage", "sheep", "wolf"] if getattr(path[0],agent)==Location[1]])
    for old, new in zip(path, path[1:]):
        boat = [
            agent
            for agent in ["man", "cabbage", "sheep", "wolf"]
            if getattr(old, agent) != getattr(new, agent)
        ]
        right = [
           agent
            for agent in ["man", "cabbage", "sheep", "wolf"]
            if getattr(new,agent) == Location[1]
        ]
        left = [
           agent
            for agent in ["man", "cabbage", "sheep", "wolf"]
            if getattr(new,agent) == Location[0]
        ]
        print(old.man, "to", new.man, ", Boat:", boat, ", Left:", left, ", Right:", right)

if __name__ == "__main__":
    describe_solution(bfs(
    start = start_state,
    finish = goal_state,
    graph = next_states))