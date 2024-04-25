import pygame
import random

#Színek
White= pygame.Color(255,255,255)
Green= pygame.Color(0,255,0)
red= pygame.Color(255,0,0)
Blue= pygame.Color(0,0,255)
black= pygame.Color(0,0,0)

window_size = 300
cell_size = window_size/3
INF = float('inf')
vec2 = pygame.math.Vector2

class TicTacToe:
    def __init__(self, game):
        self.game = game

        self.game_array=[[(INF),(INF),(INF)],
                         [(INF),(INF),(INF)],
                         [(INF),(INF),(INF)]]
        
        self.player = random.randint(0,1)
        self.game_font = pygame.font.SysFont('Arial',95)
        self.o_surface = self.game_font.render('O', True, Green)
        self.x_surface = self.game_font.render('X',True,red)

        self.win_conditions = [[(0,0),(0,1),(0,2)],
                               [(1,0),(1,1),(1,2)],
                               [(2,0),(2,1),(2,2)],
                               [(0,0),(1,0),(2,0)],
                               [(0,1),(1,1),(2,1)],
                               [(0,2),(1,2),(2,2)],
                               [(0,0),(1,1),(2,2)],
                               [(0,2),(1,1),(2,0)],]
        
        self.winner = None
    
    def run_game_logic(self):
        pygame.display.set_caption('X Következik' if self.player == 1 else 'O következik')
        current_cell = vec2(pygame.mouse.get_pos())//cell_size
        col,row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and self.winner == None:
            self.game_array[row][col] = self.player
            self.player = 0 if self.player == 1 else 1
    
    def check_winner(self):
        for condition in self.win_conditions:
            line_sum = sum([self.game_array[j][i] for i,j in condition])
            if line_sum == 0:
                self.winner = 0
                pygame.display.set_caption('O nyert')
            elif line_sum == 3:
                self.winner = 1
                pygame.display.set_caption('X nyert')
            
            if line_sum in [0,3]:
                self.draw_winner(condition)
                self.draw_winner_text()


    def draw_winner(self,condition):
        x1= condition[0][0]*cell_size+cell_size/2
        y1= condition[0][1]*cell_size+cell_size/2
        start_position= [x1,y1]

        x2= condition[2][0]*cell_size+cell_size/2
        y2= condition[2][1]*cell_size+cell_size/2
        end_position= [x2,y2]

        pygame.draw.line(self.game.screen, Blue, start_position,end_position,int(cell_size)//8  )


    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    obj_position = vec2(x,y) * cell_size
                    
                    if obj == 0:
                        obj_position[0] += cell_size/2
                        obj_position[1] += cell_size/2
                        pygame.draw.circle(self.game.screen,Green,obj_position,int(cell_size/2-5))
                        pygame.draw.circle(self.game.screen,black,obj_position,int(cell_size/2-5-10))
                        #self.game.screen.blit(self.o_surface,obj_position)
                    elif obj == 1:
                        space_lenght = int(cell_size//8)
                        start1=[obj_position[0]+space_lenght,obj_position[1]+space_lenght/2]
                        end1=[obj_position[0]+cell_size-space_lenght, obj_position[1]+cell_size-space_lenght/2]

                        start2 = [obj_position[0]+space_lenght,obj_position[1]+cell_size-space_lenght/2]
                        end2= [obj_position[0]+cell_size-space_lenght, obj_position[1]+space_lenght/2]
                        #self.game.screen.blit(self.x_surface,obj_position)
                        pygame.draw.line(self.game.screen, red, start1, end1,int(cell_size//8))
                        pygame.draw.line(self.game.screen, red, start2, end2,int(cell_size//8))
    def draw_field(self):
        pygame.draw.line(self.game.screen,White,[cell_size, 0],[cell_size,window_size], 5)
        pygame.draw.line(self.game.screen,White,[cell_size*2, 0],[cell_size*2,window_size], 5)
        pygame.draw.line(self.game.screen,White,[0, cell_size],[window_size,cell_size], 5)
        pygame.draw.line(self.game.screen,White,[0, cell_size*2],[window_size,cell_size*2], 5)

    def draw_winner_text(self):
        winner_font = pygame.font.SysFont('Impact', 50)
        winner_surface = winner_font.render('Gratulálunk!', True, Green, black)
        winner_text = '0 nyert' if self.winner == 0 else 'X nyert'
        winner_name_surface = winner_font.render(winner_text, True, Green,black)

        winner_rect = winner_surface.get_rect()
        winner_name_rect = winner_name_surface.get_rect()

        winner_rect.midtop = (window_size/2, window_size/4)
        winner_name_rect.midtop = (window_size/2, window_size/4*3)
        
        self.game.screen.blit(winner_surface,winner_rect)
        self.game.screen.blit(winner_name_surface,winner_name_rect)
    def run(self):
        self.draw_field()
        self.draw_objects()
        self.run_game_logic()
        self.check_winner()
        

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_size,window_size))
        self.clock = pygame.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
    def run(self):
        while True:
            self.handle_events()
            self.tic_tac_toe.run()
            pygame.display.update()
            self.clock.tick(30)


if __name__ == '__main__':
    game = Game()
    game.run()

