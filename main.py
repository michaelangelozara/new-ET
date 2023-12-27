import pygame
import os
import cv2
import random

#initialize pygame
pygame.init()

TITTLE = "Bubble Buster"

WIDTH, HEIGHT = 1000, 600

BUTTON_WIDTH, BUTTON_HEIGHT = 120, 75

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITTLE, icontitle="")

video = cv2.VideoCapture('start.mp4')

START_BUTTON = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 - 60, 220, 120)
START_BUTTON = START_BUTTON.inflate(-21, -21)

START_BUTTON_IMAGE = pygame.image.load('button.png')
START_BUTTON_IMAGE = pygame.transform.scale(START_BUTTON_IMAGE, (220, 120))

bullet_image = pygame.image.load('character_assets/bullet.png')

FONT = pygame.font.SysFont('Comic Sans MS', 30)

TEXT_SURFACE = FONT.render('Start', True, (255, 255, 255))

BALLOONS_DIMENSION = (50, 50)
CHARACTER_WIDTH, CHARACTER_HEIGHT = 60, 90

CHARACTER_IMAGE1 = pygame.image.load('character_assets/c1.png')
CHARACTER_IMAGE2 = pygame.image.load('character_assets/c2.png')
CHARACTER_IMAGE3 = pygame.image.load('character_assets/c3.png')
CHARACTER_IMAGE4 = pygame.image.load('character_assets/c4.png')
CHARACTER_IMAGE5 = pygame.image.load('character_assets/c5.png')

list_of_character_image = [CHARACTER_IMAGE1, CHARACTER_IMAGE2, CHARACTER_IMAGE3, CHARACTER_IMAGE4, CHARACTER_IMAGE5]

IMAGE_POSITION = 0

SCORE_FONT = pygame.font.SysFont("Arial", 30)
SCORE_COLOR_RED = (255, 255, 255)

BALLOON_IMAGE1 = pygame.image.load("balloon1.png");
BALLOON_IMAGE2 = pygame.image.load("balloon2.png");
BALLOON_IMAGE3 = pygame.image.load("balloon3.png");

list_of_balloons = [BALLOON_IMAGE1, BALLOON_IMAGE2, BALLOON_IMAGE3]

# initializing main background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("main_background.png")), (WIDTH, HEIGHT))

def flip_image(image):
    return pygame.transform.flip(image, True, False)

def is_video_ended():
  success, video_image = video.read()
  if success:
    # Convert the image from BGR to RGB format
    video_image = cv2.cvtColor(video_image, cv2.COLOR_BGR2RGB)

    # Create a pygame surface from the NumPy array
    video_surface = pygame.surfarray.make_surface(video_image)
    flipped = pygame.transform.flip(video_surface, True, False)

    WIN.blit(pygame.transform.rotate(flipped, 90), (0,0))
    return False
  else:
    return True

  
def ctr_left_clicked(CHARACTER, key_pressed, IMAGE_POSITION, CHARACTER_VEL, frame_counter):
  if key_pressed[pygame.K_LEFT] and (CHARACTER.x - CHARACTER_VEL) > 0:
      CHARACTER.x -= CHARACTER_VEL
      frame_counter = (frame_counter + 1) % 10
      if frame_counter == 0:
          IMAGE_POSITION = (IMAGE_POSITION - 1) % len(list_of_character_image)
      WIN.blit(flip_image(list_of_character_image[IMAGE_POSITION]), (CHARACTER.x, CHARACTER.y))
  return IMAGE_POSITION, CHARACTER_VEL, frame_counter

def ctr_right_clicked(CHARACTER, key_pressed, IMAGE_POSITION, CHARACTER_VEL, frame_counter):
  if key_pressed[pygame.K_RIGHT] and (CHARACTER.x + CHARACTER_VEL) < WIDTH - 70:
    CHARACTER.x += CHARACTER_VEL
    frame_counter = (frame_counter + 1) % 10
    if frame_counter == 0:
        IMAGE_POSITION = (IMAGE_POSITION + 1) % len(list_of_character_image)
    WIN.blit(list_of_character_image[IMAGE_POSITION], (CHARACTER.x, CHARACTER.y))
  return IMAGE_POSITION, CHARACTER_VEL, frame_counter

def start_balloons_fall(balloons_rect, list_of_balloons, BALLOONS_VEL):
  WIN.blit(list_of_balloons[0], (balloons_rect[0].x, balloons_rect[0].y))
  balloons_rect[0].y += BALLOONS_VEL

  if balloons_rect[0].y >= HEIGHT:
    WIN.blit(list_of_balloons[1], (balloons_rect[1].x, balloons_rect[1].y))
    balloons_rect[1].y += BALLOONS_VEL

  if balloons_rect[1].y >= HEIGHT:
    WIN.blit(list_of_balloons[2], (balloons_rect[2].x, balloons_rect[2].y))
    balloons_rect[2].y += BALLOONS_VEL

  if (balloons_rect[0].y and balloons_rect[1].y and balloons_rect[2].y) >= HEIGHT:
    balloons_rect[0].y = 0
    balloons_rect[1].y = 0
    balloons_rect[2].y = 0

    balloons_rect[0].x = random.randint(0, WIDTH - 70)
    balloons_rect[1].x = random.randint(0, WIDTH - 70)
    balloons_rect[2].x = random.randint(0, WIDTH - 70)

  return BALLOONS_VEL

def fire(bullet_image, bullet_rect, bullet_status, character_position, is_ready_to_fire, BULLET_VEL):
  if not bullet_status:
    bullet_rect.x = character_position
    WIN.blit(bullet_image, (bullet_rect.x, bullet_rect.y))
    bullet_rect.y -= BULLET_VEL
    is_ready_to_fire = False
    if bullet_rect.y <= 0:
      bullet_rect.y = 600
      bullet_status = True
      is_ready_to_fire = True

  return bullet_status, bullet_rect, is_ready_to_fire, BULLET_VEL
      
def text_draw(text, font, text_color, x, y):
  img_text = font.render(text, True, text_color)
  WIN.blit(img_text, (x, y))

def update_highest_score(score):
  highest_score = open('highest_score.txt', 'r')
  if score > int(highest_score.read()):
    score_file = open('highest_score.txt', 'w')
    score_file.write(str(score))
    score_file.close()

def get_highest_score():
  highest_score = open('highest_score.txt', 'r')
  return highest_score


def draw_window(CHARACTER, start_button_clicked, key_pressed, IMAGE_POSITION, last_direction, character_score, collision_occurred, run, balloons_rect, list_of_balloons, random_number_pos_x, bullet_status, bullet_rect, character_position, is_ready_to_fire, CHARACTER_VEL, BALLOONS_VEL, BULLET_VEL, next_stage_balloon_vel, frame_counter):
  if is_video_ended() and not start_button_clicked:
    pygame.draw.ellipse(WIN, (0, 255, 0), START_BUTTON)
    START_BUTTON_IMAGE.blit(TEXT_SURFACE, (110 - 35, 60 - 25))
    WIN.blit(START_BUTTON_IMAGE, (WIDTH // 2 - 110, HEIGHT // 2 - 60))
  elif is_video_ended() and start_button_clicked:
    text_draw("Scores : " + str(character_score), SCORE_FONT, SCORE_COLOR_RED, 20, 20)
    text_draw("Highest Score : " + str(get_highest_score().read()), SCORE_FONT, SCORE_COLOR_RED, 20, 50)
    BALLOONS_VEL = start_balloons_fall(balloons_rect, list_of_balloons, BALLOONS_VEL)
    bullet_status, bullet_rect, is_ready_to_fire, BULLET_VEL = fire(bullet_image, bullet_rect, bullet_status, character_position, is_ready_to_fire, BULLET_VEL)
    if last_direction == "right":
      WIN.blit(list_of_character_image[IMAGE_POSITION], (CHARACTER.x, CHARACTER.y))
    else:
      WIN.blit(flip_image(list_of_character_image[IMAGE_POSITION]), (CHARACTER.x, CHARACTER.y))
    if key_pressed[pygame.K_RIGHT]:
      IMAGE_POSITION, CHARACTER_VEL, frame_counter = ctr_right_clicked(CHARACTER, key_pressed, IMAGE_POSITION, CHARACTER_VEL, frame_counter)
      last_direction = "right"
    if key_pressed[pygame.K_LEFT]:
      IMAGE_POSITION, CHARACTER_VEL, frame_counter = ctr_left_clicked(CHARACTER, key_pressed, IMAGE_POSITION, CHARACTER_VEL, frame_counter)
      last_direction = "left"

  for bal in balloons_rect:
    if bullet_rect.colliderect(bal):
      bal.y = 0
      bal.x = random.randint(0, WIDTH - 70)
      bullet_rect.y = 600
      is_ready_to_fire = True
      bullet_status = True
      character_score += 1

      if character_score % next_stage_balloon_vel == 0:
        BALLOONS_VEL += 1

    #this condition handles if the player is game over
    if bal.y >= HEIGHT and not bal.colliderect(bullet_rect):
      is_game_over = True
      CHARACTER_VEL = 0
      BALLOONS_VEL = 0
      BULLET_VEL = 0
      text_draw("Game Over", SCORE_FONT, (0, 255, 0), WIDTH // 2 - 15, HEIGHT // 2 - 15)


  update_highest_score(character_score)
  pygame.display.update()
  return IMAGE_POSITION, last_direction, character_score, collision_occurred, run, random_number_pos_x, bullet_status, CHARACTER, bullet_rect, is_ready_to_fire, CHARACTER_VEL, BALLOONS_VEL, BULLET_VEL, frame_counter

def main():

  FPS = 120

  #initialize the time clock to handle fps
  clock = pygame.time.Clock()

  CHARACTER_VEL = 6
  BALLOONS_VEL = 1
  BULLET_VEL = 15

  next_stage_balloon_vel = 10


  start_button_clicked = False

  # This variable handles the constant x pos of the character every time the space key triggered
  character_position = ""

  is_ready_to_fire = True

  character_score = 0
  CHARACTER = pygame.Rect(WIDTH // 2, HEIGHT - 116, CHARACTER_WIDTH, CHARACTER_HEIGHT)

  bullet_rect = pygame.Rect(WIDTH // 2, HEIGHT, 50, 90)
  bullet_status = True

  random_number_pos_x = random.randint(0, 2)

  balloon_rect1 = pygame.Rect(random.randint(0, WIDTH - 70), 0, 100, 100)
  balloon_rect2 = pygame.Rect(random.randint(0, WIDTH - 70), 0, 100, 100)
  balloon_rect3 = pygame.Rect(random.randint(0, WIDTH - 70), 0, 100, 100)

  balloons_rect = [balloon_rect1, balloon_rect2, balloon_rect3]
    
  collision_occurred = False

  IMAGE_POSITION = 0
  last_direction = "right"

  frame_counter = 0

  run = True
  while run:
    clock.tick(FPS)
    #validating if the video is ended
    if is_video_ended():
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False  

        elif event.type == pygame.KEYDOWN:
            if is_ready_to_fire:
              if event.key == pygame.K_SPACE:
                bullet_status = False
                character_position = CHARACTER.x

      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the button is clicked
        if START_BUTTON.collidepoint(event.pos):
          start_button_clicked = True
              
    key_pressed = pygame.key.get_pressed()    
    WIN.blit(BACKGROUND, (0,0))
    is_video_ended()
    IMAGE_POSITION, last_direction, character_score, collision_occurred, run, random_number_pos_x, bullet_status, CHARACTER, bullet_rect, is_ready_to_fire, CHARACTER_VEL, BALLOONS_VEL, BULLET_VEL, frame_counter = draw_window(CHARACTER, start_button_clicked, key_pressed, IMAGE_POSITION, last_direction, character_score, collision_occurred, run, balloons_rect, list_of_balloons, random_number_pos_x, bullet_status, bullet_rect, character_position, is_ready_to_fire, CHARACTER_VEL, BALLOONS_VEL, BULLET_VEL, next_stage_balloon_vel, frame_counter)

    

  pygame.quit()


if __name__ == "__main__":
  main()
