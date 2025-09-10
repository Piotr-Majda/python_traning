from sqlmodel import Session, col, select
from sqlalchemy.exc import MultipleResultsFound
from .models import Team, Hero
from .database import create_db_and_tables, engine


def create_heroes_db():
    

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)
    hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
    
    team_wakaland = Team(name="Wakaland", headquarters="Wakaland Capital City", heroes=[hero_1, hero_3, hero_5, hero_7])
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower", heroes=[hero_2, hero_4])
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar", heroes=[hero_6, hero_sure_e])

    with Session(engine) as session:
        session.add(team_wakaland)
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()


def select_heroes():
    with Session(engine) as session:
        result = session.exec(select(Hero).offset(3).limit(3)).all()
        print("Select Heroes:\n" + repr(result))


def select_hero(name='Deadpond'):
    with Session(engine) as s:
        hero = s.exec(select(Hero).where(Hero.name == name)).first()
        print('Select Hero: ' + repr(hero))


def select_only_one_hero(name='Deadpond'):
    with Session(engine) as s:
        try:
            hero = s.exec(select(Hero).where(Hero.name == name)).one()
            print('Select Hero: ' + repr(hero))
        except MultipleResultsFound:
            print(f'Multiple Results found for Hero with name: {name}')


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        spider_boy_z_force_link = HeroTeamLink(
            team=team_z_force, hero=hero_spider_boy, is_training=True
        )
        team_z_force.hero_links.append(spider_boy_z_force_link)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.team_links)
        print("Z-Force heroes:", team_z_force.hero_links)

        for link in hero_spider_boy.team_links:
            if link.team.name == "Preventers":
                link.is_training = False

        session.add(hero_spider_boy)
        session.commit()

        for link in hero_spider_boy.team_links:
            print("Spider-Boy team:", link.team, "is training:", link.is_training)


def select_heroes_by_condition():
    condition=col(Hero.age) <= 35
    with Session(engine) as s:
        heroes = s.exec(select(Hero).where(condition)).all()
        print(f'Select Heroes by condtion{condition}: ' + repr(heroes))


def delete_heroes():
    with Session(engine) as session:
        hero = session.exec(select(Hero).limit(1).where(Hero.name == 'Rusty-Man')).one()
        print(f"Hero: {hero}")

        session.delete(hero)
        session.commit()

        print("Deleted hero:", hero)



# def select_heroes_with_team():
#     with Session(engine) as session:
#         statement = select(Hero, Team).where(Hero.teams.id == Team.id)
#         results = session.exec(statement)
#         for hero, teams in results:
#             print("Select Hero:", hero, "Select Team:", teams)


def delete_team(name: str = 'Wakaland'):
    with Session(engine) as s:
        stt = select(Team).where(Team.name == name)
        teams = s.exec(stt).first()
        s.delete(teams)
        s.commit()
        print(f'Deleted teams: {teams}')


def select_deleted_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Black Lion")
        result = session.exec(statement)
        hero = result.first()
        print("Black Lion not found:", hero)

        statement = select(Hero).where(Hero.name == "Princess Sure-E")
        result = session.exec(statement)
        hero = result.first()
        print("Princess Sure-E not found:", hero)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()
    select_hero()
    select_heroes_by_condition()
    select_only_one_hero()
    # select_heroes_with_team()
    update_heroes()
    delete_heroes()
    delete_team()
    select_deleted_heroes()

if __name__ == "__main__":
    main()
