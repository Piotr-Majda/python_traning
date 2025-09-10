from typing import Generator, List
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from sqlmodel_traning.basic_traning.database import create_db_and_tables, engine
from sqlmodel_traning.basic_traning.models import Hero, HeroCreate, HeroPublic, HeroPublicWithTeam, HeroUpdate, Team, TeamUpdate, TeamCreate, TeamPublic, TeamPublicWithHeroes
from sqlmodel_traning.basic_traning.security import hash_password, verify_password
from sqlmodel_traning.basic_traning.main import create_heroes_db


app = FastAPI()


def get_session() -> Generator[Session]:
    with Session(engine) as s:
        yield s


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_heroes_db()

# Hero api
@app.post('/heroes/', response_model=HeroPublic)
def create_heroes(hero: HeroCreate, session: Session = Depends(get_session)):
    hashed_password = hash_password(hero.password)
    extra_data = {"hashed_password": hashed_password}
    db_hero = Hero.model_validate(hero, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=List[HeroPublic])
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100), session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublicWithTeam)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.exec(select(Hero).where(Hero.id == hero_id)).one_or_none()
    if not hero:
        return JSONResponse(content=f"Hero with id {hero_id} not found", status_code=404)
    return  hero


@app.patch('/heroes/{hero_id}', response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    hero_data = hero.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in hero_data:
        password = hero_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password
    db_hero.sqlmodel_update(hero_data, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
    
    
@app.delete('/heroes/{hero_id}', status_code=204)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {'ok', True}


@app.post("/teams/", response_model=TeamPublic)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Team api
@app.get("/teams/", response_model=list[TeamPublic])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamPublicWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=TeamPublic)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
