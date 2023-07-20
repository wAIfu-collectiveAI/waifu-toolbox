import json
import logging
import os
import typing as t

from dataclasses import dataclass

from toolbox.core.dataset import BaseDataset, get_path_for

logger = logging.getLogger(__name__)

# Even simpler dataclass than AlpacaLikeDataInstance...
@dataclass(frozen=True)
class SimpleReplyDataInstance:
    prompt: str
    generation: str

class AiroborosDataset(BaseDataset[SimpleReplyDataInstance]):
    def __iter__(self) -> t.Generator[SimpleReplyDataInstance, None, None]:
        root_path = get_path_for("airoboros")
        file_path = os.path.join(root_path, "instructions.json")

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_entry = json.loads(line)
                yield SimpleReplyDataInstance(
                    prompt=line_entry["instruction"],
                    generation=line_entry["response"]
                )
