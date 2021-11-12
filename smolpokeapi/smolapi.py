import aiofiles
import asyncio
import json
import logging

# Replace with aiohttp later.
from requests import Session, HTTPError

class SmolPokeApiScraper():
    _POKEAPI = "https://pokeapi.co/api/v2/pokemon/{}"

    @classmethod
    async def new(cls,
                  cache_path="pokeapi_cache.json",
                  throttle=5,
                  timeout=30):
        logging.basicConfig(level=logging.INFO)

        self = SmolPokeApiScraper()
        try:
            load_task = asyncio.create_task(self._load_cache(cache_path))
            self._last_time = asyncio.get_running_loop().time()
            await load_task
        except RuntimeError:
            logging.critical("No running executor for SmolPokeApiScraper.")
            raise
        self._session = Session()
        self._throttle = throttle
        self._timeout = timeout
        return self

    async def _load_cache(self, cache_path):
        """Create or load Pokémon API data cache.

        Parameters
        ----------
        path: str
            File path. Loads cached Pokémon API data as JSON if exists or else
            creates a new file.
        """
        try:
            async with aiofiles.open(cache_path, 'r') as cache:
                buffer = await cache.read()
                self._cache = json.loads(buffer)
                logging.info(f"Loaded cache from {cache_path}.")
        except FileNotFoundError:
            # Create an empty cache if the file doesn't exist.
            # Also...just bubble up the rest of the errors.
            logging.info(f"No cache found at {cache_path}. Creating new cache.")
            self._cache = {}
        self._cache_path = cache_path

    async def sync(self):
        """Write cached data to file.
        """
        logging.info(f"Syncing to {self._cache_path}.")
        json_se = json.dumps(self._cache)
        async with aiofiles.open(self._cache_path, 'w') as cache:
            await cache.write(json_se)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.sync()

    def __getitem__(self, pokenum):
        """Retrieve Pokémon data from cache if exists.

        Parameters
        ----------
        pokenum: int
            Pokémon number as integer.
        """
        return self._cache[pokenum]

    def __setitem__(self, pokenum, data):
        """Add or replace data for pokenum.

        Parameters
        ----------
        pokenum: int
            Pokémon number as integer.
        data: dict[Any]
            Pokémon API data.
        """
        self._cache[pokenum] = data

    def update(self, new_pokemon):
        """Update cache with new data.

        Parameters
        ----------
        new_pokemon: Dict[int, Dict]
            Dictionary of new Pokémon to add
        """
        self._cache.update(new_pokemon)

    async def check_time(self):
        """Throttle requests."""
        aloop = asyncio.get_running_loop()
        # Check if `throttle` seconds have elapsed.
        sleep_time = self._throttle - (aloop.time() - self._last_time)
        if sleep_time > 0:
            logging.info(f"Pausing for {sleep_time} seconds.")
            await asyncio.sleep(sleep_time)
        # Update last_name to the current time.
        self._last_time = aloop.time()

    def create_url(pokenum):
        """Create a PokéAPI URL from a Pokémon number.

        Parameters
        ----------
        pokenum: int
            Pokémon number, such as 25 for Pikachu.

        Returns
        -------
        str
            Formatted URL.
        """
        return SmolPokeApiScraper._POKEAPI.format(pokenum)


    async def get_pokemon(self, pokemon_nums):
        """Retrieve data for an Iterable of Pokédex numbers.

        pokemon_nums: Iterable[int]
            Pokédex numbers.

        Returns
        -------
        Dict[int, Dict[str, Any]]
            Pokémon data.
        """
        pokedata = {}

        for pokenum in pokemon_nums:
            logging.info(f"Scraping data for {pokenum}.")
            # Check if the Pokémon data exists in the cache
            # instead of scraping again.
            if data := self._cache.get(pokenum):
                pokedata[pokenum] = data
                logging.warning(f"{pokenum} already exists in the cache.")
                continue

            # Throttle to avoid spamming the API and sync the cache
            time_task = self.check_time()
            sync_task = self.sync()
            await asyncio.gather(time_task, sync_task)

            try:
                url = SmolPokeApiScraper.create_url(pokenum)
                resp = self._session.get(url, timeout=self._timeout)
                # Raise an error for a non-200 HTTP status.
                resp.raise_for_status()
                resp = resp.json()
                pokedata[pokenum] = resp
                # Always update the cache if the request succeeded
                self.update({pokenum: resp})
            except HTTPError as e:
                logging.critical(f"HTTP status error {e} for Pokémon number {pokenum}.")

        return pokedata
