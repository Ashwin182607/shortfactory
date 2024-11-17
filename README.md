# 🎬 ShortFactory

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ashwin182607/shortfactory/blob/main/ShortFactory.ipynb)

ShortFactory is an open-source AI-powered platform for automated social media short-form video creation, inspired by [RayVentura's ShortGPT](https://github.com/RayVentura/ShortGPT). It streamlines content generation across multiple platforms like YouTube Shorts, TikTok, and Instagram Reels using advanced machine learning technologies while building upon ShortGPT's foundation with new features and improvements.

## ✨ Features

- 🎨 **Advanced Style Transfer**: Multiple AI models for unique video styles
- 🎯 **Multi-Platform Support**: Create content for various social media platforms
- 🤖 **AI-Powered Generation**: Automated content creation and enhancement
- 📊 **System Health Monitoring**: Comprehensive system checks and validation
- 🔄 **Flexible Pipeline**: Modular architecture for easy customization
- 🎵 **Audio Processing**: Advanced audio manipulation and enhancement
- 🖼️ **Asset Management**: Efficient handling of video and image assets

## 🚀 Quick Start

### Google Colab (Recommended for Quick Start)

1. Click the "Open in Colab" badge at the top of this README
2. Follow the notebook instructions
3. No local setup required!

### Local Installation

### Prerequisites

- Python 3.8 or higher
- GPU support (optional but recommended)
- FFmpeg installed on your system

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ashwin182607/shortfactory.git
   cd shortfactory
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Usage

1. Run system check:
   ```bash
   python utils/system_check.py
   ```

2. Start ShortFactory:
   ```bash
   python launch.py
   ```

## 🏗️ Project Structure

```
shortfactory/
├── factory_core/          # Core functionality
│   ├── ai/               # AI models and processing
│   ├── config/           # Configuration management
│   └── factory.py        # Main factory class
├── utils/                # Utility functions
├── tests/                # Test suite
├── assets/              # Asset storage
├── models/              # Model storage
└── output/              # Generated content
```

## 🛠️ Core Components

### Style Transfer Models

- **Neural Style Transfer**: VGG19-based artistic style transfer
- **Fast Style Transfer**: Real-time style transfer with residual blocks

### Configuration System

- Environment-based configuration
- Comprehensive validation
- Flexible fallback mechanisms

### Asset Management

- Multi-source asset fetching
- Efficient caching
- Format conversion

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Test categories:
- Unit tests
- Integration tests
- GPU-specific tests
- Network-dependent tests

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔐 Security

- API keys are managed securely through environment variables
- Asset validation before processing
- Secure dependency management

## 🎯 Roadmap

- [ ] Enhanced video generation pipeline
- [ ] More style transfer models
- [ ] Advanced text overlay capabilities
- [ ] Improved performance optimization
- [ ] Extended platform support
- [ ] Advanced audio processing

## ⚡ Performance

- GPU acceleration when available
- Efficient caching mechanisms
- Optimized asset processing
- Parallel processing capabilities

## 📚 Documentation

- [Configuration Guide](docs/configuration.md)
- [API Reference](docs/api.md)
- [Model Documentation](docs/models.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🙏 Acknowledgments

- [RayVentura's ShortGPT](https://github.com/RayVentura/ShortGPT) for pioneering AI video automation
- OpenAI for transformer models
- TensorFlow and PyTorch communities
- FFmpeg project

## 🙏 Special Thanks

This project stands on the shoulders of giants. Special thanks to:
- [RayVentura](https://github.com/RayVentura) for creating [ShortGPT](https://github.com/RayVentura/ShortGPT), which served as the inspiration and foundation for this project
- The open-source AI community for their invaluable contributions

## 📧 Contact

For questions and support, please open an issue or contact the maintainers.

---

Made with ❤️
