# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
import math
from pacman import agents, gamestate, util


class BetterReflexAgent(agents.ReflexAgent):
    def evaluate(self, gstate, move):
        newState = gstate.successor(0,move)
        # copyState = gstate.copy
        # copyState.apply_move(0,move)
        score = 0
        # if successor state is a win -> high score
        if newState.win:
            return math.inf
        # if successor state is a loss -> low sore
        if newState.loss:
            return -math.inf
        #Do not stop
        if move == util.Move.stop:
            score-=200
        #More distance to ghost is better
        minDistGhost = 10000
        closestGhost = None
        for x in newState.ghosts:
            ghostDist = util.manhattan(newState.pacman, x)
            if ghostDist < minDistGhost:
                minDistGhost = ghostDist
                closestGhost = x
        if gstate.timers[0] == 0:
            if util.manhattan(newState.pacman, closestGhost) > 5:
                score +=500
            else:
                score -=500
        if gstate.timers[0]>0:
            if util.manhattan(gstate.pacman, closestGhost) < 3:
                if util.manhattan(newState.pacman, closestGhost)<util.manhattan(gstate.pacman, closestGhost):
                    score+=500

        minFood=10000
        closestDot = None
        for x in newState.dots.list()+newState.pellets.list():
            foodDist= util.manhattan(newState.pacman, x)
            if foodDist<minFood:
                minFood = foodDist
                closestDot = x
        # Less distance to closest dot or less food left -> higher score
        if util.manhattan(newState.pacman,closestDot)<util.manhattan(gstate.pacman,closestDot):
            score+=200
        return score

class MinimaxAgent(agents.AdversarialAgent):
    def move(self, gstate):
        moves = []
        for x in gstate.legal_moves_vector(gstate.agents[0]):
            if not x == util.Move.stop:
                moves.append(x)
        bestMove = 0
        bestMoveLoc = None
        for move in moves:
            testVal = self.minimax(gstate.copy,move, self.depth, True)
            if testVal > bestMove:
                bestMove = testVal
                bestMoveLoc = move
        return bestMoveLoc

    def minimax(self, state, move, depth, minmax):
        state.apply_move(self.id,move)
        if depth == 0 or state.win or state.loss:
                return self.evaluate(state)
        if minmax:
            best = -math.inf
            moves = state.legal_moves_vector(state.agents[0])
            for move in moves:
                testValue =self.minimax(state.copy, move, depth-1, False)
                if testValue > best:
                    best = testValue
            return best

        if not minmax:
            best = math.inf
            moves = state.legal_moves_vector(state.agents[0])
            for move in moves:
                testValue = self.minimax(state.copy, move, depth-1, True)
                if testValue < best:
                    best = testValue
            return best

class AlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        moves = []
        for x in gstate.legal_moves_vector(gstate.agents[0]):
            if not x == util.Move.stop:
                moves.append(x)
        bestMove = 0
        bestMoveLoc = None
        for move in moves:
            testVal = self.minimaxAB(gstate.copy, move, -math.inf, math.inf, self.depth, True)
            if testVal > bestMove:
                bestMove = testVal
                bestMoveLoc = move
        return bestMoveLoc

    def minimaxAB(self, state, move, alpha,beta, depth, minmax):
        state.apply_move(self.id,move)
        if depth == 0 or state.win or state.loss:
                return self.evaluate(state)
        if minmax:
            best = -math.inf
            moves = state.legal_moves_vector(state.agents[0])
            for x in moves:
                best = max(best, self.minimaxAB(state.copy, x, alpha, beta, depth - 1, False))
                alpha = max(alpha, best)
            return best

        if not minmax:
            best = math.inf
            moves = state.legal_moves_vector(state.agents[0])
            for y in moves:
                best = min(best, self.minimaxAB(state.copy, y, alpha, beta, depth - 1, True))
                beta = min(beta, best)
            return best



def better_evaluate(gstate):
    raise exceptions.EmptyBonusAssignmentError


class MultiAlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        raise exceptions.EmptyBonusAssignmentError
