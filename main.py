import pygame
import random
import mysql.connector
from datetime import datetime

pygame.init()
logo_image = pygame.image.load("/Users/shaifalijain/Desktop/untitled folder/untitled folder/gamelogo.png")
pygame.display.set_icon(logo_image)

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red1 = (213, 50, 80)
red2 = (255, 0, 0)
dark_green = (0, 100, 0)
green = (179, 94, 4)
green2 = (94, 245, 83)
light_green = (144, 238, 144)
red = (255, 0, 0)  
blue = (50, 153, 213)
green3 = (1, 50, 32)
whitishcolor = (229, 217, 182)
greenishcolor = (164, 190, 123)
greenishcolor2 = (40, 84, 48)

dis_width = 1200
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Hemish Jain')

clock = pygame.time.Clock()

snake_block = 25
snake_speed = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
small_font = pygame.font.Font(None, 36)
smol_font = pygame.font.Font(None, 20)

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [50 , 50])
message_font = pygame.font.Font(None, 60)

def start_game_message():
    dis.fill(green2)  
    message("Press the up arrow key to play", red, (dis_width / 4, dis_height / 2))  
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                waiting = False
def get_player_name():
    name = ""
    name_input = True
    while name_input:
        dis.fill(green2)
        message("Enter Your Name: " + name, black, (dis_width / 6, dis_height / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name_input = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])  
        pygame.draw.rect(dis, green, [x[0] + 1, x[1] + 1, snake_block - 2, snake_block - 2]) 

def message(msg, color, position, font=small_font):
    mesg = message_font.render(msg, True, color) 
    dis.blit(mesg, position)
def draw_apple(apple_x, apple_y):
    pygame.draw.circle(dis, red2, (apple_x, apple_y), snake_block // 2)
    pygame.draw.rect(dis, green3, [apple_x - 2, apple_y - snake_block // 2, 4, snake_block // 2])
def draw_boundary():
    pygame.draw.rect(dis, dark_green, [0, 0, dis_width, snake_block])  
    pygame.draw.rect(dis, dark_green, [0, dis_height - snake_block, dis_width, snake_block]) 
    pygame.draw.rect(dis, dark_green, [0, 0, snake_block, dis_height])  
    pygame.draw.rect(dis, dark_green, [dis_width - snake_block, 0, snake_block, dis_height]) 

def draw_grid():
    for x in range(0, dis_width, snake_block):
        pygame.draw.line(dis, white, (x, 0), (x, dis_height))
    for y in range(0, dis_height, snake_block):
        pygame.draw.line(dis, white, (0, y), (dis_width, y))

def display_leaderboard():
    dis.fill(green2)
    message("Leaderboard", black, (3*dis_width / 8, 50))
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="high_score"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT player_name, score, play_date FROM high_scores ORDER BY score DESC LIMIT 10")
    leaderboard_data = cursor.fetchall()
    name_column_x = dis_width // 16
    score_column_x = 3 * dis_width // 8
    date_column_x = 9 * dis_width // 16
    column_height = 45
    pygame.draw.rect(dis, greenishcolor2, (name_column_x, 90, dis_width // 4, column_height))
    pygame.draw.rect(dis, greenishcolor2, (score_column_x, 90, dis_width // 8, column_height))
    pygame.draw.rect(dis, greenishcolor2, (date_column_x, 90, 3 * dis_width // 8, column_height))

    message("Name", white, (name_column_x + 20, 95), small_font)
    message("Score", white, (score_column_x + 20, 95), small_font)
    message("Date", white, (date_column_x + 20, 95), small_font)
    margin = 10  
    y_position = 150 
    for i, (player_name, score, play_date) in enumerate(leaderboard_data, start=1):
        formatted_date = play_date.strftime('%Y-%m-%d %H:%M:%S')

        pygame.draw.rect(dis, whitishcolor, (name_column_x, y_position, dis_width // 4, column_height))
        pygame.draw.rect(dis, whitishcolor, (score_column_x, y_position, dis_width // 8, column_height))
        pygame.draw.rect(dis, whitishcolor, (date_column_x, y_position, 3 * dis_width // 8, column_height))

        message(player_name, black, (name_column_x + 20, y_position + 10), small_font)
        message(str(score), black, (score_column_x + 20, y_position + 10), small_font)
        message(formatted_date, black, (date_column_x + 20, y_position + 10), small_font)

        y_position += column_height + margin 

    message("Press Q to quit or Press C to play again", red2, (dis_width / 6, dis_height - 100), smol_font)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    gameLoop()

    # Close the database connection
    cursor.close()
    connection.close()



def save_high_score(player_name, score):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
    )

    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS high_score")
    cursor.execute("USE high_score")

    # Create the high_scores table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS high_scores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(255) NOT NULL,
        score INT NOT NULL,
        play_date DATETIME NOT NULL
    )
    """
    cursor.execute(create_table_query)

    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the data into the table
    insert_query = "INSERT INTO high_scores (player_name, score, play_date) VALUES (%s, %s, %s)"
    data = (player_name, score, current_date)

    cursor.execute(insert_query, data)
    connection.commit()

    cursor.close()
    connection.close()


def gameLoop():
    game_over = False
    game_close = False
    name_input_needed = True  # Flag to control player name input

    start_game_message()
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        snake_speed = 5 + (Length_of_snake // 4)
        while game_close:
            dis.fill(green2)
            message("You Lost! Press C-Play Again or L-Leaderboard", red1, (dis_width / 8, dis_height / 2))
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        game_over = True
                        game_close = False
                        display_leaderboard()  # Display the leaderboard when the game ends
                    if event.key == pygame.K_c:
                        gameLoop()

            if name_input_needed:  # Prompt for player name only once
                player_name = get_player_name()
                save_high_score(player_name, Length_of_snake - 1)
                name_input_needed = False  # Set flag to False after input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(green2)
        draw_grid()
        draw_boundary()
        draw_apple(foodx + snake_block // 2, foody + snake_block // 2)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(len(snake_List) - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

