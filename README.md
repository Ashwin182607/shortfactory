# 🎬 ShortFactory

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

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shortfactory.git
cd shortfactory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.env`:
```bash
PEXELS_API_KEY=your_pexels_api_key
PIXABAY_API_KEY=your_pixabay_api_key
```

4. Launch the web interface:
```bash
./launch.py
```

## 🚀 Quick Start with Google Colab

The fastest way to get started is using our Google Colab notebook:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ashwin182607/shortfactory/blob/main/ShortFactory.ipynb?raw=true)

**Note**: If the Colab link doesn't work directly, you can:
1. Go to [Google Colab](https://colab.research.google.com)
2. Click File → Open Notebook
3. Select "GitHub" tab
4. Enter: `Ashwin182607/shortfactory`
5. Select `ShortFactory.ipynb`

1. Click the "Open in Colab" button above
2. Get your API keys:
   - [Pexels API Key](https://www.pexels.com/api/)
   - [Pixabay API Key](https://pixabay.com/api/docs/)
3. Run all cells in the notebook
4. Start creating videos!

The Colab notebook provides:
- One-click installation
- Easy API key management
- Interactive web interface
- Comprehensive usage guide
- Troubleshooting tips

## 🎯 Usage

1. Open the web interface (automatically opens in your browser)
2. Choose your target platform
3. Enter your video topic or idea
4. Select a template (Modern, Minimal, Dynamic, or AI Dynamic)
5. Customize settings if needed
6. Generate and preview your video
7. Export in platform-specific format

## 🏗️ Project Structure

```
shortfactory/
├── factory_core/          # Core functionality
│   ├── ai/               # AI models and generators
│   ├── engine/           # Video processing engine
│   └── templates/        # Base template system
├── templates/            # Video templates
│   ├── modern_template.py
│   ├── minimal_template.py
│   ├── dynamic_template.py
│   └── ai_dynamic_template.py
├── utils/                # Utility functions
│   ├── asset_sourcing.py
│   ├── music_manager.py
│   └── text_effects.py
├── gui/                  # User interface
│   └── main_ui.py
├── requirements.txt      # Dependencies
└── launch.py            # Launcher script
```

## 🛠️ Templates

1. **Modern Template**
   - Clean, professional look
   - Smooth transitions
   - Perfect for business content

2. **Minimal Template**
   - Simple, elegant design
   - Focus on content
   - Great for tutorials

3. **Dynamic Template**
   - Energetic animations
   - Eye-catching effects
   - Ideal for entertainment

4. **AI Dynamic Template**
   - AI-powered transitions
   - Smart text animations
   - Content-aware styling

## 🛡️ Failsafe System

ShortFactory implements a robust failsafe system to ensure continuous operation:

### AI Models Fallback Chain
1. Script Generation:
   - GPT-Neo 125M (Primary)
   - BLOOM 560M
   - OPT 350M
   - T5-small
   - FLAN-T5-small
   - Rule-based template system (Ultimate fallback)

2. Text Classification:
   - DistilBERT (Primary)
   - TinyBERT
   - MiniLM
   - Keyword-based classification (Fallback)

3. Style Transfer:
   - FastAI StyleGAN (Primary)
   - Basic style templates (Fallback)

### Asset Sourcing Fallback Chain
1. Video Assets:
   - Pexels API
   - Pixabay API
   - Unsplash API
   - Local asset library
   - Procedurally generated visuals

2. Music Assets:
   - Pixabay Music API
   - Free Music Archive
   - Local music library
   - Procedural music generation

### Network & API Handling
- Automatic retry with exponential backoff
- API quota monitoring and management
- Cached responses for frequently used queries
- Offline mode with local assets

### Error Recovery
- Automatic save points during video generation
- Session recovery after crashes
- Partial results saving
- Alternative template switching

## 🔧 Advanced Configuration

### Template Settings
```python
config = {
    'dimensions': (1080, 1920),  # Video dimensions
    'duration': 30,              # Video duration in seconds
    'style': 'modern',          # Template style
    'transition_duration': 0.5,  # Transition timing
    'text_duration': 3.0        # Text animation duration
}
```

### API Configuration
- Get your Pexels API key from: https://www.pexels.com/api/
- Get your Pixabay API key from: https://pixabay.com/api/docs/

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/shortfactory.git
cd shortfactory
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black isort
```

4. Run tests:
```bash
pytest
```

5. Format code:
```bash
black .
isort .
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [ShortGPT](https://github.com/RayVentura/ShortGPT)
- Uses models from [Hugging Face](https://huggingface.co/)
- Video assets from [Pexels](https://www.pexels.com/) and [Pixabay](https://pixabay.com/)

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
