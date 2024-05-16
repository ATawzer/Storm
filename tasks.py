from invoke import task
from storm.jobs import ETLPlaylistOperation
from storm import StormClient, StormDB
from storm.jobs.base import StormContext


@task
def test(c, format=True, lint=True):
    """ Runs a full test suite"""
    if format:
        c.run("invoke format")
    if lint:
        c.run("invoke lint")
    c.run("pytest ./tests --cov=storm --cov-report=term-missing")

@task
def lint(c):
    """ Runs flake8 on the project"""
    c.run("flake8 ./storm")

@task
def format(c):
    """ Runs black on the project"""
    c.run("black ./storm")

@task
def run_playlist_etl(c):
    """ Runs the playlist ETL job"""
    context = StormContext(StormClient(), StormDB())
    instrumental_safety = "0R1gw1JbcOFD0r8IzrbtYP"
    ETLPlaylistOperation([instrumental_safety]).execute(context)
    