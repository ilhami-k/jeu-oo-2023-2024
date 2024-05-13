class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print(f"{item} n'est pas dans l'inventaire.")

    def afficher(self):
        print("Inventaire :")
        for item in self.items:
            print(item.nom)
