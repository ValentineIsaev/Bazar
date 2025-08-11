from .messages import INVALID_PRICE_MESSAGE
from ..models import ValidationResult

from bot.utils.cache_utils.operators import CacheMediaOperator

def validate_price(price: str) -> ValidationResult:
    try:
        float(price)
        return ValidationResult(is_validate=True)
    except ValueError:
        return ValidationResult(is_validate=False, error_message=INVALID_PRICE_MESSAGE)

def validate_media(media: CacheMediaOperator) -> ValidationResult:
    return ValidationResult(is_validate=True)
