import os
import pickle
import typing as t
from dataclasses import dataclass

import mashumaro
import pandas as pd

from waifu.datasets import BaseDataset
from waifu.utils.dataset import get_data_path

@dataclass(frozen=True)
class SodaEpisode(mashumaro.DataClassDictMixin):
    narrative: str
    dialogue: t.List[str]
    speakers: t.List[str]

class SodaDataset(BaseDataset[SodaEpisode]):
    '''
    SODA: Million-scale Dialogue Distillation with Social Commonsense
    Contextualization

    https://huggingface.co/datasets/allenai/soda
    '''

    def generator(self) -> t.Generator[SodaEpisode, None, None]:
        root_data_path = get_data_path("soda")
        file_path = os.path.join(root_data_path, "test.parquet")
        df = pd.read_parquet(file_path)

        # now "df" contains all of the SODA test split, you'd iterate over the relevant shit and `yield` an instance of `SodaEpisode`, which you still need to define.
        # For example on CAI I have a CaiEpisode that has bot persona + bot and user messages
        for i in df.index:
            yield SodaEpisode(narrative=df['narrative'][i], dialogue=df['dialogue'][i], speakers=df['speakers'][i])
        
        