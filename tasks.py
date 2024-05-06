from invoke import task


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