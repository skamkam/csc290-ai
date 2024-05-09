# CSC290 HW6 - Minimax Chess Bot
# Asher Uman, Amanda Colby, Sarah Kam
# https://python-chess.readthedocs.io/en/latest/core.html

import chess
import random
import datetime

def minimax(color, boardstate, depth):
  """
  Takes in current player color, depth, and determines best move for that player
  White = positive score, black = negative score
  """
  # boardstate copies in a copy of the board to be evaluated
  # we have to do this for every minimax call which blows

  best_score = 0
  best_move = None
  legal_moves = list(boardstate.legal_moves)

  if boardstate.is_checkmate() and color == chess.BLACK:
    return (None, 200)
  elif boardstate.is_checkmate() and color == chess.WHITE:
    return (None, -200)

    # last level: evaluate scores for this level and pass it back
  for move in legal_moves:
    
    score = 0
    if boardstate.is_capture(move): # if evaluate to true:
      if boardstate.is_en_passant(move):
        captured = chess.PAWN
      else:
        captured = boardstate.piece_at(move.to_square).piece_type # parse move
      if (captured == chess.PAWN):
        score = 1
      elif (captured == chess.KNIGHT or captured == chess.BISHOP):
        score = 3
      elif (captured == chess.ROOK):
        score = 5
      elif (captured == chess.QUEEN):
        score = 9
      else: # king
        score = 200

    if (boardstate.gives_check(move)):
      score += 7
  
    if color == chess.BLACK:  # if black, make the score negative
      score = -1 * score

    if depth > 1:
      #call minimax
      boardstate.push(move)
      
      tuple = minimax(not color, boardstate.copy(), depth-1)
      boardstate.pop()
      score += tuple[1]
      #print(str(depth) + ": Best move found in next player: " + tuple[0].uci())


    if (color == chess.BLACK and score <= best_score):
      #print(str(depth) + ": color is black and score is less than best score")
      best_score = score
      best_move = move
    elif (color == chess.WHITE and score >= best_score):
      #print(str(depth) + ": color is white and score is more than best score")
      best_score = score
      best_move = move
    elif score == 0 and best_score == 0:
      best_score = score
      best_move = move
    elif best_move is None:
      #print(str(depth) + ": no better moves found?")
      best_move = random.choice(legal_moves)

    #print()
    #print(depth, ": Best move found now: ", best_move)
    #print("score:", score)
    #print()

    # print("Proposed move: " + str(move))
    # print("Score: " + str(score))
    # print("Best Score: " + str(best_score))

  # end of for loop
  return (best_move, best_score)



def main():
  # Header
  print("=====================================================")
  print("             CS 290 Chess Bot Version 0.2            ")
  print("=====================================================")
  # Time
  print("Time: " + str(datetime.datetime.now()))

  # Get Computer Color
  color = input("Computer Player? (w=white/b=black): ")
  computerColor = chess.WHITE if color == "w" else chess.BLACK

  # Get FEN
  FEN = input("Starting FEN position? (hit ENTER for standard starting postion): ")

  # Initialize Board
  board = chess.Board(fen=FEN) if FEN != "" else chess.Board()

  # Game Loop
  gameOn = True
  while gameOn:
    # Print current board and generate list of current legal moves
    print(board)
    print()
    legal_moves = list(board.legal_moves)

    # Computer's turn
    if board.turn == computerColor:

      # best_move = ""
      #call minimax
      new_move = minimax(computerColor, board.copy(), 4)
      score = new_move[1]
      move = new_move[0]
      # do move and print it
      print("Best score found: " + str(score))
      board.push(move)
      print("Computer's turn: " + move.uci())

    #User's turn
    else:
      user_move = input("Your turn: ")
      user_move = chess.Move.from_uci(user_move)
      # Make sure input is a legal move
      while user_move not in legal_moves:
        user_move = chess.Move.from_uci(input("Illegal move, try again: "))
      # Move
      board.push(user_move)

    # Print new FEN
    print("New FEN Position: " + board.board_fen())

    # Stopping condition
    if board.is_game_over():
      print(board)
      if board.outcome().winner == chess.WHITE:
        print("Winner: White")
      elif board.outcome().winner == chess.BLACK:
        print("Winner: Black")
      else:
        print("Draw")
      gameOn = False

  # 4k3/8/8/8/8/4q3/1r5r/4K3 w HAha - 0 1

if __name__ == "__main__":
  main()