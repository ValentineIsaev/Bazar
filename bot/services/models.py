from dataclasses import dataclass

from bot.utils.message_utils.message_utils import MessageSetting

@dataclass()
class ValidationResult:
    is_validate: bool
    error_message: MessageSetting | None = None
