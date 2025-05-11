def table_tennis_game():
    print("🏓 Welcome to Table Tennis Score Tracker!")
     
    player_a = input("Enter name for Player A: ")
    player_b = input("Enter name for Player B: ")
    
    while True:
        server = input(f"Who will serve first? ({player_a}/{player_b}): ")
        if server == player_a or server == player_b:
            break
        print("⚠️ Invalid input. Please enter exactly as the player names.")
 
    score = {player_a: 0, player_b: 0}
    round_num = 1
    history = []
    
    total_points_played = 0

    while True:
        print(f"\nRound {round_num}:")
        while True:
            point_winner = input(f"Who scores the point? ({player_a}/{player_b}): ")
            if point_winner == player_a or point_winner == player_b:
                break
            print("⚠️ Invalid input. Please enter exactly as the player names.")
        
        score[point_winner] += 1
        total_points_played += 1
        history.append(f"Round {round_num}: {point_winner} scored")
        round_num += 1

        if max(score[player_a], score[player_b]) >= 10 and abs(score[player_a] - score[player_b]) <= 1:
            
            if total_points_played % 2 == 1:
                server = player_a if server == player_b else player_b
        else:
            if total_points_played % 2 == 0:
                server = player_a if server == player_b else player_b

        print(f"[{player_a} {score[player_a]} - {score[player_b]} {player_b}] ➤ Server: {server}")

        if (score[player_a] >= 11 or score[player_b] >= 11) and abs(score[player_a] - score[player_b]) >= 2:
            winner = player_a if score[player_a] > score[player_b] else player_b
            print(f"\n🎉 {winner} wins the game!")
            print(f"🏁 Final Score: {player_a} {score[player_a]} - {score[player_b]} {player_b}")
            print("\n📜 Match History:")
            for h in history:
                print("-", h)
            break

table_tennis_game()