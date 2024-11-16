# 🎬 ShortFactory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ashwin182607/shortfactory/blob/main/ShortFactory.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An open-source AI video content automation platform for creating social media shorts, inspired by [ShortGPT](https://github.com/RayVentura/ShortGPT). This project builds upon the original ideas of ShortGPT while adding new features and a modern web interface.

## 🙏 Acknowledgments

This project is inspired by and builds upon [ShortGPT](https://github.com/RayVentura/ShortGPT) by [RayVentura](https://github.com/RayVentura). I'm grateful for  pioneering work in AI video automation.

## ✨ Features

- 🤖 AI-powered script generation with multiple model fallbacks:
  - Primary: GPT-Neo 125M
  - Fallbacks: BLOOM, OPT, T5, FLAN-T5
- 🎥 Dynamic video templates with AI transitions
- 🎨 Modern web interface using Gradio
- 🎵 Automated asset sourcing with fallbacks:
  - Videos: Pexels → Pixabay → Local Assets
  - Music: Pixabay → Free Music Archive → Local Assets
- 🔄 Offline mode support with cached assets
- 📱 Multi-platform support (YouTube Shorts, Instagram Reels, TikTok)
- 🔄 Real-time preview and editing
- 🎯 Platform-specific optimization
- 🛠️ Customizable templates and effects

## 🚀 Quick Start

### Google Colab (Recommended)

1. Click the "Open in Colab" badge above
2. Run the notebook cell
3. Follow the setup instructions

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Ashwin182607/shortfactory.git
cd shortfactory

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🔧 Requirements

- Python 3.8+
- FFmpeg
- ImageMagick
- GPU (optional, recommended for faster processing)

## 🎯 Usage

```python
from factory_core.factory import ShortFactory
from factory_core.ai.style_manager import StyleType

# Initialize ShortFactory
factory = ShortFactory()

# Generate a video
factory.create_video(
    topic="Interesting science facts",
    style=StyleType.EDUCATIONAL,
    duration=60,  # seconds
    output_path="output.mp4"
)
```

## 🎨 Supported Styles

- Educational/Informative
- Entertainment
- Tutorial/How-to
- Story/Narrative
- News/Updates
- Lifestyle/Vlog

## 🛠️ Configuration

Edit `config.yaml` to customize:
- Video settings (resolution, FPS, formats)
- Audio settings (sample rate, formats)
- Model settings (device, precision)
- API settings
- Cache settings
- Web interface settings

## 🔑 API Keys

Required API keys:
- Pexels (video/image assets)
- Pixabay (video/image/music assets)
- Unsplash (image assets)

## 📦 Project Structure

```
shortfactory/
├── assets/              # Asset storage
├── factory_core/        # Core functionality
│   ├── ai/             # AI models and processing
│   ├── assets/         # Asset management
│   ├── effects/        # Video/audio effects
│   └── utils/          # Utility functions
├── web_interface/      # Web UI
├── config.yaml         # Configuration
└── requirements.txt    # Dependencies
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- MoviePy for video processing
- PyDub for audio processing
- Gradio for web interface

## 🚨 Limitations

- Primary AI models require more resources
- Some fallback models may produce simpler results
- Local asset library requires storage space
- Initial setup needed for full offline support

## 🔮 Future Plans

- Multi-language support with offline language models
- More AI model options and fallbacks
- Advanced video effect presets
- Cloud deployment capabilities
- Social media direct posting
- Batch processing
- Expanded local asset library
- Custom model training support
- Automated asset caching system
- Smart resource management

## 📫 Support

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Join our community discussions

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/shortfactory&type=Date)](https://star-history.com/#yourusername/shortfactory&Date)

---
Made with ❤️ 
