import asyncio
import platform
from simulation_engine import SimulationEngine


async def main():
    engine = SimulationEngine()
    await engine.run()


if __name__ == "__main__":
    if platform.system() == "Emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())
