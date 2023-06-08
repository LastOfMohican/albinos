from pysat.solvers import Solver
class SatSolver: 
    def solve(self,clauses):
        s=Solver(name='g4')
        for c in clauses:
            s.add_clause(c)
        s.solve()
        return s.get_model()
