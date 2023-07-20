# Standard library imports
from typing import Annotated
# Third party imports
import typer
# Local imports
import wagerpilot.pilotSupport as support
import wagerpilot.odds as odd

app = typer.Typer()

@app.command()
def convert(odds: Annotated[str, typer.Argument(help = 'Value to convert')]):
    odds = support.castType(odds)
    print(support.createOddsTable('Converted Odds', odds))

@app.command()
def parlay(odds: Annotated[str, typer.Argument(help = 'Values in parlay (seperate values with commas)')]):
    odds = odds.split(',')
    odds = support.castListType(odds)
    odds = odd.parlayOdds(odds)
    print(support.createOdds('Parlay Odds', odds))

@app.command()
def vig(homeodds: Annotated[str, typer.Argument(help = 'Odds for home team')],
         awayodds: Annotated[str, typer.Argument(help = 'Odds for away team')],
         drawodds: Annotated[str, typer.Argument(help = 'Odds for a draw')] = 0):    
    odds = [homeodds, awayodds, drawodds]
    odds = support.castListType(odds)
    homeodds, awayodds, drawodds = odds[0], odds[1], odds[2]    
    print(support.createVig('Implied Probability and Vig', homeodds, awayodds, drawodds))

@app.command()
def fair(homeodds: Annotated[str, typer.Argument(help = 'Odds for home team')],
         awayodds: Annotated[str, typer.Argument(help = 'Odds for away team')],
         drawodds: Annotated[str, typer.Argument(help = 'Odds for a draw')] = 0):    
    odds = [homeodds, awayodds, drawodds]
    odds = support.castListType(odds)
    homeodds, awayodds, drawodds = odds[0], odds[1], odds[2]    
    print(support.createFair('Fair Odds (No-Vig)', homeodds, awayodds, drawodds))

if __name__ == "__main__":
    app()
