# Game setup
WIDTH = 800
HEIGHT = 800
FPS = 120
TITRE = 'Projet OO'
ZOOM = 1
DROP_RATE = 0.1

# Player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 150
PLAYER_MAX_HEALTH = 300
PLAYER_SHOOT_DAMAGE = 1

# Zombie settings
ZOMBIE_SPEED = 1
ZOMBIE_HEALTH = 3
ZOMBIE_ATTACK_COOLDOWN = 25
ZOMBIE_DAMAGE = 1

# Skeleton settings
SKELETON_SPEED = 3
SKELETON_HEALTH = 1
SKELETON_ATTACK_COOLDOWN = 50
SKELETON_DAMAGE = 2

# Nohead settings
NOHEAD_SPEED = 0.5
NOHEAD_HEALTH = 7
NOHEAD_ATTACK_COOLDOWN = 15
NOHEAD_DAMAGE = 5

# Golem settings
GOLEM_SPEED = 1
GOLEM_HEALTH = 50
GOLEM_ATTACK_COOLDOWN = 50
GOLEM_DAMAGE = 3
GOLEM_SHOOT_COOLDOWN = 200
GOLEM_SHOOT_LIFETIME = 250
GOLEM_SHOOT_DAMAGE = 5
GOLEM_SHOOT_SPEED = 1
GOLEM_SHOOT_RADIUS = 10
GOLEM_SHOOT_COLOR = (255,0,0)

#NPC settings
NPC_SPEED = 1
NPC_HEALTH = 10
NPC_ATTACK_COOLDOWN = 25

# basic bullet settings
BULLET_SPEED = 1
ATTACK_COOLDOWN = 10 
BULLET_LIFETIME = 200 
BULLET_DAMAGE = 1
BULLET_RADIUS = 5
BULLET_COLOR = (255,255,255)

# Super bullet settings
SUPER_BULLET_SPEED = 10
SUPER_BULLET_LIFETIME = 50
SUPER_BULLET_DAMAGE = 5
SUPER_BULLET_RADIUS = 20
SUPER_BULLET_COLOR = (0,255,0)

# Sniper bullet settings
SNIPER_BULLET_SPEED = 15
SNIPER_BULLET_LIFETIME = 200
SNIPER_BULLET_DAMAGE = 10
SNIPER_BULLET_RADIUS = 10
SNIPER_BULLET_COLOR = (0,56,255)



# Appel setting
APPLE_INFO = 'le fruit préferé de Newton' 
APPLE_SCALE = 4
APPLE_COLOR = (0,255,0)
APPLE_HEAL = 15

# Berry setting
BERRY_INFO = "souvent récolté près des arbustes"
BERRY_SCALE = 1
BERRY_COLOR = (255,0,1)
BERRY_HEAL = 1

# Military settings
MILITARY_INFO = "armure porté par l'armée americaine"
MILITARY_SCALE = 3
MILITARY_COLOR = (45,5,5)
MILITARY_SHIELD = 3

# Police settings
POLICE_INFO = "blindage de la police anti émeute"
POLICE_SCALE = 5
POLICE_COLOR = (96,3,8)
POLICE_SHIELD = 3

# Tooth settings
TOOTH_INFO = "dent de monstre"
TOOTH_SCALE = 2
TOOTH_COLOR = (255,255,255)

# Heart settings
HEART_INFO = "coeur de monstre"
HEART_SCALE = 3
HEART_COLOR = (255,0,0)

#pelluche settings
PELUCHE_INFO = "objet mystique"
PELUCHE_SCALE = 4
PELUCHE_COLOR = (128, 64, 32)

#================================
# Dialogues NPC-Joueur:
NPC_DIALOGUE_BASIC = [
    ('Brançois Furniaux', "Salut, tu dois être Billy"),
    ('Billy', "Oui c'est bien moi."),
    ('Brançois Furniaux', "J'ai quelques quêtes pour toi"),
    ('Billy', "Quelle genre de quêtes?"),
    ('Brançois Furniaux', "Les voici!")
]

NPC_DIALOGUE_10_MONSTER_QUEST = [
    ('Brançois Furniaux', "Oh, enfin quelqu'un de courageux ! Écoute, j'ai vraiment besoin de ton aide. Ces monstres... ils sont partout. Nos défenses sont en ruines, et les habitants sont terrifiés."),
    ('Billy', "Je suis ici pour aider. Que veux-tu que je fasse ?"),
    ('Brançois Furniaux', "Pour commencer, nous devons réduire leur nombre. Si tu pouvais tuer dix de ces créatures, cela nous donnerait un peu de répit et de temps pour renforcer nos défenses."),
    ('Billy', "Dix monstres, c'est noté. Où les trouver ?"),
    ('Brançois Furniaux', "Ils rôdent principalement autour des anciennes fermes à l'est de la ville et près de la forêt de Blackwood. Fais attention, ils sont dangereux. Veux-tu accepter?"),
    ('Billy', "Je m'en occupe. Je reviendrai une fois le travail terminé."),
    ('Brançois Furniaux', "Merci, vraiment. Que la chance soit de ton côté. Reviens sain et sauf.")
]

NPC_DIALOGUE_HEART_MISSION = [
('Brançois Furniaux', "Salut, aventurier!"),
('Billy', "Bonjour! Comment puis-je vous aider?"),
('Brançois Furniaux', "J'ai une quête pour toi."),
('Billy', "Quel genre de quête?"),
('Brançois Furniaux', "Écoute bien."),
('Brançois Furniaux', "Ta mission est de collecter 5 cœurs de monstres."),
('Billy', "D'accord, mais où puis-je trouver ces cœurs?"),
('Brançois Furniaux', "Les cœurs sont souvent trouvés dans les grottes au nord, où les monstres les plus redoutables se cachent."),
('Billy', "Compris, je vais m'en occuper."),
('Brançois Furniaux', "Fais attention, les monstres peuvent être dangereux. Bonne chance, aventurier.")
]
NPC_DIALOGUE_HIDDEN_OBJECT = [
('Brançois Furniaux', "Salut, aventurier!"),
('Billy', "Bonjour! Que puis-je faire pour vous?"),
('Brançois Furniaux', "J'ai une autre quête pour toi."),
('Billy', "Je suis prêt à aider. De quoi s'agit-il?"),
('Brançois Furniaux', "Écoute attentivement."),
('Brançois Furniaux', "Il y a un objet précieux caché quelque part dans la ville."),
('Brançois Furniaux', "Ta mission est de le trouver."),
('Billy', "Un objet caché? Pouvez-vous me donner plus de détails?"),
('Brançois Furniaux', "Malheureusement, je ne sais pas exactement où il se trouve."),
('Brançois Furniaux', "Cependant, des rumeurs disent qu'il est caché dans une vieille maison abandonnée près de la rivière."),
('Billy', "Je vais aller jeter un coup d'œil. Merci pour l'information."),
('Brançois Furniaux', "Bon courage, aventurier. Que la chance soit avec toi.")
]
NPC_DIALOGUE_NOT_FIRST = [
    ('Brançois Furniaux', "Salut, Billy! Tu es de retour?"),
    ('Billy', "Bonjour! Je suis bien de retour hahah!")
]
NPC_DIALOGUE_TOOTH_MISSION = [
('Brançois Furniaux', "Salut, aventurier!"),
('Billy', "Bonjour! Comment puis-je vous aider?"),
('Brançois Furniaux', "J'ai une quête pour toi."),
('Billy', "Quel genre de quête?"),
('Brançois Furniaux', "Écoute bien."),
('Brançois Furniaux', "Ta mission est de collecter 5 dents de monstres."),
('Billy', "D'accord, mais où puis-je trouver ces dents?"),
('Brançois Furniaux', "Les dents des monstres peuvent être récupérées dans les bois à l'ouest de la ville, où les créatures rôdent."),
('Billy', "Compris, je vais m'en occuper."),
('Brançois Furniaux', "Fais attention, les monstres peuvent être dangereux. Bonne chance, aventurier.")
]
