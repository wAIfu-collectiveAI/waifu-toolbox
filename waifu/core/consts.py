class PromptConstants:
    '''String constants related to prompt engineering.'''

    # Prefix for user messages.
    USER_PREFIX = "You"

    # Token to be replaced with the user's display name within bot messages.
    USER_TOKEN = "<USER>"

    # Token to be replaced by the bot's name.
    BOT_TOKEN = "<BOT>"

    # Should be kept in sync with the relevant model that will be trained. This
    # is taken from EleutherAI's Pythia (so, GPT-NeoX).
    EOS_TOKEN = "<|endoftext|>"

    # Token to separate prompt trickery from actual dialogue.
    CHAT_START_TOKEN = "<START>"

    # Global target word count. The word count is chosen in such a way that we
    # can fit all the required prompt trickery into the model's input, but still
    # leave enough space for the user's input message and the inference result.
    TARGET_WORD_COUNT_PER_EPISODE = 1024

    @staticmethod
    def pdm_prefix_for(name: str) -> str:
        '''Builds the Persona Dialogue Module prefix for a given `name`.'''
        return f"{name}'s Persona"
