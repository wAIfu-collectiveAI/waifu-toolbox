import logging

from typing import Generator, Optional

from ..core import (
    BaseFilter,
    BaseTask,
    Episode,
    Turn,
    TurnKind
)
from ..datasets import Airoboros1Dataset
from ..utils import PromptManager

LOG = logging.getLogger(__name__)

class Airoboros1InstructionFollowingTask(BaseTask):
    '''Instruction following task based on the Airoboros 1.4.1 dataset.'''
    def __init__(
        self,
        filters: list[BaseFilter],
        custom_prompts: Optional[list[str]] = None,
        **kwargs
    ) -> None:
        super().__init__(filters=filters)
        # If no custom prompts, use the generic "assistant" prompts
        kwargs = {"generic_prompts": "assistant"} if custom_prompts is None \
            else {"custom_prompts": custom_prompts}
        self.prompts = PromptManager(**kwargs)
        
    def __iter__(self) -> Generator[Episode, None, None]:
        LOG.info("Processing data for task AiroborosInstructionFollowingTask.")
        for idx, example in enumerate(Airoboros1Dataset()):
            # Throw out any responses containing "Airoboros"
            if "airoboros" in example.generation.lower():
                continue

            sys_prompt = self.prompts.sample_prompt()
            turns: list[Turn] = [
                Turn(
                    utterance=sys_prompt,
                    kind=TurnKind.SYSTEM,
                    name="Assistant",
                ),
                Turn(
                    utterance=example.prompt,
                    kind=TurnKind.USER,
                    name="Assistant",
                ),
                Turn(
                    utterance=example.generation,
                    kind=TurnKind.MODEL,
                    name="Assistant",
                ),
            ]

            # Run through the filters.
            episode = Episode(turns=turns, identifier=f"airoboros1-instruct-{idx}")
            if self.should_keep(episode):
                # Passed through filters!
                yield episode