from copy import copy, deepcopy
from itertools import combinations

START_SHORE_THINGS = ['koza', 'wilk', 'kapusta']
CAPACITY = 1
CONFLICTS = [
    ('koza', 'wilk'),
    ('koza', 'kapusta')
]


class Shore:
    def __init__(self, things, conflicts, is_destination):
        self.things = things
        self.conflicts = conflicts
        self.is_destination = is_destination

    @property
    def is_start(self):
        return not self.is_destination

    @property
    def is_empty(self):
        return len(self.things) == 0

    @property
    def is_dangerous(self):
        for conflict in self.conflicts:
            if not([x for x in conflict if x not in self.things]):
                # If all conflict sides are in things - evaluate to true
                return True
        return False

    def get_possible_cargo(self):
        cargo = [[]]
        for r in range(1, min(CAPACITY+1, len(self.things)+1)):
            cargo.extend([sorted(l) for l in combinations(self.things, r)])
        return cargo


class Path:
    def __init__(self, start_shore: Shore, steps: list, result: str):
        self.start_shore = start_shore
        self.steps = steps
        self.result = result

    def print_info(self, counter):
        print('--- PATH {} ---'.format(str(counter)))
        print('STARTING WITH: {}'.format(str(self.start_shore.things)))
        step_counter = 0
        for step in self.steps:
            step_counter += 1
            print('TRANSFER {}: {}'.format(step_counter, step))
        print('RESULT: {}'.format(self.result))
        print()


class PathFinder:
    found_paths = []

    def __init__(self, start_shore: Shore, destination_shore: Shore):
        self.start_shore = start_shore
        self.destination_shore = destination_shore

    def check_path(self,
                   from_shore: Shore,
                   to_shore: Shore,
                   start_states: list,
                   destination_states: list,
                   steps: list):
        # Checking if path ends in one of three possible ways:
        if from_shore.is_start and from_shore.is_empty:
            self.found_paths.append(Path(self.start_shore, steps, 'SUCCESS - MOVED ALL SAFELY!'))
            return
        elif steps and to_shore.is_dangerous:
            self.found_paths.append(Path(self.start_shore, steps, 'FAILURE - CONFLICT OCCURRED :('))
            return
        elif steps and any([
            to_shore.is_start and to_shore.things in start_states[:-1],
            to_shore.is_destination and to_shore.things in destination_states[:-1]
        ]):
            self.found_paths.append(Path(self.start_shore, steps, 'FAILURE - LOOP OCCURRED :('))
            return
        # If not - produce branches and recursively call the function on branches:
        else:
            possible_cargo = from_shore.get_possible_cargo()
            for cargo in possible_cargo:
                if steps and cargo == sorted(steps[-1]):
                    pass
                else:
                    steps_copy = deepcopy(steps)
                    steps_copy.append(cargo)
                    start_states_copy = deepcopy(start_states)
                    destination_states_copy = deepcopy(destination_states)
                    from_shore_copy = deepcopy(from_shore)
                    to_shore_copy = deepcopy(to_shore)
                    for x in cargo:
                        from_shore_copy.things.remove(x)
                        to_shore_copy.things.append(x)
                    from_shore_copy.things.sort()
                    to_shore_copy.things.sort()
                    if to_shore_copy.is_destination:
                        start_states_copy.append(from_shore_copy.things)
                        destination_states_copy.append(to_shore_copy.things)
                    else:
                        start_states_copy.append(to_shore_copy.things)
                        destination_states_copy.append(from_shore_copy.things)
                    self.check_path(
                        from_shore=to_shore_copy,
                        to_shore=from_shore_copy,
                        start_states=start_states_copy,
                        destination_states=destination_states_copy,
                        steps=steps_copy
                    )

    def print_paths(self, only_success=True, sort_by_length=True):
        paths_to_print = self.found_paths
        if only_success:
            paths_to_print = [p for p in self.found_paths if 'SUCCESS' in p.result]
        if sort_by_length:
            paths_to_print.sort(key=lambda x: len(x.steps))
        path_counter = 0
        for path in paths_to_print:
            path_counter += 1
            path.print_info(path_counter)

    def run(self):
        self.check_path(
            deepcopy(self.start_shore),
            deepcopy(self.destination_shore),
            [copy(self.start_shore.things)],
            [copy(self.destination_shore.things)],
            [])


if __name__ == "__main__":
    path_finder = PathFinder(
        start_shore=Shore(START_SHORE_THINGS, CONFLICTS, False),
        destination_shore=Shore([], CONFLICTS, True)
    )
    path_finder.run()
    path_finder.print_paths()