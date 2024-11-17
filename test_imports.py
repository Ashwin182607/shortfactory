"""Test imports to identify issues."""
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

logger.info(f"Python path: {sys.path}")
logger.info("Testing imports...")

try:
    from factory_core.assets import AssetManager, AssetType
    logger.info("✅ Successfully imported AssetManager and AssetType")
except ImportError as e:
    logger.error(f"❌ Failed to import from factory_core.assets: {e}")
    logger.error(f"Detailed error:", exc_info=True)

try:
    from factory_core.ai.model_manager import ModelManager, ModelType
    logger.info("✅ Successfully imported ModelManager and ModelType")
except ImportError as e:
    logger.error(f"❌ Failed to import from factory_core.ai.model_manager: {e}")
    logger.error(f"Detailed error:", exc_info=True)

try:
    from factory_core.factory import ShortFactory, VideoConfig
    logger.info("✅ Successfully imported ShortFactory and VideoConfig")
except ImportError as e:
    logger.error(f"❌ Failed to import from factory_core.factory: {e}")
    logger.error(f"Detailed error:", exc_info=True)
