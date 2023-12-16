
import asyncio
from src.app import App


if __name__ == "__main__": 
    
    PROFILING = False

    if not PROFILING:
        asyncio.run(App().run())

    # else:
    #     import cProfile
    #     import pstats

    #     out_folder = './profiler_results'
    #     out_filepath = f'{out_folder}/output.dat'
        
    #     cProfile.run('asyncio.run(App().run())', out_filepath)

    #     for agg_type in ['time', 'calls', 'cumulative']:
    #         with open(f'{out_folder}/{agg_type}.txt', 'w') as f:
                # pstats.Stats(out_filepath, stream=f).sort_stats(agg_type).print_stats()
