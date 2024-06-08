# Game setup
WIDTH = 800
HEIGHT = 800
FPS = 120
TITRE = 'Projet OO'
ZOOM = 1
DROP_RATE = 0.1

# Player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 1000
PLAYER_MAX_HEALTH = 1000

# Zombie settings
ZOMBIE_SPEED = 1
ZOMBIE_HEALTH = 3
ZOMBIE_ATTACK_COOLDOWN = 25

# Skeleton settings
SKELETON_SPEED = 3
SKELETON_HEALTH = 1
SKELETON_ATTACK_COOLDOWN = 50

# Nohead settings
NOHEAD_SPEED = 0.5
NOHEAD_HEALTH = 7
NOHEAD_ATTACK_COOLDOWN = 15

# Golem settings
GOLEM_SPEED = 1
GOLEM_HEALTH = 50
GOLEM_ATTACK_COOLDOWN = 50

#NPC settings
NPC_SPEED = 1
NPC_HEALTH = 10
NPC_ATTACK_COOLDOWN = 25

# Bullet settings
BULLET_SPEED = 2
ATTACK_COOLDOWN = 1 # Temps entre chaque tir 
BULLET_LIFETIME = 200 # Durée de vie d'une balle
BULLET_SCALE = 8
BULLET_DAMAGE = 3

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

# Uzi settings
UZI_INFO = "rapide, mais peu puissant"
UZI_SPEED = 3
UZI_DAMAGE = 1
UZI_SCALE = 9
UZI_COLOR = (95,56,75)

# Bazooka settings
BAZOOKA_INFO = "puissant mais lent"
BAZOOKA_SPEED = 1
BAZOOKA_DAMAGE = 5
BAZOOKA_SCALE = 5
BAZOOKA_COLOR = (5,5,5)

# Pistol settings
PISTOL_INFO = "arme équilibré"
PISTOL_SPEED = 2
PISTOL_DAMAGE = 2
PISTOL_SCALE = 5
PISTOL_COLOR = (18,18,8)

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
    ('npc', "Hello, adventurer!"),
    ('player', "Hello! What do you need?"),
    ('npc', "I have some quests for you."),
    ('player', "What kind of quests?"),
    ('npc', "Choose wisely!")
]

NPC_DIALOGUE_10_MONSTER_QUEST = [
    ('npc', "Oh, enfin quelqu'un de courageux ! Écoute, j'ai vraiment besoin de ton aide. Ces monstres... ils sont partout. Nos défenses sont en ruines, et les habitants sont terrifiés."),
    ('player', "Je suis ici pour aider. Que veux-tu que je fasse ?"),
    ('npc', "Pour commencer, nous devons réduire leur nombre. Si tu pouvais tuer dix de ces créatures, cela nous donnerait un peu de répit et de temps pour renforcer nos défenses."),
    ('player', "Dix monstres, c'est noté. Où les trouver ?"),
    ('npc', "Ils rôdent principalement autour des anciennes fermes à l'est de la ville et près de la forêt de Blackwood. Fais attention, ils sont dangereux. Veux-tu accepter?"),
    ('player', "Je m'en occupe. Je reviendrai une fois le travail terminé."),
    ('npc', "Merci, vraiment. Que la chance soit de ton côté. Reviens sain et sauf.")
]

NPC_DIALOGUE_HEART_MISSION= [
('npc', "Salut, aventurier!"),
('player', "Bonjour! Comment puis-je vous aider?"),
('npc', "J'ai une quête pour toi."),
('player', "Quel genre de quête?"),
('npc', "Écoute bien."),
('npc', "Ta mission est de collecter 5 dents et 5 cœurs de monstres."),
('player', "D'accord, mais où puis-je trouver ces dents et ces cœurs?"),
('npc', "Les dents des monstres peuvent être récupérées dans les bois à l'ouest de la ville, où les créatures rôdent."),
('npc', "Quant aux cœurs, ils sont souvent trouvés dans les grottes au nord, où les monstres les plus redoutables se cachent."),
('player', "Compris, je vais m'en occuper."),
('npc', "Fais attention, les monstres peuvent être dangereux. Bonne chance, aventurier.")
]
NPC_DIALOGUE_HIDDEN_OBJECT = [
('npc', "Salut, aventurier!"),
('player', "Bonjour! Que puis-je faire pour vous?"),
('npc', "J'ai une autre quête pour toi."),
('player', "Je suis prêt à aider. De quoi s'agit-il?"),
('npc', "Écoute attentivement."),
('npc', "Il y a un objet précieux caché quelque part dans la ville."),
('npc', "Ta mission est de le trouver."),
('player', "Un objet caché? Pouvez-vous me donner plus de détails?"),
('npc', "Malheureusement, je ne sais pas exactement où il se trouve."),
('npc', "Cependant, des rumeurs disent qu'il est caché dans une vieille maison abandonnée près de la rivière."),
('player', "Je vais aller jeter un coup d'œil. Merci pour l'information."),
('npc', "Bon courage, aventurier. Que la chance soit avec toi.")
]
