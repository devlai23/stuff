import chess
import time
from anytree import Node, RenderTree, PreOrderIter
#depth 2 sim game?!?!?!?!?
def main():
    global depth
    depth = int(input("Engine depth? "))
    while True:
        if makeMove() == -1:
            break

def makeMove():
    print("\n")
    start_time = time.time()
    rootNode = createTree(depth)
    minimax(rootNode, board.turn, depth)
    move = str(bestMove.name).split("/")[-1]
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Depth " + str(depth) + ": " + move)
    try:
        if board.turn:
            print("White to move")
        else:
            print("Black to move")
        print(board)
        board.push_san(input())

        if board.is_checkmate():
            print("Checkmate")
            return -1
        elif board.is_stalemate():
            print("Stalemate")
            return -1
        elif board.is_insufficient_material():
            print("Insufficient Material")
            return -1
        elif board.can_claim_threefold_repetition():
            print("Repetition of moves")
            return -1
        return 0
    except:
        print("Invalid move")
        makeMove()

def createTree(depth):
    tempboard = board.copy()
    root = Node("Root", position = tempboard, positionValue = None)

    for currentdepth in range (0, depth):
        for node in root.leaves:
            for move in list(node.position.legal_moves):
                temptempboard = node.position.copy()
                fromuci = chess.Move.from_uci(str(move))
                temptempboard.push(fromuci)
                add = Node(move, parent = node, position=temptempboard)
                if currentdepth == depth-1:
                    add.positionValue = evaluate(add.position)

    return root

def evaluate(b):
    # MATERIAL
    wq=bq=wr=br=wb=bb=wn=bn=wp=bp=0
    for square in range(0, 64):
        piece = b.piece_at(square)
        if piece != None:
            piece = piece.symbol()
        if piece == "Q":
            wq+=1
        elif piece == "q":
            bq+=1
        elif piece == "R":
            wr+=1
        elif piece == "r":
            br+=1
        elif piece == "B":
            wb+=1
        elif piece == "b":
            bb+=1
        elif piece == "N":
            wn+=1
        elif piece == "n":
            bn+=1
        elif piece == "P":
            wp+=1
        elif piece == "p":
            bp+=1
    score = 9*(wq-bq)+5*(wr-br)+3*(wb-bb)+3*(wn-bn)+(wp-bp)

    #DOUBLED PAWNS 
    whiteiso =[]
    blackiso =[]
    wdouble=bdouble=0
    for f in range(0, 8):
        wp=bp=0
        for r in range(0, 8):
            piece = b.piece_at(f+(8*r))
            if piece != None:
                piece = piece.symbol()
            if (piece == "P"):
                wp+=1
            elif (piece == "p"):
                bp+=1
        if wp > 1:
            wdouble+=1
        if bp > 1:
            bdouble+=1
        whiteiso.append(wp)
        blackiso.append(bp)
    score = score - 0.5*(wdouble-bdouble)

    #ISOLATED PAWNS
    wi = bi = 0
    for i in range(1, 7):
        if whiteiso[i] > 0:
            if whiteiso[i-1] == 0 and whiteiso[i+1] == 0:
                wi+=1
        if blackiso[i] > 0:
            if blackiso[i-1] == 0 and blackiso[i+1] == 0:
                bi+=1
    score = score - 0.5*(wi-bi)
    
    #Mobility
    if b.turn:
        whitemoves=(len(list(b.legal_moves)))
        tempboard = b.copy()
        tempboard.push(chess.Move.null())
        blackmoves=(len(list(tempboard.legal_moves)))
    else:
        blackmoves=(len(list(b.legal_moves)))
        tempboard = b.copy()
        tempboard.push(chess.Move.null())
        whitemoves=(len(list(tempboard.legal_moves)))
    
    score = score + 0.1*(whitemoves - blackmoves)
    return score

def minimax(rootNode, maxPlayer, currentDepth):
    #true means we are on max layer
    maxmin = not ((currentDepth % 2 == 1) ^ maxPlayer)
    parentNodes = []
    for node in rootNode.leaves:
        if (node.depth == currentDepth) and (node.parent not in parentNodes):
            parentNodes.append(node.parent)
            bestChild = None
            if (maxmin):
                bestVal = -1000
                for child in node.parent.children:
                    if child.positionValue > bestVal:
                        bestVal = child.positionValue
                        bestChild = child
            else:
                bestVal = 1000
                for child in node.parent.children:
                    if child.positionValue < bestVal:
                        bestVal = child.positionValue
                        bestChild = child
            node.parent.positionValue = bestVal
            global bestMove
            bestMove = bestChild
        node.parent = None

    if (currentDepth != 1):
        minimax(rootNode, maxPlayer, currentDepth-1)

def printTree(node):
    for pre, fill, n in RenderTree(node):
        print("%s%s" % (pre, n.name))

board = chess.Board()
bestMove = None
depth = 0
main()