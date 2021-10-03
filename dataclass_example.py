from dataclasses import dataclass, field

@dataclass(order=True)#, frozen=True
class Person:
    sort_index: int = field(init=False, repr=False)
    name: str
    job: str
    age: int
    strength: int = 100

    def __post_init__(self):
        self.sort_index = self.age

    def __str__(self):
        return f'{self.name}, {self.job}, {self.strength}'

p1 = Person("Geralt", "Witcher", 30)
p2 = Person("Yennifer", "Sorceress", 25)
p3 = Person("Yennifer", "Sorceress", 25)

print(id(p1))
print(p1)

print(p1 > p2)


