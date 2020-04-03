import random as r
import numpy as np
import matplotlib.pyplot as plt

x_max = 20
x_min = -20
y_max = 20
y_min = -20
infected_list = [True, False]
number_of_people = 1000
number_of_police = 5
days = 50
resources_positions = [[0, 0], [x_max/2, y_max/2], [-x_max/2, y_max/2], [x_max/2, -y_max/2], [-x_max/2, -y_max/2]]
person_list = []
police_list = []

class Person():

    def __init__(self, pos_x, pos_y, age, infected):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.age = age
        self.health = 100 - age
        self.infected = infected
        try:
            self.recklessness = 100/age
        except ZeroDivisionError:
            # If age = 0
            self.recklessness = 0

    def get_position(self):
        return [self.pos_x, self.pos_y]

    def walk(self):
        self.pos_x = r.randint(-5, 5)
        self.pos_y = r.randint(-5, 5)

    def drive(self):
        if self.age >= 18:
            self.pos_x = r.randint(x_min, x_max)
            self.pos_y = r.randint(y_min, y_max)

    def kill(self):
        if self.health == 0:
            del self

class Police():

    def __init__(self, pos_x, pos_y, age, infected):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.age = age
        self.health = 100 - age
        self.infected = infected

    def drive(self):
        self.pos_x = r.randint(x_min, x_max)
        self.pos_y = r.randint(y_min, y_max)

    def get_position(self):
        return [self.pos_x, self.pos_y]

def evolve():

    for day in range(days):
        for person in person_list:
            move = r.uniform(0, 1)
            if move > 0.7 and person.recklessness > 5:
                if person.age >= 18:
                    person.drive()
                else:
                    person.walk()
            per_pos = person.get_position()
            for police in police_list:
                if police.get_position() == per_pos:
                    if person.infected:
                        person.kill()
            if per_pos in resources_positions:
                person.infected = False
                person.health += 5
            for other_person in person_list:
                if other_person.get_position() == per_pos and other_person != person:
                    if other_person.infected:
                        person.infected = True
                    if person.infected:
                        other_person.infected = True
            if person.infected:
                person.health -= 10
                if person.health < 50 and r.uniform(0, 1) < 0.02:
                    person.kill()

        for popo in police_list:
            popo.drive()

def statistics():
    X = []
    Y = []
    X_inf = []
    Y_inf = []
    for person in person_list:
        if person.infected:
            X_inf.append(person.pos_x)
            Y_inf.append(person.pos_y)
        else:
            X.append(person.pos_x)
            Y.append(person.pos_y)
    return X, Y, X_inf, Y_inf

person_list.append(Person(r.randint(x_min, x_max), r.randint(y_min, y_max),
                              r.randint(1, 91), True))
for i in range(number_of_people):
    person_list.append(Person(r.randint(x_min, x_max), r.randint(y_min, y_max),
                              r.randint(1, 91), False))

for i in range(number_of_police):
    police_list.append(Police(r.randint(x_min, x_max), r.randint(y_min, y_max),
                              r.randint(20, 61), r.sample(infected_list, 1)[0]))

evolve()
x, y, x_inf, y_inf = statistics()
plt.scatter(x, y, color = 'k')
plt.scatter(x_inf, y_inf, color = 'r')
x_res = [resources_positions[i][0] for i in range(len(resources_positions))]
y_res = [resources_positions[i][1] for i in range(len(resources_positions))]
plt.scatter(x_res, y_res, marker = 'x', color = 'g')
plt.title(f'Corona city after {days} days\nOne person infected on day 0')
plt.legend(['Not infected', 'Infected', 'Resources'])
plt.grid(alpha = 0.5)
plt.xticks(np.arange(x_min, x_max), labels = [])
plt.yticks(np.arange(y_min, y_max), labels =[])
plt.show()
