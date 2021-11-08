import asyncio
from smolapi import SmolPokeApiScraper

async def main():
     async with await SmolPokeApiScraper.new() as pokeapi:
          await pokeapi.get_pokemon(range(1, 26))
     
asyncio.run(main())
