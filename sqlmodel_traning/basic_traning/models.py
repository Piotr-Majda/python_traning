from decimal import Decimal
import random
import uuid
from typing import List

from sqlmodel import Field, Relationship, SQLModel


#### Changed to Many to Many ! Many Heros can join one Team // One Team can have many heroes // One to Many type of relation
class TeamBase(SQLModel):
    name: str = Field(default=None, index=True)
    headquarters: str = Field(default=None)


class Team(TeamBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    heroes: List['Hero'] = Relationship(back_populates='team')
    

class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: uuid.UUID
    

class TeamPublicWithHeroes(TeamPublic):
    heroes: list['HeroPublic'] = []


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroBase(SQLModel):
    name: str = Field(default=None, index=True)
    secret_name: str = Field(default=None)
    age: int | None = Field(default=None, index=True)
    team_id: uuid.UUID = Field(default=None, foreign_key='team.id')
    money: Decimal = Field(default_factory=lambda: random.randrange(1, 10**2), max_digits=5, decimal_places=3)


class Hero(HeroBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str | None = Field(default=None)
    team: Team | None = Relationship(back_populates='heroes')


class HeroCreate(HeroBase):
    password: str


class HeroPublic(HeroBase):
    id: uuid.UUID


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None
    team_id: int | None = None


class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None
