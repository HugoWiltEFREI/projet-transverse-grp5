number_of_life = 3
player_velocity_multi = 1
display_dead = 0
val = 0
show_menu = 1
loop = 1
affichage = 1
zone_de_text = ""
moving_right = False
moving_left = False
stay_right = True
momentum = 0
now = 0
level = 1
derniereaction = 0
mode = "menu"
falling = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
val_sound = 50
val_music = 50
is_running = True

# Variables de la balle
gravite = 9.81
balle_lancee = False
ball_cpt = 0
temps = 0.5
liste_ball = []
# Positions de la balle :
ball_x = 0
ball_y = 0
cpt = 0
# liste des tiles cassés par la balle
list_broken = []
#liste des symboles de tuiles pouvant être cassées par la balle :
list_symbol_breakable = ["a"]