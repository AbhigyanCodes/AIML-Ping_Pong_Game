import pickle
import random

import pygame
import math

from pygame import font
from pygame.locals import *

from NeuralNetwork import NeuralNetwork
import numpy as np

print("")
print("*"*99)
print("*"*96)
print("")

letters = {
    'A': [' *** ', '*   *', '*****', '*   *', '*   *'],
    'B': ['**** ', '*   *', '**** ', '*   *', '**** '],
    'C': [' ****', '*    ', '*    ', '*    ', ' ****'],
    'D': ['**** ', '*   *', '*   *', '*   *', '**** '],
    'E': ['*****', '*    ', '**** ', '*    ', '*****'],
    'F': ['*****', '*    ', '***  ', '*    ', '*    '],
    'G': [' ****', '*    ', '*  **', '*   *', ' ****'],
    'H': ['*   *', '*   *', '*****', '*   *', '*   *'],
    'I': ['*****', '  *  ', '  *  ', '  *  ', '*****'],
    'J': ['*****', '    *', '    *', '*   *', ' *** '],
    'K': ['*   *', '*  * ', '**   ', '*  * ', '*   *'],
    'L': ['*    ', '*    ', '*    ', '*    ', '*****'],
    'M': ['*   *', '** **', '* * *', '*   *', '*   *'],
    'N': ['*   *', '**  *', '* * *', '*  **', '*   *'],
    'O': [' *** ', '*   *', '*   *', '*   *', ' *** '],
    'P': ['**** ', '*   *', '**** ', '*    ', '*    '],
    'Q': [' *** ', '*   *', '*   *', '*  **', ' ** *'],
    'R': ['**** ', '*   *', '**** ', '*  * ', '*   *'],
    'S': [' ****', '*    ', '**** ', '    *', '**** '],
    'T': ['*****', '  *  ', '  *  ', '  *  ', '  *  '],
    'U': ['*   *', '*   *', '*   *', '*   *', ' *** '],
    'V': ['*   *', '*   *', '*   *', ' * * ', '  *  '],
    'W': ['*   *', '*   *', '* * *', '** **', '*   *'],
    'X': ['*   *', ' * * ', '  *  ', ' * * ', '*   *'],
    'Y': ['*   *', ' * * ', '  *  ', '  *  ', '  *  '],
    'Z': ['*****', '   * ', '  *  ', ' *   ', '*****'],
}

string = "PING PONG GAME"

for i in range(5):
    for word in string:
        current_word = word.upper()
        if current_word in letters:
            if word == string[-1]:
                print(letters[current_word][i])
            else:
                print(letters[current_word][i], end='  ')
        else:
            print("     ", end=' ')

print("")
print("*"*96)
print("*"*99)

print("\n\nMENU\n")
print("1. Watch AI Training\n2. Single-Player\n3. Play against Bot")

while True:
    ch=input("\n\nWhat do you want to play? :  ")
    
    if ch=="1":
        class Bar:
            def __init__(self):
                self.length = 120
                self.height = 16
                self.bar_x = (Game1.width-self.length)/2
                self.bar_y = Game1.height-self.height
                self.center_x = (Game1.width/2)
                self.center_y = Game1.height-(self.height/2)
                self.radius = 15
                self.ball_x = self.center_x
                self.ball_y = self.bar_x+(self.length)/2-(2*self.radius)
                self.ball_center_x = random.randrange(15,Game1.width-15)
                self.ball_center_y = random.randrange(Game1.height)
                self.ball_vel_x = 10
                self.ball_vel_y = 10
                self.bar_vel = 0
                self.score = 0
                self.fitness = 0
                self.distance = 0
                self.brain = NeuralNetwork(9,4,2)
            def showBar(self,x,y):
                pygame.draw.rect(Game1.gameDisplay,Game1.black,[x,y,self.length,self.height])

            def showBall(self,x,y):
                pygame.draw.circle(Game1.gameDisplay,Game1.gray,(int(x),int(y)),self.radius)

            def predict(self):
                # Quadrant I
                if self.ball_center_x > self.center_x:
                    dis1 = self.calculateDistance((self.ball_center_x),(self.ball_center_y+self.radius))
                else:
                    dis1 = -1
                dis1/= 1000

                if self.ball_center_x < self.center_x:
                    dis2 = self.calculateDistance((self.ball_center_x),(self.ball_center_y+self.radius))
                else:
                    dis2 = -1
                dis2/= 1000

                if self.ball_center_x == self.center_x:
                    dis3 = self.calculateDistance((self.ball_center_x),(self.ball_center_y+self.radius))
                else:
                    dis3 = -1
                dis3/=1000

                vel_x = self.ball_vel_x
                vel_x/=1000

                vel_y = self.ball_vel_y
                vel_y /= 1000

                dis_wall1 = self.bar_x
                dis_wall2 = (Game1.width) -(self.bar_x)

                dis_ball1 = math.sqrt((self.ball_center_x-self.bar_x)**2+(self.ball_center_y+self.radius-(Game1.height-self.height))**2)
                dis_ball2 = math.sqrt((self.ball_center_x-(self.bar_x+self.length))**2+(self.ball_center_y+self.radius-(Game1.height-self.height))**2)

                dis_wall1/=Game1.width
                dis_wall2/=Game1.width
                dis_ball1/=1000
                dis_ball2/=1000

                inputs = [dis1,dis2,dis3,dis_wall1,dis_wall2,dis_ball1,dis_ball2,vel_x,vel_y]
                inputs = np.array(inputs)
                inputs = np.reshape(inputs,(9,1))
                output = self.brain.feedforward(inputs)
                if output[0]>output[1]:
                    self.moveRight()
                else:
                    self.moveLeft()


            def moveLeft(self):
                if self.bar_x != 0:
                    self.bar_x -= 10
                    self.center_x -= 10
                    self.distance += 1
            def moveRight(self):
                if self.bar_x != (Game1.width - self.length):
                    self.bar_x += 10
                    self.center_x += 10
                    self.distance += 1

            def updateVelocity(self):
                self.ball_center_x += self.ball_vel_x
                self.ball_center_y += self.ball_vel_y

            def isColliding(self):
                if (self.ball_center_y + self.radius) >= (Game1.height - self.height):
                    if self.ball_center_x >= self.bar_x and self.ball_center_x <= (
                            self.bar_x + self.length):
                        return True
            def isCollidingSide(self):
                if self.ball_center_x >= Game1.width or self.ball_center_x - self.radius <= 0:
                    return True

            def isCollidingAbove(self):
                if self.ball_center_y <= 0:
                    return True
            def calculateDistance(self,x,y):
                return math.sqrt((self.center_x-x)**2+(self.center_y-y)**2)


        class Game1():
            width = 900
            height = 600
            black = (0,0,0)
            gray = (70,70,70)
            gameDisplay = pygame.display.set_mode((width, height))
            population = 200
            generation = 1
            bars = []
            savedBars = []
            highscore = []
            score = []
            def __init__(self):

                pygame.init()
                self.clock = pygame.time.Clock()
                self.bar = Bar()
                self.gameLoop()

            def gameLoop(self):
                gameExit = False
                font = pygame.font.SysFont(None,25)
                for i in range(Game1.population):
                    self.bars.append(Bar())
                while not gameExit:

                    msg = 'Gen : ' + str(self.generation)
                    screen_text = font.render(msg,True,(0,0,0))
                    self.gameDisplay.blit(screen_text,[10,10])
                    for bar in self.bars:
                        bar.predict()
                        bar.updateVelocity()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameExit = True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                    print('true')
                                    self.showBest()
                        if bar.isColliding():
                            bar.ball_vel_y = -bar.ball_vel_y
                            bar.score+=10
                        if bar.bar_x == 0 or bar.bar_x == Game1.width-bar.length:
                            bar.score -=1
                        if len(self.highscore)>0:
                            if bar.score >= max(self.highscore):
                                self.bestBar = bar.brain.serialize()
                                self.highscore.append(bar.score)
                        if bar.isCollidingSide():
                            bar.ball_vel_x = -bar.ball_vel_x
                        if bar.isCollidingAbove():
                            bar.ball_vel_y = -bar.ball_vel_y
                        if bar.ball_center_y > Game1.height:
                            self.savedBars.append(bar)
                            self.score.append(bar.score)
                            self.bars.remove(bar)
                            if len(self.bars) == 0:
                                self.generation +=1
                                self.highscore.append(max(self.score))
                                self.score = []
                                ga = GA(self)
                                ga.nextGen()

                        bar.showBar(bar.bar_x,bar.bar_y)
                        bar.showBall(bar.ball_center_x,bar.ball_center_y)
                    pygame.display.update()
                    self.gameDisplay.fill((135,206,250))
                    self.clock.tick(60)
                pygame.quit()
                quit()

            def showBest(self):
                self.gameDisplay.fill((135,206,250))
                bar = Bar()
                bar.brain = pickle.loads(self.bestBar)
                gameExit = False
                while not gameExit:
                    bar.predict()
                    bar.updateVelocity()
                    if bar.isColliding():
                        bar.ball_vel_y = -bar.ball_vel_y
                        bar.score += 1
                    if bar.isCollidingSide():
                        bar.ball_vel_x = -bar.ball_vel_x
                    if bar.isCollidingAbove():
                        bar.ball_vel_y = -bar.ball_vel_y
                    if bar.ball_center_y > Game1.height:
                        return
                    pygame.display.update()
                    self.gameDisplay.fill((135,206,250))
                    self.clock.tick(30)
                pygame.quit()
                #quit()


        class GA(Game1):
            def __init__(self,game):
                self.game = game

            def nextGen(self):
                self.calculateFitness()
                for i in range(len(self.savedBars)):
                    self.game.bars.append(self.pickOne())
                self.game.savedBars = []
                self.savedBars = []

            def calculateFitness(self):
                sum = 0
                self.savedBars = self.game.savedBars
                for i in range(len(self.savedBars)):
                    self.savedBars[i].fitness = (self.savedBars[i].score)**2 + (pow(2,self.savedBars[i].distance))
                    sum+= self.savedBars[i].fitness

                for i in range(len(self.savedBars)):
                    self.savedBars[i].fitness/= sum


            def pickOne(self):
                r = random.uniform(0,1)
                index = 0
                while r>0:
                    r = r-self.savedBars[index].fitness
                    index+=1
                index-=1

                r2 = random.uniform(0,1)
                index2 = 0
                while r2>0:
                    r2 = r2-self.savedBars[index2].fitness
                    index2 +=1
                index2-=1

                child = Bar()
                bar = self.savedBars[index]
                bar2 = self.savedBars[index2]
                child.brain.in_hidden1_weights = bar.brain.crossover(bar.brain.in_hidden1_weights,bar2.brain.in_hidden1_weights)
                child.brain.in_hidden1_biases = bar.brain.crossover(bar.brain.in_hidden1_biases,bar2.brain.in_hidden1_biases)
                child.brain.hidden1_output_weights = bar.brain.crossover(bar.brain.hidden1_output_weights,bar2.brain.hidden1_output_weights)
                child.brain.hidden1_output_biases = bar.brain.crossover(bar.brain.hidden1_output_biases,bar2.brain.hidden1_output_biases)

                child.brain.mutate(child.brain.in_hidden1_weights,0.3)
                child.brain.mutate(child.brain.in_hidden1_biases,0.3)
                child.brain.mutate(child.brain.hidden1_output_weights,0.3)
                child.brain.mutate(child.brain.hidden1_output_biases,0.3)

                return child

        if __name__ == '__main__':
            game = Game1()
    
    elif ch=="2":
        class Bar:
            def __init__(self):
                self.length = 120
                self.height = 16
                self.bar_x = (Game2.width - self.length) / 2
                self.bar_y = Game2.height - self.height
                self.center_x = Game2.width / 2
                self.center_y = Game2.height - (self.height / 2)
                self.radius = 15
                self.ball_x = self.center_x
                self.ball_y = self.bar_x + (self.length / 2) - (2 * self.radius)
                self.ball_center_x = 100
                self.ball_center_y = 100
                self.ball_vel_x = 10
                self.ball_vel_y = 10
                self.bar_vel = 0

            def showBar(self, x, y):
                pygame.draw.rect(Game2.gameDisplay, Game2.black, [x, y, self.length, self.height])

            def showBall(self, x, y):
                pygame.draw.circle(Game2.gameDisplay, Game2.gray, (int(x), int(y)), self.radius)


        class Scoreboard:
            def __init__(self):
                self.score = 0
                self.font = pygame.font.SysFont(None, 25)

            def update(self, gameDisplay):
                text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
                gameDisplay.blit(text, (10, 10))

            def increase_score(self):
                self.score += 1


        class Game2:
            width = 800
            height = 600
            black = (0, 0, 0)
            gray = (70, 70, 70)
            gameDisplay = pygame.display.set_mode((width, height))

            def __init__(self):
                pygame.init()
                self.clock = pygame.time.Clock()
                self.bar = Bar()
                self.scoreboard = Scoreboard()
                self.gameLoop()

            def gameLoop(self):
                gameExit = False
                while not gameExit:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameExit = True
                    keys = pygame.key.get_pressed()
                    self.bar.ball_center_x += self.bar.ball_vel_x
                    self.bar.ball_center_y += self.bar.ball_vel_y
                    if (self.bar.ball_center_y + self.bar.radius) >= (Game2.height - self.bar.height):
                        if self.bar.ball_center_x >= self.bar.bar_x and self.bar.ball_center_x <= (self.bar.bar_x + self.bar.length):
                            self.bar.ball_vel_y = -self.bar.ball_vel_y
                            self.scoreboard.increase_score()
                    if self.bar.ball_center_x >= Game2.width or self.bar.ball_center_x - self.bar.radius <= 0:
                        self.bar.ball_vel_x = -self.bar.ball_vel_x
                    if self.bar.ball_center_y <= 0:
                        self.bar.ball_vel_y = -self.bar.ball_vel_y
                    if self.bar.ball_center_y > Game2.height:
                        gameExit = True
                    if keys[pygame.K_LEFT]:
                        if self.bar.bar_x != 0:
                            self.bar.bar_x -= 10
                            self.bar.center_x -= 10
                    if keys[pygame.K_RIGHT]:
                        if self.bar.bar_x != (Game2.width - self.bar.length):
                            self.bar.bar_x += 10
                            self.bar.center_x += 10
                    self.bar.showBar(self.bar.bar_x, self.bar.bar_y)
                    self.bar.showBall(self.bar.ball_center_x, self.bar.ball_center_y)
                    self.scoreboard.update(self.gameDisplay)
                    pygame.display.update()
                    self.gameDisplay.fill((135, 206, 250))
                    self.clock.tick(30)
                pygame.quit()
                #quit()


        if __name__ == '__main__':
            game = Game2()

    elif ch=="3":
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        WIDTH, HEIGHT = 640, 480
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Ping Pong")

        # Define colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        # Define the paddles
        PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
        PLAYER_PADDLE_X = 20
        COMPUTER_PADDLE_X = WIDTH - 30
        player_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
        computer_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
        player_paddle_speed = 0
        computer_paddle_speed = 0

        # Define the ball
        BALL_RADIUS = 10
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice([-2, 2])
        ball_dy = random.choice([-2, 2])

        # Define the scoreboard
        player_score = 0
        computer_score = 0
        SCORE_FONT = pygame.font.Font(None, 36)
        FINAL_SCORE = 5

        # Set up the clock
        clock = pygame.time.Clock()

        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        player_paddle_speed = -5
                    elif event.key == K_DOWN:
                        player_paddle_speed = 5
                elif event.type == KEYUP:
                    if event.key == K_UP or event.key == K_DOWN:
                        player_paddle_speed = 0

            # Update the player's paddle position
            player_paddle_y += player_paddle_speed
            if player_paddle_y < 0:
                player_paddle_y = 0
            elif player_paddle_y > HEIGHT - PADDLE_HEIGHT:
                player_paddle_y = HEIGHT - PADDLE_HEIGHT

            # Update the computer's paddle position based on the ball position
            if ball_y < computer_paddle_y:
                computer_paddle_speed = -3
            elif ball_y > computer_paddle_y + PADDLE_HEIGHT:
                computer_paddle_speed = 3
            else:
                computer_paddle_speed = 0
            computer_paddle_y += computer_paddle_speed
            if computer_paddle_y < 0:
                computer_paddle_y = 0
            elif computer_paddle_y > HEIGHT - PADDLE_HEIGHT:
                computer_paddle_y = HEIGHT - PADDLE_HEIGHT

            # Update the ball position
            ball_x += ball_dx
            ball_y += ball_dy

            # Check collision with paddles
            if ball_x <= PLAYER_PADDLE_X + PADDLE_WIDTH and player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT:
                ball_dx = abs(ball_dx)
            elif ball_x >= COMPUTER_PADDLE_X - BALL_RADIUS and computer_paddle_y <= ball_y <= computer_paddle_y + PADDLE_HEIGHT:
                # Introduce a chance for the computer to miss hitting the ball
                if random.random() < 0.5:
                    ball_dx = abs(ball_dx)  # Computer misses the ball
                else:
                    ball_dx = -abs(ball_dx)

            # Check collision with walls
            if ball_y <= 0 or ball_y >= HEIGHT - BALL_RADIUS:
                ball_dy = -ball_dy

            # Check if the ball is out of bounds
            if ball_x < 0:
                # Player loses
                computer_score += 1
                if computer_score == FINAL_SCORE:
                    running = False
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = random.choice([-2, 2])
                ball_dy = random.choice([-2, 2])
            elif ball_x > WIDTH - BALL_RADIUS:
                # Player wins
                player_score += 1
                if player_score == FINAL_SCORE:
                    running = False
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = random.choice([-2, 2])
                ball_dy = random.choice([-2, 2])

            # Clear the screen
            WINDOW.fill(BLACK)

            # Draw the paddles
            pygame.draw.rect(WINDOW, WHITE, (PLAYER_PADDLE_X, player_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(WINDOW, WHITE, (COMPUTER_PADDLE_X, computer_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

            # Draw the ball
            pygame.draw.circle(WINDOW, WHITE, (ball_x, ball_y), BALL_RADIUS)

            # Draw the scoreboard
            player_text = SCORE_FONT.render(f"Player: {player_score}", True, WHITE)
            computer_text = SCORE_FONT.render(f"Computer: {computer_score}", True, WHITE)
            WINDOW.blit(player_text, (20, 20))
            WINDOW.blit(computer_text, (WIDTH - computer_text.get_width() - 20, 20))

            # Update the display
            pygame.display.update()

            # Limit the frame rate
            clock.tick(120)

        # Show the winner
        winner_text = SCORE_FONT.render("Player Wins!" if player_score == FINAL_SCORE else "Computer Wins!", True, WHITE)
        winner_pos = (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2)
        WINDOW.blit(winner_text, winner_pos)
        pygame.display.update()

        # Wait for a few seconds before quitting
        pygame.time.wait(3000)

        # Quit the game
        pygame.quit()
    
    else:
        print("BYE! SEE YOU AGAIN!")
        break